# Feature Specification: 기능명

<!--
제품 요구사항을 정의하는 문서입니다.
PRD(Product Requirements Document) 수준으로 작성하며, 기술적인 세부사항은
포함하지 않습니다.

포함하지 않는 내용 (plan.md, findings.md에서 다룸):
- 도메인 모델 (Aggregate, Entity, Value Object, Exception 등)
- 동작 방식의 코드 예시
- 기술적 구현 세부사항
-->

## Overview

<!-- 기능의 핵심 내용을 설명합니다. -->

## User Scenarios & Testing (mandatory)

<!-- User Story 1, 2, ... 형식으로 작성합니다. -->

### User Story 1: 시나리오명

- As: ~는
- I: ~할 수 있다
- So: ~하기 위해

#### Acceptance Scenarios

Scenario 1: **시나리오명**

- Given: ~할 때
- When: ~하면
- Then: 결과

Scenario 2: **시나리오명**

- Given: ~할 때
- When: ~하면
- Then: 결과

## Data Structure Analysis (conditional)

<!--
동일 연산이 2개 이상의 구체 타입에 적용되거나, cascade/삭제 전파가 있는 경우 작성합니다.
추상 개념이 구체 타입으로 분화될 때, 데이터 구조 차이가
구현 전략(쿼리 경로, 스코프)에 미치는 영향을 명시합니다.

해당 없는 경우 "해당 없음 — 단일 타입 또는 cascade 없음"으로 기록합니다.
-->

| 추상 개념 | 구체 타입 | 관련 필드 | 구조 | cascade 연산 시 주의사항 |
|-----------|----------|----------|------|----------------------|

## Functional Requirements (mandatory)

<!-- FR-1, FR-2, ... 형식으로 번호를 붙여 작성합니다. -->

- FR-1: MUST 요구사항 설명
- FR-2: SHOULD 요구사항 설명

## Constraints (mandatory)

<!-- CON-1, CON-2, ... 형식으로 번호를 붙여 작성합니다.
     비즈니스 제약사항만 기록합니다. 기술적 엣지케이스는 아래 Edge Cases 섹션에 작성합니다. -->

- CON-1: MUST 제약사항 설명
- CON-2: MUST 제약사항 설명

## Edge Cases & Non-Functional Constraints (mandatory)

<!--
AI Reverse Interview를 통해 도출된 기술적 엣지케이스를 기록합니다.
각 항목은 Phase 3 ATDD 엣지케이스 테스트의 직접적 입력이 됩니다.

이 섹션은 Phase 1의 Reverse Interview 단계에서 채워집니다:
1. AI가 티켓을 분석하여 관련 제약사항 차원을 선별합니다
2. 선별된 차원별로 개발자에게 핵심 질문을 합니다
3. 개발자의 답변을 바탕으로 EC 항목을 작성합니다
-->

### 적용된 제약사항 차원

<!-- AI가 티켓 분석 후 관련 차원에 체크합니다. 모든 차원이 항상 적용되는 것은 아닙니다.
     단순 변경(설정 변경, 텍스트 수정 등)으로 해당 차원이 없는 경우,
     이 섹션에 "해당 없음"을 기록하고 EC 항목을 생략합니다. -->

- [ ] 동시성/멱등성 (Concurrency & Idempotency)
- [ ] 장애 격리 (Failure Isolation)
- [ ] 상태 정합성 (State Consistency)
- [ ] 대량 데이터 (Volume & Load)
- [ ] 인증/보안 (Security & Auth)

### Edge Case Scenarios

<!-- EC-1, EC-2, ... 형식으로 번호를 붙여 Given/When/Then으로 작성합니다.
     각 EC 항목에는 도출된 제약사항 차원을 [차원명] 태그로 표기합니다. -->

EC-1: **엣지케이스명** [차원명]

- Given: ~한 상태에서
- When: ~하면
- Then: 기대 결과 (에러 응답, 멱등 처리, 타임아웃 등)

EC-2: **엣지케이스명** [차원명]

- Given: ~한 상태에서
- When: ~하면
- Then: 기대 결과

## Success Criteria (mandatory)

<!-- SC-1, SC-2, ... 형식으로 번호를 붙여 작성합니다. -->

- SC-1: 성공 기준 설명
- SC-2: 성공 기준 설명

## OpenAPI Specification (optional)

<!-- API가 있는 경우에만 작성합니다. OpenAPI 3.0 형식(YAML)으로 정리합니다.
     API가 없는 프로젝트에서는 이 섹션을 삭제하세요. -->

```yaml
openapi: 3.0.3
info:
  title: API 제목
  version: 1.0.0
  description: |
    API 설명

paths:
  /endpoint:
    post:
      summary: 요약
      description: |
        상세 설명
      operationId: operationId
      tags:
        - Tag
      parameters:
        - name: id
          in: path
          required: true
          description: ID 설명
          schema:
            type: string
      responses:
        '200':
          description: 성공
        '400':
          description: 잘못된 요청
        '404':
          description: 리소스 없음
```
