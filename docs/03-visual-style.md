# 비주얼 스타일 기준

작성일: 2026-10-20

## 레퍼런스

- 형식: @mansi_fashion07 "GOOD vs BETTER" 게시물 (2026-10-14, 좋아요 약 6.5만, 댓글 495)
  - 따뜻한 베이지 배경, 같은 인물을 좌우에 두 번 배치
  - 위쪽에 색 점(원형 스와치)과 굵은 라벨 GOOD / BETTER
  - GOOD은 2색, BETTER는 같은 옷에 1색이나 소품을 더한 3색 → "한 끗 차이"를 보여줌
  - 상반신 위주 구도
- 인물: @hairmensguide 게시물 (얼굴 없는 흰 마네킹 머리 + 조각처럼 정리된 진회색 머리카락)
  - 눈, 입이 없는 매끈한 무광 흰 얼굴, 코와 눈썹뼈만 아주 옅게 드러남

## 우리 계정의 결정

- 인물: 무광 흰 마네킹. 얼굴 없음. 머리카락은 진회색의 조각된 질감. 사람 피부 느낌 금지.
- 형식: GOOD vs BETTER 비교. 한 장에 같은 마네킹 두 번.
- 대상: 남성 게시물과 여성 게시물을 번갈아 올린다.
- 분위기는 남녀 모두 같게, 색만 다르게.
- 캡션: 영어. 질문으로 끝낸다. 예) "Good or better? Which one would you wear?"
- 글자(GOOD, BETTER, 색 점, 색 이름)는 이미지 모델에 그리게 하지 않고 코드로 합성한다.

## 분위기 규칙 (남녀 공통)

| 항목 | 기준 |
|---|---|
| 배경 | 따뜻한 베이지 #E8DFD3, 무늬 없음 |
| 조명 | 부드러운 정면 스튜디오 조명, 그림자 옅게 |
| 마네킹 | 무광 흰색 #F3F1ED, 얼굴 없음 |
| 머리카락 | 진회색 #3B3B3B, 조각처럼 정리된 질감 |
| 구도 | 허리 위 상반신, 정면 또는 살짝 측면 |
| 색 | 채도 낮은 차분한 색만. BETTER에도 3색까지, 그중 하나는 무채색이나 크림 |

## 팔레트

남성

| 이름 | HEX |
|---|---|
| Navy | #2B3445 |
| Charcoal | #3A3B3D |
| Forest | #2F4A3A |
| Olive | #6B6A45 |
| Camel | #B58A5A |
| Washed Denim | #6F86A3 |
| Stone Grey | #A7A49E |
| Cream | #EFE7D8 |

여성

| 이름 | HEX |
|---|---|
| Dusty Rose | #C9A3A0 |
| Sage | #A9B49C |
| Butter | #EAD9A2 |
| Oatmeal | #DCCFBC |
| Lavender Grey | #A9A6B8 |
| Terracotta | #B8735A |
| Chocolate | #4E3A30 |
| Cream | #EFE7D8 |

## 이미지 생성 지시문 틀 (매일 같은 문장, 색과 옷만 바꿈)

```text
Two identical faceless white matte fashion mannequins side by side, waist-up,
smooth featureless face with only a faint nose ridge, no eyes, no mouth,
sculpted dark grey hair ({hair_style}),
left mannequin wears {good_outfit}, right mannequin wears {better_outfit},
plain warm beige studio background #E8DFD3, soft frontal studio light,
editorial fashion illustration with gentle 3D shading, muted colors,
empty space at the top for text, no text, no logos, no skin, no human face
```

- 생성 때마다 고른 기준 이미지 1~2장을 참고 이미지로 함께 넣는다.
- 생성 뒤 옷 영역 색을 뽑아 목표 HEX와 비교하고, 차이가 크면 다시 생성한다.

