src = open('/PeTTa/repos/OmegaClaw-Core/memory/v43_multi.py').read().split('random.seed(99)')[0]
exec(src)
import random
random.seed(3)
k = [[random.uniform(-1,1) for _ in range(n)] for _ in range(n)]
exec(open('/PeTTa/repos/OmegaClaw-Core/memory/v79_parts.py').read())
err=lambda F: sum(sum(abs(F[i][j]-list(patch_pms[i][j].values())[0][0])**2 for j in range(n)) for i in range(n))
lr=0.05
best=err(compute_fm(k)[0])
for it in range(60):
    f,G=grad(k)
    gmax=max(abs(G[i][j]) for i in range(n) for j in range(n))
    if gmax==0: break
    k=[[k[i][j]+lr*G[i][j]/gmax for j in range(n)] for i in range(n)]
    e=err(compute_fm(k)[0])
    if e<best: best=e
    else: lr*=0.5; k=[[k[i][j]-lr*G[i][j]/gmax for j in range(n)] for i in range(n)]
    if it%10==0: print(it, round(e,4), flush=True)
print('final best=%.4f'%best)
