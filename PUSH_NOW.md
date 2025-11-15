# 🚀 PUSH TO GITHUB - QUICK GUIDE

## Status: ✅ Ready to Push

Your Git repository is fully initialized with **4 commits** and **21 files**.

## Two Options to Push

### Option 1: Using the Helper Script (Easiest)

After creating your GitHub repository:

```powershell
cd "c:\Users\Adam\Desktop\Hobbies and Things\Rate_This_Card"
powershell -ExecutionPolicy Bypass -File push-to-github.ps1
```

### Option 2: Manual Commands (Best for Understanding)

**Step 1: Create repository on GitHub**
- Go to: https://github.com/new
- Name: `mtg-draft-rater`
- Do NOT initialize with README
- Click "Create repository"

**Step 2: Copy these exact commands into PowerShell**

```powershell
$git = "C:\Program Files\Git\bin\git.exe"
cd "c:\Users\Adam\Desktop\Hobbies and Things\Rate_This_Card"

# Add GitHub as remote (replace YOUR_USERNAME)
& $git remote add origin https://github.com/YOUR_USERNAME/mtg-draft-rater.git

# Rename branch to main
& $git branch -M main

# Push to GitHub
& $git push -u origin main
```

**Step 3: Enter credentials when prompted**
- Username: `adamd613`
- Password: Use a **Personal Access Token** (recommended)

## How to Get Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Check box: ✓ repo (all sub-boxes)
4. Click "Generate token" at bottom
5. Copy the token (save it somewhere!)
6. Use as password in git commands

## What Gets Pushed

```
✓ main.py (21 KB)
✓ card_rating_engine.py (17 KB)
✓ scryfall_api.py (5 KB)
✓ config.py (7 KB)
✓ test_application.py (4 KB)
✓ quickstart.py (2 KB)
✓ 8 documentation files
✓ requirements.txt
✓ .gitignore
✓ cache/TLA.json (sample data)
✓ GIT_STATUS.md
✓ GITHUB_SETUP.md
✓ push-to-github.ps1
```

## After Push

Your repo will be at:
```
https://github.com/adamd613/mtg-draft-rater
```

You can then:
- Share the link
- Add to your portfolio
- Collaborate with others
- Track issues and features

## Current Git Status

```
Commits: 4
  • 9fe3a14 - Git status documentation
  • a7ad5ea - GitHub push helper script
  • 5b134b0 - GitHub setup instructions
  • b0ebbd3 - Initial commit

Files: 21 (all committed)
User: adamd613 (adamore14@jcu.edu)
Branch: master (will become main)
Status: Clean - ready to push
```

## Troubleshooting

**Need to check status?**
```powershell
$git = "C:\Program Files\Git\bin\git.exe"
& $git status
& $git remote -v
& $git log --oneline
```

**Made a mistake?**
```powershell
$git = "C:\Program Files\Git\bin\git.exe"
& $git remote remove origin    # Remove wrong remote
& $git reset --hard HEAD~1     # Undo last commit (if needed)
```

---

**Next: Create GitHub repo and run the commands above!**
