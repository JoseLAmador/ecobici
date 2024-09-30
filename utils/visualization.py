import altair as alt
import pandas as pd


'''
Days of the week
'''
days = [
  'Sunday',
  'Monday',
  'Tuesday',
  'Wednesday',
  'Thursday',
  'Friday',
  'Saturday'
]

'''
Genre distribution visualization
'''
def genre_distribution(df):
  visualization = alt.Chart(df).mark_bar().encode(
    x=alt.X('Genero_Usuario:N', title='Género', sort="-y"),
    y=alt.Y('Viajes:Q', title='Viajes'),
    color=alt.Color(
      'Genero_Usuario:N',
      legend=alt.Legend(
      title="Género"
      )
    ),
    tooltip=[
      alt.Tooltip('Genero_Usuario:N', title='Género'),
      alt.Tooltip('Viajes:Q', title='Viajes', format=','),
      alt.Tooltip('Porcentaje:Q', title='Porcentaje', format='.2%'),
    ]
  ).properties(
    width=500,
    height=300
  )
  return visualization

'''
Sort age groups
'''
def sort_age_group(x):
  if x == '-18':
    return -1  # beginning
  elif x == '95+':
    return 1000  # last

  return int(x.split('-')[0])

'''
Pyramid visualization for age distribution
'''
def pyramid_age_distribution(df):
  sort_age = sorted(df['Grupo_Edad'].unique(), key=sort_age_group)
  max_trips = df['Trips'].max()
  
  color_scale = alt.Scale(domain=['M', 'F'], range=['#1f77b4', '#e377c2'])

  # Base visualization
  base = alt.Chart(df).encode(
    y=alt.Y('Grupo_Edad:O', sort=sort_age, axis=None),
    color=alt.Color('Genero_Usuario:N', scale=color_scale, legend=None)
  ).properties(width=300, height=400)

  # Left visualization
  left = base.transform_filter(
    alt.datum.Genero_Usuario == 'F'
  ).transform_calculate(
    negative_trips = '-datum.Trips'
  ).encode(
    x=alt.X(
      'negative_trips:Q',
      axis=alt.Axis(format='d', labelExpr="datum.value * -1"),
      scale=alt.Scale(domain=[-max_trips, 0]),
      title='Viajes'
    ),
    tooltip=[
      alt.Tooltip('Trips:Q', title='Viajes', format=','),
      alt.Tooltip('Grupo_Edad:N', title='Grupo de Edad')
    ]
  ).mark_bar().properties(title='Femenino')

  # Right visualization
  right = base.transform_filter(
    alt.datum.Genero_Usuario == 'M'
  ).encode(
    x=alt.X(
      'Trips:Q', 
      axis=alt.Axis(format='d'),
      scale=alt.Scale(domain=[0, max_trips]),
      title='Viajes'
    ),
    tooltip=[
      alt.Tooltip('Trips:Q', title='Viajes', format=','),
      alt.Tooltip('Grupo_Edad:N', title='Grupo de Edad')
    ]
  ).mark_bar().properties(title='Masculino')

  # Middle visualization
  middle = base.encode(
    text='Grupo_Edad:N',
    tooltip=[
      alt.Tooltip('Grupo_Edad:N', title='Grupo de Edad')
    ]
  ).mark_text().properties(width=50)

  # Concatenate visualizations
  final_chart = alt.hconcat(
    left,
    middle,
    right,
    spacing=5
  ).resolve_scale(
    x='independent',
    y='shared'
  )

  return final_chart

'''
Mean trip duration by age group and genre visualization
'''
def viz_trip_duration_by_age_group_genre(df):
  visualization = alt.Chart(
    df
  ).mark_bar().encode(
    x=alt.X('Grupo_Edad:N', title="Grupo de edad"),
    y=alt.Y('Duracion_Media:Q', title="Duración media del viaje (minutos)"),
    color=alt.Color('Genero_Usuario:N', title='Género'),
    column=alt.Column('Genero_Usuario:N', title='Género'),
    tooltip=[
      alt.Tooltip('Grupo_Edad:N', title='Grupo de edad'),
      alt.Tooltip('Genero_Usuario:N', title='Género'),
      alt.Tooltip('Duracion_Media:Q', title='Duración media del viaje', format='.2f')
    ]
  ).properties(
    width=200,
    height=300
  )
  return visualization

'''
Mean trip duration by day of the week
'''
def viz_mean_trip_duration_by_day_of_the_week(df):
  visualization = alt.Chart(
    df
  ).mark_bar().encode(
    x=alt.X('Dia_Semana_Retiro:N', sort=days, title='Día de la semana'),
    y=alt.Y('Duracion_Viaje_Minutos:Q', title='Duración media del viaje (minutos)'),
    color=alt.Color('Dia_Semana_Retiro:N', legend=None),
    tooltip=[
      alt.Tooltip('Dia_Semana_Retiro:N', title='Día de la semana'),
      alt.Tooltip('Duracion_Viaje_Minutos:Q', title='Duración media del viaje', format='.2f')
    ]
  ).properties(
    width=600,
    height=400
  )
  return visualization

