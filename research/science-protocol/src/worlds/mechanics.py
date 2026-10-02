import json, math, random

def raw_dist(a,b): return math.sqrt(sum((x-y)**2 for x,y in zip(a,b)))+1e-6

def trajectory(seed,n_particles,masses,law,steps,dt):
    r=random.Random(seed)
    res=[]
    pos=[[r.uniform(0,100) for _ in range(2)] for _ in range(n_particles)]
    vel=[[r.uniform(-5,5) for _ in range(2)] for _ in range(n_particles)]
    accel=[[0.0,0.0] for _ in range(n_particles)]
    for _ in range(steps):
        res.append([p[:] for p in pos])
        for i in range(n_particles):
            f=[0.0,0.0]
            for j in range(n_particles):
                if i==j: continue
                d=raw_dist(pos[i],pos[j])
                if law=='gravity':
                    for k in (0,1): f[k]+=masses[j]*(pos[j][k]-pos[i][k])/(d**3)
                elif law=='spring':
                    for k in (0,1): f[k]+=(pos[j][k]-pos[i][k])
            accel[i]=f
        for i in range(n_particles):
            for k in (0,1):
                vel[i][k]+=dt*accel[i][k]
                pos[i][k]+=dt*vel[i][k]
    return res

def make_task(seed,tier):
    r=random.Random(seed)
    n=2 if tier==1 else 3
    law=r.choice(['gravity','spring'])
    traj=trajectory(seed*10+tier,n,[1.0]*n,law,50,0.1)
    return {'seed':seed,'tier':tier,'n':n,'law':law,'trajectory':traj}

def main():
    tasks=[make_task(s,t) for t in (1,2) for s in range(50)]
    print(json.dumps({'num_tasks':len(tasks),'sample':tasks[0]['law']}))

if __name__=='__main__':
    main()