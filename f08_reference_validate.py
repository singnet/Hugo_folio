import math

# Executable reference implementation of the F08 validation boundary.
# NOT an integration test: the repository has no production validate
# boundary yet. Persists failure records via the FailureLog interface.

class FailureLog:
    def __init__(self):
        self.records = []
    def append_failure(self, path, kind):
        self.records.append((path, kind))
    def count(self):
        return len(self.records)

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

def validate(instance, failure_log, lane_assign, scorer):
    # Validation must run BEFORE any lane assignment or scoring.
    triggers = scan(instance, "root")
    if triggers:
        path, val, kind = triggers[0]
        failure_log.append_failure(path, kind)
        return False
    lane_assign(instance)
    scorer(instance)
    return True

def test_f08_reference():
    calls = []
    log = FailureLog()
    register_state = {'assigned_lane': None, 'entries': []}
    scores = []
    def lane(x):
        calls.append('lane')
        register_state['assigned_lane'] = 'default'
        register_state['entries'].append(id(x))
    def scorer(x):
        calls.append('scorer')
        scores.append(0.5)
    cases = {
        'cand_loss': {'candidates': [{}, {}, {'metrics': {'loss': float('inf')}}]},
        'nested_array': {'l': [1.0, [float('nan'), [2.0, [float('inf')]]]]},
        'nan': {'m': float('nan')},
        'mixed_inf': {'p': math.inf, 'n': -math.inf},
        'good': {'m': 1.5},
    }
    for name, case in cases.items():
        snap_calls = list(calls)
        snap_register = dict(register_state)
        snap_register['entries'] = list(register_state['entries'])
        snap_scores = list(scores)
        before = log.count()
        ok = validate(case, log, lane, scorer)
        assert ok == (name == 'good'), name
        if not ok:
            assert log.count() == before + 1, name
            assert calls == snap_calls, (name, calls)
            assert register_state == snap_register, (name, register_state)
            assert scores == snap_scores, (name, scores)
    assert calls == ['lane', 'scorer'], calls
    assert log.count() == 4, log.count()
    assert log.records[0] == ('root.candidates[2].metrics.loss', '+inf'), log.records[0]
    print('f08 reference implementation passed: 4 failures persisted, register/score unchanged on rejection, lane/scorer only after validation')

if __name__ == '__main__':
    test_f08_reference()
