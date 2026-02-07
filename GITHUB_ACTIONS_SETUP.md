# GitHub Actions Setup - Run Job Tracker in the Cloud ☁️

This guide will set up your job tracker to run automatically every day, even when your laptop is off!

## Why GitHub Actions?

- ✅ **Free** for public repositories (2,000 minutes/month)
- ✅ **Runs in the cloud** - no laptop needed
- ✅ **Automatic** - runs daily at your chosen time
- ✅ **Reliable** - never miss a day
- ✅ **Manual trigger** - can run on-demand anytime

---

## Setup Steps (15 minutes)

### Step 1: Create a GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click **"New repository"** (green button)
3. Name it: `linkedin-job-tracker` (or anything you like)
4. Choose **Public** (for free GitHub Actions)
5. **Don't** initialize with README
6. Click **"Create repository"**

### Step 2: Upload Your Code to GitHub

In your project folder (in Cursor terminal), run these commands:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Make first commit
git commit -m "Initial commit: LinkedIn job tracker"

# Connect to your GitHub repo (replace YOUR-USERNAME)
git remote add origin https://github.com/YOUR-USERNAME/linkedin-job-tracker.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note:** Replace `YOUR-USERNAME` with your actual GitHub username!

### Step 3: Add Google Credentials as a Secret

⚠️ **IMPORTANT:** Never commit `credentials.json` to GitHub! We'll use GitHub Secrets instead.

1. Open your `credentials.json` file
2. **Copy the entire contents** (all the JSON text)
3. Go to your GitHub repository page
4. Click **"Settings"** tab
5. In the left sidebar, click **"Secrets and variables"** → **"Actions"**
6. Click **"New repository secret"**
7. Name: `GOOGLE_CREDENTIALS`
8. Value: **Paste the entire contents** of your `credentials.json`
9. Click **"Add secret"**

### Step 4: Enable GitHub Actions

1. Go to your repository page
2. Click the **"Actions"** tab
3. If prompted, click **"I understand my workflows, go ahead and enable them"**
4. You should see **"Daily LinkedIn Job Tracker"** workflow

### Step 5: Test It (Manual Run)

1. In the **"Actions"** tab
2. Click on **"Daily LinkedIn Job Tracker"** in the left sidebar
3. Click **"Run workflow"** button (on the right)
4. Click the green **"Run workflow"** button
5. Wait 1-2 minutes
6. Click on the running workflow to see live logs
7. Check your Google Sheet - new jobs should appear!

---

## Customizing the Schedule

The workflow runs at **9:00 AM UTC** by default. To change this:

1. Open `.github/workflows/daily-job-tracker.yml`
2. Find the line: `- cron: '0 9 * * *'`
3. Change the time using [cron syntax](https://crontab.guru/)

**Examples:**

```yaml
# 8:00 AM UTC (1:30 PM IST)
- cron: '0 8 * * *'

# 6:00 AM UTC (11:30 AM IST)
- cron: '0 6 * * *'

# 2:00 PM UTC (7:30 PM IST)
- cron: '0 14 * * *'

# Multiple times per day (8 AM and 6 PM UTC)
- cron: '0 8,18 * * *'
```

**Timezone Reference:**
- UTC to IST: Add 5 hours 30 minutes
- UTC to PST: Subtract 8 hours
- UTC to EST: Subtract 5 hours

---

## How It Works

Every day (at your scheduled time):

1. ✅ GitHub spins up a cloud computer
2. ✅ Installs Python and dependencies
3. ✅ Creates credentials from your secret
4. ✅ Runs the job tracker script
5. ✅ Updates your Google Sheet with new jobs
6. ✅ Backs up to `linkedin_pm_jobs.json` in the repo

---

## Monitoring & Logs

### Check if it ran:
1. Go to **"Actions"** tab
2. See all past runs with status (✅ success or ❌ failed)
3. Click any run to see detailed logs

### Get notifications:
- GitHub will email you if a workflow fails
- You can enable notifications for successful runs too

---

## Manual Triggers (Run Anytime)

1. Go to **"Actions"** tab
2. Click **"Daily LinkedIn Job Tracker"**
3. Click **"Run workflow"**
4. Click green **"Run workflow"** button

Perfect for:
- Testing changes
- Running on-demand when you hear about new openings
- Multiple times per day during active job hunting

---

## Troubleshooting

### Workflow not showing up?
- Check `.github/workflows/daily-job-tracker.yml` exists
- File must be in exactly that path
- Push changes to GitHub: `git push`

### "Secret not found" error?
- Make sure secret name is exactly: `GOOGLE_CREDENTIALS`
- Re-add the secret with full JSON contents
- Include the opening `{` and closing `}`

### Permission errors on Google Sheets?
- Make sure sheet is shared with service account email
- Give it "Editor" permissions
- Check the email in your credentials.json

### Jobs not appearing?
- Check the workflow logs in Actions tab
- Look for any error messages
- Verify your Google Sheet has the correct headers

---

## Cost & Limits

- **Free tier:** 2,000 minutes/month for public repos
- **Your usage:** ~2 minutes per day = ~60 minutes/month
- **Way under limit!** You're using only 3% of free quota

---

## Privacy Note

Since the repo is **public** (for free Actions):
- ✅ Your code is visible
- ✅ Workflow runs are visible
- ❌ **Secrets are NOT visible** (credentials are safe!)
- ❌ **Job data is NOT in repo** (only in Google Sheets)

The `linkedin_pm_jobs.json` backup file **will** be in the repo, but:
- Only contains job IDs, titles, companies (public info)
- No personal data
- You can add it to `.gitignore` if you prefer

---

## Alternative: Private Repository

Want to keep everything private?

1. Make repo **Private** instead of Public
2. GitHub Free gives 2,000 minutes/month for private repos too!
3. Same setup, just change visibility setting

---

## Next Steps

Once this is running:
1. ✅ Check your Google Sheet daily for new jobs
2. ✅ Update "Status" column as you apply
3. ✅ Add notes for each application
4. ✅ Never miss a new PM job posting!

---

## Need Help?

Common issues:
- Workflow not running? Check if Actions are enabled
- No jobs appearing? Check workflow logs in Actions tab
- Google Sheets errors? Verify sharing permissions

Let me know what error you're seeing! 🚀
