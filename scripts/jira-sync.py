#!/usr/bin/env python3
"""
Jira 동기화 스크립트 - planning 파일과 Jira 티켓 description을 양방향 동기화

사용법:
    python scripts/jira-sync.py setup          # 최초 설정 (.env 파일 생성)
    python scripts/jira-sync.py pull PL-25324   # Jira → 로컬
    python scripts/jira-sync.py push PL-25324   # 로컬 → Jira
    python scripts/jira-sync.py pull PL-25324 --force  # 강제 pull (충돌 무시)
    python scripts/jira-sync.py push PL-25324 --force  # 강제 push (충돌 무시)

환경 변수 (.env 파일 또는 export):
    JIRA_BASE_URL    Atlassian Cloud 도메인 (예: https://your-domain.atlassian.net)
    JIRA_EMAIL       Jira 계정 이메일
    JIRA_API_TOKEN   API 토큰 (스코프 없는 클래식 토큰 권장)

인증 방식:
    기본값은 Basic Auth (클래식 토큰). 스코프 토큰 사용 시 JIRA_AUTH_METHOD=bearer 설정.

Auto-Routing:
    JIRA_BASE_URL에서 cloudId를 자동 취득하여 API Gateway(api.atlassian.com)를 사용합니다.

pull: Jira description의 PLANNING 영역 -> .planning/{티켓번호}/ 디렉토리에 파일 저장
push: .planning/{티켓번호}/ 디렉토리의 파일 -> Jira description의 PLANNING 영역에 업데이트
"""

import argparse
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

KST = timezone(timedelta(hours=9))
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S KST"


def get_kst_now():
    return datetime.now(KST).strftime(TIMESTAMP_FORMAT)


def parse_timestamp(ts_str):
    """'2026-02-22 15:30:00 KST' → datetime(KST)"""
    return datetime.strptime(ts_str, TIMESTAMP_FORMAT).replace(tzinfo=KST)


def format_short_ts(dt):
    """datetime → '2/22 15:30' (플랫폼 독립적)"""
    return f"{dt.month}/{dt.day} {dt.strftime('%H:%M')}"


def _ensure_requests():
    """requests 라이브러리 설치 여부 확인. 없으면 에러 출력 후 종료."""
    try:
        import requests  # noqa: F401
    except ImportError:
        print("오류: 'requests' 라이브러리가 설치되지 않았습니다.")
        print("설치 방법: pip3 install -r scripts/requirements.txt")
        sys.exit(1)


import importlib as _importlib


def _requests():
    """requests 모듈을 반환. 호출 전 _ensure_requests()가 선행되어야 함."""
    return _importlib.import_module("requests")


ENV_FILE = Path(__file__).resolve().parent.parent / ".env"

REQUIRED_VARS = {
    "JIRA_BASE_URL": {
        "prompt": "Atlassian Cloud 도메인 (예: https://your-domain.atlassian.net)",
        "example": "https://your-domain.atlassian.net",
    },
    "JIRA_EMAIL": {
        "prompt": "Jira 계정 이메일",
        "example": "your-email@company.com",
    },
    "JIRA_API_TOKEN": {
        "prompt": "API 토큰 (발급: https://id.atlassian.com/manage/api-tokens, 스코프 없는 클래식 토큰 권장)",
        "example": "",
        "secret": True,
    },
}

PLANNING_START_MARKER = "=== PLANNING_START ==="
PLANNING_END_MARKER = "=== PLANNING_END ==="
FILE_MARKER_PREFIX = "=== FILE: "
FILE_MARKER_SUFFIX = " ==="
FILE_MARKER_PATTERN = re.compile(r"^=== FILE: (.+?)(?:\s+\[(.+?)\])? ===$")

SYNC_META_PATTERN = re.compile(r"^<!-- LAST_SYNC: (.+?) -->$", re.MULTILINE)


