
import json, os, hashlib, hmac
HERE = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.insert(0, os.path.join(HERE, 'worlds'))
WORLDS = {n: __import__(n) for n in ('mechanics', 'chem', 'eco', 'gene', 'astro', 'geo')}

def derive_seeds():
    seed_path = os.path.join(HERE, '..', 'secrets', 'master_seed.txt')
    master = open(seed_path, 'rb').read().strip()
    out = {}
    for name in WORLDS:
        for t in (1, 2):
            for s in range(50):
                tag = ('%s:%d:%d' % (name, t, s)).encode()
                out[(name, t, s)] = int.from_bytes(hmac.new(master, tag, hashlib.sha256).digest()[:4], 'big')
    return out

def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    seeds = derive_seeds()
    for name, mod in WORLDS.items():
        tasks = [mod.make_task(seeds[(name, t, s)], t) for t in (1, 2) for s in range(50)]
        path = os.path.join(outdir, name + '.json')
        with open(path, 'w') as f:
            json.dump(tasks, f)
        print(name, len(tasks), path)

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'data')
