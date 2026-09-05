import json, random

def make_network(seed, n_genes):
    r = random.Random(seed)
    genes = ['G%d' % i for i in range(n_genes)]
    reg = {}
    for i in range(n_genes):
        for j in range(n_genes):
            if i != j and r.random() < 0.4:
                reg[(genes[j], genes[i])] = r.choice([1, -1])
    return genes, reg

def update(state, reg, r):
    new = {}
    for g in state:
        s = 0
        for (src, tgt), w in reg.items():
            if tgt == g and state[src]:
                s += w
        new[g] = (s > 0) or (s == 0 and state[g])
    return new

def simulate(reg, seed, steps, state0):
    r = random.Random(seed)
    state = dict(state0)
    hist = [dict(state)]
    for _ in range(steps):
        nxt = update(state, reg, r)
        for g in nxt:
            if r.random() < 0.05:
                nxt[g] = not nxt[g]
        state = nxt
        hist.append(dict(state))
    return hist

def make_task(seed, tier):
    r = random.Random(seed)
    n = 4 if tier == 1 else 6
    genes, reg = make_network(seed * 10 + tier, n)
    state0 = {g: r.random() < 0.5 for g in genes}
    hist = simulate(reg, seed * 100 + tier, 50, state0)
    return {'seed': seed, 'tier': tier, 'genes': genes, 'reg': {'%s->%s' % k: v for k, v in reg.items()}, 'state0': state0, 'history': hist}

def main():
    tasks = [make_task(s, t) for t in (1, 2) for s in range(50)]
    print(len(tasks), tasks[0]['genes'], len(tasks[0]['history']), tasks[0]['reg'])

if __name__ == '__main__':
    main()
