import math

def scan(val, path):
    if isinstance(val, bool):
        return []
    if isinstance(val, float):
        if math.isnan(val):
            return [(path, val, "nan")]
        if val == math.inf:
            return [(path, val, "+inf")]
        if val == -math.inf:
            return [(path, val, "-inf")]
        return []
    if isinstance(val, list):
        out = []
        for i, v in enumerate(val):
            out += scan(v, path + "[" + str(i) + "]")
        return out
    if isinstance(val, dict):
        out = []
        for k, v in val.items():
            out += scan(v, path + "." + k)
        return out
    return []

def validate(instance, append_failure, lane_assign, scorer):
    triggers = scan(instance, "root")
    if triggers:
        path, val, kind = triggers[0]
        append_failure(path, kind)
        return False
    lane_assign(instance)
    scorer(instance)
    return True

def test_f08():
    lane_calls = scorer_calls = 0
    failures = []
    state = {}

    def lane(x):
        nonlocal lane_calls
        lane_calls += 1
        state[id(x)] = "lane"

    def scorer(x):
        nonlocal scorer_calls
        scorer_calls += 1

    def fail(p, k):
        failures.append((p, k))

    cases = {
        "cand_loss": {"candidates": [{}, {}, {"metrics": {"loss": float("inf")}}]},
        "nested_array": {"l": [1.0, [float("nan"), [2.0, [float("inf")]]]]},
        "nan": {"m": float("nan")},
        "mixed_inf": {"p": math.inf, "n": -math.inf},
        "good": {"m": 1.5},
    }
    for name, case in cases.items():
        ok = validate(case, fail, lane, scorer)
        assert ok == (name == "good"), name
    assert lane_calls == 1 and scorer_calls == 1
    assert len(failures) == 4
    assert failures[0] == ("root.candidates[2].metrics.loss", "+inf")
    assert id(cases["cand_loss"]) not in state
    print("f08 tests passed: 4 failures recorded, lane/scorer invoked once (good only)")

if __name__ == "__main__":
    test_f08()