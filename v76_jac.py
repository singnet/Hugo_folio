src = open('/PeTTa/repos/OmegaClaw-Core/memory/v43_multi.py').read().split('random.seed(99)')[0]
exec(src)
import random
random.seed(3)
k = [[random.uniform(-1,1) for _ in range(n)] for _ in range(n)]
eps=1e-6
f0,kpm0,kaw0,T0,awn0=compute_fm(k)
ms=sorted(kpm0)
# full Jacobian dkpm[m]/dK[r][c] by FD
J={m:[[0.0]*n for _ in range(n)] for m in kpm0}
for r in range(n):
    for c in range(n):
        Kp=[row[:] for row in k]; Kp[r][c]+=eps
        Km=[row[:] for row in k]; Km[r][c]-=eps
        _,kpmp,_,_,_=compute_fm(Kp)
        _,kpmm,_,_,_=compute_fm(Km)
        for m in ms:
            J[m][r][c]=(kpmp[m][0]-kpmm[m][0])/(2*eps)
# gradient of f[si][sj] wrt K using FD Jacobian
si,sj=0,0
p=patch_pms[si][sj]
E={m:(p[m][0]-kpm0[m][0])**2 for m in kpm0}
S=sum(E[m]*kaw0[m] for m in kpm0)
G=[[0.0]*n for _ in range(n)]
for m in ms:
    dE={mm:-2.0*(p[mm][0]-kpm0[mm][0]) for mm in kpm0}
    dS_m={mm: dE[mm]*kaw0[mm] for mm in kpm0}
    # add attention derivative of this m
    dS_m[m]+=E[m]*(1.0 if kpm0[m][0]>=0 else -1.0)*(DECAY**kpm0[m][1])
# simpler: total dS/dK and dT/dK
for r in range(n):
    for c in range(n):
        dS=0.0; dT=0.0
        for m in ms:
            dkpm=J[m][r][c]
            dE=-2.0*(p[m][0]-kpm0[m][0])*dkpm
            dkaw=(1.0 if kpm0[m][0]>=0 else -1.0)*(DECAY**kpm0[m][1])*dkpm
            dS+=dE*kaw0[m]+E[m]*dkaw
            dT+=dkaw
        G[r][c]=(dS*T0-S*dT)/(T0*T0)
# FD f check
r,c=2,2
Kp=[row[:] for row in k]; Kp[r][c]+=eps
Km=[row[:] for row in k]; Km[r][c]-=eps
fp,_,_,_,_=compute_fm(Kp)
fm_,_,_,_,_=compute_fm(Km)
fd=(fp[si][sj]-fm_[si][sj])/(2*eps)
print('FD df/dK=%.6f analytic(J)=%.6f'%(fd,G[r][c]))
print('max|G|=%.6f'%max(abs(G[i][j]) for i in range(n) for j in range(n)))
