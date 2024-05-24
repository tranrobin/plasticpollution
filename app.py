import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
def load_data():
    # Replace this with the actual path to your CSV file
    df = pd.read_csv("cleaned_data.csv")
    return df

def display_metrics(filtered_df):
    total_plastics = int(filtered_df['grand_total'].sum().round())
    total_events = int(filtered_df['num_events'].sum().round())
    total_volunteers = int(filtered_df['volunteers'].sum().round())

    # Calculate the grand_total change from 2019 to 2020
    grand_total_2019 = filtered_df[filtered_df['year'] == 2019]['grand_total'].sum()
    grand_total_2020 = filtered_df[filtered_df['year'] == 2020]['grand_total'].sum()
    grand_total_change = grand_total_2020 - grand_total_2019
    grand_total_change_percentage = (grand_total_change / grand_total_2019) * 100 if grand_total_2019 != 0 else 0
    #grand_total_change_percentage = grand_total_change_percentage.round()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Plastics Collected", value=f"{total_plastics:,}")
    with col2:
        st.metric(label="Total Events", value=f"{total_events:,}")
    with col3:
        st.metric(label="Total Volunteers", value=f"{total_volunteers:,}")
    with col4:
        st.metric(label="Change in Total Plastics (2019-2020)", 
                  value=f"{grand_total_change_percentage:,}%")

def geographical_distribution(filtered_df):
    st.header('Geographical Distribution')
    geo_country_filter = st.multiselect('Select Country for Geographical Distribution', filtered_df['country'].unique())
    if geo_country_filter:
        geo_filtered_df = filtered_df[filtered_df['country'].isin(geo_country_filter)]
    else:
        geo_filtered_df = filtered_df
    fig_map = px.choropleth(geo_filtered_df, locations='country', locationmode='country names', color='grand_total', 
                            hover_name='country', animation_frame='year', title='Geographical Distribution of Plastic Pollution')
    st.plotly_chart(fig_map, use_container_width=True)

def plastic_type_distribution(filtered_df):
    st.header('Plastic Type')
    available_years = filtered_df['year'].unique()
    default_years = [year for year in [2019, 2020] if year in available_years]
    plastic_type_year_filter = st.multiselect('Select Year for Plastic Type Distribution', available_years, default=default_years)
    plastic_type_filtered_df = filtered_df[filtered_df['year'].isin(plastic_type_year_filter)]
    plastic_types = ['hdpe', 'ldpe', 'o', 'pet', 'pp', 'ps', 'pvc']
    plastic_counts = plastic_type_filtered_df[plastic_types].sum()
    fig_plastic_types = px.pie(values=plastic_counts.values, names=plastic_counts.index, title='Plastic Types Distribution')
    st.plotly_chart(fig_plastic_types, use_container_width=True)

def country_breakdown(filtered_df):
    st.header('Country Breakdown')
    available_years = filtered_df['year'].unique()
    default_years = [year for year in [2019, 2020] if year in available_years]
    company_year_filter = st.multiselect('Select Year for Country Breakdown', available_years, default=default_years)
    company_filtered_df = filtered_df[filtered_df['year'].isin(company_year_filter)]
    company_counts = company_filtered_df.groupby('country')['grand_total'].sum().nlargest(10).reset_index()
    fig_company = px.bar(company_counts, x='country', y='grand_total', title='Top 10 Countries by Plastic Count')
    fig_company.update_layout(height=500)
    st.plotly_chart(fig_company, use_container_width=True)

def parent_company_breakdown(filtered_df):
    st.header('Parent Company Breakdown')
    available_years = filtered_df['year'].unique()
    default_years = [year for year in [2019, 2020] if year in available_years]
    company_year_filter = st.multiselect('Select Year for Parent Company Breakdown', available_years, default=default_years)
    company_filtered_df = filtered_df[filtered_df['year'].isin(company_year_filter)]
    company_counts = company_filtered_df.groupby('parent_company')['grand_total'].sum().nlargest(10).reset_index()
    fig_company = px.bar(company_counts, x='parent_company', y='grand_total', title='Top 10 Parent Companies by Plastic Count')
    fig_company.update_layout(height=500)
    st.plotly_chart(fig_company, use_container_width=True)

def yearly_comparison(filtered_df):
    st.header('Yearly Comparison')
    plastic_type_option = st.selectbox('Select Plastic Type for Yearly Comparison', ['grand_total', 'hdpe', 'ldpe', 'o', 'pet', 'pp', 'ps', 'pvc'])
    yearly_counts = filtered_df.groupby('year')[plastic_type_option].sum().reset_index()
    fig_yearly = px.line(yearly_counts, x='year', y=plastic_type_option, title=f'{plastic_type_option.upper()} Counts by Year')
    st.plotly_chart(fig_yearly, use_container_width=True)

