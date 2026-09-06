"""Per-row agreement between a cell's recorded CQ-03 block and a blind re-judgement of it."""
import json,collections,sys
from pathlib import Path
ROOT=Path('/Users/luis/Projects/malleus-dev')
for run in sys.argv[1:]:
    a=json.load(open(ROOT/f'paper-v4/evaluation-v4/run-{run}/review-block.CQ-03.json'))
    b=json.load(open(ROOT/f'paper-v4/evaluation-v4/run-{run}/reliability/review-block.CQ-03.json'))
    assert len(a['rows'])==len(b['rows']) and [r['row_index'] for r in a['rows']]==[r['row_index'] for r in b['rows']]
    pairs=collections.Counter((x['source_support'],y['source_support']) for x,y in zip(a['rows'],b['rows']))
    agree=sum(v for (x,y),v in pairs.items() if x==y); n=len(a['rows'])
    print(f'run-{run} CQ-03: rows {n}; recorded {a["question_responsiveness"]} vs blind {b["question_responsiveness"]}; row agreement {agree}/{n} = {agree/n:.3f}')
    print('  recorded labels', dict(collections.Counter(x['source_support'] for x in a['rows'])), '| blind labels', dict(collections.Counter(y['source_support'] for y in b['rows'])))
    print('  disagreements (recorded -> blind):', {f'{x}->{y}':v for (x,y),v in sorted(pairs.items()) if x!=y})
    # Cohen's kappa over the 4-label space
    labs=['SUPPORTED','PARTIAL','UNSUPPORTED','NOT_EVALUABLE']
    pa=collections.Counter(x['source_support'] for x in a['rows']); pb=collections.Counter(y['source_support'] for y in b['rows'])
    pe=sum((pa[l]/n)*(pb[l]/n) for l in labs); po=agree/n; kappa=(po-pe)/(1-pe) if pe<1 else float('nan')
    print(f'  Cohen kappa {kappa:.3f} (expected agreement {pe:.3f})')
