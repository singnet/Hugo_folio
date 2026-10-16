import json, glob, re
from typecheck import tokenize, parse, typecheck_atom, typecheck, main

# Semantic validator:
# - truth values in (stv s c) must be 0.0<=s<=1.0 and 0.0<=c<=1.0
# - predicate arity: arguments of ordered relations (--) must be non-empty symbols
# - independent variables ($1, $2, ...) must appear in premise atoms only if in child
# - claim_id must be a non-empty string
# - claim must have a non-empty metta_atom

MAX_VAR = 8

def _find_stvs(N):
    if isinstance(N, list):
        req = [[]]
        if not N:
            return []
        for n in N:
            req += _find_stvs(n)
        if len(N) == 3 and N[0] == 'stv':
            req[0] = (stv)
        return req
    return []

def _find_vars(N):
    if isinstance(N, list):
        vars = [set()]
        for k, node in enumerate(N):
            if isinstance(node, str) and len(node) > 1 and node[0] == '$':
                vars[k].add(node)
            vars += _find_vars(node)
        return vars
    return []
