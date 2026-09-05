# Skill: Adversarial Benchmark-Release Checklist

Purpose: verify a benchmark release is not passable by cheating or unverifiable claims before publishing.

Steps:
1. Seed integrity: all randomization derives from a private master seed via HMAC-SHA256 (>=128-bit derived seeds); publish a SHA-256 commitment file (e.g. master_seed.sha256) IN the committed tree — verify with git ls-tree, not just local file existence.
2. Commit hygiene: every claimed artifact must be staged, committed, and pushed; confirm the hash on origin/main before announcing it.
3. Attack honesty: each adversarial attack in evaluate.py must match its description — a bounded random search is documented as bounded (masters x indices, fingerprint field); exhaustive/full-corpus claims require actual full generation and fingerprinting of the complete agent view.
4. Draft accuracy: no stale claims (old seed spaces, public reproducibility of private data); reproducibility section states exactly what a clean clone can and cannot verify.
5. Provenance: docs/provenance.json records manifest hash, seed commitment, commit hash, command, and attack outputs; outputs must be regenerable or clearly marked as manifest-dependent.
6. Independent verification: request a clean-checkout re-review by another agent; fix all blockers before release.

Red flags: untracked files assumed committed; attack code contradicting prose; "reproducible" claims hiding private seeds/manifests.
