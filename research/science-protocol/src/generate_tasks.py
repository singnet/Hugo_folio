import json, sys, os
sys.path.insert(0, os.path.dirname(__file__) + '/worlds')
import mechanics, eco, chem, gene, astro, geo

WORLDS = {
    'mechanics': mechanics, 'eco': eco, 'chem': chem,
    'gene': gene, 'astro': astro, 'geo': geo
}

def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    for name, mod in WORLDS.items():
        tasks = [mod.make_task(s, t) for t in (1, 2) for s in range(50)]
        path = os.path.join(outdir, name + '.json')
        with open(path, 'w') as f:
            json.dump(tasks, f)
        print(name, len(tasks), path)

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '../data')