def pollution_intensity(filtered_df):
    st.header('Pollution Intensity by Country')
    intensity_country_filter = st.multiselect('Select Country for Pollution Intensity', filtered_df['country'].unique())
    if intensity_country_filter:
        intensity_filtered_df = filtered_df[filtered_df['country'].isin(intensity_country_filter)]
    else:
        intensity_filtered_df = filtered_df
    pollution_intensity = intensity_filtered_df.groupby('country').apply(lambda x: x['grand_total'].sum() / x['volunteers'].sum()).reset_index(name='pollution_intensity')
    fig_pollution_intensity = px.bar(pollution_intensity, x='country', y='pollution_intensity', title='Pollution Intensity by Country (Plastic per Volunteer)')
    fig_pollution_intensity.update_layout(height=600)  # Adjust the height as needed
    st.plotly_chart(fig_pollution_intensity, use_container_width=True)

def reduction_rate(filtered_df):
    st.header('Reduction Rate by Country')
    reduction_country_filter = st.multiselect('Select Country for Reduction Rate', filtered_df['country'].unique())
    if reduction_country_filter:
        reduction_filtered_df = filtered_df[filtered_df['country'].isin(reduction_country_filter)]
    else:
        reduction_filtered_df = filtered_df
    pollution_2019 = reduction_filtered_df[reduction_filtered_df['year'] == 2019].groupby('country')['grand_total'].sum()
    pollution_2020 = reduction_filtered_df[reduction_filtered_df['year'] == 2020].groupby('country')['grand_total'].sum()
    reduction_rate = ((pollution_2020 - pollution_2019) / pollution_2019 * 100).reset_index(name='reduction_rate')
    fig_reduction_rate = px.bar(reduction_rate, x='country', y='reduction_rate', title='Reduction Rate by Country (2019-2020)')
    fig_reduction_rate.update_layout(height=600)  # Adjust the height as needed
    st.plotly_chart(fig_reduction_rate, use_container_width=True)

def contribution_ratio(filtered_df):
    st.header('Top 10 Companies by Contribution Ratio')
    available_years = filtered_df['year'].unique()
    default_years = [year for year in [2019, 2020] if year in available_years]
    contribution_year_filter = st.multiselect('Select Year for Contribution Ratio', available_years, default=default_years)
    contribution_filtered_df = filtered_df[filtered_df['year'].isin(contribution_year_filter)]
    total_plastic_pollution = contribution_filtered_df['grand_total'].sum()
    company_contribution = contribution_filtered_df.groupby('parent_company')['grand_total'].sum().reset_index()
    company_contribution['contribution_ratio'] = company_contribution['grand_total'] / total_plastic_pollution
    fig_contribution_ratio = px.bar(company_contribution.nlargest(10, 'contribution_ratio'), x='parent_company', y='contribution_ratio', title='Top 10 Companies by Contribution Ratio')
    fig_contribution_ratio.update_layout(height=600)  # Adjust the height as needed
    st.plotly_chart(fig_contribution_ratio, use_container_width=True)

def main():
    df = load_data()
    
    # Sidebar filters
    st.sidebar.title('Global Filters')
    country_filter = st.sidebar.multiselect('Country', df['country'].unique())
    year_filter = st.sidebar.multiselect('Year', df['year'].unique(), default=[2019, 2020])
    company_filter = st.sidebar.multiselect('Parent Company', df['parent_company'].unique())

    # Filter data based on user selection
    filtered_df = df[(df['country'].isin(country_filter) if country_filter else True) &
                     (df['year'].isin(year_filter) if year_filter else True) &
                     (df['parent_company'].isin(company_filter) if company_filter else True)]

    st.title('Global Plastic Pollution Analysis (2019-2020)')

    display_metrics(filtered_df)
    #geographical_distribution(filtered_df)
    
    # Add vertical space
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Create columns with 1/3 and 2/3 width
    col1, _, col2 = st.columns([1, 0.2, 1.5])
    with col1:
        plastic_type_distribution(filtered_df)
    with col2:
        yearly_comparison(filtered_df)
    
    country_breakdown(filtered_df)
    parent_company_breakdown(filtered_df)
    pollution_intensity(filtered_df)
    reduction_rate(filtered_df)
    contribution_ratio(filtered_df)

    # Raw Data
    st.header('Raw Data')
    st.write(filtered_df)

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.sidebar.title('Plastic Pollution Data Explorer')
    main()
