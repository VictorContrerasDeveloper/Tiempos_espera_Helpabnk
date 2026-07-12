import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página web
st.set_page_config(page_title="Dashboard de Tiempos de Espera", layout="wide")
st.title("📊 Panel Comercial: Tiempos de Espera")
st.markdown("Sube el archivo Excel del sistema para analizar los tiempos promedio por oficina y día.")

# 2. Crear la cajita para que el usuario suba el archivo
archivo_subido = st.file_uploader("Sube el archivo Excel aquí", type=['xlsx'])

# 3. Lógica: Qué pasa cuando se sube el archivo
if archivo_subido is not None:
    try:
        # Leer el Excel
        df = pd.read_excel(archivo_subido)
        st.success("✅ ¡Archivo cargado y leído correctamente!")
        
        # Nombres exactos de tus columnas
        col_oficina = 'Cola/Oficina'
        col_fecha = 'Interacción: Fecha de creación'
        col_espera = 'Tiempo de espera (min) Quenda'
        
        # Convertir la columna de texto a formato "Fecha" real para que se ordene bien
        df[col_fecha] = pd.to_datetime(df[col_fecha], dayfirst=True, errors='coerce').dt.date
        
        # 4. Matemáticas: Agrupar por Oficina y por Fecha, y sacar el promedio de espera
        df_resumen = df.groupby([col_oficina, col_fecha])[col_espera].mean().reset_index()
        df_resumen.rename(columns={col_espera: 'Espera Promedio (min)'}, inplace=True)
        
        # Ordenar cronológicamente
        df_resumen = df_resumen.sort_values(by=col_fecha)

        st.divider() # Línea divisoria visual
        
        # 5. Crear el Gráfico Interactivo
        st.subheader("📈 Evolución de Tiempos de Espera Promedio")
        
        fig = px.bar(df_resumen, 
                     x=col_fecha, 
                     y='Espera Promedio (min)', 
                     color=col_oficina,
                     barmode='group',
                     text_auto='.1f', # Mostrar el número sobre la barra (1 decimal)
                     title="Tiempo de Espera Promedio (minutos) por Día y Oficina")
        
        # Limpiar el diseño del gráfico
        fig.update_layout(xaxis_title="Día", yaxis_title="Minutos de Espera")
        
        # Mostrar gráfico en la web
        st.plotly_chart(fig, use_container_width=True)
        
        # 6. Mostrar la tabla resumen
        st.subheader("📋 Tabla Resumen de Datos")
        st.dataframe(df_resumen, use_container_width=True)
        
    except Exception as e:
        # Si algo falla, le avisa al usuario amigablemente
        st.error(f"Hubo un error procesando el archivo: {e}")
else:
    # Mensaje de espera inicial
    st.info("👆 Por favor, sube un archivo Excel para comenzar el análisis.")
