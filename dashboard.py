import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

# Page config
st.set_page_config(
    page_title="AeroFit Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Color scheme
COLORS = {
    'bg': '#0E1117',
    'card': '#1E1E1E',
    'accent': '#4A90E2',
    'text': '#FFFFFF',
    'subtext': '#A0AEC0',
    'success': '#48BB78',
    'warning': '#ED8936',
    'grid': '#2D3748'
}

# Custom CSS
st.markdown("""
<style>
    /* Main Layout */
    .main {
        background-color: #0E1117;
    }
    
    /* Cards */
    .stCard {
        background-color: #1E1E1E;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Text */
    h1, h2, h3, p {
        color: #FFFFFF !important;
    }
    
    .metric-card {
        background: linear-gradient(45deg, #1E1E1E, #2D3748);
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(74, 144, 226, 0.3);
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #4A90E2;
    }
    
    .metric-label {
        color: #A0AEC0;
        font-size: 0.875rem;
    }
    
    /* Plotly chart background */
    .js-plotly-plot {
        background-color: #1E1E1E !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1E1E1E;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Radio buttons */
    .stRadio > label {
        color: #FFFFFF !important;
    }
    
    /* Insights box */
    .insight-box {
        background: linear-gradient(45deg, #1E1E1E, #2D3748);
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #4A90E2;
    }
    
    /* Tables */
    .dataframe {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
    }
    
    .dataframe th {
        background-color: #2D3748 !important;
        color: #FFFFFF !important;
    }
    
    .dataframe td {
        color: #FFFFFF !important;
    }
    
    /* Plot area */
    .plot-container {
        background-color: #1E1E1E !important;
        border-radius: 0.5rem;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Configure plotly theme
import plotly.io as pio
template = pio.templates["plotly_dark"]
template.layout.update(
    paper_bgcolor=COLORS['card'],
    plot_bgcolor=COLORS['card'],
    font_color=COLORS['text']
)
template.layout.xaxis.update(gridcolor=COLORS['grid'])
template.layout.yaxis.update(gridcolor=COLORS['grid'])
pio.templates["custom_dark"] = template
pio.templates.default = "custom_dark"

# Load and cache data
@st.cache_data
def load_data():
    df = pd.read_csv('aerofit_treadmill_data.csv')
    return df

df = load_data()

# Chart creation functions
def create_bar_chart(data, x, y, title, color=None):
    fig = px.bar(
        data,
        x=x,
        y=y,
        title=title,
        color=color,
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_layout(
        paper_bgcolor=COLORS['card'],
        plot_bgcolor=COLORS['card'],
        font_color=COLORS['text'],
        title_font_color=COLORS['text'],
        legend_font_color=COLORS['text'],
        xaxis=dict(
            gridcolor=COLORS['grid'],
            zerolinecolor=COLORS['grid'],
            tickfont=dict(color=COLORS['text'])
        ),
        yaxis=dict(
            gridcolor=COLORS['grid'],
            zerolinecolor=COLORS['grid'],
            tickfont=dict(color=COLORS['text'])
        )
    )
    return fig

def create_box_plot(data, x, y, title, color=None):
    fig = px.box(
        data,
        x=x,
        y=y,
        title=title,
        color=color,
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_layout(
        paper_bgcolor=COLORS['card'],
        plot_bgcolor=COLORS['card'],
        font_color=COLORS['text'],
        title_font_color=COLORS['text'],
        legend_font_color=COLORS['text'],
        xaxis=dict(
            gridcolor=COLORS['grid'],
            zerolinecolor=COLORS['grid'],
            tickfont=dict(color=COLORS['text'])
        ),
        yaxis=dict(
            gridcolor=COLORS['grid'],
            zerolinecolor=COLORS['grid'],
            tickfont=dict(color=COLORS['text'])
        )
    )
    return fig

def create_scatter_plot(data, x, y, title, color=None, size=None):
    fig = px.scatter(
        data,
        x=x,
        y=y,
        title=title,
        color=color,
        size=size,
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_layout(
        paper_bgcolor=COLORS['card'],
        plot_bgcolor=COLORS['card'],
        font_color=COLORS['text'],
        title_font_color=COLORS['text'],
        legend_font_color=COLORS['text'],
        xaxis=dict(
            gridcolor=COLORS['grid'],
            zerolinecolor=COLORS['grid'],
            tickfont=dict(color=COLORS['text'])
        ),
        yaxis=dict(
            gridcolor=COLORS['grid'],
            zerolinecolor=COLORS['grid'],
            tickfont=dict(color=COLORS['text'])
        )
    )
    return fig

# Sidebar
with st.sidebar:
    st.title("🏃‍♂️ AeroFit Analytics")
    
    # Key metrics
    total_customers = len(df)
    avg_age = df['Age'].mean()
    avg_income = df['Income'].mean()
    
    st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{:,}</div>
            <div class="metric-label">Total Customers</div>
        </div>
        
        <div class="metric-card">
            <div class="metric-value">{:.1f}</div>
            <div class="metric-label">Average Age</div>
        </div>
        
        <div class="metric-card">
            <div class="metric-value">${:,.0f}</div>
            <div class="metric-label">Average Income</div>
        </div>
    """.format(total_customers, avg_age, avg_income), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation
    section = st.radio(
        "Select Analysis",
        ["Overview", "Customer Segments", "Usage Analysis", "Financial Insights", "Recommendations"]
    )

# Main content sections
if section == "Overview":
    st.title("Product Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Product Distribution
        product_dist = df['Product'].value_counts()
        fig = px.pie(
            values=product_dist.values,
            names=product_dist.index,
            title="Product Distribution",
            hole=0.4,
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(
            paper_bgcolor=COLORS['card'],
            plot_bgcolor=COLORS['card']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Age Distribution
        fig = create_box_plot(
            df,
            x='Product',
            y='Age',
            title="Age Distribution by Product"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Income Distribution
        fig = create_box_plot(
            df,
            x='Product',
            y='Income',
            title="Income Distribution by Product"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Key insights
        st.markdown("""
        <div class="insight-box">
            <h3>Key Insights</h3>
            <ul>
                <li>KP781 shows highest average income customers</li>
                <li>Age distribution varies significantly across models</li>
                <li>Product preferences show clear market segmentation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif section == "Customer Segments":
    st.title("Customer Segments")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gender Distribution
        gender_dist = pd.crosstab(df['Product'], df['Gender'], normalize='index') * 100
        gender_dist_reset = gender_dist.reset_index()
        fig = create_bar_chart(
            gender_dist_reset,
            x='Product',
            y=['Female', 'Male'],
            title="Gender Distribution by Product (%)"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Marital Status
        marital_dist = pd.crosstab(df['Product'], df['MaritalStatus'], normalize='index') * 100
        marital_dist_reset = marital_dist.reset_index()
        fig = create_bar_chart(
            marital_dist_reset,
            x='Product',
            y=['Single', 'Partnered'],
            title="Marital Status by Product (%)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Fitness Level Distribution
        fitness_counts = pd.crosstab(df['Product'], df['Fitness'], normalize='index') * 100
        # Convert column names to strings
        fitness_counts.columns = fitness_counts.columns.astype(str)
        fitness_counts_reset = fitness_counts.reset_index()
        
        # Create stacked bar chart for fitness levels
        fig = px.bar(
            fitness_counts_reset,
            x='Product',
            y=fitness_counts.columns.tolist(),
            title="Fitness Level Distribution by Product (%)",
            labels={'value': 'Percentage', 'variable': 'Fitness Level'},
            color_discrete_sequence=px.colors.qualitative.Set3,
            barmode='stack'
        )
        fig.update_layout(
            legend_title_text='Fitness Level',
            yaxis_title='Percentage',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            legend=dict(
                bgcolor='rgba(0,0,0,0)',
                bordercolor='rgba(255,255,255,0.1)',
                borderwidth=1
            )
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Fitness Level Statistics
        fitness_stats = df.groupby('Product')['Fitness'].agg(['mean', 'median', 'std']).round(2)
        st.markdown("""
        <div class="insight-box">
            <h3>Fitness Level Analysis</h3>
            <table>
                <tr><th>Product</th><th>Mean</th><th>Median</th><th>Std Dev</th></tr>
                <tr><td>KP281</td><td>{:.1f}</td><td>{:.1f}</td><td>{:.1f}</td></tr>
                <tr><td>KP481</td><td>{:.1f}</td><td>{:.1f}</td><td>{:.1f}</td></tr>
                <tr><td>KP781</td><td>{:.1f}</td><td>{:.1f}</td><td>{:.1f}</td></tr>
            </table>
            <p style="margin-top: 10px; font-size: 0.9em; color: #A0AEC0;">
                Fitness Level Scale: 1 (Beginner) to 5 (Expert)
            </p>
        </div>
        """.format(
            fitness_stats.loc['KP281', 'mean'], fitness_stats.loc['KP281', 'median'], fitness_stats.loc['KP281', 'std'],
            fitness_stats.loc['KP481', 'mean'], fitness_stats.loc['KP481', 'median'], fitness_stats.loc['KP481', 'std'],
            fitness_stats.loc['KP781', 'mean'], fitness_stats.loc['KP781', 'median'], fitness_stats.loc['KP781', 'std']
        ), unsafe_allow_html=True)
        
        # Updated Customer Segments Insights
        st.markdown("""
        <div class="insight-box">
            <h3>Segment Insights</h3>
            <ul>
                <li>KP781 attracts higher fitness levels (mean: {:.1f})</li>
                <li>KP281 shows diverse fitness distribution</li>
                <li>Gender preferences vary by model ({:.1f}% female in KP481)</li>
                <li>Marital status impacts purchase decisions</li>
            </ul>
        </div>
        """.format(
            fitness_stats.loc['KP781', 'mean'],
            gender_dist.loc['KP481', 'Female']
        ), unsafe_allow_html=True)

elif section == "Usage Analysis":
    st.title("Usage Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Usage vs Fitness Level Analysis (bubble chart - already enhanced)
        usage_fitness = pd.crosstab([df['Usage'], df['Product']], df['Fitness'])
        usage_fitness_pct = usage_fitness.div(usage_fitness.sum(axis=1), axis=0) * 100
        usage_fitness_pct = usage_fitness_pct.reset_index()
        
        usage_fitness_melted = pd.melt(
            usage_fitness_pct,
            id_vars=['Usage', 'Product'],
            var_name='Fitness',
            value_name='Percentage'
        )
        
        fig = px.scatter(
            usage_fitness_melted,
            x='Usage',
            y='Fitness',
            size='Percentage',
            color='Product',
            title='Usage vs Fitness Level Distribution',
            labels={
                'Usage': 'Usage Frequency (times/week)',
                'Fitness': 'Fitness Level',
                'Percentage': 'Percentage of Users'
            },
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        
        fig.update_traces(
            marker=dict(line=dict(width=1, color='white')),
            hovertemplate="<br>".join([
                "Product: %{customdata[0]}",
                "Usage: %{x} times/week",
                "Fitness Level: %{y}",
                "Percentage: %{marker.size:.1f}%",
                "<extra></extra>"
            ])
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=True,
            legend=dict(
                bgcolor='rgba(0,0,0,0)',
                bordercolor='rgba(255,255,255,0.1)',
                borderwidth=1
            ),
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                tickmode='linear',
                tick0=0,
                dtick=1
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                tickmode='linear',
                tick0=1,
                dtick=1
            ),
            height=500
        )
        
        fig.update_traces(customdata=usage_fitness_melted[['Product']])
        st.plotly_chart(fig, use_container_width=True)
        
        # Usage Statistics
        usage_stats = df.groupby('Product')['Usage'].agg(['mean', 'median', 'std']).round(2)
        st.markdown("""
        <div class="insight-box">
            <h3>Usage Frequency Analysis</h3>
            <table>
                <tr><th>Product</th><th>Mean</th><th>Median</th><th>Std Dev</th></tr>
                <tr><td>KP281</td><td>{:.1f}</td><td>{:.1f}</td><td>{:.1f}</td></tr>
                <tr><td>KP481</td><td>{:.1f}</td><td>{:.1f}</td><td>{:.1f}</td></tr>
                <tr><td>KP781</td><td>{:.1f}</td><td>{:.1f}</td><td>{:.1f}</td></tr>
            </table>
            <p style="margin-top: 10px; font-size: 0.9em; color: #A0AEC0;">
                Usage Frequency: Times per week
            </p>
        </div>
        """.format(
            usage_stats.loc['KP281', 'mean'], usage_stats.loc['KP281', 'median'], usage_stats.loc['KP281', 'std'],
            usage_stats.loc['KP481', 'mean'], usage_stats.loc['KP481', 'median'], usage_stats.loc['KP481', 'std'],
            usage_stats.loc['KP781', 'mean'], usage_stats.loc['KP781', 'median'], usage_stats.loc['KP781', 'std']
        ), unsafe_allow_html=True)
    
    with col2:
        # Usage vs Miles Analysis
        fig = px.scatter(
            df,
            x='Usage',
            y='Miles',
            color='Product',
            title='Usage Frequency vs Miles Covered',
            labels={
                'Usage': 'Usage Frequency (times/week)',
                'Miles': 'Miles Covered',
                'Product': 'Product Model'
            },
            color_discrete_sequence=px.colors.qualitative.Set2,
            trendline="ols",
            trendline_scope="overall"
        )
        
        fig.update_traces(
            marker=dict(
                size=8,
                line=dict(width=1, color='white')
            ),
            hovertemplate="<br>".join([
                "Product: %{customdata[0]}",
                "Usage: %{x} times/week",
                "Miles: %{y:.0f}",
                "<extra></extra>"
            ])
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=True,
            legend=dict(
                bgcolor='rgba(0,0,0,0)',
                bordercolor='rgba(255,255,255,0.1)',
                borderwidth=1
            ),
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                tickmode='linear',
                tick0=0,
                dtick=1
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.1)'
            ),
            height=500
        )
        
        fig.update_traces(customdata=df[['Product']])
        st.plotly_chart(fig, use_container_width=True)
        
        # Miles Statistics
        miles_stats = df.groupby('Product')['Miles'].agg(['mean', 'median', 'std']).round(2)
        st.markdown("""
        <div class="insight-box">
            <h3>Miles Coverage Analysis</h3>
            <table>
                <tr><th>Product</th><th>Mean</th><th>Median</th><th>Std Dev</th></tr>
                <tr><td>KP281</td><td>{:.0f}</td><td>{:.0f}</td><td>{:.1f}</td></tr>
                <tr><td>KP481</td><td>{:.0f}</td><td>{:.0f}</td><td>{:.1f}</td></tr>
                <tr><td>KP781</td><td>{:.0f}</td><td>{:.0f}</td><td>{:.1f}</td></tr>
            </table>
            <p style="margin-top: 10px; font-size: 0.9em; color: #A0AEC0;">
                Average miles covered by users of each product
            </p>
        </div>
        """.format(
            miles_stats.loc['KP281', 'mean'], miles_stats.loc['KP281', 'median'], miles_stats.loc['KP281', 'std'],
            miles_stats.loc['KP481', 'mean'], miles_stats.loc['KP481', 'median'], miles_stats.loc['KP481', 'std'],
            miles_stats.loc['KP781', 'mean'], miles_stats.loc['KP781', 'median'], miles_stats.loc['KP781', 'std']
        ), unsafe_allow_html=True)
        
        # Key Insights
        st.markdown("""
        <div class="insight-box">
            <h3>Key Usage Insights</h3>
            <ul>
                <li>Strong correlation between usage frequency and miles covered</li>
                <li>KP781 users show higher average weekly usage ({:.1f} times)</li>
                <li>KP781 users cover more miles on average ({:.0f} miles)</li>
                <li>Higher fitness levels correlate with increased usage</li>
            </ul>
        </div>
        """.format(
            usage_stats.loc['KP781', 'mean'],
            miles_stats.loc['KP781', 'mean']
        ), unsafe_allow_html=True)

elif section == "Financial Insights":
    st.title("Financial Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Income Statistics by Product
        income_stats = df.groupby('Product')['Income'].agg(['mean', 'median', 'std']).round(2)
        st.markdown("""
        <div class="insight-box">
            <h3>Income Statistics by Product</h3>
            <table>
                <tr><th>Product</th><th>Mean</th><th>Median</th><th>Std Dev</th></tr>
                <tr><td>KP281</td><td>${:,.0f}</td><td>${:,.0f}</td><td>${:,.0f}</td></tr>
                <tr><td>KP481</td><td>${:,.0f}</td><td>${:,.0f}</td><td>${:,.0f}</td></tr>
                <tr><td>KP781</td><td>${:,.0f}</td><td>${:,.0f}</td><td>${:,.0f}</td></tr>
            </table>
        </div>
        """.format(
            income_stats.loc['KP281', 'mean'], income_stats.loc['KP281', 'median'], income_stats.loc['KP281', 'std'],
            income_stats.loc['KP481', 'mean'], income_stats.loc['KP481', 'median'], income_stats.loc['KP481', 'std'],
            income_stats.loc['KP781', 'mean'], income_stats.loc['KP781', 'median'], income_stats.loc['KP781', 'std']
        ), unsafe_allow_html=True)
        
        # Income Distribution
        fig = create_box_plot(
            df,
            x='Product',
            y='Income',
            title="Income Distribution by Product"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Product Pricing
        product_prices = {
            'KP281': 1500,
            'KP481': 1750,
            'KP781': 2500
        }
        price_data = pd.DataFrame({
            'Product': list(product_prices.keys()),
            'Price': list(product_prices.values())
        })
        fig = create_bar_chart(
            price_data,
            x='Product',
            y='Price',
            title="Product Price Points ($)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Income vs Age Analysis
        fig = create_scatter_plot(
            df,
            x='Age',
            y='Income',
            title="Income vs Age Distribution",
            color='Product'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Market Share Analysis
        market_share = df['Product'].value_counts(normalize=True) * 100
        st.markdown("""
        <div class="insight-box">
            <h3>Market Share Analysis</h3>
            <table>
                <tr><th>Product</th><th>Market Share</th></tr>
                <tr><td>KP281</td><td>{:.1f}%</td></tr>
                <tr><td>KP481</td><td>{:.1f}%</td></tr>
                <tr><td>KP781</td><td>{:.1f}%</td></tr>
            </table>
        </div>
        """.format(
            market_share['KP281'],
            market_share['KP481'],
            market_share['KP781']
        ), unsafe_allow_html=True)
        
        # Financial Insights
        st.markdown("""
        <div class="insight-box">
            <h3>Financial Insights</h3>
            <ul>
                <li>Clear income segmentation across product lines</li>
                <li>KP781 targets high-income customers (${:,.0f} median income)</li>
                <li>Price points strategically positioned for market segments</li>
                <li>Market share distribution reflects pricing strategy</li>
            </ul>
        </div>
        """.format(income_stats.loc['KP781', 'median']), unsafe_allow_html=True)

else:  # Recommendations
    st.title("Marketing Recommendations")
    
    # Marketing Recommendations
    st.markdown("""
    <div class="insight-box">
        <h3>Product Strategy</h3>
        <ul>
            <li>Target KP781 towards high-income, fitness-focused customers</li>
            <li>Position KP481 as the best value-for-money option</li>
            <li>Market KP281 as an entry-level model for beginners</li>
        </ul>
    </div>
    
    <div class="insight-box">
        <h3>Customer Targeting</h3>
        <ul>
            <li>Develop gender-specific marketing campaigns</li>
            <li>Create special promotions based on marital status</li>
            <li>Tailor messaging to different fitness levels</li>
        </ul>
    </div>
    
    <div class="insight-box">
        <h3>Pricing Strategy</h3>
        <ul>
            <li>Maintain premium pricing for KP781</li>
            <li>Consider seasonal discounts for KP481</li>
            <li>Offer financing options for KP281</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("Dashboard created for AeroFit Market Analysis | Updated: 2024")
