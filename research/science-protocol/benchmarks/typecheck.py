import json, glob, sys, re

def tokenize(s):
    return s.replace('(', ' ( ').replace(')', ' ) ').split()

def parse(s):
    toks = tokenize(s)
    def rec(i):
        if i >= len(toks): raise ValueError('eof')
        if toks[i] == '(':
            out = []
            i += 1
            while toks[i] != ')':
                v, i = rec(i)
                out.append(v)
            return out, i + 1
        return toks[i], i + 1
    v, i = rec(0)
    if i != len(toks): raise ValueError('trailing')
    return v

SIGS = {
    '-->': (2, ('entity', 'entity')),
    '==>': (2, ('event', 'event')),
}

NAME_RE = re.compile(r'^[a-z][A-Za-z0-9_-]*$')

def typecheck_atom(term, rule=False):
    err = []
    if not (isinstance(term, list) and term):
        return ['unexpected term ' + str(term)]
    pred = term[0]
    args = term[1:]
    if pred == 'and':
        if not args:
            return ['and needs conjuncts']
        for a in args:
            if isinstance(a, list):
                err.extend(typecheck_atom(a, rule))
            elif isinstance(a, str) and NAME_RE.match(a):
                pass
            else:
                err.append('incompatible conjunct ' + str(a))
        return err
    if not (isinstance(pred, str) and pred in SIGS):
        return ['unknown predicate ' + str(pred)]
    arity, _ = SIGS[pred]
    is_rule = (pred == '==>')
    if pred == '-->':
        if len(args) not in (1, 2):
            err.append('wrong arity: --> expects 1 or 2, got %d' % len(args))
            return err
    elif len(args) != arity:
        err.append('wrong arity: %s expects %d, got %d' % (pred, arity, len(args)))
        return err
    for a in args:
        if isinstance(a, list):
            err.extend(typecheck_atom(a, rule or is_rule))
        elif isinstance(a, str) and a.startswith('$'):
            if not (rule or is_rule):
                err.append('unbound variable ' + a)
        elif not (isinstance(a, str) and NAME_RE.match(a)):
            err.append('incompatible type for ' + str(a))
    return err

def typecheck(atom):
    try:
        v = parse(atom)
    except Exception:
        return ['unparseable']
    # canonical (|- (term (stv s c)))
    if (isinstance(v, list) and len(v) == 2 and v[0] == '|-'
            and isinstance(v[1], list) and len(v[1]) == 2
            and isinstance(v[1][0], list) and isinstance(v[1][1], list)
            and v[1][1][0] == 'stv'):
        term, stv = v[1][0], v[1][1]
        if len(stv) != 3: return ['bad stv']
        return typecheck_atom(term)
    # (|- (term)) with no stv wrapper
    if isinstance(v, list) and len(v) == 2 and v[0] == '|-' and isinstance(v[1], list):
        return typecheck_atom(v[1])
    # multi-premise (|- p1 p2 ... conclusion (stv s c))
    if isinstance(v, list) and len(v) >= 3 and v[0] == '|-':
        errs = []
        for p in v[1:]:
            if isinstance(p, list) and len(p) == 3 and p[0] == 'stv':
                continue  # trailing truth value
            if isinstance(p, list) and len(p) == 2 and isinstance(p[0], list) and isinstance(p[1], list) and p[1][0] == 'stv':
                if len(p[1]) != 3: errs.append('bad stv')
                errs.extend(typecheck_atom(p[0]))
            elif isinstance(p, list):
                if len(p) == 1 and isinstance(p[0], list):
                    errs.extend(typecheck_atom(p[0]))
                else:
                    errs.extend(typecheck_atom(p))
            else:
                errs.append('incompatible premise ' + str(p))
        return errs
    # bare atom form (term) with no |-/stv wrapper
    if isinstance(v, list) and len(v) >= 2:
        return typecheck_atom(v)
    return ['unexpected structure']

CANARIES = [
    ('positive-valid', '(|- ((--> sam garfield) (stv 1.0 0.9)))', []),
    ('positive-nested-rule', '(|- ((==> (--> $1 hydrogen-fusing) (--> $1 bright)) (stv 1.0 0.9)))', []),
    ('positive-unary-and', '(|- ((--> isomerism (and same-formula different-structure)) (stv 1.0 0.9)))', []),
    ('negative-unbound-var', '(|- ((--> sam $x) (stv 1.0 0.9)))', ['unbound variable']),
    ('negative-unbound-nested', '(|- ((and (--> sam $x)) (stv 1.0 0.9)))', ['unbound variable']),
    ('negative-wrong-arity', '(|- ((--> sam garfield kitty) (stv 1.0 0.9)))', ['wrong arity']),
    ('negative-incompatible-type', '(|- ((--> Sam garfield) (stv 1.0 0.9)))', ['incompatible type']),
]

def main():
    ok = True
    for name, atom, expect in CANARIES:
        errs = typecheck(atom)
        if expect:
            good = errs and all(any(e.startswith(x) for e in errs) for x in expect)
        else:
            good = not errs
        print(name, 'PASS' if good else 'FAIL', errs)
        if not good: ok = False
    fails = 0
    for f in sorted(glob.glob('fixtures/sample_*.jsonl')):
        data = json.load(open(f))
        for c in data['claims']:
            atom = c.get('metta_atom')
            if atom:
                errs = typecheck(atom)
                if errs:
                    fails += 1
                    print(f, c['claim_id'], errs)
    print('corpus failures:', fails)
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
