# Agent 2 Setup - OpenAI Version 🤖

## Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
pip3 install openai python-docx PyPDF2
```

Or install everything from requirements.txt:
```bash
pip3 install -r requirements.txt
```

### Step 2: Set Your OpenAI API Key

You already have an OpenAI key, so just set it:

```bash
export OPENAI_API_KEY='sk-proj-your-key-here'
```

**To make it permanent (Mac/Linux):**
```bash
echo 'export OPENAI_API_KEY="sk-proj-your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

**Windows:**
```bash
set OPENAI_API_KEY=sk-proj-your-key-here
```

### Step 3: Test Agent 2

```bash
python3 test_agent_2.py
```

---

## ✅ What Changed from Anthropic?

- ✅ Using **OpenAI GPT-4o-mini** instead of Claude
- ✅ GPT-4o-mini is **cheaper** ($0.15 per million tokens vs Claude's $3)
- ✅ Still does the same job analysis and cover letter generation
- ✅ Quality is excellent for this use case

---

## 💰 Cost Estimate

**OpenAI GPT-4o-mini costs:**
- ~$0.02-0.05 per job (much cheaper than Claude!)
- 10 jobs/day = ~$0.20-0.50/day
- 300 jobs/month = ~$6-15/month

**Way more affordable!** 🎉

---

## 🧪 Testing

Run the test:
```bash
python3 test_agent_2.py
```

**Expected output:**
```
🧪 Testing Agent 2: Resume Customizer
============================================================
✅ OpenAI API configured
📋 Test Job:
   Title: Senior Product Manager - AI/ML
   Company: TechCorp India
   
Testing AI Analysis...
   ✓ AI analysis complete
   
📊 Analysis Results:
   Required Skills: [...]
   Match Score: 75%
   
✅ Test Complete!
```

---

## 📁 File Structure

Make sure your folder looks like this:

```
JOB_TRACKER/
├── linkedin_job_tracker.py       ← Agent 1
├── agent_2_resume_customizer.py  ← Agent 2 (NEW)
├── test_agent_2.py                ← Test script (NEW)
├── resume_master.docx             ← Mock resume (NEW)
├── credentials.json               ← Google Sheets auth
├── requirements.txt               ← Updated with OpenAI
└── ...
```

---

## 🚀 Run Agent 2 on Real Jobs

Once testing works:

```bash
python3 agent_2_resume_customizer.py
```

This will:
1. Read jobs from your Google Sheet
2. Process jobs with Status = "New"
3. Create customized resumes
4. Generate cover letters
5. Update Google Sheet

---

## 🐛 Troubleshooting

### "OPENAI_API_KEY not found"
```bash
export OPENAI_API_KEY='your-key-here'
```

### "No module named 'openai'"
```bash
pip3 install openai
```

### "Invalid API key"
- Check your key at https://platform.openai.com/api-keys
- Make sure it starts with `sk-proj-` or `sk-`
- Key must have credits/billing enabled

### "Rate limit exceeded"
- OpenAI has rate limits on free tier
- Add a small delay between jobs (already built-in)
- Or upgrade to paid tier

---

## ✨ Ready!

You're all set with OpenAI! Run the test and let me know how it goes! 🚀
