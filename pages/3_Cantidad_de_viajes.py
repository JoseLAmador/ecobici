# ==============================================================
# Author: Jose Luis Amador
# Twitter: @a_josel
# Copyright (c) 2024
# ==============================================================

# Importing libraries
import streamlit as st
from utils.load_data import load_data, dtype, parse_dates
from utils.transforms import add_day_hour_pickup, transform_trip_quantity_by_day_of_the_week
from utils.visualization import viz_trip_quantity_by_day_of_the_week
from utils.transforms import transform_trip_quantity_by_hour_of_the_day
from utils.visualization import viz_trip_quantity_by_hour_of_the_day
from utils.transforms import transform_trip_quantity_by_hour_day
from utils.visualization import viz_trip_quantity_by_hour_day


# Page config
st.set_page_config(
  page_title="Ecobici - Cantidad de viajes",
  page_icon="🚲"
)

# ==============================================================
# Load data
# ==============================================================
path = "agosto-trips.csv.gz"
df = load_data(path, dtype, parse_dates)

df_trips = add_day_hour_pickup(df)

mean_trip_quantity_by_day = len(df_trips) / 31 # 31 days in August 2024

st.markdown("# Ecobici - Cantidad de viajes")

st.markdown(
  f"""
  Los usuarios de Ecobici realizaron un promedio de {mean_trip_quantity_by_day:.0f} viajes por día en agosto de 2024.
  """
)

st.divider()


# ==============================================================
# Visualization A Trip Quantity by day of the week
# ==============================================================

# Transform data
df_trips_by_day = transform_trip_quantity_by_day_of_the_week(df_trips)

# Visualization
st.subheader("(A) Cantidad de viajes por día de la semana")
visualization_a = viz_trip_quantity_by_day_of_the_week(df_trips_by_day)
visualization_a

# ==============================================================
# Visualization B Trip Quantity by hour of the day
# ==============================================================

# Transform data
df_trips_by_hour = transform_trip_quantity_by_hour_of_the_day(df_trips)

# Visualization
st.subheader("(B) Cantidad de viajes por hora del día")
visualization_b = viz_trip_quantity_by_hour_of_the_day(df_trips_by_hour)
visualization_b


# ==============================================================
# Visualization C Trip Quantity by hour of the day and day of the week
# ==============================================================

# Transform data
df_trips_by_hour_day = transform_trip_quantity_by_hour_day(df_trips)

# Visualization
st.subheader("(C) Cantidad de viajes por hora del día y día de la semana")
visualization_c = viz_trip_quantity_by_hour_day(df_trips_by_hour_day)
visualization_c


# ==============================================================
# Sidebar
# ==============================================================

day_max_trips = df_trips_by_day['Viajes'].max()
day_max = df_trips_by_day.loc[df_trips_by_day['Viajes'].idxmax(), 'Dia_Semana_Retiro']

hour_max_trips = df_trips_by_hour['Viajes'].max()
hour_max = df_trips_by_hour.loc[df_trips_by_hour['Viajes'].idxmax(), 'Hora_Retiro']
hour_max_trips = df_trips_by_hour['Viajes'].max()

day_number_group = df_trips_by_hour_day.groupby('Dia_Semana_Retiro_Num')['Viajes'].sum()
day_number_max = day_number_group.idxmax()
day_number_min = day_number_group.idxmin()

st.sidebar.markdown(
  f"""
  **(A)** El día {day_max} es el más popular para realizar viajes, con {day_max_trips:,} viajes.
  """
)
st.sidebar.markdown(
  f"""
  Los días con menos viajes son los fines de semana. Esto puede sugerir
que el uso de Ecobici está más relacionado con actividades de transporte diario que con
el ocio.
  """
)
st.sidebar.markdown(
  f"""
  **(B)** La hora pico es {hour_max} horas. Con {hour_max_trips:,} viajes.
  """
)

st.sidebar.markdown(
  f"""
  **(C)** El uso de Ecobici es más frecuente durante la semana laboral.
  """
)

st.sidebar.markdown(
  f"""
  El día más popular para realizar viajes fue el {day_number_max} de agosto con {day_number_group[day_number_max]:,} viajes.
  """
)

st.sidebar.markdown(
  f"""
  El día con menos viajes fue el {day_number_min} de agosto con {day_number_group[day_number_min]:,} viajes.
  """
)


st.sidebar.markdown("*Reporte actualizado: septiembre 2024.*")
