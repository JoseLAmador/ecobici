# ==============================================================
# Author: Jose Luis Amador
# Twitter: @a_josel
# Copyright (c) 2024
# ==============================================================

# Importing libraries
import streamlit as st
import pandas as pd
import folium
from folium.plugins import AntPath
import ast
import json

from utils.load_data import load_data, dtype, parse_dates
from utils.load_data import load_stations_data, popular_routes_coordinates
from utils.transforms import transform_popular_routes
from utils.visualization import viz_top10_routes

# Page config
st.set_page_config(
  page_title="Ecobici - Rutas",
  page_icon="🚲"
)

# ==============================================================
# Load data
# ==============================================================
path = "agosto-trips.csv.gz"
df = load_data(path, dtype, parse_dates)

path_stations = "ciclo_estaciones_cluster.csv.gz"
df_cicloestaciones = load_stations_data(path_stations)

# ==============================================================
# Global stats
# ==============================================================

st.markdown("# Ecobici - Rutas")
st.markdown(
  f"""
  En esta sección se presentan las rutas más populares de Ecobici durante el mes de agosto de 2024.
  """
)
st.divider()


# ==============================================================
# Visualization A Top 10 routes by frequency of use
# ==============================================================

# Transform data
df_popular_routes = transform_popular_routes(df)

df_top_10_routes = df_popular_routes.head(10)

# Visualization
st.subheader("(A) Top 10 rutas por frecuencia de uso")
vizualization_a = viz_top10_routes(df_top_10_routes)

vizualization_a


# ==============================================================
# Visualization B Show a map with the top 5 routes
# ==============================================================

# Transform data
df_top5_routes = df_popular_routes.head(5)
# Pickups
df_top5_routes_pickup_stations = df_top5_routes.merge(
  df_cicloestaciones,
  left_on='Ciclo_Estacion_Retiro',
  right_on='short_name', how='left'
)

df_top5_routes_pickup_stations = df_top5_routes_pickup_stations.rename(
  columns={
    'lat': 'Ciclo_Estacion_Retiro_Lat',
    'lon': 'Ciclo_Estacion_Retiro_Lon',
    'name': 'Ciclo_Estacion_Retiro_Name',
    'cluster': 'Ciclo_Estacion_Retiro_Cluster',
    'short_name': 'Ciclo_Estacion_Retiro_Short_Name'
  }
)

# Pickups and Arrives

df_top5_routes_pickup_arrives = df_top5_routes_pickup_stations.merge(
  df_cicloestaciones,
  left_on='Ciclo_Estacion_Arribo',
  right_on='short_name',
  how='left'
)

df_top5_routes_pickup_arrives = df_top5_routes_pickup_arrives.rename(
  columns={
    'lat': 'Ciclo_Estacion_Arribo_Lat',
    'lon': 'Ciclo_Estacion_Arribo_Lon',
    'name': 'Ciclo_Estacion_Arribo_Name',
    'cluster': 'Ciclo_Estacion_Arribo_Cluster',
    'short_name': 'Ciclo_Estacion_Arribo_Short_Name'
  }
)

df_top5_routes_final = df_top5_routes_pickup_arrives[[
  'Ciclo_Estacion_Retiro', 'Ciclo_Estacion_Retiro_Lat', 'Ciclo_Estacion_Retiro_Lon', 'Ciclo_Estacion_Retiro_Name',
  'Ciclo_Estacion_Arribo', 'Ciclo_Estacion_Arribo_Lat', 'Ciclo_Estacion_Arribo_Lon', 'Ciclo_Estacion_Arribo_Name'
]]

df_top5_routes_final['Ruta'] = df_top5_routes_final['Ciclo_Estacion_Retiro'] + '/' + df_top5_routes_final['Ciclo_Estacion_Arribo']


# DF_Coordinates
df_coordinates = pd.DataFrame(
  list(popular_routes_coordinates.items()),
  columns=['Ruta', 'Coordinates']
)

# Convert the 'Coordinates' column to a string
df_coordinates['Coordinates'] = df_coordinates['Coordinates'].apply(json.dumps)

# Merge df_top5_routes_final with df_coordinates by 'Ruta'
df_top5_routes_final = df_top5_routes_final.merge(
  df_coordinates,
  on='Ruta',
  how='left'
)

# Visualization
st.subheader("(B) Visualización de las 5 rutas más populares")

map_center = [
  df_top5_routes_final.loc[0, 'Ciclo_Estacion_Retiro_Lat'],
  df_top5_routes_final.loc[0, 'Ciclo_Estacion_Retiro_Lon']
]

# # Map
top_5_routes_map = folium.Map(
  location=map_center,
  zoom_start=12,
  tiles='CartoDB Positron'
)

colors = ['blue', 'green', 'red', 'purple', 'orange']

for i, row in df_top5_routes_final.iterrows():
  start_coords = [
    row['Ciclo_Estacion_Retiro_Lat'],
    row['Ciclo_Estacion_Retiro_Lon']
  ]
  
  end_coords = [
    row['Ciclo_Estacion_Arribo_Lat'],
    row['Ciclo_Estacion_Arribo_Lon']
  ]
  
  route_coords = ast.literal_eval(row['Coordinates'])
 
  route_layer = folium.FeatureGroup(name=f"Ruta {row['Ruta']}")

  folium.Marker(
    location=start_coords,
    popup=row['Ciclo_Estacion_Retiro_Name'],
    icon=folium.Icon(color='green', icon='square-parking', prefix='fa')
  ).add_to(route_layer)
  
  folium.Marker(
    location=end_coords,
    popup=row['Ciclo_Estacion_Arribo_Name'],
    icon=folium.Icon(color='green', icon='square-parking', prefix='fa')
  ).add_to(route_layer)

  AntPath(
    locations=route_coords,
    color=colors[i],
    weight=5,
    opacity=0.7,
    delay=1000
  ).add_to(route_layer)
  
  route_layer.add_to(top_5_routes_map)


folium.LayerControl().add_to(top_5_routes_map)

# Show map
html_string = top_5_routes_map.get_root().render()
st.components.v1.html(html_string, height=500)

# ==============================================================
# Sidebar
# ==============================================================

st.sidebar.markdown(
  f"""
  **(A)** La visualización muestra las 10 rutas más populares de Ecobici.
  """
)

st.sidebar.markdown(
  f"""
  La ruta CE-271-272 Jesús García - Carlos J. Meneses - CE-014 Reforma - Río de Plata es la más popular.
  """
)

st.sidebar.markdown(
  f"""
  La ruta más popular se visualiza en color azul.
  """
)

st.sidebar.markdown(
  f"""
  **(B)** El mapa muestra las cinco rutas ciclistas más populares de forma aproximada,
  ya que las rutas en bicicleta pueden variar según las condiciones del tráfico
  y las preferencias individuales.
  """
)

st.sidebar.markdown("*Reporte actualizado: septiembre 2024.*")