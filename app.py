%%writefile app.py
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_jupyter import StreamlitPatcher,tqdm
sp=StreamlitPatcher()
import sqlalchemy
import warnings
warnings.filterwarnings('ignore')
import plotly.io as pio
pio.templates.default='plotly'
pio.renderers.default='notebook'
import textwrap
import ipywidgets as widgets
from ipywidgets import interact, interact_manual
import IPython.display
from IPython.display import display, clear_output
import plotly.graph_objects as go
from ipywidgets import Layout,Box,Dropdown,Label
#pull data from mysql
engine=sqlalchemy.create_engine('mysql+pymysql://root:root@localhost:3306/new_schema')
df_2019=pd.read_sql_table('constituency_wise_results_2019',engine)
df_2019['voterturnout_ratio']=(df_2019['total_votes']/df_2019['total_electors'])*100
df_2014=pd.read_sql_table('2014',engine)
df_2014['voterturnout_ratio']=(df_2014['total_votes']/df_2014['total_electors'])*100
df_2014['year']=2014
df_2019['year']=2019
df2014_vs_2019=pd.concat([df_2019,df_2014],axis=0)
#extract state who won in 2014 and 2019 and givning rank
df=pd.read_sql_query('select distinct(m.state),m.party,m.candidate,m.sex,m.max_voter_turnout_ratio, rank()over( order by m.max_voter_turnout_ratio desc) as party_rank from(select  state,party,candidate,sex,max((total_votes/total_electors)*100) as max_voter_turnout_ratio from new_schema.2014  group by state,party,candidate,sex)m order by party_rank ',engine)
df['year']=2014
df2014=df.copy()
df1=pd.read_sql_query('select distinct(m.state),m.party,m.sex,m.candidate,m.max_voter_turnout_ratio, rank()over( order by m.max_voter_turnout_ratio desc) as party_rank from (select  state,party,candidate,sex,max((total_votes/total_electors)*100) as max_voter_turnout_ratio from new_schema.constituency_wise_results_2019  group by state,party,candidate,sex)m order by party_rank ',engine)
df1['year']=2019
df2019=df1.copy()
#above code will give me maximum voter turnout ration for state,gender,party etc.below code will give me who will won in particular state
#so this two code part I juse use to extract winning data

df2=df2014.drop_duplicates(subset=['state'])
df2.reset_index(inplace=True)
df2.drop(columns=['index'],inplace=True)

df19=df2019.drop_duplicates(subset=['state'])
df19.reset_index(inplace=True)
df19.drop(columns=['index'],inplace=True)

df14_19=pd.concat([df19,df2],axis=0)

st.set_page_config(page_title='Election Dashbard',
                   page_icon=':bar chart:',
                   layout='wide'
)

import base64
# Function to convert image to base64
def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Path to your local image
import base64
import os

# Get the base64 string of the image
def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Path to your local image
 # Ensure this path is correct

# Check if the image file exists
background_image_path = "C://Users//Dell//Downloads\\istockphoto-1140760252-612x612.jpg"

if not os.path.isfile(background_image_path):
    st.error(f"Image file not found: {background_image_path}")
else:
    # Get the base64 string of the image
    base64_image = get_base64_encoded_image(background_image_path)

    # Define the CSS for the background image
    background_css = f"""
    <style>
    body {{
        background-image: url("data:image/jpg;base64,{base64_image}");
        background-size: cover;
        background-image: url("data:image/jpg;base64,{base64_image}");
        background-repeat: not repeat;
        background-attachment: fixed;
        background-position: center;
        background-color: white;
        z-index: -1;
    }}
    .stApp {{
        background: none; /* Remove any other background to ensure visibility */
    }}
     .title, .header, .subheader, .kpi {{
        color: black; /* Change text color to be visible */
        background-color: rgba(255, 255, 255, 0.7); /* Semi-transparent background */
        padding: 10px; /* Add padding for better readability */
        border-radius: 10px; /* Rounded corners */
        display: inline-block; /* Ensure it doesn't take full width */
    }}
    .kpi-container {{
        display: flex;
        justify-content: space-around;
    }}rder-radius: 10px; /* Rounded corners */
    }}
    </style>
    """
content_css = """
<style>
main .block-container {
    position: relative;
    z-index: 1;
}
header, .css-1v3fvcr {
    position: relative;
    z-index: 1;
}
</style>
"""

# Inject the CSS into the Streamlit app
st.markdown(background_css + content_css, unsafe_allow_html=True)
#
st.title('indian election for 2019 and 2014 Dashboard')
st.markdown('##')



