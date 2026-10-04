# OPRN 월드맵 키트 · 아이콘 하네스

16px 월드맵(EasyRPG World 칩셋 결)의 **장소 아이콘 17개 세계관 · 346장**과, 그 아이콘을 만들고 거르는 **하네스**다.
[OPRN Studio](https://github.com/MovieHolic-Plex) 의 월드맵 작업에서 떼어 낸 공개본이다.

**갤러리:** https://movieholic-plex.github.io/oprn-worldmap-kit/ — 세트별 아이콘, 지도에 붙인 모습, 검수자 판정, 사람의 받기 여부.

2026-10-04: **사람 선택 79장(원본 72 · 재작성 후보 7)**의 게임용 PNG 시트와 전체 칸 배열을 추가했다.
미선택 267장은 선택 시트에 포함하지 않는다. 실제 해안선·높이·강·호수 자료로 지형을 만드는 `style=real`도 들어 있다.

*World-map place icons (17 themes, 346 icons) for 16px RPG world maps in the EasyRPG World chipset style, plus the harness that builds, reviews and filters them. Icons are 3D scenes written in Python and raycast to 16px — no generated images. Docs are in Korean.*

## 무엇이 들어 있나

| 경로 | 내용 |
|---|---|
| `tiledata/worldmap-kit/` | 월드맵 키트 — 공용 지형 · 팔레트 6종 · 아이콘 세트 17개 · 여정 템플릿. `docs/README.md` 가 설계 문서 |
| `tiledata/worldmap-kit/iconsets/_scene3d/` | 아이콘 렌더러 — 경사 투영 레이캐스터 + 세트 빌더(정면 3/4 카메라, 16px 칸 맞춤, 색 한도) |
| `tiledata/worldmap-kit/iconsets/<세트>/` | 세트마다 `scenes.py`(장면 코드) · `sheet.png` · `manifest.json` · `preview/` |
| `src/harnesses/worldmap-icons/` | 하네스 — 지도에 붙여 보기 · LLM 검수 · 받기/버리기 웹 화면 · 다시 그리기 판 |
| `harness-data/worldmap-icons/decisions.json` | 이 저장소의 아이콘에 대한 실제 검수·결정 사본 |
| `tiledata/worldmap-kit/selected/` | 사람이 고른 실제 PNG·SHA256·칸 사전·전체 배열·정상/누락 예시 |
| `public/assets/worldmap-icons/worldmap-selected.png` | 기존 EasyRPG 지형 480칸 + 선택 아이콘. 16px · 30열 · 총 1,620칸 |
| `tiledata/worldmap-kit/geo/` | Natural Earth·NOAA ETOPO1 실제 지리 자료와 출처. 지역 프리셋 20개 및 직접 범위 지정 |
| `docs/` | 갤러리(GitHub Pages). `tools/export_gallery.py` 로 다시 만든다 |

## 어떻게 만드나

```
① 장면 코드      iconsets/<세트>/scenes.py — 성·마을·탑을 상자·원통·원뿔·지붕 도형으로 짓는다
② 16px 렌더      _scene3d/buildset.py — 정면 3/4 카메라(윗면 + 남쪽 벽, 평평한 옆벽 0px), 빛은 왼쪽 위
                 색은 EasyRPG World.png 팔레트 + 세트당 새 색 24개까지, 역할마다 정해진 칸(수도 6×6, 마을 2×2 …)
③ 지도에 붙이기  공용 지형 · 여정 템플릿의 같은 역할 자리에 붙여 8배 · 지도 3배 · 지도 1배를 만든다
④ 검수자         LLM 검수자(기본 Codex CLI)가 시점 계약(review.md)으로 PASS/FAIL + 사유 코드(SIDE·DIAG·FRONT·READ·STYLE)
⑤ 사람           웹 화면에서 받기 / 버리기. 버린 것은 다시 그리기 판 — 작업자가 원래 화소를 재료로 후보를 다시 만든다
```

검수자 판정은 참고다. 받기/버리기는 사람만 한다 — 검수자는 원통 탑·모임지붕의 오른쪽 명암을 옆면으로 잘못 읽는 일이 잦았다(정면 세트에는 그 오판을 막는 규칙 `FRONT3D_RULE` 이 들어 있다).

## 돌려 보기

Python 3.10+ 와 `pip install -r requirements.txt`(numpy · Pillow).

```bash
# 세트 하나 다시 빌드 (sheet.png · manifest.json · preview/ · build-report.json)
python3 tiledata/worldmap-kit/iconsets/joseon/build.py

# 월드맵 한 장 그리기 (지형 + 팔레트 + 아이콘 세트 + 여정)
python3 tiledata/worldmap-kit/kit/build_world.py --iconset joseon --palette original --journey fantasy-5act --out /tmp/wm --cache /tmp/wmk-cache

# 키트 자체 검사
python3 tiledata/worldmap-kit/kit/selftest.py
```

하네스:

```bash
export WMI_HARNESS_DATA=~/.local/share/oprn/worldmap-icon-harness   # 데이터(sqlite·그림) 위치. 기본값이 이것
python3 src/harnesses/worldmap-icons/harness.py intake --set joseon  # 지도에 붙인 그림 만들기(첫 실행은 지형 렌더로 몇 분)
python3 src/harnesses/worldmap-icons/harness.py review --set joseon  # 검수 — codex CLI 필요
python3 src/harnesses/worldmap-icons/harness.py serve --port 18313   # 받기/버리기 화면 → http://localhost:18313/

# 이 공개본에 포함된 선택 PNG 사본으로 시트·사전을 다시 만들기(SQLite 불필요)
python3 src/harnesses/worldmap-icons/bake.py build --snapshot
python3 src/harnesses/worldmap-icons/bake.py check --snapshot
```

- 검수·다시 그리기는 `codex` CLI 를 부른다. 모델은 `WMI_HARNESS_CODEX_MODEL`, 다시 그리기 엔진을 Claude Code 로 바꾸려면 `WMI_HARNESS_ENGINE=claude`.
  검수 없이 화면만 써도 된다(검수 표시가 비어 있을 뿐).
- 새 세계관 세트를 만드는 절차는 `tiledata/worldmap-kit/docs/README.md` 「새 세계관 아이콘 세트를 추가하는 절차」와 `_scene3d/workflow/BRIEF.md`(작업자 지시서).

## 세트

판타지(기본, 손 도트) · 사막·동양풍 · 현대·SF(경사 카메라, 옆면 약간) · 판타지 던전·신전 입구(부분 세트) · 몬스터 수집 · 조선 · 일본 전국 · 무협 중국 ·
고대 그리스·로마 · 다크 판타지·고딕 · 설원·북방 · 바다·군도 · 선사·원시 · 스팀펑크·마도 · 현대 소도시 · 외계 행성 · 성계 지도(우주 배경).

## 아직 없는 것

- 성계 지도의 우주 지형층(성운·소행성대·항로) — 지금은 임시 별 바탕
- 이 공개본은 Python 키트와 자료다. OPRN 편집기 도구·SQLite 프로젝트 본문은 포함하지 않는다.

## 라이선스

- **그림**(아이콘 시트·지형 타일·`world-plus.png`·갤러리 이미지): **CC BY 4.0**. EasyRPG RTP `ChipSet/World.png`(JasonPerry, CC0 원작, EasyRPG RTP 는 CC BY 4.0)의 팔레트·결을 따른 파생물이다. 출처: `tiledata/worldmap-kit/ATTRIBUTION.md`, `public/assets/ATTRIBUTION.md`.
- **코드**(Python·HTML·셸): **MIT** — `LICENSE`.
- 생성 이미지·트레이싱 없음. 다른 게임(크로노 트리거·파이널 판타지 등)의 그림·색값은 쓰지 않았다.