def read_local_timestamp(file_path):
    """로컬 파일에서 LAST_SYNC 타임스탬프 추출. 없으면 None."""
    if not file_path.exists():
        return None
    content = file_path.read_text(encoding="utf-8")
    match = SYNC_META_PATTERN.search(content)
    if match:
        try:
            return parse_timestamp(match.group(1))
        except ValueError:
            return None
    return None


def write_local_timestamp(file_path, timestamp_str):
    """로컬 파일 하단의 LAST_SYNC 주석을 삽입 또는 갱신."""
    content = file_path.read_text(encoding="utf-8")
    new_meta = f"<!-- LAST_SYNC: {timestamp_str} -->"
    if SYNC_META_PATTERN.search(content):
        content = SYNC_META_PATTERN.sub(new_meta, content)
    else:
        # 파일 끝에 추가 (마지막 줄바꿈 보존)
        if content.endswith("\n"):
            content = content + new_meta + "\n"
        else:
            content = content + "\n" + new_meta + "\n"
    file_path.write_text(content, encoding="utf-8")


TARGET_FILES = ["spec.md", "plan.md", "tasks.md", "findings.md", "progress.md", "README.md"]

TICKET_PATTERN = re.compile(r"^[A-Z][A-Z0-9]+-\d+$")


def validate_ticket(ticket):
    """티켓 번호 형식 검증. 유효하지 않으면 에러 출력 후 종료."""
    if not TICKET_PATTERN.match(ticket):
        print(f"오류: 유효한 티켓 번호가 아닙니다: '{ticket}'")
        print("형식: PROJECT-123 (예: PL-25324)")
        sys.exit(1)


def validate_filename(filename, target_dir):
    """파일명 검증. 경로 조작(path traversal) 방지."""
    if ".." in filename or "/" in filename or "\\" in filename:
        print(f"경고: 안전하지 않은 파일명 무시: '{filename}'")
        return None
    resolved = (target_dir / filename).resolve()
    if not str(resolved).startswith(str(target_dir.resolve())):
        print(f"경고: 대상 디렉토리 외부 경로 무시: '{filename}'")
        return None
    return resolved


def load_env_file():
    """프로젝트 루트의 .env 파일을 읽어 환경 변수에 설정한다. 기존 환경 변수를 덮어쓰지 않는다."""
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip("\"'")
        if key and not os.environ.get(key):
            os.environ[key] = value


def save_env_file(values):
    """값을 .env 파일에 저장한다. 기존 파일이 있으면 해당 키만 갱신한다."""
    existing = {}
    lines = []
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and "=" in stripped:
                key = stripped.partition("=")[0].strip()
                existing[key] = len(lines)
            lines.append(line)

    for key, value in values.items():
        new_line = f'{key}="{value}"'
        if key in existing:
            lines[existing[key]] = new_line
        else:
            lines.append(new_line)

    ENV_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def prompt_env_vars(missing_vars):
    """누락된 환경 변수를 대화형으로 입력받는다."""
    import getpass

    print("\n환경 변수가 설정되지 않았습니다. 값을 입력해 주세요.")
    print("(입력한 값은 .env 파일에 저장할 수 있습니다)\n")

    values = {}
    for var in missing_vars:
        info = REQUIRED_VARS[var]
        label = f"  {var}"
        if info.get("example"):
            label += f" (예: {info['example']})"
        label += ": "

        if info.get("secret"):
            value = getpass.getpass(f"  {var} (입력 시 표시되지 않음): ")
        else:
            value = input(label)

        value = value.strip()
        if not value:
            print(f"오류: {var} 값은 필수입니다.")
            sys.exit(1)
        values[var] = value
        os.environ[var] = value

    # .env 저장 제안
    print()
    save = input("입력한 값을 .env 파일에 저장하시겠습니까? (Y/n): ").strip().lower()
    if save != "n":
        save_env_file(values)
        print(f"저장 완료: {ENV_FILE}")
    print()

    return values


