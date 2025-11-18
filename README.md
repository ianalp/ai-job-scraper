# 💼 AI Job Scraper Pro

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Maintenance](https://img.shields.io/badge/Maintained-Yes-brightgreen.svg)

**Automated job scraping tool that collects job postings from multiple Korean job sites and provides an interactive dashboard for analysis.**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Demo](#-demo) • [Configuration](#%EF%B8%8F-configuration)

</div>

---

## 🎯 Features

### 🔍 Multi-Site Scraping
- **Saramin** (사람인) - Korea's leading job portal
- **JobKorea** (잡코리아) - Comprehensive job listings
- Easily extendable to add more job sites

### 📊 Interactive Dashboard
- Real-time job statistics and analytics
- Advanced filtering (keyword, location, experience, date)
- Visual charts and graphs
- Export to CSV
- Mobile-responsive design

### 📧 Smart Notifications
- Email alerts for new job postings
- Daily summary reports
- Customizable notification rules
- HTML-formatted professional emails

### 💾 Database Management
- SQLite database for efficient storage
- Automatic duplicate detection
- Historical data tracking
- Fast queries and indexing

### 🤖 Automation Ready
- Async/await for high performance
- Cron job compatible
- Configurable scraping schedules
- Headless browser support

---

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Git (for cloning)

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/ai-job-scraper.git
cd ai-job-scraper
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Install Playwright Browsers
```bash
playwright install chromium
```

### Step 5: Configure Environment Variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your settings
# Required: Email credentials for notifications
```

---

## 💻 Usage

### Basic Scraping

Run the scraper with default settings:
```bash
python scraper.py
```

### Custom Keywords
Edit the `scraper.py` file or create your own script:
```python
from scraper import JobScraper
import asyncio

scraper = JobScraper()
keywords = ["Python 개발자", "데이터 사이언티스트", "머신러닝 엔지니어"]
asyncio.run(scraper.scrape_all(keywords=keywords, pages_per_site=5))
```

### Launch Dashboard
```bash
streamlit run dashboard.py
```

Then open your browser to `http://localhost:8501`

### Send Email Notifications
```python
from email_notifier import EmailNotifier
from scraper import JobScraper

scraper = JobScraper()
notifier = EmailNotifier()

# Scrape and notify
jobs = asyncio.run(scraper.scrape_saramin("Python", pages=3))
notifier.send_email(jobs)
```

---

## ⚙️ Configuration

### Email Settings (.env)

For Gmail users:
1. Enable 2-factor authentication on your Google account
2. Generate an App Password:
   - Go to Google Account → Security
   - Under "Signing in to Google", select "App passwords"
   - Create a new app password for "Mail"
3. Use this app password in your `.env` file

```env
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-16-digit-app-password
RECEIVER_EMAIL=alerts@yourdomain.com
```

### Scraping Configuration

Customize scraping behavior:
```python
# Number of pages per site
pages_per_site = 5

# Keywords to search
keywords = ["개발자", "엔지니어", "프로그래머"]

# Headless mode (True for background, False to see browser)
headless = True
```

---

## 🗂️ Project Structure

```
ai-job-scraper/
│
├── scraper.py              # Main scraping engine
├── dashboard.py            # Streamlit web dashboard
├── email_notifier.py       # Email notification system
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── README.md              # This file
│
├── jobs.db                # SQLite database (created after first run)
└── screenshots/           # Dashboard screenshots (optional)
```

---

## 📊 Database Schema

```sql
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    location TEXT,
    salary TEXT,
    experience TEXT,
    education TEXT,
    url TEXT UNIQUE NOT NULL,
    source TEXT NOT NULL,
    posted_date TEXT,
    scraped_date TEXT NOT NULL,
    keywords TEXT
);
```

---

## 🔄 Automation with Cron

### Linux/macOS

Edit crontab:
```bash
crontab -e
```

Add daily scraping at 9 AM:
```bash
0 9 * * * cd /path/to/ai-job-scraper && /path/to/venv/bin/python scraper.py
```

### Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., Daily at 9:00 AM)
4. Action: Start a program
5. Program: `C:\path\to\python.exe`
6. Arguments: `C:\path\to\scraper.py`

---

## 🛠️ Troubleshooting

### Playwright Installation Issues
```bash
# Install specific browser
playwright install chromium

# Install system dependencies (Linux)
playwright install-deps
```

### Database Locked Error
```python
# Increase timeout in scraper.py
conn = sqlite3.connect('jobs.db', timeout=10.0)
```

### SMTP Authentication Error
- Verify app password (not regular password)
- Check 2FA is enabled
- Try "Less secure app access" if app passwords unavailable

### Scraping Failures
- Check internet connection
- Verify target website is accessible
- Some sites may have anti-scraping measures
- Add delays between requests if needed

---

## 🚀 Future Enhancements

- [ ] Support for more job sites (LinkedIn, Indeed, etc.)
- [ ] AI-powered job matching and recommendations
- [ ] Telegram bot integration
- [ ] Advanced analytics and trends
- [ ] Resume matching and scoring
- [ ] API endpoint for external integrations
- [ ] Docker containerization
- [ ] Cloud deployment guide

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

This tool is for educational and personal use only. Please:
- Respect website terms of service
- Don't overload servers with excessive requests
- Add appropriate delays between requests
- Use scraped data responsibly
- Comply with local data protection laws

---

## 🌟 Acknowledgments

- [Playwright](https://playwright.dev/) - Web automation framework
- [Streamlit](https://streamlit.io/) - Dashboard framework
- [Plotly](https://plotly.com/) - Interactive charts
- Korean job sites for providing valuable data

---

## 👤 About the Developer

**ianalp** - AI Automation & Full-Stack Developer

I specialize in creating intelligent automation solutions that save time and boost productivity.

### 🛠️ Tech Stack

- **Backend:** Python, FastAPI, Node.js
- **Frontend:** React, Next.js, TypeScript
- **AI/ML:** OpenAI API, Claude API, LangChain
- **Automation:** Playwright, Selenium, Web Scraping
- **Data:** Pandas, SQL, Data Visualization

### 📫 Contact

- 📧 **Email:** forplanai@gmail.com
- 🔗 **GitHub:** [github.com/ianalp](https://github.com/ianalp)
- 🐦 **Twitter:** [@ianalp0914](https://twitter.com/ianalp0914)
- 💼 **Kmong:** Available for freelance projects

### 🌟 Services

Looking for automation solutions? I can help with:

- 🤖 Web Scraping & Data Collection
- 📊 Business Dashboards & Analytics
- ✍️ AI-Powered Content Generation
- 🔄 Workflow Automation
- 💻 Custom Software Development

**Open for freelance projects!** Feel free to reach out.

---

<div align="center">

**Made with ❤️ by [Chan Yeon Park](https://github.com/ianalp)**

⭐ Star this repo if you find it useful!

</div>
