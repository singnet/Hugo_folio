from f10_consistency import TransLog, verify_consistency


def test_all_pairs():
    log = TransLog()
    heads = []
    for i in range(1, 33):
        hh = 'head' + str(i)
        heads.append(hh)
        log.append(hh)
        if i > 1:
            for m in range(1, i):
                old, proof = log.consistency_proof(m)
                assert old == log._root_of(heads[:m])
                assert verify_consistency(old, m, proof, log.root(), i)


def test_tamper_rejected():
    log = TransLog()
    for i in range(1, 9):
        log.append('x' + str(i))
    old, proof = log.consistency_proof(4)
    bad = list(proof)
    bad[0] = 'ffff'
    assert not verify_consistency(old, 4, bad, log.root(), 8)