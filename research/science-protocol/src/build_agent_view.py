import json, glob, hashlib, os, random, sys
HIDDEN = {
 'mechanics': ['law'],
 'chem': ['rules'],
 'eco': ['pos','signs'],
 'gene': ['reg'],
 'astro': ['params'],
 'geo': ['layers'],
}
def make_prefix(world, t):
    # returns (agent task with strict prefix, target for manifest)
    agent = {k:v for k,v in t.items() if k not in HIDDEN.get(world,[]) and k != 'seed' and 'seed' not in k.lower()}
    tgt = {}
    if world == 'mechanics':
        agent['trajectory'] = t['trajectory'][:-1]
        tgt['predict_at'] = len(t['trajectory'])-1
        tgt['target'] = t['trajectory'][-1]
    elif world == 'eco':
        agent['history'] = t['history'][:-1]
        tgt['predict_at'] = len(t['history'])-1
        tgt['target'] = t['history'][-1]
    elif world == 'chem':
        agent['history'] = t['history'][:40]
        tgt['predict_at'] = len(t['history'])-1
        tgt['target'] = t['history'][-1]
    elif world == 'gene':
        agent['history'] = t['history'][:-1]
        tgt['predict_at'] = len(t['history'])-1
        tgt['target'] = t['history'][-1]
    elif world == 'astro':
        tgt['target'] = t['params']['mode']
    elif world == 'geo':
        tgt['target'] = None  # derived from hidden layers server-side
    return agent, tgt
data_dir = sys.argv[1] if len(sys.argv)>1 else 'data'
out_dir = os.path.join(os.path.dirname(data_dir), 'agent_view')
os.makedirs(out_dir, exist_ok=True)
tasks = []
for f in sorted(glob.glob(os.path.join(data_dir, '*.json'))):
    try: d = json.load(open(f))
    except Exception: continue
    world = os.path.basename(f).replace('.json','').replace('_tasks','')
    items = d if isinstance(d, list) else d.get('tasks', [])
    for i, t in enumerate(items):
        if not isinstance(t, dict): continue
        tid = hashlib.sha256((world+str(i)+os.path.basename(f)).encode()).hexdigest()[:16]
        agent, tgt = make_prefix(world, t)
        labels = {k:v for k,v in t.items() if k in HIDDEN.get(world,[])}
        labels['seed'] = t.get('seed')
        if tgt['target'] is not None: labels['target'] = tgt['target']
        tasks.append({'id': tid, 'world': world, 'agent': agent, 'labels': labels,
                      'predict_at': tgt.get('predict_at'), 'src': os.path.basename(f)})
rng = random.Random(42); rng.shuffle(tasks)
n = len(tasks)
train, dev, test = tasks[:int(.7*n)], tasks[int(.7*n):int(.85*n)], tasks[int(.85*n):]
splits = {'train':train,'dev':dev,'test':test}
for name, split in splits.items():
    with open(os.path.join(out_dir, name+'.jsonl'),'w') as fh:
        for t in split:
            fh.write(json.dumps({'id': t['id'], 'world': t['world'],
                'predict_at': t['predict_at'], **t['agent']})+'\n')
manifest = []
for name, split in splits.items():
    for t in split:
        rec = {'id': t['id'], 'world': t['world'], 'split': name,
               'generator': t['src'], 'labels': t['labels']}
        blob = json.dumps(rec, sort_keys=True)
        rec['integrity'] = hashlib.sha256(blob.encode()).hexdigest()
        manifest.append(rec)
mp = os.path.join(os.path.dirname(out_dir), 'labels_manifest.json')
json.dump(manifest, open(mp,'w'), indent=1)
print('tasks:', n, 'train/dev/test:', len(train), len(dev), len(test), 'manifest:', mp)
