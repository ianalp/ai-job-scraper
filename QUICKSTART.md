# 🚀 Quick Start Guide

## For Absolute Beginners

### 1️⃣ Prerequisites

**Install Python** (if you don't have it):
- Windows: Download from [python.org](https://www.python.org/downloads/)
- Mac: `brew install python3` or download from python.org
- Linux: `sudo apt-get install python3 python3-pip`

**Install Git** (optional, for cloning):
- Download from [git-scm.com](https://git-scm.com/)

---

### 2️⃣ Get the Project

**Option A: Download ZIP**
1. Click the green "Code" button on GitHub
2. Select "Download ZIP"
3. Extract to a folder

**Option B: Git Clone**
```bash
git clone https://github.com/yourusername/ai-job-scraper.git
cd ai-job-scraper
```

---

### 3️⃣ Automated Setup

**Windows:**
- Double-click `setup.bat`
- Wait for installation to complete

**Mac/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

---

### 4️⃣ Configure Email (Optional)

1. Open `.env` file in any text editor
2. Add your email credentials:
   ```
   SENDER_EMAIL=your-email@gmail.com
   SENDER_PASSWORD=your-app-password
   RECEIVER_EMAIL=where-to-send-alerts@email.com
   ```

**For Gmail:**
- Enable 2-factor authentication
- Generate App Password: [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
- Use the 16-digit app password (not your regular password)

---

### 5️⃣ Run the Scraper

**Windows:**
```cmd
venv\Scripts\activate
python scraper.py
```

**Mac/Linux:**
```bash
source venv/bin/activate
python scraper.py
```

This will:
- Scrape job sites
- Save to database
- Send email notifications (if configured)

---

### 6️⃣ View Dashboard

```bash
streamlit run dashboard.py
```

Open your browser to: `http://localhost:8501`

---

## 📝 Common Issues

### "Python not found"
- Reinstall Python and check "Add to PATH" during installation
- Try `python3` instead of `python`

### "playwright install failed"
```bash
playwright install-deps
playwright install chromium
```

### "Permission denied" (Mac/Linux)
```bash
chmod +x setup.sh
```

### Email not sending
- Check email credentials in `.env`
- Verify app password (not regular password)
- Ensure 2FA is enabled on Gmail

---

## 🎯 Customization

### Change Search Keywords

Edit `scraper.py`:
```python
keywords = ["Python 개발자", "데이터 엔지니어", "Your Keywords"]
```

### Scrape More Pages

Edit `scraper.py`:
```python
asyncio.run(scraper.scrape_all(keywords=keywords, pages_per_site=5))
```

### Schedule Automatic Scraping

**Windows Task Scheduler:**
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily at 9 AM
4. Action: Run `C:\path\to\venv\Scripts\python.exe scraper.py`

**Linux/Mac Cron:**
```bash
crontab -e
# Add this line:
0 9 * * * cd /path/to/ai-job-scraper && ./venv/bin/python scraper.py
```

---

## 💡 Tips

1. **First Run**: Let it scrape for a few minutes
2. **Database**: Check `jobs.db` file is created
3. **Dashboard**: Refresh browser to see new jobs
4. **Export**: Use dashboard to export CSV

---

## 🆘 Need Help?

- Check README.md for detailed documentation
- Open an issue on GitHub
- Email: your.email@example.com

---

**Happy Job Hunting!** 🎯💼