def get_env_vars():
    """환경 변수를 읽어 반환. .env 파일 로딩 → 누락 시 대화형 입력."""
    load_env_file()

    required = list(REQUIRED_VARS.keys())
    missing = [var for var in required if not os.environ.get(var)]

    if missing and sys.stdin.isatty():
        prompt_env_vars(missing)
    elif missing:
        print("오류: 다음 환경 변수가 설정되지 않았습니다:")
        for var in missing:
            print(f"  - {var}")
        print("\n설정 방법:")
        print("  1. python3 scripts/jira-sync.py setup  (대화형 설정)")
        print("  2. 직접 환경 변수 export")
        sys.exit(1)

    return {
        "base_url": os.environ["JIRA_BASE_URL"].rstrip("/"),
        "email": os.environ["JIRA_EMAIL"],
        "api_token": os.environ["JIRA_API_TOKEN"],
    }


def get_cloud_id(base_url):
    """
    Atlassian Cloud의 cloudId를 자동 취득한다.
    JIRA_BASE_URL에서 /_edge/tenant_info를 호출하여 cloudId를 반환한다.
    실패 시 에러 출력 후 종료.
    """
    req = _requests()
    url = f"{base_url}/_edge/tenant_info"
    try:
        response = req.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            cloud_id = data.get("cloudId")
            if cloud_id:
                return cloud_id
    except Exception:
        pass

    print("오류: Atlassian Cloud ID를 가져올 수 없습니다.")
    print(f"  요청 URL: {url}")
    print("  JIRA_BASE_URL이 올바른 Atlassian Cloud 도메인인지 확인하세요.")
    print("  예: https://your-domain.atlassian.net")
    sys.exit(1)


def build_issue_url(cloud_id, ticket):
    """스코프 토큰용 API Gateway URL을 반환한다. API v2는 plain text description을 허용한다."""
    return f"https://api.atlassian.com/ex/jira/{cloud_id}/rest/api/2/issue/{ticket}"


def build_auth_kwargs(env):
    """인증 kwargs를 반환한다.
    JIRA_AUTH_METHOD=bearer → Bearer Auth (스코프 토큰용)
    JIRA_AUTH_METHOD=basic 또는 미설정 → Basic Auth (기본값)
    """
    method = os.environ.get("JIRA_AUTH_METHOD", "basic").lower()
    if method == "bearer":
        return {"headers": {"Authorization": f"Bearer {env['api_token']}"}}
    return {"auth": (env["email"], env["api_token"])}


def _handle_api_error(response, ticket):
    """API 응답 에러를 공통 처리한다."""
    if response.status_code == 401:
        print("오류: 인증 실패. JIRA_EMAIL과 JIRA_API_TOKEN을 확인하세요.")
        sys.exit(1)
    elif response.status_code == 403:
        print(f"오류: 티켓 '{ticket}'에 대한 접근 권한이 없습니다.")
        sys.exit(1)
    elif response.status_code == 404:
        print(f"오류: 티켓 '{ticket}'을 찾을 수 없습니다.")
        sys.exit(1)


def _handle_request_exception(e, base_url):
    """요청 예외를 공통 처리한다."""
    req = _requests()
    if isinstance(e, req.exceptions.ConnectionError):
        print(f"오류: Jira 서버에 연결할 수 없습니다. URL을 확인하세요: {base_url}")
    elif isinstance(e, req.exceptions.Timeout):
        print("오류: Jira 서버 응답 시간이 초과되었습니다.")
    else:
        print(f"오류: 네트워크 요청 실패 - {e}")
    sys.exit(1)


def fetch_issue_description(cloud_id, auth_kwargs, ticket):
    """Jira REST API v2 (Gateway)로 티켓 description을 가져온다."""
    req = _requests()
    url = build_issue_url(cloud_id, ticket)
    params = {"fields": "description"}

    try:
        response = req.get(url, params=params, timeout=30, **auth_kwargs)
    except req.exceptions.RequestException as e:
        _handle_request_exception(e, "api.atlassian.com")

    _handle_api_error(response, ticket)
    if response.status_code != 200:
        print(f"오류: API 요청 실패 (HTTP {response.status_code})")
        print(f"응답: {response.text[:200]}")
        sys.exit(1)

    data = response.json()
    description = data.get("fields", {}).get("description") or ""
    return description


