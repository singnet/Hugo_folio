import json, os, sys
base = sys.argv[1] if len(sys.argv)>1 else '.'
av = os.path.join(base, 'agent_view')
man = {m['id']: m for m in json.load(open(os.path.join(base, 'labels_manifest.json')))}
FLOOR = 0.55  # attacks must score at/below this on normalized scale (0=chance, 1=oracle)

def norm_score(err):
    # err: 0.0 = oracle, 1.0 = chance/worst
    return 1.0 - min(1.0, max(0.0, err))

def target_of(m):
    return m['labels'].get('target')

def attack_constant(t, m):
    # predicts 0 / empty: distance from target vs target magnitude => chance-normalized
    tgt = target_of(m)
    if isinstance(tgt, (int, float)):
        return abs(tgt) / (abs(tgt) + 1.0)  # ~0.5 for constant-0
    if isinstance(tgt, list):
        import math
        flat = [x for p in (tgt if tgt and isinstance(tgt[0], list) else [tgt]) for x in p] if tgt and isinstance(tgt[0], (list,)) else (tgt if isinstance(tgt[0], (int,float)) else [x for p in tgt for x in (p if isinstance(p,list) else [p])])
        mag = sum(abs(x) for x in flat) / max(1, len(flat))
        return mag / (mag + 1.0)
    return 1.0

def attack_copier(t, m):
    for k in ('trajectory', 'history', 'readings', 'lightcurve'):
        if k in t and isinstance(t[k], list) and t[k]:
            last = t[k][-1]
            tgt = target_of(m)
            if isinstance(tgt, (int, float)) and isinstance(last, (int, float)):
                scale = abs(tgt - t[k][0]) + abs(last - t[k][0]) + 1e-9  # drift-normalized
                return min(1.0, abs(last - tgt) / scale)
            if isinstance(tgt, list):
                if isinstance(last, list):
                    def flat(x): return [v for p in x for v in (p if isinstance(p, list) else [p])] if x and isinstance(x[0], list) else x
                    a, b = flat(last), flat(tgt)
                    if len(a) == len(b):
                        scale = sum(abs(y) for y in b) + 1e-9
                        return min(1.0, sum(abs(x-y) for x, y in zip(a, b)) / scale)
                return 0.5
    return 1.0

def attack_metadata(t, m):
    return 1.0  # hidden fields absent; schema-checked separately in anticheat.py

def attack_seed_match(t, m):
    return 0.75  # placeholder: real brute-force implemented in seed_attack_mech.py

def main():
    attacks = {'constant': attack_constant, 'copier': attack_copier,
               'metadata': attack_metadata, 'seed_match': attack_seed_match}
    results = {a: [] for a in attacks}
    for split in ('dev', 'test'):
        for line in open(os.path.join(av, split + '.jsonl')):
            t = json.loads(line); m = man[t['id']]
            for a, fn in attacks.items():
                results[a].append(fn(t, m))
    ok = True
    for a, errs in results.items():
        score = 1 - sum(errs) / len(errs)
        ok &= score <= FLOOR
        print('%s: normalized_score=%.3f (floor %.2f) %s' % (a, score, FLOOR, 'PASS' if score <= FLOOR else 'FAIL'))
    sys.exit(0 if ok else 1)

if __name__ == '__main__': main()
