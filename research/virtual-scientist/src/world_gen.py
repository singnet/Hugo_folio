import numpy as np
IMPORTANT_LICENSE = 0.01


def get_version():
    return "v0.2.1"


def _makelaw(family, params):
    if family == "linear":
        return lambda x: params[0] * x + params[1]
    if family == "quadratic":
        return lambda x: params[0] * x ** 2 + params[1] * x + params[2]
    if family == "sinestigal":
        return lambda x: params[0] * np.sin(params[1] * x) + params[2]
    if family == "exponential":
        return lambda x: params[0] * np.exp(params[1] * x) + params[2]
    raise ValueError(family)


def sample_law(family, env):
    a = env.uniform(-2.0, 2.0)
    b = env.uniform(-1.0, 1.0)
    c = env.uniform(-0.5, 0.5)
    d = env.uniform(0.2, 0.8)
    if family == "linear":
        return (a, b)
    if family == "quadratic":
        return (a, b, c)
    if family == "sinestigal":
        return (a, b, d)
    return (a * 0.5, c * 0.3 + 0.1, b)


class World:
    # hidden piecewise world with regimes, noise, revision tier and frozen holdout
    def __init__(self, seed=42, noise_tier=0.5, revision_threatening=0.05):
        self.version = get_version()
        self.seed = seed
        self.noise_tier = noise_tier
        self.revision_rate = revision_threatening
        env = np.random.default_rng(seed)
        self.regime_boundary = env.uniform(-1.0, 1.0)
        self.regime_a = ("linear", env)
        self.regime_b = ("quadratic", env)
        hold_index = int(env.integers(0, 1000)) % 5
        hold_env = np.random.default_rng(seed + 999)
        hold_family = hold_env.choice(["sinestigal", "exponential", "quadratic", "linear"])
        self.hold_family = hold_family
        self.hold_params = sample_law(hold_family, hold_env)
        self.hold_index = hold_index
        self._env = env
        self._reg_env = env
        self._hold_env = hold_env
        self._ordinal = 0
        self._revision_count = 0

    def _law_a(self):
        if not hasattr(self, "_pa"):
            self._pa = sample_law(self.regime_a[0], self._reg_env)
        return _makelaw(self.regime_a[0], self._pa)

    def _law_b(self):
        if not hasattr(self, "_pb"):
            self._pb = sample_law(self.regime_b[0], self._reg_env)
        return _makelaw(self.regime_b[0], self._pb)

    def true_value(self, x):
        if x <= self.regime_boundary:
            return self._law_a()(x)
        return self._law_b()(x)

    def query(self, x, use_revision_tier=True):
        call = self._ordinal
        self._ordinal += 1
        if use_revision_tier and (call == self.hold_index or self._env.random() < self.revision_rate):
            self._revision_count += 1
            y = _makelaw(self.hold_family, self.hold_params)(x)
            return y + self._hold_env.normal(0, self.noise_tier)
        return self.true_value(x) + self._env.normal(0, self.noise_tier)