def parse_planning_section(description):
    """description에서 PLANNING 영역을 파싱하여 {파일명: (내용, 타임스탬프_또는_None)} 딕셔너리 반환."""
    if PLANNING_START_MARKER not in description or PLANNING_END_MARKER not in description:
        return None

    start_idx = description.index(PLANNING_START_MARKER) + len(PLANNING_START_MARKER)
    end_idx = description.rindex(PLANNING_END_MARKER)
    planning_content = description[start_idx:end_idx]

    files = {}
    current_filename = None
    current_timestamp = None
    current_lines = []

    for line in planning_content.splitlines():
        m = FILE_MARKER_PATTERN.match(line)
        if m:
            # 이전 파일 저장
            if current_filename is not None:
                content = "\n".join(current_lines)
                files[current_filename] = (content.strip("\n"), current_timestamp)

            # 새 파일 시작
            current_filename = m.group(1).strip()
            ts_raw = m.group(2)
            current_timestamp = None
            if ts_raw:
                try:
                    current_timestamp = parse_timestamp(ts_raw)
                except ValueError:
                    current_timestamp = None
            current_lines = []
        else:
            if current_filename is not None:
                current_lines.append(line)

    # 마지막 파일 저장
    if current_filename is not None:
        content = "\n".join(current_lines)
        files[current_filename] = (content.strip("\n"), current_timestamp)

    return files


def build_planning_section(files_content):
    """파일 내용 딕셔너리를 PLANNING 영역 문자열로 조합. files_content: {filename: (content, timestamp_str_or_None)}"""
    parts = [PLANNING_START_MARKER]
    for filename, entry in files_content.items():
        if isinstance(entry, tuple):
            content, ts = entry
        else:
            content, ts = entry, None
        ts_part = f" [{ts}]" if ts else ""
        parts.append(f"\n{FILE_MARKER_PREFIX}{filename}{ts_part}{FILE_MARKER_SUFFIX}\n")
        if content:
            parts.append(content)
    parts.append(f"\n{PLANNING_END_MARKER}")
    return "\n".join(parts) if len(parts) > 2 else f"{PLANNING_START_MARKER}\n{PLANNING_END_MARKER}"


def replace_or_append_planning(description, new_planning_section):
    """description에서 기존 PLANNING 영역을 교체하거나 끝에 append."""
    if PLANNING_START_MARKER in description and PLANNING_END_MARKER in description:
        # 기존 영역 교체 (rindex로 마지막 END 마커 사용 — 파일 내용에 마커가 포함된 경우 대비)
        start_idx = description.index(PLANNING_START_MARKER)
        end_idx = description.rindex(PLANNING_END_MARKER) + len(PLANNING_END_MARKER)
        updated = description[:start_idx] + new_planning_section + description[end_idx:]
        return updated
    else:
        # 끝에 append
        separator = "\n\n" if description and not description.endswith("\n\n") else ""
        return description + separator + new_planning_section


def update_issue_description(cloud_id, auth_kwargs, ticket, new_description):
    """Jira REST API v2 (Gateway)로 티켓 description을 업데이트."""
    req = _requests()
    url = build_issue_url(cloud_id, ticket)
    payload = {
        "fields": {
            "description": new_description
        }
    }

    try:
        response = req.put(url, json=payload, timeout=30, **auth_kwargs)
    except req.exceptions.RequestException as e:
        _handle_request_exception(e, "api.atlassian.com")

    _handle_api_error(response, ticket)
    if response.status_code not in (200, 204):
        print(f"오류: description 업데이트 실패 (HTTP {response.status_code})")
        print(f"응답: {response.text[:200]}")
        sys.exit(1)


