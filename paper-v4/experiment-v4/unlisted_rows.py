"""Per frozen cell and question: executed ENTITY and SUBJECT rows whose witness
record's own type the question's type set never named (E-0199). Reads the
frozen public type sets and the private query results and export records,
which exist only where the private run directories do; nothing typed."""import json
from collections import Counter
from pathlib import Path
ROOT=Path('/Users/luis/Projects/malleus-dev')
RUNS=['08','09','10','11','12','13','14','15','16','19','20','21']
grand=Counter()
for n in RUNS:
    pub=ROOT/f'paper-v4/experiment-v4/run-{n}/results/query-type-sets.json'
    priv=ROOT/f'private/paper-v4-v4-run-{n}'
    sets=json.loads(pub.read_bytes()); ex=json.loads((priv/'results/export-records.json').read_bytes())
    typ={r['id']:r['type'] for fam in ('entities','events','relations') for r in ex.get(fam,[])}
    q=json.loads((priv/'query/query-result.json').read_bytes())
    for qq in q['queries']:
        qid=qq['question_id']; listed=set(sets[qid]); rows=qq['rows']
        own=Counter(); unlisted=Counter(); total=0
        for r in rows:
            if r.get('kind') not in ('ENTITY','SUBJECT'): continue
            total+=1; t=typ.get(r['witness']['record_id'],'?'); own[t]+=1
            if t not in listed: unlisted[t]+=1
        grand[n]+=sum(unlisted.values())
        flag=f"  UNLISTED {sum(unlisted.values())}: {dict(unlisted)}" if unlisted else ""
        print(f"run-{n} {qid}: rows {len(rows)} entity+subject {total}{flag}")
print('per cell unlisted rows:',dict(grand),'total',sum(grand.values()))
