# GIT CONFIGURATION FIX

You need to tell Git your name and email. Run these commands:

## Set Your Git Identity

**Replace with YOUR actual information:**

```bash
git config --global user.email "tstr.site@gmail.com"
```

```bash
git config --global user.name "Alber"
```

These commands tell Git who is making the commits.

## Then Retry the Commit

```bash
git commit -m "Initial commit - TSTR.site MVP"
```

## Then Continue with Remaining Commands

```bash
git branch -M main
```

```bash
git remote add origin https://github.com/JAvZZe/tstr-site.git
```

```bash
git push -u origin main
```

When asked for password, use your GitHub Personal Access Token.
