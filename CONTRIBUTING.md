# Contributing

## Branching strategy

`main` must always be deployable. Never commit directly to `main`.

```
main
 └── feature/<short-description>   ← your work goes here
```

1. Branch off `main`: `git checkout -b feature/<short-description>`
2. Make small, focused commits.
3. Open a PR against `main` when the feature is complete.
4. Delete the branch after it is merged.

## Commit messages

Use the imperative mood, present tense, under 72 characters:

```
feat: add Key Vault secret caching with lru_cache
fix: correct gunicorn entry point to wsgi:app
```

## Running tests locally

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest tests/
```

## Pull request checklist

- [ ] Tests pass (`pytest tests/`)
- [ ] No secrets committed (no `.env`, no hardcoded credentials)
- [ ] Branch is up to date with `main`
- [ ] PR description explains *why*, not just *what*
