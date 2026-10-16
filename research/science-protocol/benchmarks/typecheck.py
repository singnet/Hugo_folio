import json, glob, sys, re

def tokenize(s):
    return s.replace('(', ' ( ').replace(')', ' ) ').split()

def parse(s):
    # returns nested list
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

def typecheck(atom):
    try:
        v = parse(atom)
    except Exception:
        return ['unparseable']
    # expect (|- ((PRED args...) (stv s c)))
    if not (isinstance(v, list) and len(v) == 2 and v[0] == '|-'
            and isinstance(v[1], list) and len(v[1]) == 2
            and isinstance(v[1][0], list) and isinstance(v[1][1], list)
            and v[1][1][0] == 'stv'):
        return ['unexpected structure']
    term, stv = v[1][0], v[1][1]
    if len(stv) != 3: return ['bad stv']
    if not term or not isinstance(term[0], str):
        return ['unexpected structure']
    pred = term[0]
    args = term[1:]
    if pred not in SIGS:
        return ['unknown predicate ' + pred]
    arity, types = SIGS[pred]
    err = []
    if len(args) != arity:
        err.append('wrong arity: %s expects %d, got %d' % (pred, arity, len(args)))
    rule = pred == '==>'
    for a in args:
        if isinstance(a, str) and a.startswith('$') and not rule:
            err.append('unbound variable ' + a)
        elif not (isinstance(a, str) and re.match(r'^[a-z][A-Za-z0-9_-]*$', a)):
            err.append('incompatible type for ' + str(a))
    return err

CANARIES = [
    ('positive-valid', '(|- ((--> sam garfield) (stv 1.0 0.9)))', []),
    ('negative-unbound-var', '(|- ((--> sam $x) (stv 1.0 0.9)))', ['unbound variable ']),
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
    for f in sorted(glob.glob('fixtures/sample_*.jsonl')):
        data = json.load(open(f))
        for c in data['claims']:
            atom = c.get('metta_atom')
            if atom:
                errs = typecheck(atom)
                if errs:
                    print(f, c['claim_id'], errs)
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
