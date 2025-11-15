# GitHub Setup Instructions

Your Git repository is initialized and ready to push to GitHub!

## Current Status ✅

- ✅ Git repository initialized locally
- ✅ All 18 files committed
- ✅ Initial commit created: `b0ebbd3`
- ✅ User configured: adamd613 (adamore14@jcu.edu)

## Next Steps to Push to GitHub

### Step 1: Create a New Repository on GitHub

1. Go to https://github.com/new
2. Create a new repository with these settings:
   - **Repository name**: `mtg-draft-rater` (or your preferred name)
   - **Description**: "AI-powered MTG draft deck analysis and recommendations"
   - **Visibility**: Public (recommended for portfolio) or Private
   - **Do NOT initialize with README** (we already have one)
   - Click "Create repository"

### Step 2: Add Remote and Push

After creating the repo on GitHub, run these commands in PowerShell:

```powershell
# Navigate to your project
cd "C:\Users\Adam\Desktop\Hobbies and Things\Rate_This_Card"

# Add the remote repository (replace USERNAME and REPO_NAME)
& "C:\Program Files\Git\bin\git.exe" remote add origin https://github.com/USERNAME/REPO_NAME.git

# Rename branch to main if needed
& "C:\Program Files\Git\bin\git.exe" branch -M main

# Push to GitHub (you'll be prompted for credentials)
& "C:\Program Files\Git\bin\git.exe" push -u origin main
```

### Step 3: GitHub Authentication

When pushing, GitHub will ask for authentication:

**Option A: Personal Access Token (Recommended)**
1. Go to https://github.com/settings/tokens/new
2. Create a token with `repo` scope
3. Use token as password when prompted

**Option B: GitHub CLI**
1. Install GitHub CLI from https://cli.github.com/
2. Run: `gh auth login`
3. Follow prompts to authenticate

**Option C: SSH Key**
1. Set up SSH keys if not already done
2. Use SSH URL instead: `git@github.com:USERNAME/REPO_NAME.git`

## Quick Reference

Your git config:
- User: adamd613
- Email: adamore14@jcu.edu
- Local repo: C:\Users\Adam\Desktop\Hobbies and Things\Rate_This_Card
- Branch: master → main (will be renamed when you push)

## After Pushing

Once pushed to GitHub, you can:
- Share the repository link
- Add it to your portfolio
- Collaborate with others
- Track issues and features
- Get feedback from community

## Troubleshooting

**"Remote already exists"**
- Remove it first: `git remote remove origin`
- Then add the correct one

**"Permission denied"**
- Check your GitHub credentials
- Try personal access token instead of password

**"Repository already has commits"**
- That's fine, push with: `git push -u origin main`

---

Let me know once you've created the GitHub repo and I can help complete the push!
