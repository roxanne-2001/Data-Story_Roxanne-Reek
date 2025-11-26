
import pandas as pd

#importen van plotly
import plotly.express as px

import plotly.io as pio
pio.renderers.default = "browser"  # opent de grafiek in je standaardbrowser

#zorgt ervoor dat ik de kaart van Nederland kan in laden
import geopandas as gpd

import numpy as np  

import plotly.graph_objects as go  




# eerste CSV bestand
df = pd.read_csv("/Users/roxanne/Desktop/HHS YEAR 3/1. Minor/4. Design /4. Data Story/Dataset/Veiligheidsmonitor.csv")

# --- Figure 1 Header website ----
# --- Originele data ---
data = {
    "Categorie": [
        "Vaak onveilig in eigen buurt",
        "Wel eens onveilig eigen buurt",
        "Wel eens onveilig algemeen",
        "Vaak onveilig algemeen"
    ],
    "Vrouwen": [2.2, 15.0, 2.1, 34.9],
    "Mannen": [2.0, 13.9, 2.0, 33.0],  
    "Leeftijdsgroep": [
        "15 tot 25 jaar",
        "25 tot 45 jaar",
        "45 tot 65 jaar",
        "65 jaar of ouder"
    ]
}

df = pd.DataFrame(data)

# Melt zodat Geslacht in een kolom komt
df_melt = df.melt(
    id_vars=["Categorie", "Leeftijdsgroep"],
    value_vars=["Mannen", "Vrouwen"],
    var_name="Geslacht",
    value_name="Percentage"
)

# Kleur mapping per geslacht
kleur_geslacht = {"Mannen": "#013E6E", "Vrouwen": "#C54F4F"}

# Hover info zonder jaar
df_melt["HoverInfo"] = (
    "Leeftijd: " + df_melt["Leeftijdsgroep"] + "<br>" +
    "Percentage: " + df_melt["Percentage"].astype(str) + "%"
)

# Horizontale staafdiagram
fig = px.bar(
    df_melt,
    x="Percentage",
    y="Categorie",
    orientation='h',
    text="Percentage",
    color="Geslacht",
    color_discrete_map=kleur_geslacht,
    labels={"Percentage": "Percentage (%)", "Categorie": "Categorie"},
    hover_data=["HoverInfo"]
)

fig.update_traces(
    textposition='outside',
    hovertemplate="<b>%{y}</b><br>%{customdata}<extra></extra>",
    customdata=df_melt["HoverInfo"]
)

# Layout
fig.update_layout(
    barmode='group',  # mannen en vrouwen naast elkaar
    title={
        'text': "Veiligheid op straat", 
        'x':0.5,
        'xanchor': 'center',
    },
    title_font=dict(family="Poppins", size=15, color="#333333"),
    font=dict(family="Poppins", size=10, color="#000000"),
    margin=dict(l=100, r=50, t=50, b=50),
    yaxis={'categoryorder':'total ascending'},
    showlegend=True,
    plot_bgcolor="rgba(220, 235, 255, 1)",
    paper_bgcolor="rgba(0,0,0,0)"
)

fig.write_html("onveilig-buur.html", auto_open=True)





#---- Figure 2 Veiligheidsgevoel----

# CSV inladen
df = pd.read_csv("/Users/roxanne/Desktop/HHS YEAR 3/1. Minor/4. Design /4. Data Story/Dataset/Onveiligheid in beurt.csv")


data = {
    "Categorie": [
        "Mannen", "Vrouwen",
        "Homoseksuele mannen", "Homoseksuele vrouwen",
        "Biseksuele mannen", "Biseksuele vrouwen",
        "Heteroseksuele mannen", "Heteroseksuele vrouwen",
        "Aseksuele personen", "Anders", "Weet (nog) niet"
    ],
    "Voelt zich weleens onveilig in buurt (%)": [
        11.9, 18.1, 16, 18.5, 14.1, 23.6, 10.8, 17, 13.9, 19.9, 21.3
    ],
    "Voelt zich weleens onveilig (%)": [
        25.5, 44.1, 36.9, 45.7, 31.2, 58.6, 24.5, 44, 33.4, 46.3, 38.6
    ],
    "Geslacht": [
        "Man", "Vrouw",
        "Man", "Vrouw",
        "Man", "Vrouw",
        "Man", "Vrouw",
        "Neutraal", "Neutraal", "Neutraal"
    ],
    "Leeftijd": [
        "Alle leeftijden", "Alle leeftijden",
        "15-25", "15-25",
        "15-25", "15-25",
        "Alle leeftijden", "Alle leeftijden",
        "Alle leeftijden", "Alle leeftijden", "Alle leeftijden"
    ]
}

