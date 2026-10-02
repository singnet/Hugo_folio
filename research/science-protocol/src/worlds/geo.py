import json, random

def make_terrain(seed, n_layers):
    r = random.Random(seed)
    layers = []
    for i in range(n_layers):
        layers.append({
            'density': round(r.uniform(1.5, 4.0), 2),
            'wave_speed': round(r.uniform(1.0, 8.0), 2),
            'thickness': round(r.uniform(0.5, 5.0), 2)
        })
    return layers

def seismogram(layers, seed, n_sensors):
    # synthetic travel times: observable; layer params hidden
    r = random.Random(seed)
    total = 0.0
    times = []
    for L in layers:
        total += L['thickness'] / L['wave_speed']
        times.append(total)
    readings = []
    for s in range(n_sensors):
        row = [round(t + r.gauss(0, 0.05), 3) for t in times]
        readings.append(row)
    return readings

def make_task(seed, tier):
    r = random.Random(seed)
    n = 3 if tier == 1 else 5
    layers = make_terrain(seed * 10 + tier, n)
    sensors = 4 if tier == 1 else 8
    readings = seismogram(layers, seed * 100 + tier, sensors)
    return {'seed': seed, 'tier': tier, 'layers': layers, 'readings': readings}

def main():
    tasks = [make_task(s, t) for t in (1, 2) for s in range(50)]
    print(len(tasks), len(tasks[0]['layers']), len(tasks[0]['readings']), len(tasks[0]['readings'][0]))

if __name__ == '__main__':
    main()
