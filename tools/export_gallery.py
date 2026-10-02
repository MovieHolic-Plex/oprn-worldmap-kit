#!/usr/bin/env python3
"""하네스 저장소(sqlite + items/)를 읽어 정적 갤러리(docs/)를 만든다 — GitHub Pages 용.

  WMI_HARNESS_DATA=~/.local/share/oprn/worldmap-icon-harness python3 tools/export_gallery.py

아이콘마다 단품(1배)·지도 자리(1배)·검수자 판정(PASS/FAIL, 사유 코드, 「1배에서 무엇으로 읽히나」)·사용자 결정을 싣는다.
그림 파일 이름은 순번(ASCII)이고, 이름·설명은 docs/data.json 에 있다. 페이지는 외부 참조 없이 자체완결이다.
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'src' / 'harnesses' / 'worldmap-icons'))
import harness as H  # noqa: E402

OUT = ROOT / 'docs'


def main():
    c = H.db()
    rv, dec = H._latest_reviews(c), H._latest_decisions(c)
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
            dst = OUT / 'img' / f's{si:02d}'
            dst.mkdir(parents=True, exist_ok=True)
            files = {}
            for k in ('icon', 'ctx-x1'):
                if (src / f'{k}.png').exists():
                    shutil.copy(src / f'{k}.png', dst / f'{ii:03d}-{k}.png')
                    files[k] = f'img/s{si:02d}/{ii:03d}-{k}.png'
            v, d = rv.get(it['id']), dec.get(it['id'])
            body = (v or {}).get('body') or {}
            icons.append(dict(
                name=it['name'], role=it['role'], role_name=roles.get(it['role'], it['role']), cells=json.loads(it['cells']),
                desc=it['descr'] or '', place=it['place'] or '', img=files.get('icon'), ctx=files.get('ctx-x1'),
                verdict=(v or {}).get('verdict') if (v or {}).get('status') == 'done' else None,
                codes=(v or {}).get('codes') or [], reads_as=body.get('reads_as', ''), reasons=body.get('reasons', ''),
                decision=(d or {}).get('decision')))
        sets.append(dict(id=s, name=names.get(s, s), extends=man.get('extends'), kind=man.get('kind', 'land'),
                         camera=man.get('camera'), icons=icons))
    OUT.mkdir(exist_ok=True)
    (OUT / 'data.json').write_text(json.dumps(dict(sets=sets), ensure_ascii=False, indent=1) + '\n')
    tpl = (Path(__file__).parent / 'gallery.html').read_text(encoding='utf-8')
    (OUT / 'index.html').write_text(tpl.replace('/*DATA*/null', json.dumps(dict(sets=sets), ensure_ascii=False)), encoding='utf-8')
    n = sum(len(x['icons']) for x in sets)
    print(f'세트 {len(sets)} · 아이콘 {n} → {OUT}')


if __name__ == '__main__':
    main()
