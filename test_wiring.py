import probe_multilabel as pm
from rev9_wiring import probe_episode

class Policy:
    def form_query(self, fam): return 1.0
    def extract(self, fam, res): return [1]
    def secret_target(self): return [1]

class Oracle:
    def eval_query(self, q): return 1.0

pm.reconstruction_score = lambda sec, g: 0.5
pm.permutation_baseline = lambda sec, i: 0.4
pm.majority_baseline = lambda sec, i: 0.5

res = probe_episode(Policy(), [[0, 1]], ['a', 'b', 'c'], Oracle(), 'generic')
print(res)
assert res[passed] in (True, False)
assert res[used] == 3
print('WIRING_OK')