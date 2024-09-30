# ==============================================================
# Author: Jose Luis Amador
# Twitter: @a_josel
# Copyright (c) 2024
# ==============================================================

# Importing libraries
import streamlit as st
import altair as alt
from utils.load_data import load_data, dtype, parse_dates
from utils.transforms import add_day_hour_pickup, transform_mean_trip_duration_by_age_group_genre
from utils.transforms import transform_mean_trip_duration_by_day_of_the_week
from utils.transforms import transform_mean_trip_duration_by_hour_of_the_day
from utils.visualization import viz_trip_duration_by_age_group_genre
from utils.visualization import viz_mean_trip_duration_by_day_of_the_week
from utils.visualization import viz_mean_trip_duration_by_hour_of_the_day



# Page config
st.set_page_config(
  page_title="Ecobici - Duración promedio de viajes",
  page_icon="🚲"
)

# ==============================================================
# Load data
# ==============================================================
path = "agosto-trips.csv.gz"
df = load_data(path, dtype, parse_dates)

mean_duration = df['Duracion_Viaje_Minutos'].mean()

st.markdown("# Ecobici - Duración promedio de viajes")

st.markdown(
  f"""
  La duración media de los viajes realizados por los usuarios es de {mean_duration:.2f} minutos, lo que indica una preferencia por trayectos cortos y ágiles.
  """
)

st.divider()



df_trips = add_day_hour_pickup(df)

# ==============================================================
# Visualization A
# ==============================================================

# Transform data
df_trip_duration_by_age_group_genre = transform_mean_trip_duration_by_age_group_genre(df_trips)

# Visualization
st.subheader("(A) Duración media de viajes por grupo de edad y género")
vizualization_a = viz_trip_duration_by_age_group_genre(
  df_trip_duration_by_age_group_genre
)

vizualization_a


# ==============================================================
# Visualization B
# ==============================================================

# Transform data
df_trip_duration_by_day_of_the_week = transform_mean_trip_duration_by_day_of_the_week(df_trips)

# Visualization
st.subheader("(B) Duración media de viajes por día de la semana")
vizualization_b = viz_mean_trip_duration_by_day_of_the_week(df_trip_duration_by_day_of_the_week)

vizualization_b

# ==============================================================
# Visualization C
# ==============================================================
# Transform data
df_trip_duration_by_hour_of_the_day = transform_mean_trip_duration_by_hour_of_the_day(df_trips)

# Visualization
st.subheader("(C) Duración media de viajes por hora del día")
vizualization_c = viz_mean_trip_duration_by_hour_of_the_day(df_trip_duration_by_hour_of_the_day)

vizualization_c


# ==============================================================
# Sidebar
# ==============================================================

stats_duration_by_gender = df_trips.groupby('Genero_Usuario')['Duracion_Viaje_Minutos'].mean()
female_mean_duration = stats_duration_by_gender.loc['F'].round(2)
male_mean_duration = stats_duration_by_gender.loc['M'].round(2)

stats_duration_by_age_group = df_trips.groupby('Grupo_Edad')['Duracion_Viaje_Minutos'].mean()
mean_duration_85_94 = stats_duration_by_age_group.loc['85-94'].round(2)
mean_duration_35_44 = stats_duration_by_age_group.loc['35-44'].round(2)

top_mean_trip_duration_by_hour_of_the_day = df_trip_duration_by_hour_of_the_day.sort_values(
  'Duracion_Viaje_Minutos', ascending=False
).head(2)

st.sidebar.markdown(
  f"""
  **(A)** Las mujeres tienen una duración media ligeramente superior ({female_mean_duration} minutos) en
comparación con los hombres ({male_mean_duration} minutos).
  """
)
st.sidebar.markdown(
  f"""
  En general la duración media de los viajes aumenta con la edad, alcanzando su máximo en el
grupo de 85-94 años con {mean_duration_85_94} minutos, mientras que el grupo de 35-44 años tiene la
duración más baja, de {mean_duration_35_44} minutos.
  """
)
st.sidebar.markdown(
  f"""
  **(B)** Los viajes realizados los domingos tienen la duración media más alta, con un promedio de
19.11 minutos, lo que sugiere que los usuarios podrían usar las bicicletas de manera
recreativa.
  """
)


st.sidebar.markdown(
  f"""
  **(C)** La duración media más larga se registra a las 12:00 AM (medianoche), con {top_mean_trip_duration_by_hour_of_the_day['Duracion_Viaje_Minutos'].values[0]:.2f} minutos,
seguida de las 6:00 PM con {top_mean_trip_duration_by_hour_of_the_day['Duracion_Viaje_Minutos'].values[1]:.2f} minutos. Esto podría reflejar la relajación de los
usuarios en horas no laborales.
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
