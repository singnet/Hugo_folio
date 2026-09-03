# baselines.py v0.2.1 seed=42
import numpy as np
import world_gen

N_TRAIN = 200
N_EVAL = 50
SEED = 42


def collect_data(world, n, rng):
    xs = rng.uniform(-3.0, 3.0, n)
    return xs, np.array([world.query(float(x)) for x in xs])


class Memorizer:
    # nearest-neighbor echo of training data
    def __init__(self, xs, ys):
        self.xs, self.ys = np.asarray(xs), np.asarray(ys)
    def predict(self, x):
        i = int(np.argmin(np.abs(self.xs - x)))
        return float(self.ys[i])


class CurveFitter:
    # global polynomial fit, degree 4 (robust to small n)
    def __init__(self, xs, ys, degree=4):
        self.coef = np.polyfit(xs, ys, min(degree, len(set(xs)) - 1))
    def predict(self, x):
        return float(np.polyval(self.coef, x))


def _fit_family(name, xs, ys):
    # return fitted predictions and residual mse for a candidate family
    xs, ys = np.asarray(xs), np.asarray(ys)
    if name == "linear":
        c = np.polyfit(xs, ys, 1)
    elif name == "quadratic":
        c = np.polyfit(xs, ys, 2)
    elif name == "sinestigal":
        c = np.polyfit(np.sin(2 * xs), ys, 1)
    elif name == "exponential":
        c = np.polyfit(np.exp(xs), ys, 1)
    else:
        return None, None
    preds = np.polyval(c, {"linear": xs, "quadratic": xs,
                           "sinestigal": np.sin(2 * xs),
                           "exponential": np.exp(xs)}[name])
    return preds, float(np.mean((preds - ys) ** 2))


class HonestAgent:
    # extra queries + per-family fits -> posterior over candidate laws
    def __init__(self, xs, ys, world, rng, n_extra=100):
        extra_x = rng.uniform(-3.0, 3.0, n_extra)
        extra_y = np.array([world.query(float(x)) for x in extra_x])
        self.xs = np.concatenate([np.asarray(xs), extra_x])
        self.ys = np.concatenate([np.asarray(ys), extra_y])
        d = min(4, len(set(self.xs)) - 1)
        self.model = CurveFitter(self.xs, self.ys, degree=d)
        order = np.argsort(self.xs)
        xs_o, ys_o = self.xs[order], self.ys[order]
        best_b, best_r = None, np.inf
        for b in np.linspace(-2.5, 2.5, 21):
            lo = xs_o <= b; hi = xs_o > b
            if lo.sum() < 5 or hi.sum() < 5: continue
            r = 0.0
            for m in (lo, hi):
                c = np.polyfit(xs_o[m], ys_o[m], 1)
                r += float(np.mean((np.polyval(c, xs_o[m]) - ys_o[m])**2))
            if r < best_r: best_b, best_r = b, r
        self.boundary = best_b
        self.family_mse = {}
        lo = xs_o <= best_b; hi = xs_o > best_b
        for fam in ['linear', 'quadratic', 'sinestigal', 'exponential']:
            mses = []
            for m in (lo, hi):
                xt = {'linear': xs_o[m], 'quadratic': xs_o[m],
                      'sinestigal': np.sin(2*xs_o[m]), 'exponential': np.exp(xs_o[m])}[fam]
                if xt.std() < 1e-12: continue
                c = np.polyfit(xt, ys_o[m], 1)
                mses.append(float(np.mean((np.polyval(c, xt) - ys_o[m])**2)))
            self.family_mse[fam] = sum(mses)/len(mses) if mses else None
        # composite hypotheses: (left_family, right_family) piecewise at boundary
        self.composite_mse = {}
        fams = ['linear', 'quadratic', 'sinestigal', 'exponential']
        for fl in fams:
            for fr in fams:
                mses = []
                for m, fam in ((lo, fl), (hi, fr)):
                    xt = {'linear': xs_o[m], 'quadratic': xs_o[m],
                          'sinestigal': np.sin(2*xs_o[m]), 'exponential': np.exp(xs_o[m])}[fam]
                    if xt.std() < 1e-12: continue
                    c = np.polyfit(xt, ys_o[m], 1)
                    mses.append(float(np.mean((np.polyval(c, xt) - ys_o[m])**2)))
                if len(mses) == 2:
                    self.composite_mse[(fl, fr)] = sum(mses)/2
        # merge into family_mse under composite names for posterior()
        for k, v in self.composite_mse.items():
            self.family_mse['%s->%s' % k] = v
    def posterior(self, cands):
        # softmax over negative mses; uniform if unknown family
        import math
        vals = []
        for c in cands:
            mse = self.family_mse.get(c)
            vals.append(-math.log(mse if mse and mse > 1e-12 else 1e-12))
        m = max(vals)
        ex = [math.exp(v - m) for v in vals]
        s = sum(ex)
        return [e / s for e in ex]
    def predict(self, x):
        return self.model.predict(x)


def run():
    rng = np.random.default_rng(SEED)
    world = world_gen.World(seed=SEED)
    xs, ys = collect_data(world, N_TRAIN, rng)
    eval_x = np.linspace(-3.0, 3.0, N_EVAL)
    truth = np.array([world.true_value(float(x)) for x in eval_x])
    results = {"version": world_gen.get_version(), "seed": SEED, "n_train": N_TRAIN, "n_eval": N_EVAL}
    for name, agent in [("memorizer", Memorizer(xs, ys)), ("curve-fitter", CurveFitter(xs, ys)), ("honest-stub", HonestAgent(xs, ys, world, rng))]:
        preds = np.array([agent.predict(float(x)) for x in eval_x])
        results[name] = float(np.mean((preds - truth) ** 2))
    return results


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2))
