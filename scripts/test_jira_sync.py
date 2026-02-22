#!/usr/bin/env python3
"""
jira-sync.py 순수 함수 테스트 (네트워크 접근 없음)
"""

import os
import sys
import tempfile
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

# jira_sync 모듈명으로 임포트 (파일명이 jira-sync.py이므로 importlib 사용)
import importlib.util

_spec = importlib.util.spec_from_file_location(
    "jira_sync",
    os.path.join(os.path.dirname(__file__), "jira-sync.py"),
)
jira_sync = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(jira_sync)

KST = jira_sync.KST
TIMESTAMP_FORMAT = jira_sync.TIMESTAMP_FORMAT

get_kst_now = jira_sync.get_kst_now
parse_timestamp = jira_sync.parse_timestamp
parse_planning_section = jira_sync.parse_planning_section
build_planning_section = jira_sync.build_planning_section
replace_or_append_planning = jira_sync.replace_or_append_planning
read_local_timestamp = jira_sync.read_local_timestamp
write_local_timestamp = jira_sync.write_local_timestamp
PLANNING_START_MARKER = jira_sync.PLANNING_START_MARKER
PLANNING_END_MARKER = jira_sync.PLANNING_END_MARKER


# ---------------------------------------------------------------------------
# 1. Timestamp utility tests
# ---------------------------------------------------------------------------

class TestTimestampUtils(unittest.TestCase):

    def test_get_kst_now(self):
        """get_kst_now() 반환값이 TIMESTAMP_FORMAT 형식과 일치해야 한다."""
        result = get_kst_now()
        # 파싱 가능해야 하고 KST 접미사를 포함해야 한다
        self.assertIsInstance(result, str)
        self.assertTrue(result.endswith(" KST"), f"Expected ' KST' suffix: {result!r}")
        # strptime으로 역파싱 가능한지 확인
        parsed = datetime.strptime(result, TIMESTAMP_FORMAT)
        self.assertIsNotNone(parsed)

    def test_parse_timestamp(self):
        """알려진 문자열을 파싱하여 datetime 필드와 tzinfo를 검증한다."""
        ts_str = "2026-02-22 15:30:00 KST"
        dt = parse_timestamp(ts_str)

        self.assertEqual(dt.year, 2026)
        self.assertEqual(dt.month, 2)
        self.assertEqual(dt.day, 22)
        self.assertEqual(dt.hour, 15)
        self.assertEqual(dt.minute, 30)
        self.assertEqual(dt.second, 0)
        self.assertIsNotNone(dt.tzinfo)
        # KST는 UTC+9
        expected_offset = timedelta(hours=9)
        self.assertEqual(dt.tzinfo.utcoffset(dt), expected_offset)


# ---------------------------------------------------------------------------
# 2. parse_planning_section tests
# ---------------------------------------------------------------------------

