# ==============================================================
# Author: Jose Luis Amador
# Twitter: @a_josel
# Copyright (c) 2024
# ==============================================================

# Importing libraries
import streamlit as st
import altair as alt
from utils.load_data import load_data, dtype, parse_dates
from utils.transforms import transform_gender, transform_age_group_by_top_genders
from utils.visualization import genre_distribution, pyramid_age_distribution


# Page config
st.set_page_config(
  page_title="Ecobici - Distribución de usuarios",
  page_icon="👥"
)

# ==============================================================
# Load data
# ==============================================================
path = "agosto-trips.csv.gz"
df = load_data(path, dtype, parse_dates)

st.markdown("# Ecobici - Distribución de usuarios")

st.markdown(
  """
  Los géneros registrados son los siguientes:

  | Género | Código | Descripción |
  |---|---|---|
  | Femenino | F | Individuo que se identifica como mujer. |
  | Masculino | M | Individuo que se identifica como hombre. |
  | Otro/Prefiero no decir | O | Individuo que se identifica con un género distinto a hombre o mujer, o que prefiere no especificar su género. |
  """
)

st.divider()


# ==============================================================
# Visualization A
# ==============================================================

# Transform data
df_genre = transform_gender(df)
# Visualization
genre_visulization = genre_distribution(df_genre)


# ==============================================================
# Visualization B
# ==============================================================
# Transform data
df_age_group_by_top_genders = transform_age_group_by_top_genders(df)
# Visualization
pyramid_visulization = pyramid_age_distribution(df_age_group_by_top_genders)

st.subheader("(A) Distribución de género")
genre_visulization
st.subheader("(B) Distribución de Viajes por Grupo de Edad")
pyramid_visulization


# ==============================================================
# Sidebar
# ==============================================================

age_mean = df['Edad_Usuario'].mean()
age_median = df['Edad_Usuario'].median().astype(int)

age_group_percentage = df['Grupo_Edad'].value_counts(normalize=True) * 100
age_group_percentage = age_group_percentage.reset_index()
age_group_percentage.columns = ['Grupo_Edad', 'Porcentaje']
age_group_percentage['Porcentaje'] = age_group_percentage['Porcentaje'].round(2)

# find the name group with the highest percentage and percentaje
age_group_percentage_max = age_group_percentage[age_group_percentage['Porcentaje'] == age_group_percentage['Porcentaje'].max()]

# Extract most popular genre with percentage
genre_max = df_genre[df_genre['Porcentaje'] == df_genre['Porcentaje'].max()]

# Extract F genre with percentage
genre_f = df_genre[df_genre['Genero_Usuario'] == 'F']

st.sidebar.markdown(
  f"""
  **(A)** La mayoría de los usuarios son hombres, representando el {genre_max['Porcentaje'].values[0] * 100:.2f}% de los viajes, mientras que las mujeres constituyen el {genre_f['Porcentaje'].values[0]*100:.2f}%.
  """
)
st.sidebar.markdown(
  """
  Un pequeño porcentaje de los usuarios no especificó su género.
  """
)
st.sidebar.markdown(
  f"""
  **(B)** El grupo de personas predominante es el de **{age_group_percentage_max['Grupo_Edad'].values[0]} años**, que representa más del {age_group_percentage_max['Porcentaje'].values[0]}% de los viajes.
  """
)

st.sidebar.markdown(
  f"""
  La edad promedio de los usuarios es de {age_mean:.2f} años y la mediana es de {age_median} años.
  """
)


st.sidebar.markdown("*Reporte actualizado: septiembre 2024.*")