def find_planning_dir(ticket):
    """
    .planning/{ticket}/ 하위 디렉토리 탐색.
    하위 디렉토리가 있으면 그 안을 대상으로, 없으면 바로 해당 디렉토리를 반환.
    """
    base_dir = Path(".planning") / ticket
    if not base_dir.exists():
        return base_dir  # 없어도 base_dir 반환 (push 시 파일 없음 처리)

    # 하위 디렉토리 확인
    subdirs = [d for d in base_dir.iterdir() if d.is_dir()]
    if subdirs:
        # 하위 디렉토리가 여러 개면 첫 번째 사용 (알파벳 정렬)
        subdirs.sort()
        return subdirs[0]

    return base_dir


def cmd_pull(args):
    """pull 커맨드: Jira description -> 로컬 파일"""
    ticket = args.ticket
    force = getattr(args, "force", False)
    validate_ticket(ticket)
    env = get_env_vars()
    auth_kwargs = build_auth_kwargs(env)
    cloud_id = get_cloud_id(env["base_url"])
    print(f"[pull] API Gateway 사용 (cloudId: {cloud_id[:8]}...)")

    print(f"[pull] 티켓 '{ticket}' description을 가져오는 중...")
    description = fetch_issue_description(cloud_id, auth_kwargs, ticket)

    files = parse_planning_section(description)
    if files is None:
        print("planning 데이터가 없습니다. Jira description에 PLANNING 영역이 존재하지 않습니다.")
        sys.exit(0)

    if not files:
        print("planning 영역은 존재하지만 파일 데이터가 없습니다.")
        sys.exit(0)

    # 저장 디렉토리 결정 (push와 동일한 경로 사용)
    target_dir = find_planning_dir(ticket)
    target_dir.mkdir(parents=True, exist_ok=True)

    now_str = get_kst_now()
    synced = []
    skipped = []
    created = []

    for filename, (content, jira_ts) in files.items():
        file_path = validate_filename(filename, target_dir)
        if file_path is None:
            continue

        local_ts = read_local_timestamp(file_path) if file_path.exists() else None

        if not force and jira_ts and local_ts and jira_ts < local_ts:
            jira_short = format_short_ts(jira_ts)
            local_short = format_short_ts(local_ts)
            skipped.append((filename, f"로컬이 더 최신 - 로컬 {local_short} > Jira {jira_short}"))
            continue

        is_new = not file_path.exists()
        file_path.write_text(content + "\n" if content else "", encoding="utf-8")
        write_local_timestamp(file_path, now_str)

        if is_new:
            created.append(filename)
        else:
            jira_short = format_short_ts(jira_ts) if jira_ts else "시각 없음"
            synced.append((filename, jira_short))

    # 결과 출력
    print("\n[pull] 동기화 결과:")
    for name, ts in synced:
        print(f"  ✓ {name:<16} (Jira {ts} → 로컬 갱신)")
    for name in created:
        print(f"  ✓ {name:<16} (신규 파일)")
    for name, reason in skipped:
        print(f"  - {name:<16} (스킵: {reason})")

    if skipped:
        print(f"\n강제 동기화: python3 scripts/jira-sync.py pull {ticket} --force")

    print("\npull 완료.")


