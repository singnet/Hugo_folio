# test_world_gen.py v0.2.1 seed=42
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
import world_gen
from world_gen import World

def test_regime_correctness():
    w = World(seed=42)
    xs = np.linspace(-3, 3, 100)
    for x in xs:
        if x <= w.regime_boundary:
            assert abs(w.true_value(x) - w._law_a()(x)) < 1e-12
        else:
            assert abs(w.true_value(x) - w._law_b()(x)) < 1e-12
    print("PASS regime correctness")

def test_holdout_freeze():
    w1, w2 = World(seed=42), World(seed=42)
    assert w1.hold_family == w2.hold_family
    assert w1.hold_params == w2.hold_params
    assert w1.hold_index == w2.hold_index
    print("PASS holdout freeze (deterministic seed 42)")

def test_revision_indistinguishable():
    # KS test: revision-tier residuals should be similar in scale to ordinary noise
    from scipy.stats import ks_2samp
    w = World(seed=42, noise_tier=0.5, revision_threatening=0.0)
    xs = np.random.default_rng(1).uniform(-3, 3, 300)
    resid = [w.query(float(x)) - w.true_value(float(x)) for x in xs]
    hold_r = np.random.default_rng(43).normal(0, 0.5, 300)
    stat, p = ks_2samp(resid, hold_r)
    assert p > 0.05, f"residuals distinguishable: p={p}"
    print(f"PASS residual indistinguishability (KS p={p:.3f})")

def test_revision_tier_occurs():
    w = World(seed=42)
    for _ in range(500):
        w.query(0.5)
    assert w._revision_count > 0
    print("PASS revision tier active")

def test_version():
    assert world_gen.get_version() == "v0.2.1"
    print("PASS version")

if __name__ == "__main__":
    test_regime_correctness()
    test_holdout_freeze()
    test_revision_indistinguishable()
    test_revision_tier_occurs()
    test_version()
    print("ALL TESTS PASSED")