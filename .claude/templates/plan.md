# Implementation Plan: 기능명

<!-- 기능의 한국어 이름을 제목에 포함합니다. -->

## Summary

<!-- 주요 구현 방식을 1-2문장으로 요약합니다. -->

## Requirements

<!-- spec.md의 요구사항을 간단히 정리합니다. -->

1. 요구사항 1
2. 요구사항 2

## Critical Files

<!-- 작업 범위를 파악하기 위한 파일 목록입니다. -->

### New Files

- `path/to/NewFile`

### Modified Files

- `path/to/ExistingFile`

### Reference Files

- `path/to/ReferenceFile`

## Architecture

<!-- Outside-In 순서로 다이어그램을 표현합니다. -->

### User Flow

```text
사용자 → [요청] → Controller
                      ↓
              Application Service
                      ↓
                  처리 완료
```

### Event Flow

```text
1. Controller: POST /endpoint
       ↓
2. ApplicationService.method()
       ↓
3. Domain 로직
       ↓
4. Event 발생
```

### Domain Model

```text
Entity (기존)
├── newMethod()  ← 새로운 메서드
└── events
    └── NewEvent  ← 새로운 이벤트
```

## Implementation Steps

<!-- 구현 단계를 Outside-In 순서로 작성합니다. -->

### Step 1: UI Layer

설명

### Step 2: Application Layer

설명

### Step 3: Domain Layer

설명

## Verification

### Build

```bash
# 빌드 명령어
```

### Test

```bash
# 테스트 명령어
```

### Manual Test

1. 정상 케이스 테스트
2. 에러 케이스 테스트

## Considerations

### 기존 코드 재사용

설명

### 호환성

설명
