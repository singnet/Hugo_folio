import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from baselines import load, BASE

def score_mech(t, pred):
    truth = t['trajectory'][-1]
    return sum((a-b)**2 for a,b in zip(truth[0], pred))

def pred_mech(t):
    traj = t['trajectory']
    pts = [row[0] for row in traj]
    m = 10
    seg = pts[-m:]
    pred = []
    for d in range(len(pts[0])):
        ys = [p_[d] for p_ in seg]
        S = [sum(x**k for x in range(m)) for k in range(5)]
        T = [sum(ys[x]*x**k for x in range(m)) for k in range(3)]
        A = [[S[0],S[1],S[2]],[S[1],S[2],S[3]],[S[2],S[3],S[4]]]
        for i in range(3):
            pv = A[i][i]
            for j in range(i,3): A[i][j] /= pv
            T[i] /= pv
            for r2 in range(3):
                if r2 != i and A[r2][i] != 0:
                    f = A[r2][i]
                    for j in range(i,3): A[r2][j] -= f*A[i][j]
                    T[r2] -= f*T[i]
        a0,a1,a2 = T
        pred.append(a0 + a1*m + a2*m*m)
    return pred

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
    # majority rule over last 5 steps: predict gene state per gene
    hist = t['history'][-5:]
    pred = {}
    genes = list(hist[-1].keys())
    for g in genes:
        votes = [h[g] for h in hist if g in h]
        pred[g] = 1 if sum(votes) > len(votes)/2 else 0
    return pred

def score_gene(t, pred):
    truth = t['history'][-1]
    agree = sum(1 for g in truth if truth[g]==pred.get(g, not truth[g]))
    return 1 - agree/len(truth)

def pred_astro(t):
    import math
    lc = t['lightcurve']
    mean = sum(lc)/len(lc)
    var = sum((x-mean)**2 for x in lc)/len(lc)
    std = math.sqrt(var)
    # min/max excursion relative to std separates modes
    lo = min(lc); hi = max(lc)
    if std < 0.01:
        mode = 'flare'      # low variance: quiet/flare baseline
    elif hi - lo > 0.8:
        mode = 'spot'       # deep asymmetric dips
    else:
        mode = 'pulsator'   # regular moderate variation
    return {'mean': mean, 'std': std, 'mode': mode}

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
