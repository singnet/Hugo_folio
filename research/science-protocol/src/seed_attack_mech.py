import sys, os, json, random
sys.path.insert(0, '/PeTTa/repos/OmegaClaw-Core/memory/Hugo_folio/research/science-protocol/src/worlds')
import mechanics
base = '/PeTTa/repos/OmegaClaw-Core/memory/Hugo_folio/research/science-protocol'
av = os.path.join(base, 'agent_view')
man = {m['id']: m for m in json.load(open(os.path.join(base, 'labels_manifest.json')))}
def brute(seed_guess, tier, obs0):
    try:
        t = mechanics.make_task(seed_guess, tier)
        return t['trajectory'][0] == obs0
    except Exception:
        return False
def attack(t, m):
    traj = t.get('trajectory')
    if not traj or t['world'] != 'mechanics': return None
    obs0 = traj[0]
    n = len(traj[0])
    tier = 1 if n == 2 else 2
    for s in range(50):
        if brute(s, tier, obs0):
            task = mechanics.make_task(s, tier)
            true = m['labels'].get('target')
            pred = task['trajectory'][-1]
            if true is None: return None
            err = sum(abs(a-b) for pa,pb in zip(pred,true) for a,b in zip(pa,pb))/max(1e-9, sum(abs(x) for p in true for x in p))
            return min(1.0, err)
    return 1.0
res = []
for split in ('dev','test'):
    for line in open(os.path.join(av, split+'.jsonl')):
        t = json.loads(line); m = man[t['id']]
        r = attack(t, m)
        if r is not None: res.append(r)
print('seed_match mechanics: n=%d normalized_score=%.3f' % (len(res), 1 - sum(res)/len(res)))
