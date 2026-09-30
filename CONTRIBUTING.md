# Contributing

Start with the [repository map](docs/repository-map.md) and [reproduction guide](docs/reproduction.md).

## Report a problem

Open an [issue](https://github.com/Moemu/OtakuLab/issues). Include:

- Git revision and local changes.
- Notebook, cell heading, and minimal reproduction steps.
- Relevant Python, package, operating-system, CUDA, and GPU versions.
- Dataset version, sample count, model revision, and checkpoint location.
- Expected behavior and error message or traceback.

Remove keys and private data from logs. For score differences, include the formula, threshold, test-set hash, and labels.

## Change experiments

Keep changes focused. Preserve supplied data and results when exploring variants. Write new outputs separately and record inputs.

Update producers, consumers, and documents when changing paths or schemas. Distinguish historical experiments from validated reproduction routes.

Check notebook outputs for credentials and unrelated logs. Retain outputs that explain the experiment. Avoid committing weights without a release plan.

Report checks actually performed. Documentation needs link checks; metric changes need known-score examples and regenerated affected results.

## Contribution terms

Repository licensing and data redistribution terms remain unresolved. Confirm intended terms with the maintainer before contributing third-party data or weights.
