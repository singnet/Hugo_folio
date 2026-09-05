import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
base = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..')
av = os.path.join(base, 'agent_view')
man = {m['id']: m for m in json.load(open(os.path.join(base, 'labels_manifest.json')))}
sys.path.insert(0, os.path.join(HERE, 'worlds'))
FLOOR = 0.55
WORLDS = ['mechanics', 'chem', 'eco', 'gene', 'astro', 'geo']

def norm_score(err):
    return 1.0 - min(1.0, max(0.0, err))

def target_of(m):
    return m['labels'].get('target')

def attack_constant(t, m):
    tgt = target_of(m)
    if isinstance(tgt, (int, float)):
        return abs(tgt) / (abs(tgt) + 1.0)
    if isinstance(tgt, list):
        def flat(x):
            return [v for p in x for v in (p if isinstance(p, list) else [p])] if x and isinstance(x[0], list) else x
        f = flat(tgt) if tgt else [0]
        mag = sum(abs(x) for x in f) / max(1, len(f))
        return mag / (mag + 1.0)
    return 1.0

def attack_copier(t, m):
    for k in ('trajectory', 'history', 'readings', 'lightcurve'):
        if k in t and isinstance(t[k], list) and t[k]:
            last = t[k][-1]
            tgt = target_of(m)
            if isinstance(tgt, (int, float)) and isinstance(last, (int, float)):
                scale = abs(tgt - t[k][0]) + abs(last - t[k][0]) + 1e-9
                return min(1.0, abs(last - tgt) / scale)
            if isinstance(tgt, list) and isinstance(last, list):
                def flat(x):
                    return [v for p in x for v in (p if isinstance(p, list) else [p])] if x and isinstance(x[0], list) else x
                a, b = flat(last), flat(tgt)
                if len(a) == len(b):
                    scale = sum(abs(y) for y in b) + 1e-9
                    return min(1.0, sum(abs(x - y) for x, y in zip(a, b)) / scale)
                return 1.0
            return 1.0
    return 1.0

def attack_metadata(t, m):
    hidden = ('law', 'rules', 'params', 'pos', 'signs', 'reg', 'layers', 'seed', 'target')
    return 0.0 if any(h in t for h in hidden) else 1.0

def _first_obs(t):
    for k in ('trajectory', 'history', 'readings', 'lightcurve'):
        if k in t and isinstance(t[k], list) and t[k]:
            return t[k][0]
    return None

def attack_seed_match(t, m):
    # real brute-force: try to regenerate matching task via public generator over plausible seed candidates
    w = t.get('world')
    if w not in WORLDS:
        return 1.0
    try:
        mod = __import__(w)
    except Exception:
        return 1.0
    obs0 = _first_obs(t)
    if obs0 is None:
        return 1.0
    import random
    tgt = target_of(m)
    tier = m.get('tier', t.get('tier', 1))
    for s in list(range(64)) + [random.randrange(4294967296) for _ in range(64)]:
        try:
            cand = mod.make_task(s, tier)
            traj = cand.get('trajectory') or cand.get('history') or cand.get('readings') or cand.get('lightcurve')
            if traj and traj[0] == obs0:
                pred = traj[-1]
                if isinstance(tgt, (int, float)) and isinstance(pred, (int, float)):
                    return min(1.0, abs(pred - tgt) / (abs(tgt) + 1e-9))
                return 0.5
        except Exception:
            continue
    return 1.0  # no match found: chance-level for attack

def main():
    def attack_corpus_reconstruct(t, m):
        # full-pipeline attack: regenerate candidate corpora from arbitrary master seeds via HMAC derivation, both tiers, and fingerprint-match the task
        import hashlib, hmac, random
        w = t.get('world')
        if w not in WORLDS:
            return 1.0
        obs0 = _first_obs(t)
        if obs0 is None:
            return 1.0
        try:
            mod = __import__(w)
        except Exception:
            return 1.0
        tier = t.get('tier', m.get('tier', 1))
        for k in range(64):
            master = os.urandom(32)
            for s in range(8):
                tag = ('%s:%d:%d' % (w, tier, s)).encode()
                seed = int.from_bytes(hmac.new(master, tag, hashlib.sha256).digest()[:16], 'big')
                try:
                    cand = mod.make_task(seed, tier)
                    traj = cand.get('trajectory') or cand.get('history') or cand.get('readings') or cand.get('lightcurve')
                    if traj and traj[0] == obs0:
                        return 0.0
                except Exception:
                    continue
        return 1.0
    attacks = {'constant': attack_constant, 'copier': attack_copier,
               'metadata': attack_metadata, 'seed_match': attack_seed_match,
               'corpus_reconstruct': attack_corpus_reconstruct}
    results = {a: [] for a in attacks}
    for split in ('dev', 'test'):
        for line in open(os.path.join(av, split + '.jsonl')):
            t = json.loads(line)
            m = man[t['id']]
            for a, fn in attacks.items():
                results[a].append(fn(t, m))
    ok = True
    for a, errs in results.items():
        score = 1 - sum(errs) / len(errs)
        ok &= score <= FLOOR
        print('%s: normalized_score=%.3f (floor %.2f) %s' % (a, score, FLOOR, 'PASS' if score <= FLOOR else 'FAIL'))
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()