class TestParsePlanningSection(unittest.TestCase):

    def test_parse_without_timestamp(self):
        """타임스탬프 없는 FILE 마커 파싱: {filename: (content, None)} 형식."""
        desc = """\
=== PLANNING_START ===

=== FILE: tasks.md ===

# Tasks
- item 1

=== FILE: spec.md ===

# Spec
overview

=== PLANNING_END ==="""

        result = parse_planning_section(desc)

        self.assertIsNotNone(result)
        self.assertIn("tasks.md", result)
        self.assertIn("spec.md", result)

        tasks_content, tasks_ts = result["tasks.md"]
        self.assertEqual(tasks_content, "# Tasks\n- item 1")
        self.assertIsNone(tasks_ts)

        spec_content, spec_ts = result["spec.md"]
        self.assertEqual(spec_content, "# Spec\noverview")
        self.assertIsNone(spec_ts)

    def test_parse_with_timestamp(self):
        """타임스탬프 있는 FILE 마커 파싱: datetime 객체로 변환되어야 한다."""
        desc = """\
=== PLANNING_START ===

=== FILE: tasks.md [2026-02-22 15:30:00 KST] ===

# Tasks
- item 1

=== FILE: spec.md [2026-02-22 16:00:00 KST] ===

# Spec

=== PLANNING_END ==="""

        result = parse_planning_section(desc)

        self.assertIsNotNone(result)

        tasks_content, tasks_ts = result["tasks.md"]
        self.assertEqual(tasks_content, "# Tasks\n- item 1")
        self.assertIsInstance(tasks_ts, datetime)
        self.assertEqual(tasks_ts.year, 2026)
        self.assertEqual(tasks_ts.month, 2)
        self.assertEqual(tasks_ts.day, 22)
        self.assertEqual(tasks_ts.hour, 15)
        self.assertEqual(tasks_ts.minute, 30)
        self.assertEqual(tasks_ts.tzinfo.utcoffset(tasks_ts), timedelta(hours=9))

        _spec_content, spec_ts = result["spec.md"]
        self.assertIsInstance(spec_ts, datetime)
        self.assertEqual(spec_ts.hour, 16)
        self.assertEqual(spec_ts.minute, 0)

    def test_parse_mixed_timestamps(self):
        """타임스탬프 있는 파일과 없는 파일이 섞인 경우 모두 올바르게 처리해야 한다."""
        desc = """\
=== PLANNING_START ===

=== FILE: tasks.md [2026-02-22 15:30:00 KST] ===

# Tasks

=== FILE: spec.md ===

# Spec

=== PLANNING_END ==="""

        result = parse_planning_section(desc)

        self.assertIsNotNone(result)

        _, tasks_ts = result["tasks.md"]
        self.assertIsInstance(tasks_ts, datetime)

        _, spec_ts = result["spec.md"]
        self.assertIsNone(spec_ts)

    def test_parse_no_planning_section(self):
        """PLANNING 마커가 없으면 None을 반환해야 한다."""
        desc = "일반 Jira description 내용입니다.\n추가 내용."
        result = parse_planning_section(desc)
        self.assertIsNone(result)

    def test_parse_with_embedded_markers(self):
        """파일 내용에 PLANNING_END 마커가 포함되어도 마지막 마커 기준으로 파싱해야 한다."""
        desc = (
            "=== PLANNING_START ===\n"
            "\n"
            "=== FILE: spec.md [2026-02-22 15:30:00 KST] ===\n"
            "\n"
            "# Spec\n"
            "예시:\n"
            "    === PLANNING_START ===\n"
            "    === FILE: tasks.md ===\n"
            "    === PLANNING_END ===\n"
            "\n"
            "=== FILE: tasks.md [2026-02-22 15:30:00 KST] ===\n"
            "\n"
            "# Tasks\n"
            "- item 1\n"
            "\n"
            "=== PLANNING_END ==="
        )
        result = parse_planning_section(desc)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        self.assertIn("spec.md", result)
        self.assertIn("tasks.md", result)
        self.assertIn("=== PLANNING_END ===", result["spec.md"][0])
        self.assertEqual(result["tasks.md"][0], "# Tasks\n- item 1")

    def test_parse_empty_planning(self):
        """PLANNING 마커는 있지만 FILE 마커가 없으면 빈 dict를 반환해야 한다."""
        desc = """\
=== PLANNING_START ===

=== PLANNING_END ==="""

        result = parse_planning_section(desc)
        self.assertIsNotNone(result)
        self.assertEqual(result, {})


# ---------------------------------------------------------------------------
# 3. build_planning_section tests
# ---------------------------------------------------------------------------

class TestBuildPlanningSection(unittest.TestCase):

    def test_build_without_timestamp(self):
        """타임스탬프 None인 경우 FILE 마커에 타임스탬프가 포함되지 않아야 한다."""
        files_content = {
            "tasks.md": ("# Tasks\n- item 1", None),
        }
        result = build_planning_section(files_content)

        self.assertIn(PLANNING_START_MARKER, result)
        self.assertIn(PLANNING_END_MARKER, result)
        self.assertIn("=== FILE: tasks.md ===", result)
        # 타임스탬프 브래킷이 없어야 한다
        self.assertNotIn("[", result)
        self.assertIn("# Tasks", result)
        self.assertIn("- item 1", result)

    def test_build_with_timestamp(self):
        """타임스탬프가 있는 경우 FILE 마커에 [timestamp] 형식으로 포함되어야 한다."""
        files_content = {
            "tasks.md": ("# Tasks\n- item 1", "2026-02-22 15:30:00 KST"),
        }
        result = build_planning_section(files_content)

        self.assertIn(PLANNING_START_MARKER, result)
        self.assertIn(PLANNING_END_MARKER, result)
        self.assertIn("=== FILE: tasks.md [2026-02-22 15:30:00 KST] ===", result)
        self.assertIn("# Tasks", result)

    def test_round_trip_with_timestamp(self):
        """build → parse 라운드트립에서 내용과 타임스탬프가 보존되어야 한다."""
        original_files = {
            "tasks.md": ("# Tasks\n- item 1", "2026-02-22 15:30:00 KST"),
            "spec.md": ("# Spec\noverview", "2026-02-22 16:00:00 KST"),
        }

        # build
        planning_section = build_planning_section(original_files)

        # parse (PLANNING 마커가 이미 포함되어 있음)
        result = parse_planning_section(planning_section)

        self.assertIsNotNone(result)
        self.assertIn("tasks.md", result)
        self.assertIn("spec.md", result)

        tasks_content, tasks_ts = result["tasks.md"]
        self.assertEqual(tasks_content, "# Tasks\n- item 1")
        self.assertIsInstance(tasks_ts, datetime)
        self.assertEqual(tasks_ts.strftime(TIMESTAMP_FORMAT), "2026-02-22 15:30:00 KST")

        spec_content, spec_ts = result["spec.md"]
        self.assertEqual(spec_content, "# Spec\noverview")
        self.assertIsInstance(spec_ts, datetime)
        self.assertEqual(spec_ts.strftime(TIMESTAMP_FORMAT), "2026-02-22 16:00:00 KST")


