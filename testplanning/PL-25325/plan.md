# Implementation Plan: Kotlin 콘솔 지뢰찾기

## Summary
Kotlin으로 콘솔 기반 지뢰찾기 게임을 구현한다. 5개의 파일로 책임을 분리하고, 각 파일이 단일 책임을 갖도록 설계한다.

## Requirements
1. 9x9 보드에 10개 지뢰 배치
2. 셀 열기 및 인접 지뢰 수 표시
3. 재귀적 자동 열기
4. 깃발 표시 토글
5. 승리/패배 판정
6. 첫 클릭 안전 보장

## Critical Files

### New Files
- src/Main.kt - 진입점, 게임 루프
- src/Board.kt - 보드 생성 및 지뢰 배치
- src/Cell.kt - 셀 데이터 모델
- src/GameEngine.kt - 게임 로직
- src/Renderer.kt - 콘솔 보드 렌더링

### Reference Files
- testplanning/PL-25325/spec.md - 요구사항 명세

## Architecture

```
Main.kt (진입점)
  ├── GameEngine (게임 로직 관리)
  │     ├── Board (보드 상태 관리)
  │     │     └── Cell (셀 데이터)
  │     └── 승패 판정, 셀 열기, 깃발 처리
  └── Renderer (보드 출력)
        └── Board 상태를 콘솔에 렌더링
```

## Implementation Steps

### Step 1: Cell.kt - 셀 데이터 모델
- `CellState` enum: HIDDEN, REVEALED, FLAGGED
- `Cell` data class: state, hasMine, adjacentMines

### Step 2: Board.kt - 보드 생성
- `Board` class: 9x9 2차원 배열로 Cell 관리
- `placeMines(count: Int)`: 지뢰 무작위 배치
- `calculateAdjacentMines()`: 각 셀의 인접 지뢰 수 계산
- `relocateMine(row: Int, col: Int)`: 첫 클릭 안전을 위한 지뢰 재배치

### Step 3: Renderer.kt - 콘솔 렌더링
- `Renderer` class: Board 상태를 콘솔에 출력
- `render(board: Board)`: 보드를 텍스트로 렌더링
- 숨김 셀: `■`, 열린 셀: 숫자(0은 공백), 깃발: `▶`, 지뢰: `✹`

### Step 4: GameEngine.kt - 게임 로직
- `GameEngine` class: 게임 상태 관리
- `revealCell(row: Int, col: Int)`: 셀 열기 + 재귀적 열기
- `toggleFlag(row: Int, col: Int)`: 깃발 토글
- `checkWin()`: 승리 조건 확인
- `checkLose(row: Int, col: Int)`: 패배 조건 확인
- `handleFirstClick(row: Int, col: Int)`: 첫 클릭 안전 처리

### Step 5: Main.kt - 게임 루프
- 게임 초기화: Board 생성, GameEngine 초기화
- 입력 루프: "open 행 열" 또는 "flag 행 열" 명령 파싱
- Renderer로 매 턴 보드 출력
- 승패 판정 후 게임 종료

## Verification
- 게임 시작 시 9x9 보드 표시 확인
- 셀 열기 동작 확인
- 재귀적 열기 동작 확인
- 깃발 토글 동작 확인
- 승패 판정 동작 확인
- 첫 클릭 안전 동작 확인

## Considerations
- 보드 크기와 지뢰 수는 하드코딩 (확장성은 고려하지 않음)
- 콘솔 입력만 지원 (GUI 없음)
