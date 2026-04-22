# 🎯 TA Automation — LinkedIn Talent Acquisition Pipeline

A Streamlit app that automates end-to-end recruitment:
**Requirements → LinkedIn Search → AI Scoring → Outreach → Dashboard**

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
cd ta_automation
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run app.py
```

### 3. Open in browser
Visit `http://localhost:8501`

---

## 📁 Project Structure

```
ta_automation/
├── app.py                  # Main entry point + home page
├── requirements.txt        # Python dependencies
├── pages/
│   ├── 1_requirements.py   # Add/manage job specs
│   ├── 2_candidates.py     # Fetch + AI score candidates
│   ├── 3_outreach.py       # Generate messages + track replies
│   └── 4_dashboard.py      # Analytics + pipeline overview
├── utils/
│   ├── mock_data.py        # Mock LinkedIn candidate generator
│   ├── storage.py          # CSV read/write helpers
│   └── ai_scorer.py        # Claude API scoring (mock + real)
└── data/                   # Auto-created — stores your CSVs
    ├── candidates.csv
    ├── requirements.csv
    └── outreach.csv
```

---

## 🔌 Enabling Real Integrations

### Real AI Scoring (Claude API)
1. Get your API key from https://console.anthropic.com
2. Create a `.env` file:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```
3. In `utils/ai_scorer.py`, set:
   ```python
   USE_REAL_API = True
   ```

### Real LinkedIn Scraping (Apify)
1. Sign up at https://apify.com
2. Use the **LinkedIn Profile Scraper** actor
3. Replace `generate_candidates()` in `utils/mock_data.py`:
   ```python
   from apify_client import ApifyClient
   client = ApifyClient("YOUR_TOKEN")
   run = client.actor("curious_coder/linkedin-profile-scraper").call(
       run_input={"searchUrl": f"https://linkedin.com/search/results/people/?keywords={job_title}"}
   )
   ```

### Outreach Automation (Dripify)
- Sign up at https://dripify.io
- Use their REST API to trigger sequences
- Replace the "Mark as Sent" button logic in `pages/3_outreach.py`

---

## ⚠️ LinkedIn Fair Use Note
- Stay under 50–80 connection requests/day
- Use cloud-based tools (not browser plugins)
- Always personalize messages
- LinkedIn Recruiter API is the safest official option for scale
