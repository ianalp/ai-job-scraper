#!/bin/bash

# AI Job Scraper - Quick Start Script

echo "🚀 AI Job Scraper - Quick Start"
echo "================================"
echo ""

# Check Python version
echo "📌 Checking Python version..."
python3 --version

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
playwright install chromium

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your email credentials!"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your email settings"
echo "2. Run scraper: python scraper.py"
echo "3. Launch dashboard: streamlit run dashboard.py"
echo ""
echo "Happy job hunting! 💼"
