import json, random

def make_rules(seed, n_elements):
    r = random.Random(seed)
    elements = ['E%d' % i for i in range(n_elements)]
    rules = []
    for _ in range(n_elements + 2):
        a, b = r.sample(elements, 2)
        prod = r.choice([x for x in elements if x not in (a, b)])
        rules.append({'reactants': sorted([a, b]), 'product': prod, 'rate': round(r.uniform(0.05, 0.3), 3)})
    return elements, rules

def simulate(rules, seed, steps, conc0):
    r = random.Random(seed)
    conc = dict(conc0)
    hist = [dict(conc)]
    for _ in range(steps):
        for rule in rules:
            a, b = rule['reactants']
            if r.random() < rule['rate'] * min(conc[a], conc[b]) * 0.1:
                if conc[a] > 0 and conc[b] > 0:
                    conc[a] -= 1; conc[b] -= 1; conc[rule['product']] += 1
        hist.append(dict(conc))
    return hist

def make_task(seed, tier):
    r = random.Random(seed)
    n = 4 if tier == 1 else 6
    elements, rules = make_rules(seed * 10 + tier, n)
    conc0 = {e: r.randint(2, 10) for e in elements}
    hist = simulate(rules, seed * 100 + tier, 50, conc0)
    return {'seed': seed, 'tier': tier, 'elements': elements, 'conc0': conc0, 'history': hist, 'rules': rules}

def main():
    tasks = [make_task(s, t) for t in (1, 2) for s in range(50)]
    print(len(tasks), tasks[0]['elements'], len(tasks[0]['history']), tasks[0]['rules'][0])

if __name__ == '__main__':
    main()
