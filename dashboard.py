"""
AI Job Scraper - Streamlit Dashboard
Interactive web interface for viewing and filtering job listings
"""

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="AI Job Scraper Dashboard",
    page_icon="💼",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    .job-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=300)
def load_jobs(db_path: str = "jobs.db"):
    """Load jobs from database"""
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM jobs ORDER BY scraped_date DESC", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error loading database: {e}")
        return pd.DataFrame()


def get_stats(df):
    """Calculate statistics"""
    total_jobs = len(df)
    
    # Jobs by source
    by_source = df['source'].value_counts().to_dict()
    
    # Recent jobs (last 24 hours)
    if not df.empty and 'scraped_date' in df.columns:
        df['scraped_datetime'] = pd.to_datetime(df['scraped_date'])
        recent_cutoff = datetime.now() - timedelta(days=1)
        recent_jobs = len(df[df['scraped_datetime'] > recent_cutoff])
    else:
        recent_jobs = 0
    
    # Unique companies
    unique_companies = df['company'].nunique() if not df.empty else 0
    
    return {
        'total': total_jobs,
        'recent': recent_jobs,
        'companies': unique_companies,
        'by_source': by_source
    }


def main():
    # Header
    st.title("💼 AI Job Scraper Dashboard")
    st.markdown("---")
    
    # Load data
    df = load_jobs()
    
    if df.empty:
        st.warning("⚠️ No jobs found in database. Run the scraper first!")
        st.code("python scraper.py", language="bash")
        return
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Keyword search
    search_term = st.sidebar.text_input("Search (title, company)", "")
    
    # Source filter
    sources = ['All'] + list(df['source'].unique())
    selected_source = st.sidebar.selectbox("Source", sources)
    
    # Location filter
    locations = ['All'] + list(df['location'].dropna().unique())
    selected_location = st.sidebar.selectbox("Location", locations)
    
    # Experience filter
    experiences = ['All'] + list(df['experience'].dropna().unique())
    selected_experience = st.sidebar.selectbox("Experience", experiences)
    
    # Date range
    st.sidebar.subheader("Date Range")
    if 'scraped_date' in df.columns:
        df['scraped_datetime'] = pd.to_datetime(df['scraped_date'])
        min_date = df['scraped_datetime'].min().date()
        max_date = df['scraped_datetime'].max().date()
        
        date_range = st.sidebar.date_input(
            "Scraped Date",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
    
    # Apply filters
    filtered_df = df.copy()
    
    if search_term:
        mask = (
            filtered_df['title'].str.contains(search_term, case=False, na=False) |
            filtered_df['company'].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[mask]
    
    if selected_source != 'All':
        filtered_df = filtered_df[filtered_df['source'] == selected_source]
    
    if selected_location != 'All':
        filtered_df = filtered_df[filtered_df['location'] == selected_location]
    
    if selected_experience != 'All':
        filtered_df = filtered_df[filtered_df['experience'] == selected_experience]
    
    if 'scraped_datetime' in filtered_df.columns and len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['scraped_datetime'].dt.date >= start_date) &
            (filtered_df['scraped_datetime'].dt.date <= end_date)
        ]
    
    # Statistics
    stats = get_stats(df)
    filtered_stats = get_stats(filtered_df)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Jobs", stats['total'], f"{filtered_stats['total']} filtered")
    
    with col2:
        st.metric("Recent (24h)", stats['recent'])
    
    with col3:
        st.metric("Companies", stats['companies'])
    
    with col4:
        st.metric("Showing", len(filtered_df))
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Jobs by Source")
        if not filtered_df.empty:
            source_counts = filtered_df['source'].value_counts()
            fig = px.pie(
                values=source_counts.values,
                names=source_counts.index,
                title="Distribution by Source"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 Top 10 Companies")
        if not filtered_df.empty:
            company_counts = filtered_df['company'].value_counts().head(10)
            fig = px.bar(
                x=company_counts.values,
                y=company_counts.index,
                orientation='h',
                title="Most Job Postings"
            )
            fig.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Job listings
    st.subheader(f"📋 Job Listings ({len(filtered_df)} results)")
    
    # Sort options
    sort_col, order_col = st.columns([3, 1])
    with sort_col:
        sort_by = st.selectbox(
            "Sort by",
            ["scraped_date", "title", "company", "location"],
            index=0
        )
    with order_col:
        sort_order = st.radio("Order", ["Desc", "Asc"], horizontal=True)
    
    # Apply sorting
    filtered_df = filtered_df.sort_values(
        by=sort_by,
        ascending=(sort_order == "Asc")
    )
    
    # Display jobs
    for idx, row in filtered_df.iterrows():
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### [{row['title']}]({row['url']})")
                st.markdown(f"**🏢 {row['company']}** | 📍 {row['location']} | 🎓 {row['education']}")
                
                tags = []
                if row['experience']:
                    tags.append(f"💼 {row['experience']}")
                if row['salary']:
                    tags.append(f"💰 {row['salary']}")
                tags.append(f"🔖 {row['source']}")
                
                st.markdown(" • ".join(tags))
            
            with col2:
                if row['url']:
                    st.link_button("Apply →", row['url'], use_container_width=True)
                
                scraped = row['scraped_date']
                st.caption(f"Scraped: {scraped}")
            
            st.markdown("---")
    
    # Export functionality
    st.sidebar.markdown("---")
    st.sidebar.subheader("📥 Export Data")
    
    if st.sidebar.button("Download as CSV"):
        csv = filtered_df.to_csv(index=False)
        st.sidebar.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )


if __name__ == "__main__":
    main()