left_column,middle_column,right_column=st.columns([1,1,1])
with left_column:
    
    year = st.selectbox('Select Year', df2014_vs_2019['year'].unique())
    state= st.selectbox('Select State', df2014_vs_2019['state'].unique())

    # Filter data based on selections
    df = df2014_vs_2019[(df2014_vs_2019['year'] == year) & (df2014_vs_2019['state'] == state)]
    avg_voterturnout_ratio=int(df['voterturnout_ratio'].mean())
    st.subheader('avg_voterturnout_ratio')
    st.subheader(f"% {avg_voterturnout_ratio:,}"
)
with right_column:
    total_electors=int(df['total_electors'].sum())
    st.subheader('total_electors')
    st.subheader(f" {total_electors:,}"
)
with middle_column:
    total_votes=int(df['total_votes'].sum())
    st.subheader('total_casted_votes',color='blue')
    st.subheader(f" {total_votes:,}"
)

main_col1, other_col2 = st.columns([2,1])
with main_col1:
    
    
    fig5= px.bar(df, x='party', y='total_votes',title='votes split at national level')
    

# Display Plotly figure
    st.plotly_chart(fig5)
    turnout = df['total_votes'].values[0] if not df.empty else None
    if turnout:
        st.write(f'total casted votes in {state} for {year}: {turnout}')
    else:
        st.write('No data available for the selected year and state.')
with other_col2:
    
    fig6= px.bar(df, x='pc_name', y='total_votes',title='votes split at state level')
    st.plotly_chart(fig6)
    st.markdown("""---""")

df=df14_19.copy()

# plotly table setup
main_col3, other_col3,other_col4 = st.columns([1,1,1])
with main_col3:
    
    st.write("winning party table:")
    table_year = st.selectbox('Select Year for Table', df14_19['year'].unique(), key='table_year')

    # Filter data for the selected year for the table
    table_data = df14_19[df14_19['year'] == table_year]

    # Display the table
    st.dataframe(table_data)
     

# update layout with buttons, and show the figure

with other_col3:
    df_repeat=df14_19[df14_19.duplicated(subset=['state','party'],keep=False)] 
    df_repeat.drop(columns=['party_rank'],inplace=True)
    df_repeat['party_rank']=df_repeat['max_voter_turnout_ratio'].rank(ascending=False,method='first')
    df=df_repeat.copy()


    hj=df_repeat.groupby(['state','year'])['max_voter_turnout_ratio'].mean().reset_index()
    result = df_repeat.groupby('year')['state'].unique().reset_index()
    result = result.explode('state')
    df = pd.merge(hj, result, on=['year', 'state'], how='inner')
# Explode the list of states into separate rows
    

    df_filtered = df[df['year'].isin([2014, 2019])]

# Pivoting the DataFrame to have separate columns for 2014 and 2019
    df_pivot = df_filtered.pivot(index='state', columns='year', values='max_voter_turnout_ratio').reset_index()
    

# Renaming columns for clarity
    df_pivot.columns = ['state', 'value_2014', 'value_2019']
    df_pivot['gain/loss']=df_pivot['value_2019']-df_pivot['value_2014']
    st.write("party gain/loss who came in two consucative years:")
    
    

    # Display the table
    st.dataframe(df_pivot)
     

    # Display the table
    
     


with other_col4:
    engine=sqlalchemy.create_engine('mysql+pymysql://root:root@localhost:3306/new_schema')
    df2019m=pd.read_sql_query('with cte as (select distinct(m.state),m.party,m.candidate,m.sex,m.max_voter_turnout_ratio, rank()over(partition by state order by m.max_voter_turnout_ratio desc) as party_rank from (select  state,party,candidate,sex,max((total_votes/total_electors)*100) as max_voter_turnout_ratio from new_schema.constituency_wise_results_2019  group by state,party,candidate,sex)m order by party_rank) select * from cte where party_rank<3 ',engine)
    dfwin19=df2019m[['state','party','candidate','max_voter_turnout_ratio']][df2019m['party_rank']==1]
    dfrun19=df2019m[['state','party','candidate','max_voter_turnout_ratio']][df2019m['party_rank']==2]
    dfwin19.rename(columns = {'party':'party1','candidate':'candidate1','max_voter_turnout_ratio':'max_voter_turnout_ratio1'},inplace=True)
    df_win_run19=pd.merge(dfwin19,dfrun19,on='state',how='outer')
    df_win_run19['margin_between_winner&runnuerup']=(df_win_run19['max_voter_turnout_ratio1']-df_win_run19['max_voter_turnout_ratio']).round(3)
    df2014m=pd.read_sql_query('with cte as (select distinct(m.state),m.party,m.candidate,m.sex,m.max_voter_turnout_ratio, rank()over(partition by state order by m.max_voter_turnout_ratio desc) as party_rank from (select  state,party,candidate,sex,max((total_votes/total_electors)*100) as max_voter_turnout_ratio from new_schema.2014  group by state,party,candidate,sex)m order by party_rank) select * from cte where party_rank<3 ',engine)

    dfwin14=df2014m[['state','party','candidate','max_voter_turnout_ratio']][df2014m['party_rank']==1]
    dfrun14=df2014m[['state','party','candidate','max_voter_turnout_ratio']][df2014m['party_rank']==2]
    dfwin14.rename(columns = {'party':'party1','candidate':'candidate1','max_voter_turnout_ratio':'max_voter_turnout_ratio1'},inplace=True)
    df_win_run14=pd.merge(dfwin14,dfrun14,on='state',how='outer')
    df_win_run14['margin_between_winner&runnuerup']=(df_win_run14['max_voter_turnout_ratio1']-df_win_run14['max_voter_turnout_ratio']).round(3)

    df_win_run19['year']=2019
    df_win_run14['year']=2014
    df_margin=pd.concat([df_win_run19,df_win_run14],axis=0)
    df_margin['margin_rank']=df_margin['margin_between_winner&runnuerup'].rank(ascending=False,method='first')
    df_margin.sort_values('margin_rank',inplace=True)
    df=df_margin.copy()
  
    st.write("table for winner and runnuerup with margin diffrent:")
    table_year2 = st.selectbox('Select Year for Table', df['year'].unique(), key='table_year2')

    # Filter data for the selected year for the table
    table_data2 = df[df['year'] == table_year2]

    # Display the table
    st.dataframe(table_data2)
    # Display the table
   
    