def cmd_push(args):
    """push 커맨드: 로컬 파일 -> Jira description"""
    ticket = args.ticket
    force = getattr(args, "force", False)
    validate_ticket(ticket)
    env = get_env_vars()
    auth_kwargs = build_auth_kwargs(env)
    cloud_id = get_cloud_id(env["base_url"])
    print(f"[push] API Gateway 사용 (cloudId: {cloud_id[:8]}...)")

    planning_dir = find_planning_dir(ticket)

    if not planning_dir.exists():
        print(f"오류: .planning/{ticket}/ 디렉토리가 존재하지 않습니다.")
        print("먼저 planning 파일을 생성하거나 pull을 실행하세요.")
        sys.exit(1)

    # 현재 Jira description 가져오기 (충돌 감지용)
    print(f"[push] 티켓 '{ticket}'의 현재 상태 확인 중...")
    current_description = fetch_issue_description(cloud_id, auth_kwargs, ticket)
    jira_files = parse_planning_section(current_description) or {}

    now_str = get_kst_now()

    # 대상 파일 읽기 + 충돌 감지
    files_content = {}
    missing = []
    skipped = []
    synced = []
    created = []

    for filename in TARGET_FILES:
        file_path = planning_dir / filename
        if not file_path.exists():
            missing.append(filename)
            continue

        content = file_path.read_text(encoding="utf-8").rstrip("\n")
        # LAST_SYNC 메타데이터 제거 후 push (Jira에는 메타데이터 불필요)
        content_clean = SYNC_META_PATTERN.sub("", content).rstrip("\n")

        local_ts = read_local_timestamp(file_path)
        jira_ts = jira_files.get(filename, (None, None))[1] if filename in jira_files else None

        if not force and local_ts and jira_ts and local_ts < jira_ts:
            local_short = format_short_ts(local_ts)
            jira_short = format_short_ts(jira_ts)
            skipped.append((filename, f"Jira가 더 최신 - Jira {jira_short} > 로컬 {local_short}"))
            continue

        is_new = filename not in jira_files
        files_content[filename] = (content_clean, now_str)

        if is_new:
            created.append(filename)
        else:
            synced.append(filename)

    if not files_content and not skipped:
        print(f"오류: {planning_dir}/ 에 대상 파일이 하나도 없습니다.")
        print(f"대상 파일: {', '.join(TARGET_FILES)}")
        sys.exit(1)

    if missing:
        print(f"참고: 다음 파일이 없어 제외됩니다: {', '.join(missing)}")

    # 스킵되지 않은 기존 Jira 파일도 유지 (push 대상이 아닌 파일은 기존 값 보존)
    for filename, (content, ts) in jira_files.items():
        if filename not in files_content and filename not in [s[0] for s in skipped]:
            ts_str = ts.strftime(TIMESTAMP_FORMAT) if ts else None
            files_content[filename] = (content, ts_str)

    if files_content:
        print(f"[push] 티켓 '{ticket}'에 파일을 업로드하는 중...")
        print(f"대상 디렉토리: {planning_dir}")

        # PLANNING 영역 구성
        new_planning_section = build_planning_section(files_content)

        # description 업데이트 (기존 내용 보존)
        new_description = replace_or_append_planning(current_description, new_planning_section)

        # Jira 업데이트
        update_issue_description(cloud_id, auth_kwargs, ticket, new_description)

        # 성공한 파일의 로컬 LAST_SYNC 갱신
        for filename in synced + created:
            file_path = planning_dir / filename
            if file_path.exists():
                write_local_timestamp(file_path, now_str)

    # 결과 출력
    print("\n[push] 동기화 결과:")
    for name in synced:
        print(f"  ✓ {name:<16} (로컬 → Jira 갱신)")
    for name in created:
        print(f"  ✓ {name:<16} (신규 파일)")
    for name, reason in skipped:
        print(f"  - {name:<16} (스킵: {reason})")

    if skipped:
        print(f"\n강제 동기화: python3 scripts/jira-sync.py push {ticket} --force")

    print(f"\n티켓 '{ticket}' description 업데이트 완료.")


