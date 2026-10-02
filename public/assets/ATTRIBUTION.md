# 원본 칩셋 출처

이 저장소는 아래 파일 중 `easyrpg-chipset-world.png` 하나만 싣는다(월드맵 팔레트·결의 기준).

## EasyRPG RTP bundled map and object assets

- Files:
  - `easyrpg-chipset-exterior.png` from `ChipSet/Exterior.png` (renamed 2026-08-21 — the
    former name `rm2k3-original-chipset.png` wrongly implied the proprietary RPG Maker RTP)
  - `easyrpg-chipset-dungeon.png` from `ChipSet/Dungeon.png`
  - `easyrpg-chipset-interior.png` from `ChipSet/Interior.png`
  - `easyrpg-chipset-ship.png` from `ChipSet/Ship.png`
  - `easyrpg-chipset-world.png` from `ChipSet/World.png`
  - `easyrpg-chipset-retro-dungeon.png` from `ChipSet/retro_Dungeon.png`
  - `easyrpg-chipset-retro-exterior.png` from `ChipSet/retro_Exterior.png`
  - `easyrpg-chipset-retro-world.png` from `ChipSet/retro_World.png`
  - `easyrpg-charset-object1.png` from `CharSet/Object1.png`
  - `easyrpg-charset-object2.png` from `CharSet/Object2.png`
- Repository: https://github.com/EasyRPG/RTP
- License: Creative Commons Attribution 4.0 International for EasyRPG RTP materials
- Upstream asset attribution:
  - `ChipSet/Dungeon.png`, `Exterior.png`, `Interior.png`, `Ship.png`, `World.png` by JasonPerry, CC0, https://finalbossblues.itch.io/
  - `ChipSet/retro_Dungeon.png` by Dmytro Kushnariov, CC0, https://easyrpg.org
  - `ChipSet/retro_Exterior.png`, `retro_World.png`: see `vendor/easyrpg-rtp/AUTHORS.md` for mixed CC-BY/CC0/WTFPL source attribution.
  - `CharSet/Object1.png` by Tom Lemmens and Blarumyrran, CC0 original chest, https://github.com/lemtom
  - `CharSet/Object2.png` by Verdant_Jack, CC0, https://community.easyrpg.org/t/test-for-new-rtp/1067/8
- Notes: This is an open replacement RTP material, not the proprietary RPG Maker 2000/2003 RTP.
- Pixel provenance verified 2026-08-23: `easyrpg-chipset-exterior.png` is produced by
  `scripts/generate-easyrpg-chipset-exterior.mjs` (renamed from `generate-rm2k3-original-chipset.mjs`)
  from `vendor/easyrpg-rtp/ChipSet/Exterior.png`. Its `IHDR`, `PLTE`, and `IDAT` chunks are
  byte-identical to the vendor file; the only difference is an inserted `tRNS` chunk making
  palette index 0 transparent. The pixels are JasonPerry's CC0 replacement art, not Enterbrain's.
- Derived sheet (2026-09-18): `easyrpg-chipset-combined-town-retro-world-transparent.png` (480×608) is
  produced by `scripts/gen-combined-town-retro-world-chipset.mjs`. Rows 0–255 are
  `easyrpg-chipset-combined-town-transparent.png` copied byte-for-byte; rows 256–511 are
  `easyrpg-chipset-retro-world-transparent.png` with its palette-index-0 colour (224,103,191) keyed to
  alpha 0 (that file ships with no alpha at all); rows 512–607 are `chipset-ext-forest-trees.png`
  copied byte-for-byte (see the next section). No pixels are authored here. The retro_World half
  carries the mixed CC-BY/CC0/WTFPL attribution listed above, which is why the in-app name says
  "혼합 출처".

