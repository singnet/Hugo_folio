import json, os

def load(outdir):
    data = {}
    for f in os.listdir(outdir):
        if f.endswith('.json'):
            with open(os.path.join(outdir, f)) as fh:
                data[f[:-5]] = json.load(fh)
    return data

def score_task(task, pred):
    return float(pred)

def main(outdir):
    data = load(outdir)
    for w, tasks in data.items():
        print(w, len(tasks), 'sample keys:', sorted(tasks[0].keys())[:6])

if __name__ == '__main__':
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else '../data')
