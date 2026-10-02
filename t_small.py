from f10_consistency import TransLog, verify_consistency
log = TransLog()
for i in range(1, 5):
    log.append('x' + str(i))
old, proof = log.consistency_proof(3)
print('proof', proof)
print('old', old, 'expected', log._root_of(['x1', 'x2', 'x3']))
print('new', log.root())
print('verify', verify_consistency(old, 3, proof, log.root(), 4))