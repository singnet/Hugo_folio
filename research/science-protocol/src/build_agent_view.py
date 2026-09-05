import json, glob, hashlib, os, random, sys
HIDDEN = {
 'mechanics': ['law'],
 'chem': ['rules'],
 'eco': ['pos','signs'],
 'gene': ['reg'],
 'astro': ['params'],
 'geo': ['layers'],
}
data_dir = sys.argv[1] if len(sys.argv)>1 else 'data'
out_dir = os.path.join(os.path.dirname(data_dir), 'agent_view')
os.makedirs(out_dir, exist_ok=True)
tasks = []
for f in sorted(glob.glob(os.path.join(data_dir, '*.json'))):
    try:
        d = json.load(open(f))
    except Exception:
        continue
    world = os.path.basename(f).replace('.json','').replace('_tasks','')
    items = d if isinstance(d, list) else d.get('tasks', [])
    for i, t in enumerate(items):
        if not isinstance(t, dict): continue
        tid = hashlib.sha256((world+str(i)+f).encode()).hexdigest()[:16]
        agent = {k:v for k,v in t.items() if k not in HIDDEN.get(world,[]) and k != 'seed' and 'seed' not in k.lower()}
        labels = {k:v for k,v in t.items() if k in HIDDEN.get(world,[])}
        tasks.append({'id': tid, 'world': world, 'agent': agent, 'labels': labels, 'src': os.path.basename(f)})
rng = random.Random(42); rng.shuffle(tasks)
n = len(tasks)
train, dev, test = tasks[:int(.7*n)], tasks[int(.7*n):int(.85*n)], tasks[int(.85*n):]
for name, split in [('train',train),('dev',dev),('test',test)]:
    with open(os.path.join(out_dir, name+'.jsonl'),'w') as fh:
        for t in split:
            fh.write(json.dumps({'id': t['id'], 'world': t['world'], **t['agent']})+'\n')
manifest = []
for t in tasks:
    rec = {'id': t['id'], 'world': t['world'], 'split': 'train' if t in train else ('dev' if t in dev else 'test'),
           'generator': t['src'], 'targets': t['labels']}
    blob = json.dumps(rec, sort_keys=True)
    rec['integrity'] = hashlib.sha256(blob.encode()).hexdigest()
    manifest.append(rec)
mp = os.path.join(os.path.dirname(out_dir), 'labels_manifest.json')
json.dump(manifest, open(mp,'w'), indent=1)
print('tasks:', n, 'train/dev/test:', len(train), len(dev), len(test), 'manifest:', mp)