df = pd.DataFrame(data)

# Heteroseksuele categorieën verwijderen
df = df[~df["Categorie"].isin(["Heteroseksuele mannen", "Heteroseksuele vrouwen"])]

# Alleen de kolom 'Voelt zich weleens onveilig (%)' behouden
df_long = df.melt(
    id_vars=["Categorie", "Geslacht", "Leeftijd"],
    value_vars=["Voelt zich weleens onveilig (%)"],
    var_name="Type onveiligheid",
    value_name="Percentage"
)

# Plotly Express bar chart (geen facet meer nodig)
fig = px.bar(
    df_long,
    x="Categorie",
    y="Percentage",
    color="Geslacht",
    barmode="group",
    text_auto=True,
    hover_data={"Leeftijd": True, "Type onveiligheid": False, "Geslacht": False},
    labels={"Percentage": "Percentage (%)", "Categorie": "Categorie"},
    title="Voelt zich weleens onveilig",
    color_discrete_map={
        "Man": "#013E6E",
        "Vrouw": "#C54F4F",
        "Neutraal": "#63465F"
    }
)

fig.update_traces(width=1)
fig.update_layout(
    xaxis_tickangle=-45,
    yaxis=dict(range=[0, 65]),
    legend_title_text="Geslacht",
    template="plotly_white",
    bargap=0.25,
    title_font=dict(family="Poppins", size=30, color="#013E6E"),
    font=dict(family="Poppins", size=15, color="#000000")
)

# Exporteren naar HTML
fig.write_html("grafiek.html", auto_open=True)





#------ Figure 3 Cijfers over discussie / meningen -- invloed media -----
# -----------------------------
# Data
# -----------------------------
data = {
    "Meningen": [
        "Mannen die vinden dat vrouwen overdrijven",
        "Vrouwen die vinden dat #MeToo- discussie oplevert",
        "Mannen die vinden dat de discussies te ver gaan.",
        "Vrouwen die zich onveilig voelen op stations",
        "Vrouwen die zich onveilig voelen in het OV"
    ],
    "Percentage": ["43%", "51%", "37%", "90%", "82%"],
    "Categorie": ["Man", "Vrouw", "Man", "Vrouw", "Vrouw"],
    "Leeftijdsgroep": ["25-45", "25-45", "45+", "15-25", "15-25"],
    "Bron": ["NOS", "NOS", "RTL Nieuws", "CBS", "CBS"]
}

# DataFrame voorbereiden
df = pd.DataFrame(data)
df["Percentage_int"] = df["Percentage"].str.replace("%", "").astype(int)
df["text_label"] = df["Percentage"]

# Kleur per categorie
kleuren = {"Man": "#013E6E", "Vrouw": "#C54F4F"}

# -----------------------------
# Scatter plot maken
# -----------------------------
fig = px.scatter(
    df,
    x="Percentage_int",
    y="Meningen",
    size="Percentage_int",
    color="Categorie",
    text="text_label",
    hover_data=["Categorie", "Leeftijdsgroep", "Percentage", "Bron"],
    color_discrete_map=kleuren,
    title="Meningen en Discussie door media invloed",
    size_max=60
)

# Marker instellingen
fig.update_traces(
    marker=dict(
        symbol="circle",
        sizemode='area',
        sizeref=2.*max(df['Percentage_int'])/(60.**2),
        sizemin=5
    ),
    textposition="middle center"
)

# -----------------------------
# Layout aanpassen
# -----------------------------
fig.update_layout(
    title_font=dict(family="Poppins", size=16, color="#000000"),
    font=dict(family="Poppins", size=11, color="#000000"),
    xaxis_title="Percentage (%)",
    yaxis_title="Meningen",
    plot_bgcolor="rgba(220, 235, 255, 1)",
    paper_bgcolor="rgba(0,0,0,0)",
    legend_title_text="Categorie"
)