# ---------------------------------------------------------------------------
# 4. Local LAST_SYNC tests
# ---------------------------------------------------------------------------

class TestLocalTimestamp(unittest.TestCase):

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmpdir.name)

    def tearDown(self):
        self._tmpdir.cleanup()

    def test_read_local_timestamp_missing_file(self):
        """존재하지 않는 파일은 None을 반환해야 한다."""
        file_path = self.tmp_path / "nonexistent.md"
        result = read_local_timestamp(file_path)
        self.assertIsNone(result)

    def test_read_local_timestamp_no_meta(self):
        """LAST_SYNC 주석이 없는 파일은 None을 반환해야 한다."""
        file_path = self.tmp_path / "tasks.md"
        file_path.write_text("# Tasks\n- item 1\n", encoding="utf-8")

        result = read_local_timestamp(file_path)
        self.assertIsNone(result)

    def test_write_and_read_local_timestamp(self):
        """write 후 read하면 동일한 타임스탬프가 반환되어야 한다."""
        file_path = self.tmp_path / "tasks.md"
        file_path.write_text("# Tasks\n- item 1\n", encoding="utf-8")

        ts_str = "2026-02-22 15:30:00 KST"
        write_local_timestamp(file_path, ts_str)

        result = read_local_timestamp(file_path)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, datetime)
        self.assertEqual(result.strftime(TIMESTAMP_FORMAT), ts_str)

    def test_write_local_timestamp_update(self):
        """두 번 write하면 두 번째 타임스탬프가 반환되고 LAST_SYNC 줄이 중복되지 않아야 한다."""
        file_path = self.tmp_path / "tasks.md"
        file_path.write_text("# Tasks\n", encoding="utf-8")

        ts_first = "2026-02-22 10:00:00 KST"
        ts_second = "2026-02-22 18:00:00 KST"

        write_local_timestamp(file_path, ts_first)
        write_local_timestamp(file_path, ts_second)

        # 두 번째 타임스탬프가 반환되어야 한다
        result = read_local_timestamp(file_path)
        self.assertIsNotNone(result)
        self.assertEqual(result.strftime(TIMESTAMP_FORMAT), ts_second)

        # LAST_SYNC 줄이 정확히 하나만 존재해야 한다
        content = file_path.read_text(encoding="utf-8")
        occurrences = content.count("LAST_SYNC")
        self.assertEqual(occurrences, 1, f"LAST_SYNC should appear exactly once, got {occurrences}")


# ---------------------------------------------------------------------------
# 5. Conflict detection tests
# ---------------------------------------------------------------------------

class TestConflictDetection(unittest.TestCase):
    """충돌 감지 로직: 타임스탬프 비교를 직접 검증한다."""

    def _make_ts(self, hour):
        """테스트용 KST datetime 생성."""
        return datetime(2026, 2, 22, hour, 0, 0, tzinfo=KST)

    def test_conflict_skip_pull(self):
        """pull 시 로컬이 더 최신이면 스킵 조건(jira_ts < local_ts)이 True여야 한다."""
        jira_ts = self._make_ts(10)   # 오래된 Jira
        local_ts = self._make_ts(15)  # 최신 로컬

        # cmd_pull 내 스킵 조건: jira_ts < local_ts
        should_skip = jira_ts < local_ts
        self.assertTrue(should_skip)

    def test_conflict_skip_push(self):
        """push 시 Jira가 더 최신이면 스킵 조건(local_ts < jira_ts)이 True여야 한다."""
        local_ts = self._make_ts(10)  # 오래된 로컬
        jira_ts = self._make_ts(15)   # 최신 Jira

        # cmd_push 내 스킵 조건: local_ts < jira_ts
        should_skip = local_ts < jira_ts
        self.assertTrue(should_skip)

    def test_no_conflict_when_jira_newer_pull(self):
        """pull 시 Jira가 더 최신이면 스킵 조건이 False여야 한다 (pull 진행)."""
        jira_ts = self._make_ts(15)   # 최신 Jira
        local_ts = self._make_ts(10)  # 오래된 로컬

        should_skip = jira_ts < local_ts
        self.assertFalse(should_skip)

    def test_no_conflict_when_local_newer_push(self):
        """push 시 로컬이 더 최신이면 스킵 조건이 False여야 한다 (push 진행)."""
        local_ts = self._make_ts(15)  # 최신 로컬
        jira_ts = self._make_ts(10)   # 오래된 Jira

        should_skip = local_ts < jira_ts
        self.assertFalse(should_skip)


