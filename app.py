import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# ✅ Load your real CSVs
matches_df = pd.read_csv('matches.csv')
batting_df = pd.read_csv('batting_stats.csv')
bowling_df = pd.read_csv('bowling_stats.csv')

# ✅ Clean up
matches_df['Date_of_match'] = pd.to_datetime(matches_df['Date_of_match'], dayfirst=True)

# Remove trailing spaces
batting_df['Batsman'] = batting_df['Batsman'].astype(str).str.strip()
bowling_df['Bowler'] = bowling_df['Bowler'].astype(str).str.strip()

# ✅ Create app
app = dash.Dash(__name__)
server = app.server

# ✅ Layout
app.layout = html.Div([
    html.H1("🏏 ICC Cricket World Cup Dashboard"),

    html.H2("📅 Matches Overview"),
    html.Label("Select Team:"),
    dcc.Dropdown(
        id='team-dropdown',
        options=[{'label': t, 'value': t} for t in sorted(matches_df['Team_1'].dropna().unique())],
        value=matches_df['Team_1'].dropna().unique()[0]
    ),
    dcc.Graph(id='matches-graph'),

    html.H2("🏏 Batting Stats"),
    html.Label("Select Batsman:"),
    dcc.Dropdown(
        id='batsman-dropdown',
        options=[{'label': b, 'value': b} for b in sorted(batting_df['Batsman'].dropna().unique())],
        value=batting_df['Batsman'].dropna().unique()[0]
    ),
    dcc.Graph(id='batting-graph'),

    html.H2("🎯 Bowling Stats"),
    html.Label("Select Bowler:"),
    dcc.Dropdown(
        id='bowler-dropdown',
        options=[{'label': b, 'value': b} for b in sorted(bowling_df['Bowler'].dropna().unique())],
        value=bowling_df['Bowler'].dropna().unique()[0]
    ),
    dcc.Graph(id='bowling-graph')
])

# ✅ Matches callback
@app.callback(
    Output('matches-graph', 'figure'),
    Input('team-dropdown', 'value')
)
def update_matches(team):
    df = matches_df[(matches_df['Team_1'] == team) | (matches_df['Team_2'] == team)].copy()
    df['Year'] = df['Date_of_match'].dt.year
    fig = px.histogram(df, x='Venue_city', color='Winning_team',
                       title=f'Match Results by City for {team}')
    return fig

# ✅ Batting callback
@app.callback(
    Output('batting-graph', 'figure'),
    Input('batsman-dropdown', 'value')
)
def update_batting(batsman):
    batsman = str(batsman).strip()
    df = batting_df[batting_df['Batsman'] == batsman]

    if df.empty:
        fig = px.bar(
            x=['Metric'],
            y=[0],
            title=f'No data for {batsman}'
        )
    else:
        metrics = ['Runs', 'Strike_rate', 'Fours', 'Sixes']
        values = [
            df['Runs'].iloc[0] if 'Runs' in df.columns else 0,
            df['Strike_rate'].iloc[0] if 'Strike_rate' in df.columns else 0,
            df['Fours'].iloc[0] if 'Fours' in df.columns else 0,
            df['Sixes'].iloc[0] if 'Sixes' in df.columns else 0
        ]

        fig = px.bar(
            x=metrics,
            y=values,
            labels={'x': 'Metric', 'y': 'Value'},
            title=f'Performance of {batsman}'
        )

    return fig

# ✅ Bowling callback
@app.callback(
    Output('bowling-graph', 'figure'),
    Input('bowler-dropdown', 'value')
)
def update_bowling(bowler):
    bowler = str(bowler).strip()
    df = bowling_df[bowling_df['Bowler'] == bowler]

    if df.empty:
        fig = px.bar(
            x=['Metric'],
            y=[0],
            title=f'No data for {bowler}'
        )
    else:
        metrics = ['Wickets', 'Economy', 'Runs']
        values = [
            df['Wickets'].iloc[0] if 'Wickets' in df.columns else 0,
            df['Economy'].iloc[0] if 'Economy' in df.columns else 0,
            df['Runs'].iloc[0] if 'Runs' in df.columns else 0
        ]

        fig = px.bar(
            x=metrics,
            y=values,
            labels={'x': 'Metric', 'y': 'Value'},
            title=f'Performance of {bowler}'
        )

    return fig

# ✅ Run server
if __name__ == '__main__':
    app.run(debug=True)
