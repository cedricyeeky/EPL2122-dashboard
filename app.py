import streamlit as st
import pandas as pd
import plost

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

st.sidebar.header('English Premier League `2021 - 2022`')

st.sidebar.subheader('Choose your favourite team')
team_selection = st.sidebar.selectbox('Team', ('Arsenal', 'Aston Villa', 'Brentford', 'Brighton', 'Burnley', 'Chelsea', 'Crystal Palace', 'Everton',
                                               'Leeds', 'Leicester', 'Liverpool', 'Man City', 'Man United', 
                                               'Newcastle', 'Norwich', 'Southampton', 'Tottenham', 'Watford', 'West Ham', 'Wolves')) 

# st.sidebar.subheader('Donut chart parameter')
# donut_theta = st.sidebar.selectbox('Select data', ('q2', 'q3'))

st.sidebar.subheader('Line chart parameters')
plot_data = st.sidebar.multiselect('Select data', ['Home Goals', 'Away Goals', 'Home Conceded Goals', 'Away Conceded Goals'], 
                                   ['Home Goals', 'Away Goals', 'Home Conceded Goals', 'Away Conceded Goals'])
plot_height = st.sidebar.slider('Specify plot height', 200, 500, 250)

st.sidebar.markdown('''
---
Created with ❤️ by Cedric Yee.
''')

df = pd.read_csv('2021-2022.csv')

# Convert the 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

table = pd.DataFrame(list(df.HomeTeam.unique()),columns = ['Team'])
table[['Played','Win','Draw','Loss','GF','GA','GD','Points']] = 0
table = table.set_index('Team')
for i in df.index:
    home = df.HomeTeam.loc[i]
    away = df.AwayTeam.loc[i]
    table.loc[home,'Played'] += 1
    table.loc[away,'Played'] += 1
    table.loc[home,'GF'] += df.FTHG.loc[i]
    table.loc[away,'GF'] += df.FTAG.loc[i]
    table.loc[home,'GA'] += df.FTAG.loc[i]
    table.loc[away,'GA'] += df.FTHG.loc[i]
    if df.loc[i,'FTR'] == "H":
        table.loc[home,'Win'] += 1
        table.loc[away,'Loss'] += 1
    elif df.loc[i,'FTR'] == "A":
        table.loc[away,'Win'] += 1
        table.loc[home,'Loss'] += 1
    else:
        table.loc[away,'Draw'] += 1
        table.loc[home,'Draw'] += 1
table['Points'] = 3*table['Win'] + table['Draw']
table['GD'] = table['GF'] - table['GA']

# Adding the ranking column
table['Rank'] = table['Points'].rank(ascending=False, method='min')

table = table.sort_values(by='Points', ascending=False)
table = table.reset_index()
 
st.markdown('### EPL Table')
st.dataframe(table, use_container_width=True)

st.markdown(f"### {team_selection}'s 2021-2022 EPL Season")

team_sel_home = df[df['HomeTeam']==team_selection]
team_sel_away = df[df['AwayTeam']==team_selection]
team_sel_records = pd.concat([team_sel_home,team_sel_away], ignore_index=True)
team_sel_records = team_sel_records.sort_values(by='Date')

# Get selected team's points over time
team_sel_records['Points'] = team_sel_records.apply(lambda row: 3 if row['FTR'] == 'H' and row['HomeTeam'] == team_selection 
                                       else (3 if row['FTR'] == 'A' and row['AwayTeam'] == team_selection else 
                                             (1 if row['FTR'] == 'D' else 0)), axis=1)
# Group by date and sum the points
team_points_over_time = team_sel_records.groupby('Date')['Points'].sum().reset_index()
team_points_over_time['Cumulative Points'] = team_points_over_time['Points'].cumsum()

# Display line chart of points over time
st.markdown('### Points Over Time')
st.line_chart(team_points_over_time.set_index('Date')[['Cumulative Points']], height=500)

st.dataframe(team_sel_records, use_container_width=True)





