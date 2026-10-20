# 비주얼 스타일 기준

작성일: 2026-10-20 (같은 날 방향 수정)

## 확정 방향 (2026-10-20 2차 수정)

- 게시물 한 장 = 추천 컬러 조합 하나. 한 장면에 남자 마네킹 1명(왼쪽) + 여자 마네킹 1명(오른쪽)이 같은 3색 조합을 나눠 입는다.
- 마네킹 비율: 8.5등신 패션 비율. 무광 흰색, 얼굴 없음(코와 눈썹뼈만 옅게), 조각처럼 정리된 진회색 머리카락.
- 배경: 따뜻한 베이지 단색 스튜디오. 사진을 칸에 넣지 않고 배경이 화면 끝까지 이어지게 합성한다.
- 색 강조: 하단에 화면 폭 전체를 3등분한 색 띠(색 이름 + HEX). 상단에 번호와 "A × B × C" 제목.
- 칩 색은 생성 이미지의 옷에서 직접 뽑는다(그림자 없는 밝은 면 기준).
- 생성: gpt-image-2, 1088x1360(4:5), high. 최종 1080x1350 JPEG.
- 합성 도구: scripts/compose_post.py (layout: "pair")

## 지시문 틀

```text
Fashion lookbook photo of two realistic life-size display mannequins standing side by side in one scene, a male mannequin on the left and a female mannequin on the right,
with a small gap between them, both facing the camera in a relaxed natural stance. Elegant elongated fashion proportions: both mannequins are 8.5 heads tall,
small heads, long necks, long legs, realistic shoulders and natural hands; the male slightly taller. Faceless matte white heads with only a subtle sculpted nose and brow ridge,
no eyes, no mouth. Sculpted dark grey hair: male short textured crop swept slightly up, female shoulder-length straight hair tucked behind the ears. Matte white neck and hands.
They wear a coordinated outfit pair built from exactly this color combination: {palette}. Male: {male}. Female: {female}.
Solid fabrics, no patterns, no logos, the three colors clearly readable as large color blocks.
Plain warm beige seamless studio backdrop and floor, soft diffused studio light, soft floor shadow, realistic fabric texture, calm editorial mood.
Both full bodies from top of hair to shoes fully in frame, figures centered and occupying about 70 percent of the image height,
leave clean empty beige background in the top 12 percent and the bottom 16 percent of the image for text. No text, no logos, no human skin, no human face.
```

## 비용 (2026-10-20 실측)

- 고화질 1088x1360 한 장: 출력 6,431 토큰 x $30/100만 = 약 $0.19
- 하루 1장: 한 달 약 $6, 다시 생성하는 경우를 합쳐 약 $8~10

---

## (이전 검토 기록) GOOD vs BETTER 안

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