main_col, other_col1 = st.columns([2,1]) 
with main_col:
    engine=sqlalchemy.create_engine('mysql+pymysql://root:root@localhost:3306/new_schema')
    df=pd.read_sql_query('select distinct(m.state),m.party,m.candidate,m.sex,m.max_voter_turnout_ratio, rank()over( order by m.max_voter_turnout_ratio desc) as party_rank from(select  state,party,candidate,sex,max((total_votes/total_electors)*100) as max_voter_turnout_ratio from new_schema.2014  group by state,party,candidate,sex)m order by party_rank ',engine)
    df['year']=2014
    df2014=df.copy()
    df1=pd.read_sql_query('select distinct(m.state),m.party,m.sex,m.candidate,m.max_voter_turnout_ratio, rank()over( order by m.max_voter_turnout_ratio desc) as party_rank from (select  state,party,candidate,sex,max((total_votes/total_electors)*100) as max_voter_turnout_ratio from new_schema.constituency_wise_results_2019  group by state,party,candidate,sex)m order by party_rank ',engine)
    df1['year']=2019
    df2019=df1.copy()
#above code will give me maximum voter turnout ration for state,gender,party etc.below code will give me who will won in particular state
#so this two code part I juse use to extract winning data

    df2=df2014.drop_duplicates(subset=['state'])
    df2.reset_index(inplace=True)
    df2.drop(columns=['index'],inplace=True)

    df19=df2019.drop_duplicates(subset=['state'])
    df19.reset_index(inplace=True)
    df19.drop(columns=['index'],inplace=True)
    df14_19=pd.concat([df19,df2],axis=0)
    df_nrepeat=df14_19.drop_duplicates(subset=['state','party'],keep=False)
    df_nrepeat.drop(columns=['party_rank'],inplace=True)
    df_nrepeat['party_rank']=df_nrepeat['max_voter_turnout_ratio'].rank(ascending=False,method='first')
    df_nrepeat.sort_values('party_rank',inplace=True)
    df_nrepeat_10=df_nrepeat.nlargest(10,'max_voter_turnout_ratio') 
    df = df_nrepeat.copy()
# Streamlit UI components


    year = st.selectbox('Select Year', df['year'].unique())


# Filter data based on selections
    filtered_df = df[df['year'] == year]

# Create Plotly figure
    fig4= px.bar(filtered_df, x='state', y='max_voter_turnout_ratio',color='party',title='not repeated party for two consucative year')

# Display Plotly figure
    st.plotly_chart(fig4)
    turnout = filtered_df['max_voter_turnout_ratio'].values[0] if not filtered_df.empty else None
    if turnout:
        st.write(f'Voter Turnout for not repeated party based on {year}: {turnout}%')
    else:
        st.write('No data available for the selected year and state.')
with other_col1:
    dft=df14_19[(df14_19['party']=='BJP')|(df14_19['party']=='INC')]
    df=dft.copy()
    party= st.selectbox('Select party', df['party'].unique())
    year= st.selectbox('Select year', df['year'].unique())
    filtered_df = df[(df['year'] == year) & (df['party'] == party)]
    fig5= px.bar(filtered_df, x='state', y='max_voter_turnout_ratio',title='two major party details')

# Display Plotly figure
    st.plotly_chart(fig5)
    turnout = filtered_df['max_voter_turnout_ratio'].values[0] if not filtered_df.empty else None
    if turnout:
        st.write(f' {party} voter_turnout on {year} : {turnout}%')
    else:
        st.write('No data available for the selected year and state.')


# Display Plotly figure
  



# Function to update the plot


# Use ipywidgets.interactive to create an interactive plot






hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
