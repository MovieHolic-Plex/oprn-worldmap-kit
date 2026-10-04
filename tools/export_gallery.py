#!/usr/bin/env python3
"""하네스 저장소(sqlite + items/)를 읽어 정적 갤러리(docs/)를 만든다 — GitHub Pages 용.

  WMI_HARNESS_DATA=~/.local/share/oprn/worldmap-icon-harness python3 tools/export_gallery.py

아이콘마다 단품(1배)·지도 자리(1배)·검수자 판정(PASS/FAIL, 사유 코드, 「1배에서 무엇으로 읽히나」)·사용자 결정을 싣는다.
그림 파일 이름은 순번(ASCII)이고, 이름·설명은 docs/data.json 에 있다. 페이지는 외부 참조 없이 자체완결이다.
"""
import json
import shutil
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'src' / 'harnesses' / 'worldmap-icons'))
import harness as H  # noqa: E402
import bake  # noqa: E402

OUT = ROOT / 'docs'


def main():
    c = sqlite3.connect(f'file:{H.DATA}/harness.sqlite?mode=ro', uri=True)
    c.row_factory = sqlite3.Row
    c.execute('begin')
    rv, dec = H._latest_reviews(c), H._latest_decisions(c)
    selected = {x['id']: x for x in bake.live_selections()}
    names, roles = H.set_names(), H.role_names()
    if (OUT / 'img').exists():
        shutil.rmtree(OUT / 'img')
    sets = []
    for si, s in enumerate(H.SETS):
        man = json.loads((H.KIT_DIR / 'iconsets' / s / 'manifest.json').read_text())
        icons = []
        rows = list(c.execute('select * from items where iset=? order by role, name', (s,)))
        for ii, it in enumerate(rows):
            src = H.item_dir(it['id'])
            chosen = selected.get(it['id'])
            if chosen and chosen['candidate']:
                src = chosen['file'].parent
            dst = OUT / 'img' / f's{si:02d}'
            dst.mkdir(parents=True, exist_ok=True)
            files = {}
            for k in ('icon', 'ctx-x1'):
                file = chosen['file'] if k == 'icon' and chosen else src / f'{k}.png'
                if file.exists():
                    shutil.copy(file, dst / f'{ii:03d}-{k}.png')
                    files[k] = f'img/s{si:02d}/{ii:03d}-{k}.png'
            v, d = rv.get(it['id']), dec.get(it['id'])
            if chosen and chosen['candidate']:
                rid, letter = chosen['candidate'].split('/')
                cand = c.execute('select * from cands where round=? and letter=?', (int(rid[1:]), letter)).fetchone()
                v = dict(cand)
                v['body'] = json.loads(v['body']) if v.get('body') else {}
                v['codes'] = json.loads(v['codes']) if v.get('codes') else []
            body = (v or {}).get('body') or {}
            icons.append(dict(
                name=it['name'], role=it['role'], role_name=roles.get(it['role'], it['role']), cells=json.loads(it['cells']),
                desc=it['descr'] or '', place=it['place'] or '', img=files.get('icon'), ctx=files.get('ctx-x1'),
                verdict=(v or {}).get('verdict') if (v or {}).get('status') == 'done' else None,
                codes=(v or {}).get('codes') or [], reads_as=body.get('reads_as', ''), reasons=body.get('reasons', ''),
                decision=chosen['decision'] if chosen else ('reject' if (d or {}).get('decision') == 'reject' else None),
                selected_candidate=(chosen or {}).get('candidate'), sha256=(chosen or {}).get('sha256')))
        sets.append(dict(id=s, name=names.get(s, s), extends=man.get('extends'), kind=man.get('kind', 'land'),
                         camera=man.get('camera'), icons=icons))
    OUT.mkdir(exist_ok=True)
    c.close()
    downloads = OUT / 'downloads'
    downloads.mkdir(exist_ok=True)
    for source, name in [(bake.SHEET, 'worldmap-selected.png'), (bake.META, 'worldmapSelectedSheet.json'),
                         (bake.SOURCE / 'selected.json', 'selected.json'),
                         (ROOT / 'public/assets/worldmap-icons/ATTRIBUTION.md', 'ATTRIBUTION.md')]:
        shutil.copy2(source, downloads / name)
    (OUT / 'data.json').write_text(json.dumps(dict(sets=sets), ensure_ascii=False, indent=1) + '\n')
    tpl = (Path(__file__).parent / 'gallery.html').read_text(encoding='utf-8')
    (OUT / 'index.html').write_text(tpl.replace('/*DATA*/null', json.dumps(dict(sets=sets), ensure_ascii=False)), encoding='utf-8')
    n = sum(len(x['icons']) for x in sets)
    print(f'세트 {len(sets)} · 아이콘 {n} → {OUT}')


if __name__ == '__main__':
    main()