'''
Meand trip duration by hour of the day
'''
def viz_mean_trip_duration_by_hour_of_the_day(df):
  visualization = alt.Chart(
    df
  ).mark_line(point=True).encode(
    x=alt.X('Hora_Retiro:O', title='Hora del día', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('Duracion_Viaje_Minutos:Q', title='Duración media del viaje (minutos)'),
    tooltip=[
      alt.Tooltip('Hora_Retiro:O', title='Hora del día'),
      alt.Tooltip('Duracion_Viaje_Minutos:Q', title='Duración media del viaje', format='.2f')
    ]
  ).properties(
    width=600,
    height=400
  )
  return visualization

'''
Trip Quantity by day of the week
'''
def viz_trip_quantity_by_day_of_the_week(df):
  visualization = alt.Chart(
    df
  ).mark_bar().encode(
    x=alt.X('Dia_Semana_Retiro:N', title='Día de la semana', sort=days),
    y=alt.Y('Viajes:Q', title='Viajes'),
    color=alt.Color('Dia_Semana_Retiro:N', legend=None),
    tooltip=[
      alt.Tooltip('Viajes:Q', title='Viajes', format=','),
      alt.Tooltip('Dia_Semana_Retiro:N', title='Día de la semana')
    ]
  ).properties(
    width=400,
  )
  return visualization

'''
Trip Quantity by hour of the day
'''
def viz_trip_quantity_by_hour_of_the_day(df):
  visualization = alt.Chart(
    df
  ).mark_line(point=True).encode(
    x=alt.X('Hora_Retiro:O', title='Hora'),
    y=alt.Y('Viajes:Q', title='Viajes'),
    tooltip=[
      alt.Tooltip('Hora_Retiro:N', title='Hora'),
      alt.Tooltip('Viajes:Q', title='Viajes', format=",")
    ]
  ).properties(
    width=400,
    height=300
  )
  return visualization


'''
Trip Quantity by hour of the day and day of the week
'''
def viz_trip_quantity_by_hour_day(df):
  visualization = alt.Chart(
    df
  ).mark_rect().encode(
    x=alt.X('Hora_Retiro:O', title='Hora del día'),
    y=alt.Y('Dia_Semana_Retiro_Num:O', title='Día de la semana'),
    color=alt.Color('Viajes:Q', scale=alt.Scale(scheme='viridis'), title='Viajes'),
    tooltip=[
      alt.Tooltip('Hora_Retiro:O', title='Hora del día'),
      alt.Tooltip('Dia_Semana_Retiro_Num:O', title='Día de la semana'),
      alt.Tooltip('Viajes:Q', title='Viajes por hora', format=','),
      alt.Tooltip('Total:Q', title='Total viajes', format=',')


    ]
  ).properties(
    width=600,
    height=400
  )
  return visualization


'''
Top 10 stations by trip quantity
'''
def viz_top10_stations(df):
  melt = pd.melt(
    df,
    id_vars='Ciclo_Estacion',
    value_vars=[
      'Cantidad_Retiros',
      'Cantidad_Arribos'
    ]
  )

  melt.columns = ['Ciclo_Estacion', 'Tipo', 'Frecuencia']

  melt['Tipo'] = melt['Tipo'].replace({
    'Cantidad_Retiros': 'Retiros',
    'Cantidad_Arribos': 'Arribos'
  })

  visualization = alt.Chart(melt).mark_bar().encode(
    x=alt.X('Frecuencia:Q', title='Frecuencia de uso'),
    y=alt.Y('Ciclo_Estacion:N', title='Ciclo estación', sort='-x'),
    color=alt.Color(
      'Tipo:N',
      title='Tipo',
      scale=alt.Scale(range=['#1f77b4', '#ff7f0e']),
    ),
    tooltip=[
      alt.Tooltip('Ciclo_Estacion:N', title='Ciclo estación'),
      alt.Tooltip('Frecuencia:Q', title='Frecuencia de uso', format=','),
      alt.Tooltip('Tipo:N', title='Tipo')
    ]
  ).properties(
    width=600,
    height=400
  )

  return visualization

'''
Top 10 routes
'''
def viz_top10_routes(df):
  visualization = alt.Chart(df).mark_rect().encode(
    x=alt.X('Ciclo_Estacion_Arribo:N', title='Arribo'),
    y=alt.Y('Ciclo_Estacion_Retiro:N', title='Retiro'),
    color=alt.Color('Frecuencia:Q', scale=alt.Scale(scheme='viridis'), title='Frecuencia'),
    tooltip=[
      alt.Tooltip('Ciclo_Estacion_Retiro:N', title='Retiro'),
      alt.Tooltip('Ciclo_Estacion_Arribo:N', title='Arribo'),
      alt.Tooltip('Frecuencia:Q', title='Frecuencia', format=',')
    ]
  ).properties(
    width=500,
    height=400
  )

  return visualization