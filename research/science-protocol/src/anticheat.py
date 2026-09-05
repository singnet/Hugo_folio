import json, glob, os, sys
base = sys.argv[1] if len(sys.argv)>1 else '.'
av = os.path.join(base, 'agent_view')
man = {m['id']: m for m in json.load(open(os.path.join(base, 'labels_manifest.json')))}
BANNED_KEYS = ['law','rules','pos','signs','reg','params','layers','seed']
def load(split):
    return [json.loads(l) for l in open(os.path.join(av, split+'.jsonl'))]
def check_copier(t):
    # last-observation copier: predict final history state for mechanics/eco/gene
    if 'history' in t: return t['history'][-1]
    return None
fails = []
for split in ['train','dev','test']:
    for t in load(split):
        for k in BANNED_KEYS:
            if k in t: fails.append((t['id'], 'metadata leak: '+k))
        # constant/copier trivially available via history; count as leak only if scoring hits ceiling (checked in evaluator)
        if 'seed' in json.dumps(t).lower(): fails.append((t['id'], 'seed string present'))
# manifest must be outside agent view and match ids
ids_av = set(); 
for split in ['train','dev','test']:
    ids_av |= {t['id'] for t in load(split)}
ids_man = set(man)
if ids_av != ids_man: fails.append(('manifest','id mismatch: %d/%d' % (len(ids_av-ids_man), len(ids_man-ids_av))))
print('anticheat:', 'PASS' if not fails else 'FAIL %d' % len(fails))
for f in fails[:10]: print(f)
sys.exit(1 if fails else 0)
