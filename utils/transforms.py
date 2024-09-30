import pandas as pd
import streamlit as st

# ==============================================================
# Gender transform
# ==============================================================

@st.cache_data
def transform_gender(df):
  df_genre = df.groupby(
    'Genero_Usuario'
    ).size().reset_index(name='Viajes')
    # Average
  df_genre_total = df_genre['Viajes'].sum()
  df_genre['Porcentaje'] = (df_genre['Viajes'] / df_genre_total)
  return df_genre

# ==============================================================
# Age Group + 'M' & 'F' genre transform
# ==============================================================
@st.cache_data
def transform_age_group_by_top_genders(df):
  df_filtered = df[
    df['Genero_Usuario'].isin(['M', 'F'])
  ]
  df_grouped = df_filtered.groupby([
    'Genero_Usuario',
    'Grupo_Edad'
  ]).size().reset_index(name='Trips')

  return df_grouped

# ==============================================================
# Adding 'Dia_Semana_Retiro' & 'Hora_Retiro'
# ==============================================================
@st.cache_data
def add_day_hour_pickup(df):
  df_transformed = df.copy()

  df_transformed['Dia_Semana_Retiro'] = df_transformed['Fecha_Hora_Retiro'].dt.day_name()
  df_transformed['Hora_Retiro'] = df_transformed['Fecha_Hora_Retiro'].dt.hour
  df_transformed['Dia_Semana_Retiro_Num'] = df_transformed['Fecha_Hora_Retiro'].dt.day

  return df_transformed

# ==============================================================
# Transform mean trip duration by age group and genre
# ==============================================================
@st.cache_data
def transform_mean_trip_duration_by_age_group_genre(df):
  df_grouped = df.groupby(
    ['Grupo_Edad', 'Genero_Usuario']
  )['Duracion_Viaje_Minutos'].mean().reset_index()

  df_grouped = df_grouped.rename(
    columns={'Duracion_Viaje_Minutos': 'Duracion_Media'}
  )

  return df_grouped

# ==============================================================
# Transform mean trip duration by day of the week
# ==============================================================
@st.cache_data
def transform_mean_trip_duration_by_day_of_the_week(df):
  df_grouped = df.groupby(
    'Dia_Semana_Retiro'
  )['Duracion_Viaje_Minutos'].mean().reset_index()

  return df_grouped

# ==============================================================
# Transform mean trip duration by hour of the day
# ==============================================================
@st.cache_data
def transform_mean_trip_duration_by_hour_of_the_day(df):
  df_grouped = df.groupby(
    'Hora_Retiro'
  )['Duracion_Viaje_Minutos'].mean().reset_index()

  return df_grouped

# ==============================================================
# Transform trip quantity by day of the week
# ==============================================================
@st.cache_data
def transform_trip_quantity_by_day_of_the_week(df):
  df_grouped = df.groupby(
    'Dia_Semana_Retiro'
  ).size().reset_index(name='Viajes')

  return df_grouped

# ==============================================================
# Transform trip quantity by hour of the day
# ==============================================================
@st.cache_data
def transform_trip_quantity_by_hour_of_the_day(df):
  df_grouped = df.groupby(
    'Hora_Retiro'
  ).size().reset_index(name='Viajes')

  return df_grouped

# ==============================================================
# Transform Trip Quantity by hour of the day and day of the week
# ==============================================================
@st.cache_data
def transform_trip_quantity_by_hour_day(df):
  df_grouped = df.groupby(
    ['Dia_Semana_Retiro_Num', 'Hora_Retiro']
  ).size().reset_index(name='Viajes')

  # Calculate sum total by day
  df_grouped['Total'] = df_grouped.groupby('Dia_Semana_Retiro_Num')['Viajes'].transform('sum')

  return df_grouped

# ==============================================================
# Transform popular stations
# ==============================================================
@st.cache_data
def transform_popular_stations(df):
  df_stations_pickup = df['Ciclo_Estacion_Retiro'].value_counts().reset_index()
  df_stations_pickup.columns = ['Ciclo_Estacion', 'Cantidad_Retiros']


  df_station_arrives = df['Ciclo_Estacion_Arribo'].value_counts().reset_index()
  df_station_arrives.columns = ['Ciclo_Estacion', 'Cantidad_Arribos']


  df_popular_stations = df_stations_pickup.merge(df_station_arrives, on='Ciclo_Estacion', how='inner')
  df_popular_stations['Frecuencia_Uso'] = df_popular_stations['Cantidad_Retiros'] + df_popular_stations['Cantidad_Arribos']

  return df_popular_stations

# ==============================================================
# Transform popular routes
# ==============================================================
@st.cache_data
def transform_popular_routes(df):
  df_popular_routes = df.groupby([
    'Ciclo_Estacion_Retiro',
    'Ciclo_Estacion_Arribo'
  ]).size().reset_index(name='Frecuencia').sort_values('Frecuencia', ascending= False)

  return df_popular_routes
