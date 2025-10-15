import streamlit as st
import pandas as pd
import numpy as np
st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            width: 400px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('DNJ 2025 - Diocese de São José dos Pinhais')
st.subheader('Lista de Inscritos')
st.divider()
df = pd.read_excel('lista-inscritos-dnj-2025-diocese-de-sao-jose-dos-pinhais-tratado.xlsx')

df = df.sort_values(by=['Paróquia', 'Nome'])


st.sidebar.title('Filtros')


# Criar um filtro para a coluna "Paróquia"
paroquias = df['Paróquia'].sort_values().unique()

paroquias = np.insert(paroquias, 0, '')  # Adicionar uma opção vazia no início
paroquia_selecionada = st.sidebar.selectbox('Selecione a Paróquia', paroquias)

# Se não tiver nenhuma paróquia selecionada, não mostrar nada
if paroquia_selecionada == '' or paroquia_selecionada is None:
    st.write('Nenhuma paróquia selecionada')
    st.stop()



df_filtrado = df[df['Paróquia'] == paroquia_selecionada]
st.dataframe(df_filtrado)
st.write(f'Total de inscritos: {len(df_filtrado)}')

