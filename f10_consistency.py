from f10_reference import PROTO, h


class TransLog:
    def __init__(self):
        self.leaves = []
    def append(self, head):
        self.leaves.append(head)
        return len(self.leaves)
    def _leaf(self, head):
        return h((PROTO + '/leaf').encode() + b'|' + head.encode())
    def _node(self, l, r):
        return h((PROTO + '/node').encode() + b'|' + l.encode() + b'|' + r.encode())
    def root(self):
        return self._root_of(self.leaves)
    def _root_of(self, heads):
        if not heads:
            return h((PROTO + '/empty').encode())
        level = [self._leaf(x) for x in heads]
        while len(level) > 1:
            level = [self._node(level[i], level[i+1]) for i in range(0, len(level) - 1, 2)] + ([level[-1]] if len(level) % 2 else [])
        return level[0]
    def consistency_proof(self, m):
        n = len(self.leaves)
        assert 0 < m <= n, 'm out of range'
        if m == n:
            return self._root_of(self.leaves), []
        return self._root_of(self.leaves[:m]), self._cproof(m, 0, n)
    def _cproof(self, m, lo, hi):
        n = hi - lo
        if m == n:
            return [self._root_of(self.leaves[lo:hi])]
        k = 1 << ((n - 1).bit_length() - 1)
        if m <= k:
            return self._cproof(m, lo, lo + k) + [self._root_of(self.leaves[lo + k:hi])]
        return self._cproof(m - k, lo + k, hi) + [self._root_of(self.leaves[lo:lo + k])]


def _node(l, r):
    return h((PROTO + '/node').encode() + b'|' + l.encode() + b'|' + r.encode())


def verify_consistency(old_root, m, proof, new_root, n):
    if m == n:
        return old_root == new_root and not list(proof)
    if not (0 < m < n):
        return False
    p = list(proof)

    def fold(m, n):
        if m == n:
            r = p.pop(0)
            return r, r
        k = 1 << ((n - 1).bit_length() - 1)
        if m <= k:
            rm, rk = fold(m, k)
            right = p.pop(0)
            return rm, _node(rk, right)
        rm2, rn = fold(m - k, n - k)
        left = p.pop(0)
        return _node(left, rm2), _node(left, rn)

    if len(p) == 0:
        return False
    try:
        rm, rn = fold(m, n)
    except IndexError:
        return False
    return rm == old_root and rn == new_root and not p