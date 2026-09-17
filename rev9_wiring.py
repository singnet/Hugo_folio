# rev9: wiring probe + feedback budget
from feedback_budget import FeedbackBudget, Q_DEFAULT, Q_REDUCED
import probe_multilabel as pm


def probe_episode(policy, instances, families, oracle, task):
    q = Q_REDUCED if task == 'fm_kernel_loss' else Q_DEFAULT
    budget = FeedbackBudget(q=q)
    guesses = []
    for fam in families:
        if budget.remaining() <= 0:
            break
        query = policy.form_query(fam)
        result = budget.submit(query, oracle.eval_query(query))
        if result is None:
            break
        if not result['duplicate']:
            guesses.append(policy.extract(fam, result))
    probe_score = pm.reconstruction_score(policy.secret_target(), guesses)
    perm = pm.permutation_baseline(policy.secret_target(), instances)
    maj = pm.majority_baseline(policy.secret_target(), instances)
    passed = pm.evaluate(probe_score, [perm, maj])
    return {'probe_score': probe_score, 'permutation': perm, 'majority': maj,
            'passed': passed, 'used': budget.used}


if __name__ == '__main__':
    raise NotImplementedError  # pending sealed oracle integration
