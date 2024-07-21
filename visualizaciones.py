import altair as alt

def crear_grafico_autores(top_autores):
    bar_chart1 = alt.Chart(top_autores).mark_bar().encode(
        y=alt.Y('name_author', sort='-x', title='Autor'),
        x=alt.X('n_articles_total', title='Número de artículos totales'),
        color=alt.Color('name_author', scale=alt.Scale(scheme='set1'), legend=None)
    ).properties(
        title='Mayores productores'
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16
    )
    return bar_chart1

def crear_grafico_filiaciones(filiaciones_ordenadas):
    bar_chart2 = alt.Chart(filiaciones_ordenadas).mark_bar().encode(
        y=alt.Y('name_affiliation', sort='-x', title='Filiación'),
        x=alt.X('n_articles', title='Número de Artículos'),
        color=alt.Color('name_affiliation', scale=alt.Scale(scheme='set2'), legend=None)
    ).properties(
        title='Filiaciones más productivas'
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16
    )
    return bar_chart2

def crear_grafico_revistas(revistas_ordenadas):
    bar_chart3 = alt.Chart(revistas_ordenadas).mark_bar().encode(
        y=alt.Y('title', sort='-x', title='Revista'),
        x=alt.X('n', title='Número de Artículos'),
        color=alt.Color('title', scale=alt.Scale(scheme='set3'), legend=None)
    ).properties(
        title='Revistas donde más se publica'
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16
    )
    return bar_chart3

def crear_grafico_articulos_por_año(frecuencia_por_año):
    line_chart4 = alt.Chart(frecuencia_por_año).mark_line(point=True).encode(
        x=alt.X('Año:O', title='Año'),
        y=alt.Y('n_articulos', title='Número de Artículos'),
        # color="symbol:N"
    ).properties(
        title='Artículos publicados por año',
        width=400,
        height=600,
    ).configure_axis(
        labelFontSize=14,
        titleFontSize=16
    ).configure_title(
        fontSize=16
    ).configure_legend(
        orient='top-left'
    )
    return line_chart4

def crear_grafico_idiomas_por_año(df_resultado):
    line_chart5 = alt.Chart(df_resultado).mark_line(point=True).encode(
        x=alt.X('Año:O', title='Año'),
        y=alt.Y('value:Q', title='Número de artículos'),
        color=alt.Color('variable:N', title='Serie')
    ).transform_fold(
        ['Art_es', 'Art_en'],
        as_=['variable', 'value']
    ).properties(
        title='Tendencia de publicación de artículos en español e inglés',
        width=400,
        height=600,
    ).configure_axis(
        labelFontSize=14,
        titleFontSize=16
    ).configure_title(
        fontSize=16
    ).configure_legend(
        orient='top-left'
    )
    return line_chart5

def crear_grafico_publicaciones_area(df_agrupado_total):
    line_chart6 = alt.Chart(df_agrupado_total).mark_line().encode(
        x='Year:N',
        y=alt.Y('n_art:Q', title='Número de Artículos'),
        color='Area:N',
        tooltip=['Year:N', 'Area:N', 'n_art:Q']
    ).properties(
        title='Evolución de Publicaciones por Área de Investigación (2015-2020)',
        width=600,
        height=600,
    ).configure_axis(
        labelFontSize=14,
        titleFontSize=16
    ).configure_legend(
        orient='top-left',
        title=None
    )
    return line_chart6