# -----------------------------
# Opslaan en openen
# -----------------------------
fig.write_html("discussie-meningen.html", auto_open=True)




#------- Figure 4 Online veiligheid ------

# ==== 1. CSV inladen ====
df = pd.read_csv("/Users/roxanne/Desktop/HHS YEAR 3/1. Minor/4. Design /4. Data Story/Dataset/Online criminaliteit.csv")

# ==== 2. Komma's vervangen door punten en naar float ====
value_cols = df.columns[3:]  # alle kolommen met percentages
for col in value_cols:
    df[col] = df[col].astype(str).str.replace(",", ".")
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ==== 3. Filter rijen op Leeftijd en maak kopie (veilig tegen SettingWithCopyWarning) ====
df_leeftijd = df[df["Kenmerken "].str.contains("Leeftijd:")].copy()

# ==== 4. Leeftijdsgroep kolom aanmaken ====
df_leeftijd["Leeftijdsgroep"] = df_leeftijd["Kenmerken "].apply(lambda x: x.split(":")[1].strip())

# ==== 5. Filter op de belangrijkste categorieën ====
belangrijke_categorieen = [
    "Online criminaliteit Totaal slachtoffers (%)",
    "Online oplichting en fraude Totaal slachtoffers (%)",
    "Hacken Totaal slachtoffers (%)",
    "Online bedreiging en intimidatie Totaal slachtoffers (%)"
]

df_leeftijd_long = pd.melt(
    df_leeftijd,
    id_vars=["Leeftijdsgroep"],
    value_vars=belangrijke_categorieen,
    var_name="Categorie",
    value_name="Percentage"
)

# ==== 6. Labels maken ====
df_leeftijd_long["Label"] = df_leeftijd_long["Percentage"].apply(
    lambda x: f"{x}%" if pd.notna(x) else "geen data beschikbaar"
)

# ==== 7. Kleuren instellen per categorie ====
kleuren = {
    "Online criminaliteit Totaal slachtoffers (%)": "#013E6E",
    "Online oplichting en fraude Totaal slachtoffers (%)": "#C54F4F",
    "Hacken Totaal slachtoffers (%)": "#63465F",
    "Online bedreiging en intimidatie Totaal slachtoffers (%)": "#FF9696"
}

# ==== 8. Bar chart maken ====
fig = px.bar(
    df_leeftijd_long,
    x="Percentage",
    y="Categorie",
    color="Categorie",
    color_discrete_map=kleuren,
    facet_col="Leeftijdsgroep",  # Facet per leeftijdsgroep
    barmode="group",
    text="Label",
    title="Online criminaliteit (CBS 2023)"
)

fig.update_traces(textposition="outside")
fig.update_layout(
    title_font=dict(family="Poppins", size=20, color="#000000"),
    font=dict(family="Poppins", size=12, color="#000000"),
    plot_bgcolor="rgba(220, 235, 255, 1)",
    paper_bgcolor="rgba(0,0,0,0)"
)

# ==== 9. Grafiek opslaan en openen ====
fig.write_html("online_criminaliteit_leeftijd.html", auto_open=True)






# ------- Figure 5 kaart van Nederland onveiligheid ------

# ------- Figure 5 kaart van Nederland onveiligheid ------

# --- 1. Inladen eerste dataset: Onveiligheidsgevoelens ---
df_onveilig = pd.read_csv(
    "/Users/roxanne/Desktop/HHS YEAR 3/1. Minor/4. Design /4. Data Story/Dataset/Onveiligheidsgevoelens.csv",
    names=['region', '2023 (% weleens)', '2021 (% weleens)'],
    header=0
)
df_onveilig.columns = df_onveilig.columns.str.strip()

# --- 2. Inladen tweede dataset: Gemeentes ---
bestand_gemeentes = "/Users/roxanne/Desktop/HHS YEAR 3/1. Minor/4. Design /4. Data Story/Dataset/gemeentes.csv.xls"
df_gemeentes = pd.read_csv(bestand_gemeentes)
df_gemeentes.columns = df_gemeentes.columns.str.strip()

