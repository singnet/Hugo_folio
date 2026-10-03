src = open('/PeTTa/repos/OmegaClaw-Core/memory/v43_multi.py').read().split('random.seed(99)')[0]
exec(src)
import random
random.seed(3)
k = [[random.uniform(-1,1) for _ in range(n)] for _ in range(n)]
def depthB(m):
    seq=[s for s in m.split('_') if s]
    d=0
    for s in seq[:-1]:
        if s in ('LL','LH','HL','HH'): d+=1
    return d
eps=1e-6
r,c=2,2
def Kpert(dv):
    K=[row[:] for row in k]; K[r][c]+=dv; return K
f0,kpm0,kaw0,T0,awn0=compute_fm(k)
fp,kpmp,kawp,Tp,awnp=compute_fm(Kpert(+eps))
fm,kpmm,kawm,Tm,awnm=compute_fm(Kpert(-eps))
for m in sorted(kpm0):
    ik,jk=kidx(m)
    h=H[r*n+c][ik*n+jk]
    if h==0: continue
    fdv=(kpmp[m][0]-kpmm[m][0])/(2*eps)
    print('dkpm',m,'fd=%.6f pred=%.6f'%(fdv,(0.5**depthB(m))*h))
si,sj=0,0
fd_f=(fp[si][sj]-fm[si][sj])/(2*eps)
p=patch_pms[si][sj]
E={m:(p[m][0]-kpm0[m][0])**2 for m in kpm0}
S=sum(E[m]*kaw0[m] for m in kpm0)
tot=0.0
for m in kpm0:
    dE=-2.0*(p[m][0]-kpm0[m][0])
    dkaw=(1.0 if kpm0[m][0]>=0 else -1.0)*(DECAY**kpm0[m][1])
    dS=dE*kaw0[m]+E[m]*dkaw
    dT=dkaw
    g=(dS*T0-S*dT)/(T0*T0)
    ik,jk=kidx(m)
    tot+=g*(0.5**depthB(m))*H[r*n+c][ik*n+jk]
print('FD df/dK=%.6f analytic=%.6f'%(fd_f,tot))
