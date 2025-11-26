import pandas as pd

#importen van plotly
import plotly.express as px

import plotly.io as pio
pio.renderers.default = "browser"  # opent de grafiek in je standaardbrowser

import numpy as np  # <- Zorg dat dit erbij staat


#---- figure 6 ----- meldings bereidheid 

df = pd.read_csv("/Users/roxanne/Desktop/HHS YEAR 3/1. Minor/4. Design /4. Data Story/Dataset/municipality.csv")

# ==== 2. Kolommen bekijken ====
print("Kolommen:", df.columns.tolist())
print("Aantal rijen:", len(df))

# ==== 3. Datum omzetten naar datetime + jaar toevoegen ====
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['year'] = df['date'].dt.year

# ==== 4. Controleren welke jaren beschikbaar zijn ====
available_years = df['year'].dropna().unique()
print("Beschikbare jaren:", sorted(available_years))

if len(available_years) == 0:
    raise ValueError("Geen geldige datums gevonden in de kolom 'date'.")

# ==== 5. Automatisch meest recente jaar selecteren ====
latest_year = int(df['year'].max())
print(f"Gebruik meest recente jaar: {latest_year}")

# ==== 6. Numerieke kolommen ====
numeric_cols = ['registered_crimes', 'pressed_charges', 'pressed_charges_online']

# Controleren of deze kolommen bestaan
for col in numeric_cols:
    if col not in df.columns:
        raise KeyError(f"Kolom '{col}' ontbreekt in de dataset.")

# ==== 7. Data filteren + groeperen ====
df_latest = (
    df[df['year'] == latest_year]
    .groupby('region')[numeric_cols]
    .sum()
    .reset_index()
)

# Als het gefilterde jaar geen data heeft, foutmelding
if df_latest.empty:
    raise ValueError(f"Geen data gevonden voor het jaar {latest_year}.")

# ==== 8. Missende waarden opvullen ====
df_latest[numeric_cols] = df_latest[numeric_cols].fillna(0)

# ==== 9. Totale aantallen berekenen ====
total_registered = df_latest['registered_crimes'].sum()
total_pressed = df_latest['pressed_charges'].sum()
total_online = df_latest['pressed_charges_online'].sum()

# ==== 10. DataFrame voor donut-grafiek ====
df_donut = pd.DataFrame({
    'Categorie': ['Geregistreerde misdrijven', 'Niet vervolgd', 'Online vervolgd'],
    'Aantal': [
        total_registered,
        max(total_registered - total_pressed, 0),  # voorkomt negatieve waarde
        total_online
    ]
})

# ==== 11. Plotly Donut Chart ====
fig = px.pie(
    df_donut,
    names='Categorie',
    values='Aantal',
    hole=0.5,
    color='Categorie',
    color_discrete_map={
        'Geregistreerde misdrijven': '#013E6E',  
        'Niet vervolgd': 'C54F4F',              
        'Online vervolgd': '#63465F'            
    },
    title='Misdrijven en vervolging in {latest_year}',
)

# ==== 12. Layout & Hover Info ====
fig.update_traces(
    textinfo='percent+label',
    hovertemplate='%{label}<br>Aantal: %{value}<br>Percentage: %{percent}'
)

fig.update_layout(
    title={
        'text': f"Geregistreerde misdrijven en vervolging in {latest_year}",
        'x': 0.5,
        'xanchor': 'center'
    },
    font=dict(family="Poppins", size=8, color="#000000"),
    plot_bgcolor="rgba(220, 235, 255, 1)",
    paper_bgcolor="rgba(0,0,0,0)",
    legend=dict(
        orientation='h',   # horizontaal
        y=-0.1,            # positie onder de grafiek
        x=0.5,             # horizontaal gecentreerd
        xanchor='center',
        yanchor='top'
    )
)


fig.write_html("Donut_Misdrijven.html", auto_open=True)



# ---- Line chart: trends per jaar ---- figure 7 
df_yearly = df.groupby('year')[numeric_cols].sum().reset_index()

fig_line = px.line(
    df_yearly,
    x='year',
    y=numeric_cols,
    markers=True,
    labels={
        'value':'Aantal misdrijven / vervolgingen',
        'year':'Jaar',
        'variable':'Categorie'
    },
    title='Trends in criminaliteit en vervolging in Nederland'
)

# Kleuren instellen
fig_line.update_traces(selector=dict(name='registered_crimes'), line=dict(color='#853131'))
fig_line.update_traces(selector=dict(name='pressed_charges'), line=dict(color='#FF9696'))
fig_line.update_traces(selector=dict(name='pressed_charges_online'), line=dict(color='#F36969'))

fig_line.update_layout(
    xaxis=dict(dtick=1),
    yaxis=dict(rangemode='tozero'),
    legend_title_text='Categorie',
    plot_bgcolor="rgba(220, 235, 255, 1)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Poppins", size=12, color="#000000")
)

fig_line.write_html("Linechart_Criminaliteit.html", auto_open=True)