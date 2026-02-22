# Kotlin 콘솔 지뢰찾기 (Minesweeper)

## Background
file-based workflow로 생성된 planning 파일(spec, plan 등)을 CodeRabbit이 참조하여 코드 리뷰를 수행하는지 검증하기 위한 테스트 프로젝트이다.

## Goal
Kotlin으로 콘솔 기반 지뢰찾기 게임을 구현하고, planning 파일과 코드 간 불일치에 대해 CodeRabbit이 pinpoint 리뷰를 제공하는지 확인한다.

## How it works

### 게임 플레이
- 9x9 보드에 10개의 지뢰가 무작위 배치
- 사용자가 좌표를 입력하여 셀을 열거나 깃발을 놓음
- 인접 지뢰가 없는 셀은 주변이 자동으로 열림
- 모든 안전 셀을 열면 승리, 지뢰를 열면 패배
- 첫 클릭은 항상 안전

### CodeRabbit 검증
- spec.md의 Functional Requirements 충족 여부 확인
- plan.md의 파일 구조 및 구현 단계 일치 확인

## Related Documents
- [spec.md](spec.md): 요구사항 및 상세 스펙
- [plan.md](plan.md): 기술 구현 계획
