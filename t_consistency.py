from f10_consistency import TransLog, verify_consistency

log = TransLog()
heads = []
ok = True
for i in range(1, 33):
    hh = 'head' + str(i)
    heads.append(hh)
    log.append(hh)
    if i > 1:
        for m in range(1, i):
            old_root = log._root_of(heads[:m])
            pr_old, proof = log.consistency_proof(m)
            r = verify_consistency(pr_old, m, proof, log.root(), i)
            if not r or pr_old != old_root:
                ok = False
                print('FAIL', i, m)
log2 = TransLog()
for i in range(1, 9):
    log2.append('x' + str(i))
_, proof = log2.consistency_proof(4)
bad = list(proof)
bad[0] = 'ffff' if isinstance(bad[0], str) else bad[0]
if verify_consistency(log2._root_of(['x' + str(j) for j in range(1, 5)]), 4, bad, log2.root(), 8):
    ok = False
    print('TAMPER-ACCEPTED')
print('ALL-OK' if ok else 'PROBLEMS')