# ---------------------------------------------------------------------------
# 6. replace_or_append_planning tests
# ---------------------------------------------------------------------------

class TestReplaceOrAppendPlanning(unittest.TestCase):

    def test_replace_existing_planning(self):
        """기존 PLANNING 영역이 있으면 새 내용으로 교체되어야 한다."""
        original_description = (
            "기존 설명 내용\n"
            "\n"
            "=== PLANNING_START ===\n"
            "\n"
            "=== FILE: tasks.md ===\n"
            "\n"
            "# Old Tasks\n"
            "\n"
            "=== PLANNING_END ===\n"
            "\n"
            "후속 내용"
        )

        new_planning = (
            "=== PLANNING_START ===\n"
            "\n"
            "=== FILE: tasks.md ===\n"
            "\n"
            "# New Tasks\n"
            "\n"
            "=== PLANNING_END ==="
        )

        result = replace_or_append_planning(original_description, new_planning)

        self.assertIn("기존 설명 내용", result)
        self.assertIn("# New Tasks", result)
        self.assertNotIn("# Old Tasks", result)
        # PLANNING 마커가 정확히 하나씩만 존재해야 한다
        self.assertEqual(result.count(PLANNING_START_MARKER), 1)
        self.assertEqual(result.count(PLANNING_END_MARKER), 1)

    def test_append_planning(self):
        """PLANNING 영역이 없으면 description 끝에 추가되어야 한다."""
        original_description = "기존 Jira 티켓 설명입니다."

        new_planning = (
            "=== PLANNING_START ===\n"
            "\n"
            "=== FILE: tasks.md ===\n"
            "\n"
            "# Tasks\n"
            "\n"
            "=== PLANNING_END ==="
        )

        result = replace_or_append_planning(original_description, new_planning)

        self.assertIn("기존 Jira 티켓 설명입니다.", result)
        self.assertIn(PLANNING_START_MARKER, result)
        self.assertIn(PLANNING_END_MARKER, result)
        self.assertIn("# Tasks", result)
        # 기존 내용이 PLANNING 마커보다 앞에 위치해야 한다
        start_idx = result.index(PLANNING_START_MARKER)
        original_idx = result.index("기존 Jira 티켓 설명입니다.")
        self.assertLess(original_idx, start_idx)


# ---------------------------------------------------------------------------
# 7. Argparse --force flag test
# ---------------------------------------------------------------------------

class TestArgparseForceFlag(unittest.TestCase):

    def _build_parser(self):
        """main()과 동일한 방식으로 파서를 생성한다."""
        import argparse

        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")

        pull_parser = subparsers.add_parser("pull")
        pull_parser.add_argument("ticket")
        pull_parser.add_argument("--force", "-f", action="store_true")

        push_parser = subparsers.add_parser("push")
        push_parser.add_argument("ticket")
        push_parser.add_argument("--force", "-f", action="store_true")

        return parser

    def test_pull_parser_force_flag(self):
        """pull 서브커맨드가 --force 플래그를 수락해야 한다."""
        parser = self._build_parser()

        args = parser.parse_args(["pull", "PL-123", "--force"])
        self.assertEqual(args.command, "pull")
        self.assertEqual(args.ticket, "PL-123")
        self.assertTrue(args.force)

    def test_pull_parser_force_short_flag(self):
        """pull 서브커맨드가 -f 단축 플래그를 수락해야 한다."""
        parser = self._build_parser()

        args = parser.parse_args(["pull", "PL-123", "-f"])
        self.assertTrue(args.force)

    def test_pull_parser_no_force_flag(self):
        """--force 없이 pull 파싱 시 force가 False여야 한다."""
        parser = self._build_parser()

        args = parser.parse_args(["pull", "PL-123"])
        self.assertFalse(args.force)

    def test_push_parser_force_flag(self):
        """push 서브커맨드가 --force 플래그를 수락해야 한다."""
        parser = self._build_parser()

        args = parser.parse_args(["push", "PL-456", "--force"])
        self.assertEqual(args.command, "push")
        self.assertEqual(args.ticket, "PL-456")
        self.assertTrue(args.force)

    def test_push_parser_force_short_flag(self):
        """push 서브커맨드가 -f 단축 플래그를 수락해야 한다."""
        parser = self._build_parser()

        args = parser.parse_args(["push", "PL-456", "-f"])
        self.assertTrue(args.force)

    def test_push_parser_no_force_flag(self):
        """--force 없이 push 파싱 시 force가 False여야 한다."""
        parser = self._build_parser()

        args = parser.parse_args(["push", "PL-456"])
        self.assertFalse(args.force)


if __name__ == "__main__":
    unittest.main()
