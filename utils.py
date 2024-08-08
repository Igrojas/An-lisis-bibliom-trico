import streamlit as st
import pandas as pd
import json

def principales_indicadores(salida_autores, salida_articulos):
    # Cálculo de los indicadores
    num_autores = len(salida_autores)
    num_articulos = len(salida_articulos)

    suma_n_autores = salida_articulos["n_authors"].sum()
    largo_salida_articulos = len(salida_articulos)
    n_autores_por_paper = suma_n_autores / largo_salida_articulos

    suma_n_paper = salida_autores["n_articles_total"].sum()
    largo_salida_autores = len(salida_autores)
    n_paper_por_autores = suma_n_paper / largo_salida_autores

    return num_autores, num_articulos, n_autores_por_paper, n_paper_por_autores

def n_articulos_por_autor(salida_autores):
    autores_por_paper = salida_autores.sort_values(by=['n_articles_total'], ascending=False)
    autores_por_paper = autores_por_paper.loc[:, ['name_author', 'n_articles_total', 'n_articulos_chile']]
    return autores_por_paper.head(15)

def paper_por_filiacion(salida_filiaciones):
    filiaciones = salida_filiaciones.sort_values(by=['n_articles'], ascending=False)
    filiaciones = filiaciones.loc[:,['name_affiliation', 'n_articles']]
    filiaciones["Porcentaje de Artículos"] = round(filiaciones['n_articles'] / 3003 * 100, 2)
    filiaciones_ordenados = filiaciones.sort_values('n_articles', ascending=False).head(15)
    return filiaciones_ordenados

def paper_por_revistas(salida_revistas):
    revistas = salida_revistas.loc[:,['title','n']]
    revistas["Porcentaje de Artículos"] = revistas['n'] / len(revistas) * 100
    revistas_ordenados = revistas.sort_values('n', ascending=False)
    revistas_ordenados['title'] = revistas_ordenados['title'].str.lower()
    revistas_ordenados
    return revistas_ordenados.head(15)

def paper_por_año(salida_articulos):
    frecuencia_por_año = pd.DataFrame()
    frecuencia_por_año["Año"] = salida_articulos['year'].value_counts().index
    frecuencia_por_año["n_articulos"] = salida_articulos['year'].value_counts().values
    return frecuencia_por_año

def cambiar_idioma(salida_articulos):
    idiomas_counts = salida_articulos['language'].replace({
        'en': 'Inglés',
        'English': 'Inglés',
        'es': 'Español',
        'Spanish': 'Español',
        'en, es': 'Inglés, Español',
        'English; Spanish': 'Inglés, Español',
        'French': 'Francés',
        'pt': 'Portugués',
        'Portuguese': 'Portugués',
        'German': 'Alemán',
        'English; French': 'Inglés, Francés',
        'English; Portuguese; Spanish': 'Inglés, Portugués, Español',
        'Estonian': 'Estonio',
        'English; Portuguese': 'Inglés, Portugués'
    }).value_counts()
    return idiomas_counts

def topic_counts(salida_articulos, salida_topicos):
    counts = salida_articulos['topic_name'].value_counts()

    df_topicos = pd.DataFrame({
        'N': range(1, len(counts) + 1),
        'Keywords': counts.index,
        'n_art': counts.values
    })

    areas = []
    for keyword in df_topicos['Keywords']:
        area = salida_topicos.loc[salida_topicos['Keywords'] == keyword, 'Area'].values
        areas.append(area[0] if len(area) > 0 else 'No especificado')

    df_topicos['Area'] = areas

    return df_topicos

def prop_idiomas_por_año(salida_articulos):
    idiomas_reemplazo = {
        'en': 'Inglés', 'English': 'Inglés', 'es': 'Español', 'Spanish': 'Español',
        'en, es': 'Inglés, Español', 'French': 'Francés', 'pt': 'Portugués', 
        'Portuguese': 'Portugués', 'German': 'Alemán', 'English; French': 'Inglés, Francés',
        'English; Portuguese; Spanish': 'Inglés, Portugués, Español', 'Estonian': 'Estonio',
        'English; Portuguese': 'Inglés, Portugués'
    }

    salida_articulos['language'] = salida_articulos['language'].replace(idiomas_reemplazo)

    df_resumen_idiomas = pd.DataFrame()
    df_resumen_idiomas['Año'] = sorted(salida_articulos['year'].unique())

    counts_por_año = salida_articulos['year'].value_counts().sort_index()
    df_resumen_idiomas['n_art'] = counts_por_año.values

    art_es = salida_articulos[salida_articulos['language'] == 'Español']
    counts_art_es = art_es.groupby('year').size().reindex(df_resumen_idiomas['Año'], fill_value=0)
    df_resumen_idiomas['Art_es'] = counts_art_es.values

    df_resumen_idiomas["Prop_es"] = round(df_resumen_idiomas['Art_es'] / df_resumen_idiomas['n_art'] * 100, 2)

    art_en = salida_articulos[salida_articulos['language'] == 'Inglés']
    counts_art_en = art_en.groupby('year').size().reindex(df_resumen_idiomas['Año'], fill_value=0)
    df_resumen_idiomas['Art_en'] = counts_art_en.values

    df_resumen_idiomas["Prop_en"] = round(df_resumen_idiomas['Art_en'] / df_resumen_idiomas['n_art'] * 100, 2)

    return df_resumen_idiomas

def contar_areas(salida_articulos, salida_topicos):
    counts = salida_articulos['topic_name'].value_counts()
    
    df_topicos = pd.DataFrame({
        'Keywords': counts.index,
        'n_art': counts.values
    })

    df_topicos['Area'] = [salida_topicos[salida_topicos['Keywords'] == valor].iloc[0][1] for valor in df_topicos['Keywords']]

    df_agrupado = df_topicos.groupby('Area').sum()

    df_agrupado = df_agrupado.sort_values(by='n_art', ascending=False)

    return df_agrupado

def generar_df_agrupado_total(salida_articulos, salida_topicos):
    df_agrupado_total = pd.DataFrame()

    for year in range(2015, 2021):
        salida_articulos_year = salida_articulos[salida_articulos['year'] == year]
        counts = salida_articulos_year['topic_name'].value_counts()
        
        df_topicos = pd.DataFrame()
        df_topicos['Keywords'] = counts.index
        df_topicos['Area'] = [salida_topicos[salida_topicos['Keywords'] == valor].iloc[0][1] for valor in df_topicos['Keywords']]
        df_topicos['n_art'] = counts.values
        df_topicos = df_topicos.reset_index(drop=True)
        
        df_agrupado_year = df_topicos.groupby(['Area']).sum()
        df_agrupado_year = df_agrupado_year.sort_values(by='n_art', ascending=False)
        
        df_agrupado_year['Year'] = year
        
        df_agrupado_total = pd.concat([df_agrupado_total, df_agrupado_year])

    df_agrupado_total = df_agrupado_total.reset_index()

    df_agrupado_total
    return df_agrupado_total

 # # # # #  # # # # #  # # # # #  # # # # #  # # # # #  # # # # #  # # # # #  # # # # #  # # # # #  # # # # # 

def mostrar_tabla():

    centralidad_final = pd.read_excel("data/centralidad_final.xlsx", index_col= 0)
    st.dataframe(centralidad_final)


