"""
MBAN626 Dashboard Project — Streamlit App
Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import requests
import warnings
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

warnings.filterwarnings('ignore')

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Hospital Analytics Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-left: 4px solid #4e9af1;
        border-radius: 6px;
        padding: 14px 18px;
        margin-bottom: 10px;
    }
    .metric-card h4 { margin: 0 0 4px; font-size: 13px; color: #6c757d; }
    .metric-card p  { margin: 0; font-size: 22px; font-weight: 600; color: #212529; }
    .section-header {
        font-size: 18px; font-weight: 600;
        border-bottom: 2px solid #e9ecef;
        padding-bottom: 6px; margin: 24px 0 16px;
    }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('healthcare_dataset.csv')
    df.columns = (
        df.columns.str.strip().str.lower().str.replace(' ', '_')
    )
    df['date_of_admission'] = pd.to_datetime(df['date_of_admission'])
    df['discharge_date']    = pd.to_datetime(df['discharge_date'])
    df['length_of_stay']    = (df['discharge_date'] - df['date_of_admission']).dt.days
    df['admission_month']   = df['date_of_admission'].dt.to_period('M').astype(str)
    df['admission_year']    = df['date_of_admission'].dt.year

    str_cols = ['gender', 'blood_type', 'medical_condition',
                'admission_type', 'insurance_provider', 'test_results']
    for col in str_cols:
        df[col] = df[col].str.strip().str.title()

    # Billing bands via loop
    billing_bands = []
    for amt in df['billing_amount']:
        if amt < 10000:
            billing_bands.append('Low (<$10k)')
        elif amt < 30000:
            billing_bands.append('Medium ($10k–$30k)')
        elif amt < 50000:
            billing_bands.append('High ($30k–$50k)')
        else:
            billing_bands.append('Very High (>$50k)')
    df['billing_band'] = billing_bands

    # Age groups via loop
    age_groups = []
    for age in df['age']:
        if age < 18:
            age_groups.append('Minor (<18)')
        elif age < 35:
            age_groups.append('Young Adult (18–34)')
        elif age < 55:
            age_groups.append('Middle Age (35–54)')
        elif age < 70:
            age_groups.append('Senior (55–69)')
        else:
            age_groups.append('Elderly (70+)')
    df['age_group'] = age_groups

    return df


@st.cache_data(ttl=3600)
def fetch_disease_data():
    try:
        r = requests.get('https://disease.sh/v3/covid-19/all', timeout=10)
        r.raise_for_status()
        d = r.json()
        return {
            'total_cases'  : d.get('cases', 'N/A'),
            'active_cases' : d.get('active', 'N/A'),
            'total_deaths' : d.get('deaths', 'N/A'),
            'recovered'    : d.get('recovered', 'N/A'),
            'critical'     : d.get('critical', 'N/A'),
            'updated'      : pd.to_datetime(d.get('updated', 0), unit='ms')
        }
    except Exception:
        return None


def summarize_condition(dataframe):
    return (
        dataframe.groupby('medical_condition')
        .agg(
            patient_count = ('name', 'count'),
            avg_billing   = ('billing_amount', 'mean'),
            avg_los       = ('length_of_stay', 'mean'),
            common_result = ('test_results', lambda x: x.mode()[0])
        )
        .reset_index()
        .sort_values('patient_count', ascending=False)
        .assign(avg_billing=lambda d: d['avg_billing'].round(2),
                avg_los    =lambda d: d['avg_los'].round(1))
    )


class PatientFilter:
    def __init__(self, dataframe):
        self.df = dataframe.copy()

    def by_condition(self, condition):
        return self.df[self.df['medical_condition'].str.lower() == condition.lower()]

    def by_admission_type(self, admission_type):
        return self.df[self.df['admission_type'].str.lower() == admission_type.lower()]

    def by_age_group(self, age_group):
        return self.df[self.df['age_group'] == age_group]

    def by_insurance(self, provider):
        return self.df[self.df['insurance_provider'].str.lower() == provider.lower()]


# ── Load data ─────────────────────────────────────────────────────────────────
df = load_data()
pf = PatientFilter(df)

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/hospital.png", width=64)
st.sidebar.title("Filters")

selected_conditions = st.sidebar.multiselect(
    "Medical Condition",
    options=sorted(df['medical_condition'].unique()),
    default=sorted(df['medical_condition'].unique())
)
selected_admission = st.sidebar.multiselect(
    "Admission Type",
    options=sorted(df['admission_type'].unique()),
    default=sorted(df['admission_type'].unique())
)
selected_insurance = st.sidebar.multiselect(
    "Insurance Provider",
    options=sorted(df['insurance_provider'].unique()),
    default=sorted(df['insurance_provider'].unique())
)
year_range = st.sidebar.slider(
    "Admission Year Range",
    int(df['admission_year'].min()),
    int(df['admission_year'].max()),
    (int(df['admission_year'].min()), int(df['admission_year'].max()))
)

# Apply filters
filtered = df[
    df['medical_condition'].isin(selected_conditions) &
    df['admission_type'].isin(selected_admission) &
    df['insurance_provider'].isin(selected_insurance) &
    df['admission_year'].between(*year_range)
]

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🏥 Hospital Analytics Dashboard")
st.caption("MBAN626 Dashboard Project · AI and Data Analytics Strategy · 2T 2025–2026")
st.markdown("---")

# ── KPI Cards ─────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.metric("Total Patients", f"{len(filtered):,}")
with k2:
    st.metric("Avg Billing", f"${filtered['billing_amount'].mean():,.0f}")
with k3:
    st.metric("Avg Length of Stay", f"{filtered['length_of_stay'].mean():.1f} days")
with k4:
    st.metric("Top Condition", filtered['medical_condition'].mode()[0] if len(filtered) > 0 else "—")
with k5:
    st.metric("Emergency Rate",
              f"{(filtered['admission_type'] == 'Emergency').mean() * 100:.1f}%")

st.markdown("---")

# ── Row 1: Admissions by Condition  |  Billing by Admission Type ─────────────
st.markdown('<div class="section-header">Admissions & Billing Overview</div>',
            unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    cond_counts = filtered['medical_condition'].value_counts().reset_index()
    cond_counts.columns = ['medical_condition', 'count']
    fig = px.bar(
        cond_counts, x='count', y='medical_condition',
        orientation='h', color='count',
        color_continuous_scale='Blues',
        title="Patient Admissions by Medical Condition",
        labels={'count': 'Admissions', 'medical_condition': 'Condition'}
    )
    fig.update_layout(coloraxis_showscale=False, height=380, margin=dict(l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Chronic conditions dominate admission volumes.")

with col2:
    fig = px.box(
        filtered, x='admission_type', y='billing_amount',
        color='admission_type',
        title="Billing Amount by Admission Type",
        labels={'admission_type': 'Admission Type', 'billing_amount': 'Billing (USD)'},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(showlegend=False, height=380,
                      yaxis_tickprefix='$', yaxis_tickformat=',',
                      margin=dict(l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Emergency admissions show the widest billing spread.")

# ── Row 2: Length of Stay  |  Insurance Pie ───────────────────────────────────
st.markdown('<div class="section-header">Length of Stay & Insurance</div>',
            unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    los_data = (
        filtered.groupby(['medical_condition', 'admission_type'])['length_of_stay']
        .mean().reset_index()
    )
    fig = px.bar(
        los_data, x='medical_condition', y='length_of_stay',
        color='admission_type', barmode='group',
        title="Avg Length of Stay by Condition & Admission Type",
        labels={'length_of_stay': 'Avg Days', 'medical_condition': 'Condition'},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(height=380, xaxis_tickangle=-20, margin=dict(l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Cancer and Obesity patients typically stay the longest.")

with col4:
    ins_counts = filtered['insurance_provider'].value_counts().reset_index()
    ins_counts.columns = ['insurance_provider', 'count']
    fig = px.pie(
        ins_counts, names='insurance_provider', values='count',
        title="Patient Share by Insurance Provider",
        hole=0.38,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textposition='outside', textinfo='percent+label')
    fig.update_layout(height=380, margin=dict(l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Coverage is evenly distributed across providers.")

# ── Row 3: Monthly Trend  |  Billing by Age Group ────────────────────────────
st.markdown('<div class="section-header">Trends & Demographics</div>',
            unsafe_allow_html=True)

col5, col6 = st.columns(2)

with col5:
    monthly = (
        filtered.groupby('admission_month').size()
        .reset_index(name='admissions')
        .sort_values('admission_month')
    )
    fig = px.line(
        monthly, x='admission_month', y='admissions',
        title="Monthly Admissions Trend",
        markers=True,
        labels={'admission_month': 'Month', 'admissions': 'Admissions'}
    )
    fig.update_layout(height=360, xaxis_tickangle=-45, margin=dict(l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Stable admission volumes with minor seasonal variation.")

with col6:
    order = ['Minor (<18)', 'Young Adult (18–34)', 'Middle Age (35–54)',
             'Senior (55–69)', 'Elderly (70+)']
    age_billing = (
        filtered.groupby('age_group')['billing_amount']
        .mean().reindex(order).reset_index()
    )
    fig = px.bar(
        age_billing, x='age_group', y='billing_amount',
        title="Average Billing by Age Group",
        color='billing_amount',
        color_continuous_scale='Oranges',
        labels={'age_group': 'Age Group', 'billing_amount': 'Avg Billing (USD)'}
    )
    fig.update_layout(coloraxis_showscale=False, height=360,
                      yaxis_tickprefix='$', yaxis_tickformat=',',
                      xaxis_tickangle=-10, margin=dict(l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Elderly patients incur the highest average billing.")

# ── Row 4: Condition Summary Table ───────────────────────────────────────────
st.markdown('<div class="section-header">Condition Summary Table</div>',
            unsafe_allow_html=True)

summary = summarize_condition(filtered)
summary['avg_billing'] = summary['avg_billing'].apply(lambda x: f"${x:,.2f}")
summary.columns = ['Condition', 'Patients', 'Avg Billing', 'Avg LOS (Days)', 'Common Result']
st.dataframe(summary, use_container_width=True, hide_index=True)

# ── Row 5: Live API Data ──────────────────────────────────────────────────────
st.markdown('<div class="section-header">Live Global Disease Context (Open Disease API)</div>',
            unsafe_allow_html=True)

with st.spinner("Fetching live data from disease.sh..."):
    disease_data = fetch_disease_data()

if disease_data:
    d1, d2, d3, d4, d5 = st.columns(5)
    d1.metric("Total Cases",    f"{disease_data['total_cases']/1e6:.1f}M")
    d2.metric("Active Cases",   f"{disease_data['active_cases']/1e6:.2f}M")
    d3.metric("Total Deaths",   f"{disease_data['total_deaths']/1e6:.2f}M")
    d4.metric("Recovered",      f"{disease_data['recovered']/1e6:.1f}M")
    d5.metric("Critical",       f"{disease_data['critical']:,}")
    st.caption(f"Last updated: {disease_data['updated']} · Source: disease.sh")

    api_df = pd.DataFrame({
        'Category': ['Total Cases', 'Recovered', 'Deaths', 'Active'],
        'Count': [
            disease_data['total_cases'], disease_data['recovered'],
            disease_data['total_deaths'], disease_data['active_cases']
        ]
    })
    fig = px.bar(
        api_df, x='Category', y='Count',
        color='Category',
        color_discrete_sequence=['#4e9af1', '#5cb85c', '#d9534f', '#f0ad4e'],
        title="Global COVID-19 Overview",
        labels={'Count': 'Number of Cases'}
    )
    fig.update_layout(showlegend=False, height=340,
                      yaxis_tickformat='.2s', margin=dict(l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Could not fetch live data from disease.sh. Check your internet connection.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("MBAN626 · Hospital Analytics Dashboard · Data: Kaggle (prasad22/healthcare-dataset) · API: disease.sh")
