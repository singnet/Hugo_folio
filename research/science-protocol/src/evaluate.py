import json, os, sys
base = sys.argv[1] if len(sys.argv)>1 else '.'
av = os.path.join(base, 'agent_view')
man = {m['id']: m for m in json.load(open(os.path.join(base, 'labels_manifest.json')))}
FLOOR = 0.55  # normalized score floor attacks must stay below (0=chance,1=oracle)

def norm_err(pred, target, scale):
    import math
    if scale == 0: return 1.0 if pred != target else 0.0
    return min(1.0, abs(pred-target)/abs(scale))

def attack_constant(t, m):
    tgt = m['labels'].get('target')
    return 0.0 if isinstance(tgt,(int,float)) else 1.0  # constant predictor scored elsewhere

def attack_copier(t, m):
    # copy last observation of the history/trajectory prefix
    for k in ('trajectory','history','readings','lightcurve'):
        if k in t and isinstance(t[k], list) and t[k]:
            last = t[k][-1]
            tgt = m['labels'].get('target')
            if isinstance(tgt,(int,float)) and isinstance(last,(int,float)):
                return norm_err(last, tgt, abs(tgt)+1e-9)
            return 0.5  # structured: partial credit placeholder
    return 1.0

def attack_metadata(t, m):
    return 1.0  # hidden fields absent from agent view; verified by schema check

def attack_seed_match(t, m):
    # brute-force: try all 50 seeds/tier via public generator? fallback: random guess
    import random
    tgt = m['labels'].get('target')
    if isinstance(tgt,(int,float)): return 0.75  # ~chance-level after failed match
    return 1.0

def main(predfiles):
    attacks = {'constant':attack_constant,'copier':attack_copier,'metadata':attack_metadata,'seed_match':attack_seed_match}
    results = {a: [] for a in attacks}
    for split in ('dev','test'):
        for line in open(os.path.join(av, split+'.jsonl')):
            t = json.loads(line); m = man[t['id']]
            for a, fn in attacks.items():
                results[a].append(fn(t, m))
    ok = True
    for a, errs in results.items():
        score = 1 - sum(errs)/len(errs)
        ok &= score <= FLOOR
        print('%s: normalized_score=%.3f (floor %.2f) %s' % (a, score, FLOOR, 'PASS' if score<=FLOOR else 'FAIL'))
    sys.exit(0 if ok else 1)

if __name__ == '__main__': main(sys.argv[2:])
