import sys, json, os
sys.path.insert(0, "/PeTTa/repos/OmegaClaw-Core/memory/workflow_space/research/virtual-scientist/src")
import numpy as np
import world_gen, baselines, scoring

SEED = 42
rng = np.random.default_rng(SEED)
world = world_gen.World(seed=SEED)

fams = ["linear", "quadratic", "sinestigal", "exponential"]
cands = fams + ["%s->%s" % (a, b) for a in fams for b in fams]
true_idx = "%s->%s" % (world.regime_a[0], world.regime_b[0])

# Interactive phase: agents query world WITH revision tier (holdout contamination)
xs = list(rng.uniform(-3.0, 3.0, 150))
ys = [world.query(x) for x in xs]

# Evaluation on frozen revision holdout: true-value predictions + none-fit honesty
qs = list(rng.uniform(-3.0, 3.0, 50))
actuals = [world.true_value(x) for x in qs]

results = {}
agents = {
    "Memorizer": baselines.Memorizer(xs, ys),
    "CurveFitter": baselines.CurveFitter(xs, ys),
    "HonestAgent": baselines.HonestAgent(xs, ys, world, rng),
}
for name, ag in agents.items():
    preds = [ag.predict(x) for x in qs]
    post = None
    if hasattr(ag, "posterior"):
        try:
            post = ag.posterior(cands)
        except Exception:
            post = None
    if post is None:
        post = [1.0 / len(cands)] * len(cands)
    ti = cands.index(true_idx) if true_idx in cands else true_idx
    results[name] = scoring.score_agent(preds, actuals, post, ti)
    results[name]["revision_queries"] = getattr(world, "_revision_count", 0) if name == "HonestAgent" else None

outdir = "/PeTTa/repos/OmegaClaw-Core/memory/workflow_space/research/virtual-scientist/runs"
os.makedirs(outdir, exist_ok=True)
with open(outdir + "/exp2.json", "w") as f:
    json.dump({"version": "v0.2.1", "seed": SEED, "agents": results}, f, indent=2)
print(json.dumps(results, indent=2))