# --- 3. Mapping regio -> provincie ---
mapping = {
    "Amsterdam": "Noord-Holland",
    "Rotterdam": "Zuid-Holland",
    "Den Haag": "Zuid-Holland",
    "Zeeland-West-Brabant": "Zeeland",
    "Midden-Nederland": "Utrecht",
    "Oost-Brabant": "Noord-Brabant",
    "Noord-Nederland": "Groningen",
    "Oost-Nederland": "Overijssel"
}
df_onveilig['provincie'] = df_onveilig['region'].replace(mapping)

# --- 4. Kolommen omzetten naar numeriek ---
df_onveilig['2023 (% weleens)'] = pd.to_numeric(
    df_onveilig['2023 (% weleens)'].str.replace(',', '.'),
    errors='coerce'
)
df_onveilig['2021 (% weleens)'] = pd.to_numeric(
    df_onveilig['2021 (% weleens)'].str.replace(',', '.'),
    errors='coerce'
)

# --- 5. Gemiddelde per provincie ---
df_grouped = df_onveilig.groupby('provincie')[['2023 (% weleens)', '2021 (% weleens)']].mean().reset_index()

# --- 6. GeoJSON inladen ---
gdf = gpd.read_file("/Users/roxanne/Desktop/HHS YEAR 3/1. Minor/4. Design /4. Data Story/Dataset/provincie_2025.geojson")

# --- 7. Merge data met geodata ---
merged = gdf.merge(df_grouped, left_on='statnaam', right_on='provincie', how='left')
merged['2023 (% weleens)'] = merged['2023 (% weleens)'].fillna(0)

# --- 8. Choropleth kaart maken (Nederland lichtgrijs) ---
fig = px.choropleth_mapbox(
    merged,
    geojson=merged.geometry,
    locations=merged.index,
    color_discrete_sequence=["lightgrey"],  # hele Nederland lichtgrijs
    hover_name='statnaam',
    opacity=0.5
)

# --- 9. Grootste steden selecteren ---
steden = [
    "Alkmaar", "Amsterdam", "Groningen", "Heemskerk",
    "Leiden", "Maastricht", "Rotterdam", "'s-Hertogenbosch",
    "'s-Gravenhage", "Tilburg"
]
df_steden = df_gemeentes[df_gemeentes['municipality'].isin(steden)].drop_duplicates(subset=['municipality']).copy()

# Zorg dat de volgorde exact overeenkomt
df_steden['municipality'] = pd.Categorical(df_steden['municipality'], categories=steden, ordered=True)
df_steden = df_steden.sort_values('municipality').reset_index(drop=True)

# Voeg crime-waarden toe
crime_waarden = [8, 16, 120, 135, 182, 199, 271, 281, 280, 308]
df_steden['crime'] = crime_waarden

# --- Vaste grootte voor markers zodat alle steden zichtbaar zijn ---
df_steden['marker_size'] = 20

# --- 10. Scatterlaag met blauwe gradient en aangepaste hover ---
scatter_traces = go.Scattermapbox(
    lat=df_steden['latitude'],
    lon=df_steden['longitude'],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=20,
        color=df_steden['crime'],
        colorscale=[
            "#BFD7EA",  # Laag
            "#7BAEDC",  # Matig
            "#336699",  # Hoog
            "#013E6E"   # Zeer hoog
        ],
        cmin=df_steden['crime'].min(),
        cmax=df_steden['crime'].max(),
        colorbar=dict(
            title="Aantal crime",
            tickvals=[10, 100, 200, 300],
            ticktext=["Laag", "Matig", "Hoog", "Zeer hoog"]
        )
    ),
    hovertemplate="<b>%{customdata[0]}</b><br>Crime: %{customdata[1]}<extra></extra>",
    customdata=df_steden[['municipality','crime']].values
)

# --- 11. Voeg de scatterlaag toe aan de choropleth ---
fig.add_trace(scatter_traces)

# --- 12. Layout met duidelijke kleurenlegenda ---
fig.update_layout(
    title="Crime in de grootste steden van Nederland",
    mapbox_zoom=6,
    mapbox_center={"lat": 52.2, "lon": 5.3},
    margin={"r":0, "t":40, "l":0, "b":0},
    mapbox_style="carto-positron"
)

# --- 13. Export naar HTML ---
fig.write_html("Nederland.html", auto_open=True)



