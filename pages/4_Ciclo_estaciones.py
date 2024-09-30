# ==============================================================
# Author: Jose Luis Amador
# Twitter: @a_josel
# Copyright (c) 2024
# ==============================================================

# Importing libraries
import streamlit as st
import pandas as pd
import folium

from utils.load_data import load_data, dtype, parse_dates
from utils.transforms import transform_popular_stations
from utils.visualization import viz_top10_stations

# Page config
st.set_page_config(
  page_title="Ecobici - Ciclo estaciones",
  page_icon="🚲"
)

# ==============================================================
# Load data
# ==============================================================
path = "agosto-trips.csv.gz"
df = load_data(path, dtype, parse_dates)

path_cicloestaciones = "ciclo_estaciones_cluster.csv.gz"
df_cicloestaciones = pd.read_csv(
  path_cicloestaciones,
  usecols=['name', 'short_name', 'lat', 'lon', 'cluster'],
  compression='gzip'
)

df_popular_stations = transform_popular_stations(df)

mean = df_popular_stations['Frecuencia_Uso'].mean()

st.markdown("# Ecobici - Ciclo estaciones")

st.markdown(
  f"""
  Cada cicloestación es utilizada, en promedio, {mean:.2f} veces al día.
  """
)

st.divider()


# ==============================================================
# Visualization A Top 10 ciclo estaciones por frecuencia de uso
# ==============================================================

# Transform data
df_top10_stations = df_popular_stations.sort_values(by='Frecuencia_Uso', ascending=False).head(10)

# Visualization
st.subheader("(A) Top 10 ciclo estaciones por frecuencia de uso")
vizualization_a = viz_top10_stations(df_top10_stations)
vizualization_a





# ==============================================================
# Visualization B Show a map with the top 10 stations
# ==============================================================

# Transform data
df_top10_stations_map = df_top10_stations.merge(df_cicloestaciones, left_on='Ciclo_Estacion', right_on='short_name')


# Visualization
st.subheader("(B) Visualización de las 10 ciclo estaciones más populares")
map_center = [df_top10_stations_map['lat'].mean(), df_top10_stations_map['lon'].mean()]
my_map = folium.Map(
  location=map_center,
  zoom_start=12,
  tiles='CartoDB Positron'
  )

for index, row in df_top10_stations_map.iterrows():
    folium.Marker(
      [row['lat'], row['lon']],
      popup=row['name'],
      icon=folium.Icon(
        icon='square-parking',
        prefix='fa'
      )
    ).add_to(my_map)

# Convierte el mapa de Folium a un objeto HTML
html_string = my_map.get_root().render()

# Muestra el mapa en Streamlit
st.components.v1.html(html_string, height=500)


# ==============================================================
# Sidebar
# ==============================================================

st.sidebar.markdown(
  f"""
  **(A)** La ciclo estación 271-272 (CE-271-272 Jesús García - Carlos J. Meneses, Buenavista) es
la más popular tanto para retiros como para arribos, lo que la convierte en el principal hub de Ecobici.
  """
)

st.sidebar.markdown(
  f"""
  **(B)** El análisis revela que la mayoría de los usuarios no recorren largas
distancias, sino que tienden a permanecer en áreas cercanas.
  """
)


st.sidebar.markdown("*Reporte actualizado: septiembre 2024.*")

# ==============================================================
# Footer
# ==============================================================

footer = """
  <style>
  footer {
    visibility: hidden;
  }
  .footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #0d1116;
    text-align: center;
    padding: 8px;
    font-size: 12px;
    color: rgb(191, 197, 211);
  }

  .footer a {
    color: rgb(191, 197, 211);
    text-decoration: none;
  } 
  </style>
  <div class="footer">
      <p> Hecho con ❤️ por <a href="https://mx.linkedin.com/in/josel-dev" target="_blank">Jose Luis Amador</a> | México 🇲🇽</p>
  </div>
  """
st.markdown(footer, unsafe_allow_html=True)