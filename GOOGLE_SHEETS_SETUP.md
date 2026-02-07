# Google Sheets Setup Guide 📊

Follow these steps to connect your job tracker to Google Sheets. This will take about 10 minutes.

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Select a Project"** at the top
3. Click **"New Project"**
4. Name it something like "LinkedIn Job Tracker"
5. Click **"Create"**

## Step 2: Enable Google Sheets API

1. In the Google Cloud Console, make sure your new project is selected
2. Go to **"APIs & Services"** > **"Library"** (from the left menu)
3. Search for **"Google Sheets API"**
4. Click on it and press **"Enable"**
5. Go back and search for **"Google Drive API"**
6. Click on it and press **"Enable"**

## Step 3: Create Service Account Credentials

1. Go to **"APIs & Services"** > **"Credentials"**
2. Click **"Create Credentials"** at the top
3. Select **"Service Account"**
4. Fill in the details:
   - **Service account name**: `job-tracker-bot`
   - **Service account ID**: (auto-filled)
   - Click **"Create and Continue"**
5. For **"Grant this service account access to project"**:
   - Select role: **"Editor"**
   - Click **"Continue"**
6. Skip the optional step, click **"Done"**

## Step 4: Download Credentials JSON

1. You'll see your new service account in the list
2. Click on the **email address** of the service account (looks like `job-tracker-bot@...`)
3. Go to the **"Keys"** tab
4. Click **"Add Key"** > **"Create new key"**
5. Choose **JSON** format
6. Click **"Create"**
7. A JSON file will download automatically

## Step 5: Setup Credentials File

1. **Rename** the downloaded file to `credentials.json`
2. **Move** it to your project folder (same folder as `linkedin_job_tracker.py`)

Your folder should now look like:
```
your-project-folder/
├── linkedin_job_tracker.py
├── requirements.txt
├── credentials.json          ← New file!
└── linkedin_pm_jobs.json     ← Already exists
```

## Step 6: Share Sheet with Service Account

**IMPORTANT:** When you run the script for the first time, it will create a Google Sheet. You need to share it with your service account.

1. Open the `credentials.json` file
2. Find the line with `"client_email"` - it looks like:
   ```json
   "client_email": "job-tracker-bot@your-project.iam.gserviceaccount.com"
   ```
3. Copy that email address
4. When the script creates your sheet, go to the Google Sheet
5. Click **"Share"** button
6. Paste the service account email
7. Give it **"Editor"** permissions
8. Uncheck **"Notify people"**
9. Click **"Share"**

## Step 7: Run the Script!

```bash
python3 linkedin_job_tracker.py
```

You should see:
```
✅ Found credentials.json - will save to Google Sheets
✨ Created new Google Sheet: 'LinkedIn PM Jobs'
🔗 Access it here: https://docs.google.com/spreadsheets/d/...
```

## What You'll Get

Your Google Sheet will have these columns:

| Job ID | Title | Company | Location | Link | Found Date | Status | Notes |
|--------|-------|---------|----------|------|------------|--------|-------|
| 123456 | Senior Product Manager | Google | SF, CA | [link] | 2026-02-07 | New | |

**You can now:**
- ✅ View jobs on your phone
- ✅ Update Status column (New → Applied → Interview → Offer)
- ✅ Add notes for each job
- ✅ Share with mentors or friends
- ✅ Track your entire job search in one place

## Troubleshooting

### "credentials.json not found"
- Make sure the file is in the same folder as your script
- Check the filename is exactly `credentials.json`

### "Permission denied" error
- Make sure you shared the sheet with your service account email
- Give it "Editor" permissions

### "API not enabled" error
- Go back to Step 2 and make sure both APIs are enabled
- Wait 1-2 minutes for changes to propagate

### Can't find the service account email?
- Open `credentials.json` in a text editor
- Look for the `"client_email"` field
- Copy the entire email address

## Security Notes

⚠️ **Important:**
- **Never** share your `credentials.json` file with anyone
- **Never** commit it to GitHub or public repositories
- Add `credentials.json` to your `.gitignore` file

## Next Steps

Once this is working:
1. ✅ Set up daily automation (cron job or GitHub Actions)
2. ✅ Customize search parameters
3. ✅ Add email notifications for new jobs

Need help? Let me know what error you're seeing!
