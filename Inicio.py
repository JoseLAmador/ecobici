# ==============================================================
# Author: Jose Luis Amador
# Twitter: @a_josel
# Copyright (c) 2024
# ==============================================================

# Importing libraries
import streamlit as st
from utils.load_data import load_data

def run():
  # Page config
  st.set_page_config(
    layout="wide",
    page_title="Ecobici | Patrón de uso",
    page_icon="🚴"
  )

  st.title("Patrón de uso Ecobici - Agosto 2024 🚴")
  st.markdown(
    """  
    Este estudio explora los patrones de uso del sistema Ecobici durante el mes de **agosto de 2024.**
    Se identifican **tendencias clave** relacionadas con el comportamiento de los usuarios, horarios y días más populares, distribución por género y edad, así como la demanda en diferentes ciclo estaciones.
    Los resultados ofrecen una base para futuros análisis que permitan seguir ajustando y evolucionando el servicio de movilidad urbana.
    """
  )
  st.divider()

  # ==============================================================
  # Load data
  # ==============================================================
  path = "agosto-resume.csv.gz"
  df = load_data(path)

  # ==============================================================
  # Display general stats in card format
  # ==============================================================

  st.subheader("📊 Estadísticas generales")

  # Display general stats in card format
  left, middle, right = st.columns([0.3, 0.3, 0.3])

  left_tile = left.container(height=120, border=True)
  left_tile.markdown("**Total de viajes**")
  total_trips = df['Total_Viajes'].sum()
  left_tile.write(f"{total_trips:,}")

  middle_tile = middle.container(height=120, border=True)
  middle_tile.markdown("**Ciclo estaciones disponibles**")
  total_stations = df['Total_Ciclo_Estaciones'].sum()
  middle_tile.write(f"{total_stations}")

  right_tile = right.container(height=120, border=True)
  # Calculate the average trip duration
  trip_average_duraction = df['Duracion_Promedio_Viaje_Minutos'].sum() 
  # Convert the average trip duration to hours and minutes 
  hours = int(trip_average_duraction // 60)
  minutes = int(trip_average_duraction % 60)

  right_tile.markdown("**Promedio de viaje**")
  right_tile.write(f"{hours} horas y {minutes} minutos")

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





if __name__ == "__main__":
    run()