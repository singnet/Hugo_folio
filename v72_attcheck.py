src = open('/PeTTa/repos/OmegaClaw-Core/memory/v43_multi.py').read().split('random.seed(99)')[0]
exec(src)
import random
random.seed(3)
k = [[random.uniform(-1,1) for _ in range(n)] for _ in range(n)]
eps=1e-6
r,c=2,2
def Kpert(dv):
    K=[row[:] for row in k]; K[r][c]+=dv; return K
f0,kpm0,kaw0,T0,awn0=compute_fm(k)
fp,kpmp,kawp,Tp,awnp=compute_fm(Kpert(+eps))
fm,kpmm,kawm,Tm,awnm=compute_fm(Kpert(-eps))
# 1) verify dkaw/dkpm via FD
for m in sorted(kpm0)[:8]:
    fd_kaw=(kawp[m]-kawm[m])/(2*eps)
    fd_kpm=(kpmp[m][0]-kpmm[m][0])/(2*eps)
    if abs(fd_kpm)>1e-12:
        pred=(1.0 if kpm0[m][0]>=0 else -1.0)*(DECAY**kpm0[m][1])
        print('dkaw',m,'fd=%.6f pred=%.6f'%(fd_kaw/fd_kpm*fd_kpm, pred), 'chainfd=%.6f'%(fd_kaw/fd_kpm))
# 2) verify awn/T derivative: FD d(awn[m]/T) per m vs pred using observed dkpm_fd
for m in sorted(kpm0)[:8]:
    fd_awn=(awnp[m]-awnm[m])/(2*eps)
    fd_T=(Tp-Tm)/(2*eps)
    ik,jk=kidx(m)
    h=H[r*n+c][ik*n+jk]
    fd_kpm=(kpmp[m][0]-kpmm[m][0])/(2*eps)
    pred_dkpm=(1.0 if True else 1)*fd_kpm  # observed
    pred_dawn=(1.0 if kpm0[m][0]>=0 else -1.0)*(DECAY**kpm0[m][1])*fd_kpm if abs(fd_kpm)>1e-12 else 0.0
    print('awn',m,'fd_dawn=%.6f pred=%.6f fd_dT=%.6f sum_dawn=%.6f'%(fd_awn,pred_dawn,fd_T,0.0))
# 3) FD df/dK and analytic with FD-verified dkaw chain per m
si,sj=0,0
fd_f=(fp[si][sj]-fm[si][sj])/(2*eps)
p=patch_pms[si][sj]
E={m:(p[m][0]-kpm0[m][0])**2 for m in kpm0}
S=sum(E[m]*kaw0[m] for m in kpm0)
tot=0.0
for m in kpm0:
    fd_kpm=(kpmp[m][0]-kpmm[m][0])/(2*eps)
    if abs(fd_kpm)<1e-12: continue
    dE=-2.0*(p[m][0]-kpm0[m][0])*fd_kpm
    fd_dkaw_per_kpm=(kawp[m]-kawm[m])/(2*eps)/fd_kpm
    dS=dE*kaw0[m]+E[m]*fd_dkaw_per_kpm*fd_kpm
    dT=fd_dkaw_per_kpm*fd_kpm
    g=(dS*T0-S*dT)/(T0*T0)
    tot+=g
print('FD df/dK=%.6f analytic(FDchain)=%.6f'%(fd_f,tot))
