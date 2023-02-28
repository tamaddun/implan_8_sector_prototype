import os
import glob
import pandas as pd
import streamlit as st
import plotly.express as px

# Set the page title and header
st.set_page_config(page_title="IMPLAN Results",layout="wide")
# st.title("Industry-specific Effects of CISFs")

# Locate the files in the appropriate directory
path = os.getcwd()+'\\AllData'
files = glob.glob(path+'\\*.csv')

# Load the data
data = []
for file in files:
    df = pd.read_csv(file,index_col=None,header=0)
    data.append(df)
data = pd.concat(data,axis=0,ignore_index=True)

# Clean the data
data.drop(['Unnamed: 0'],axis=1,inplace=True) # Redundant column
# data['Value'] = data['Value'].round().astype(int)
# data = data.loc[data['Value']>=1] # Dropping values with 0

# Rename years
data.loc[data["Year"]==2035,'Year']=5
data.loc[data["Year"]==2040,'Year']=10
data.loc[data["Year"]==2045,'Year']=15
data.loc[data["Year"]==2050,'Year']=20
data.loc[data["Year"]==2055,'Year']=25
data.loc[data["Year"]==2060,'Year']=30
data.loc[data["Year"]==2065,'Year']=35
data.loc[data["Year"]==2070,'Year']=40
data.loc[data["Year"]==2075,'Year']=45
data.loc[data["Year"]==2080,'Year']=50
data.loc[data["Year"]==2085,'Year']=55
data.loc[data["Year"]==2090,'Year']=60
data.loc[data["Year"]==2095,'Year']=65
data.loc[data["Year"]==2100,'Year']=70
data.loc[data["Year"]==2105,'Year']=75
data.loc[data["Year"]==2109,'Year']=80

# Remove the numbers from the metrics
data['Metric'] = data['Metric'].str.slice(start=2)

# Rename metrics to add spaces
data['Metric'] = data['Metric'].replace({'EmployeeCompensation': 'Employee Compensation', 'PropietorsIncome': "Proprietor's Income",'LaborIncome':'Labor Income','OtherPropertyTypeIncome':'Other Property Type Income','IndirectBusinessTaxes':'Indirect Business Taxes','TotalValueAdded':'Total Value Added'})
data['Industry'] = data['Industry'].replace({'TIPU (Transportation, Information, Power and Utilities)':'TIPU'})
# data.rename(columns={'Year': 'Year '},inplace=True)

# Create lists to hold unique names of Metric, Attribute, and Scenario
scenario = data['Scenario'].unique().tolist()
attribute = data['Attribute'].unique().tolist()
metric = data['Metric'].unique().tolist()

# Create selection options
scenario_selection = st.sidebar.selectbox('Select a Scenario',scenario)
attribute_selection = st.sidebar.selectbox('Select an Attribute',attribute)
metric_seletion = st.sidebar.selectbox('Select a Metric',metric)

data = data[data['Scenario']==scenario_selection]
data = data[data['Attribute']==attribute_selection]
data = data[data['Metric']==metric_seletion]

# Create bar chart
bar_chart = px.bar(data,
                    x = 'Value',
                    y = 'Industry',
                    animation_frame='Year',
                    # color = 'Value',
                    # color_continuous_scale='Blugrn',
                    color_discrete_sequence = ['rgb(14, 166, 223)'],
                    # 14, 166, 223; 7, 90, 120; 0, 127, 113; 122, 197, 67; 247, 227, 208; 243, 110, 33; 156, 28, 74
                    orientation='h',
                    # template='ggplot2',
                    template="seaborn",
                    height=600,
                    width=800)

# Adjust axis limits
bar_chart.update(layout_xaxis_range=[data['Value'].min(),data['Value'].max()+data['Value'].max()/50])

# Change label styles
bar_chart.update_layout(xaxis=dict(title=dict(text="<b>Value</b>",font=dict(color="rgb(7, 90, 120)",size=20))))
bar_chart.update_layout(yaxis=dict(title=dict(text="<b>Industry</b>",font=dict(color="rgb(7, 90, 120)",size=20))))
# bar_chart.update_layout(title='<b>Contributions from Industries across the Life Cycles of CISFs</b>')

bar_chart.update_layout(title={'text': "Contributions from Industries across the Life Cycles of CISFs",
                               'y':0.96,
                               'x':0.55,
                               'xanchor': 'center',
                               'yanchor': 'top',})

bar_chart.update_layout(title_font_color='rgb(7, 90, 120)')
bar_chart.update_layout(title_font_size=24)

st.plotly_chart(bar_chart)

css = """
img {
    min-width: 600px;
}
"""
# Set the CSS style for the page
st.write(f'<style>{css}</style>', unsafe_allow_html=True)

css = """
img {
    object-position: left;
}
"""

# Set the CSS style for the page
st.write(f'<style>{css}</style>', unsafe_allow_html=True)

# Display the images with the desired position

if scenario_selection == 'Large Base Case' or scenario_selection == 'Small Base Case':
    image = 'base.jpg'
elif scenario_selection == 'Large Higher Receipt':
    image = 'higherreceipt.jpg'
elif scenario_selection == 'Large Hold 10' or scenario_selection == 'Small Hold 10':
    image = 'hold10.jpg'
else:
    image = 'holdzero.jpg'

col1, col2, col3 = st.columns([17.7,60,70])

with col1:
    st.write("")

with col2:
    st.image(image,use_column_width=True)

with col3:
    st.write("")
