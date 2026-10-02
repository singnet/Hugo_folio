import json, random

def make_web(seed, n_species):
    r = random.Random(seed)
    names = ['s%d' % i for i in range(n_species)]
    pos = {}
    signs = {}
    for i in range(n_species):
        for j in range(n_species):
            if i == j:
                pos[(i, j)] = -0.1 * r.random()
                continue
            sign = r.choice([1, -1])
            signs[(i, j)] = sign * r.uniform(0.2, 0.8)
            pos[(i, j)] = sign * r.uniform(0.02, 0.1)
    return names, pos, signs

def simulate(pos, seed, steps, dt, pops0):
    r = random.Random(seed)
    pops = list(pops0)
    hist = [list(pops)]
    for _ in range(steps):
        deriv = []
        for i in range(len(pops)):
            deriv.append(pops[i] * (0.5 - 0.05 * pops[i] + sum(pos[(i, j)] * pops[j] * pops[i] for j in range(len(pops)))))
        pops = [p + m * dt for p, m in zip(pops, deriv)]
        pops = [max(0.0, p) for p in pops]
        dist = {}
        for i in range(len(pops)):
            if r.random() < 0.1:
                pops[i] += r.uniform(0.0, 0.05)
                dist[i] = True
        hist.append(list(pops) + [1 if dist.get(i) else 0 for i in range(len(pops))])
    return hist

def make_task(seed, tier):
    r = random.Random(seed)
    n = 3 if tier == 1 else 5
    names, pos, signs = make_web(seed * 10 + tier, n)
    pops0 = [r.uniform(0.5, 2.0) for _ in range(n)]
    hist = simulate(pos, seed * 100 + tier, 50, 0.1, pops0)
    return {'seed': seed, 'tier': tier, 'species': names, 'pos': {'%d,%d' % k: v for k, v in pos.items()}, 'signs': {'%d,%d' % k: v for k, v in signs.items()}, 'pops0': pops0, 'history': hist}

def main():
    tasks = [make_task(s, t) for t in (1, 2) for s in range(50)]
    print(len(tasks), tasks[0]['species'], len(tasks[0]['history']), tasks[0]['tier'])

if __name__ == '__main__':
    main()
