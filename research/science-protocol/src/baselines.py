import json, math, os, sys

def load(outdir):
    data = {}
    for f in os.listdir(outdir):
        if f.endswith('.json'):
            with open(os.path.join(outdir, f)) as fh:
                data[f[:-5]] = json.load(fh)
    return data

def baseline_mechanics(t):
    # extrapolate last velocity linearly
    traj = t['trajectory']
    p0, p1 = traj[-2], traj[-1]
    return [2*b-a for a,b in zip(p0[0],p1[0])]

def baseline_eco(t):
    hist = t['history']
    n = len(t['species'])
    return [h[:n] for h in hist]

def baseline_chem(t):
    return t['history']

def baseline_gene(t):
    return t['history'][-1]

def baseline_astro(t):
    lc = t['lightcurve']
    mean = sum(lc)/len(lc)
    var = sum((x-mean)**2 for x in lc)/len(lc)
    return {'mean': round(mean,4), 'std': round(math.sqrt(var),4)}

def baseline_geo(t):
    rows = t['readings']
    return [round(sum(r)/len(r),3) for r in zip(*rows)]

BASE = {'mechanics':baseline_mechanics,'eco':baseline_eco,'chem':baseline_chem,
        'gene':baseline_gene,'astro':baseline_astro,'geo':baseline_geo}

def main(outdir):
    data = load(outdir)
    for w, tasks in data.items():
        preds = [BASE[w](t) for t in tasks[:5]]
        print(w, 'baseline sample:', str(preds[0])[:120])

if __name__=='__main__':
    main(sys.argv[1] if len(sys.argv)>1 else '../data')
