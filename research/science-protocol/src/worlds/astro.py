import json, random

def make_star(seed):
    r = random.Random(seed)
    # observable light curve; hidden params: mass, mode
    mass = r.uniform(0.5, 5.0)
    mode = r.choice(['pulsator', 'spot', 'flare'])
    period = r.uniform(0.5, 20.0)
    amp = r.uniform(0.05, 0.4) if mode != 'flare' else 0.02
    return mass, mode, period, amp

def lightcurve(params, seed, n_points):
    r = random.Random(seed)
    mass, mode, period, amp = params
    pts = []
    for i in range(n_points):
        t = i * 0.1
        if mode == 'pulsator':
            flux = 1.0 + amp * math_sin(2 * 3.14159 * t / period)
        elif mode == 'spot':
            flux = 1.0 - amp * max(0, math_sin(2 * 3.14159 * t / period))
        else:
            flux = 1.0
            if r.random() < 0.05:
                flux -= r.uniform(0.1, 0.5)
        pts.append(round(flux + r.gauss(0, 0.01), 4))
    return pts

def math_sin(x):
    import math
    return math.sin(x)

def make_task(seed, tier):
    r = random.Random(seed)
    params = make_star(seed * 10 + tier)
    n = 100 if tier == 1 else 200
    lc = lightcurve(params, seed * 100 + tier, n)
    return {'seed': seed, 'tier': tier, 'params': {'mass': params[0], 'mode': params[1], 'period': params[2], 'amp': params[3]}, 'lightcurve': lc}

def main():
    tasks = [make_task(s, t) for t in (1, 2) for s in range(50)]
    print(len(tasks), tasks[0]['params']['mode'], len(tasks[0]['lightcurve']))

if __name__ == '__main__':
    main()
