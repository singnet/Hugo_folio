import json, math

def predictive_match(preds, actuals):
    return sum((p - a) ** 2 for p, a in zip(preds, actuals)) / max(len(actuals), 1)

def calibration_score(post, true_idx):
    # post: posterior probs over candidate laws; true_idx: index of ground-truth law (None if unknown)
    if true_idx is None or not (0 <= true_idx < len(post)):
        return 0.0
    return post[true_idx]

def score_agent(preds, actuals, post, true_idx, fp_penalty=0.5):
    m = predictive_match(preds, actuals)
    c = calibration_score(post, true_idx)
    spurious = sum(1 for p in post if p > 0.3) - (1 if true_idx is not None and post[true_idx] > 0.3 else 0)
    return {'mse': m, 'calibration': c, 'spurious_count': spurious, 'score': c - fp_penalty * spurious}
