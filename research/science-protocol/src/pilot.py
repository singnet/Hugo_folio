import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from baselines import load, BASE

def score_mech(t, pred):
    truth = t['trajectory'][-1]
    return sum((a-b)**2 for a,b in zip(truth[0], pred))

def pred_mech(t):
    traj = t['trajectory']
    p0, p1 = traj[-2], traj[-1]
    return [2*b-a for a,b in zip(p0[0],p1[0])]

def pred_eco(t):
    hist = t['history']; n = len(t['species'])
    rows = [h[:n] for h in hist]
    return [2*b-a for a,b in zip(rows[-2],rows[-1])]

def score_eco(t, pred):
    hist = t['history']; n = len(t['species'])
    truth = [h[:n] for h in hist]
    return sum((a-b)**2 for a,b in zip(truth[-1], pred))

def pred_chem(t):
    return t['history'][40]

def score_chem(t, pred):
    truth = t['history'][-1]
    return sum(abs(truth[e]-pred.get(e,0)) for e in truth)

def pred_gene(t):
    return t['history'][-2]

def score_gene(t, pred):
    truth = t['history'][-1]
    agree = sum(1 for g in truth if truth[g]==pred.get(g, not truth[g]))
    return 1 - agree/len(truth)

def pred_astro(t):
    import math
    lc = t['lightcurve']
    mean = sum(lc)/len(lc)
    var = sum((x-mean)**2 for x in lc)/len(lc)
    # guess mode from variance
    if var < 0.005: mode = 'flare'
    elif min(lc) < 0.6: mode = 'spot'
    else: mode = 'pulsator'
    return {'mean': mean, 'std': math.sqrt(var), 'mode': mode}

def score_astro(t, pred):
    truth = t['params']['mode']
    return 0.0 if pred['mode']==truth else 1.0

def pred_geo(t):
    rows = t['readings']
    return [round(sum(r)/len(r),3) for r in zip(*rows)]

def score_geo(t, pred):
    total=0.0; truth=[]
    for L in t['layers']:
        total += L['thickness']/L['wave_speed']; truth.append(total)
    return sum((a-b)**2 for a,b in zip(truth, pred))

PRED = {'mechanics':pred_mech,'eco':pred_eco,'chem':pred_chem,'gene':pred_gene,'astro':pred_astro,'geo':pred_geo}
SCORE = {'mechanics':score_mech,'eco':score_eco,'chem':score_chem,'gene':score_gene,'astro':score_astro,'geo':score_geo}

def main(outdir):
    data = load(outdir)
    for w, tasks in data.items():
        errs = [SCORE[w](t, PRED[w](t)) for t in tasks[:10]]
        print(w, 'mean score over 10 tasks:', round(sum(errs)/len(errs),4))

if __name__=='__main__':
    main(sys.argv[1] if len(sys.argv)>1 else '../data')