def cmd_setup(args):
    """setup 커맨드: .env 파일에 Jira 연동 설정을 저장"""
    print("=== Jira 연동 설정 ===\n")

    load_env_file()

    values = {}
    import getpass

    for var, info in REQUIRED_VARS.items():
        current = os.environ.get(var, "")
        if current:
            masked = current[:4] + "****" if info.get("secret") and len(current) > 4 else current
            keep = input(f"  {var} [{masked}] (Enter로 유지, 새 값 입력으로 변경): ").strip()
            if keep:
                values[var] = keep
                os.environ[var] = keep
        else:
            if info.get("secret"):
                value = getpass.getpass(f"  {var} - {info['prompt']}: ")
            else:
                example = f" (예: {info['example']})" if info.get("example") else ""
                value = input(f"  {var} - {info['prompt']}{example}: ").strip()
            if not value:
                print(f"오류: {var} 값은 필수입니다.")
                sys.exit(1)
            values[var] = value
            os.environ[var] = value

    if values:
        save_env_file(values)
        print(f"\n저장 완료: {ENV_FILE}")

    # 연결 테스트
    print("\n연결 테스트 중...")
    _ensure_requests()
    try:
        base_url = os.environ["JIRA_BASE_URL"].rstrip("/")
        cloud_id = get_cloud_id(base_url)
        print(f"  cloudId 취득 성공: {cloud_id[:8]}...")
        print("\n설정이 완료되었습니다. 이제 pull/push 명령을 사용할 수 있습니다.")
    except SystemExit:
        print("\n설정은 저장되었지만 연결 테스트에 실패했습니다. 값을 확인해 주세요.")


def main():
    parser = argparse.ArgumentParser(
        description="planning 파일과 Jira 티켓 description을 양방향 동기화합니다.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python3 scripts/jira-sync.py setup           # 최초 설정
  python3 scripts/jira-sync.py pull PL-25324   # Jira → 로컬
  python3 scripts/jira-sync.py push PL-25324   # 로컬 → Jira

환경 변수 (.env 파일 또는 export):
  JIRA_BASE_URL    Atlassian Cloud 도메인 (예: https://your-domain.atlassian.net)
  JIRA_EMAIL       Jira 계정 이메일
  JIRA_API_TOKEN   API 토큰 (스코프 없는 클래식 토큰 권장)
                   발급: https://id.atlassian.com/manage/api-tokens

동작 방식:
  1. .env 파일 또는 환경 변수에서 설정 로딩 (없으면 대화형 입력)
  2. JIRA_BASE_URL에서 cloudId를 자동 취득 → API Gateway(api.atlassian.com) 사용
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="실행할 커맨드")

    # pull 서브커맨드
    pull_parser = subparsers.add_parser(
        "pull",
        help="Jira description의 planning 데이터를 로컬 파일로 가져옵니다.",
    )
    pull_parser.add_argument("ticket", help="Jira 티켓 번호 (예: PL-25324)")
    pull_parser.add_argument("--force", "-f", action="store_true",
        help="타임스탬프 비교 없이 강제 덮어쓰기")
    pull_parser.set_defaults(func=cmd_pull)

    # push 서브커맨드
    push_parser = subparsers.add_parser(
        "push",
        help="로컬 planning 파일을 Jira description에 업로드합니다.",
    )
    push_parser.add_argument("ticket", help="Jira 티켓 번호 (예: PL-25324)")
    push_parser.add_argument("--force", "-f", action="store_true",
        help="타임스탬프 비교 없이 강제 덮어쓰기")
    push_parser.set_defaults(func=cmd_push)

    # setup 서브커맨드
    setup_parser = subparsers.add_parser(
        "setup",
        help="Jira 연동 환경 변수를 .env 파일에 설정합니다.",
    )
    setup_parser.set_defaults(func=cmd_setup)

    args = parser.parse_args()

    if not args.command:
        print("Jira 동기화 스크립트\n")
        print("사용 가능한 커맨드:")
        print("  setup    .env 파일에 Jira 연동 설정")
        print("  pull     Jira → 로컬 파일")
        print("  push     로컬 파일 → Jira")
        print()
        if not ENV_FILE.exists():
            print("최초 사용 시 setup을 먼저 실행하세요:")
            print(f"  python3 {sys.argv[0]} setup")
        else:
            print(f"예시: python3 {sys.argv[0]} pull PL-25324")
        print()
        parser.print_usage()
        sys.exit(0)

    _ensure_requests()
    args.func(args)


if __name__ == "__main__":
    main()
