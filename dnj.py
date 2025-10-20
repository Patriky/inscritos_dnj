import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

st.set_page_config(layout="wide")

#Centralizar a imagem no topo
st.image("images/logo_padrao.png", width=200)


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
# Ultima atualização em:


# ultima_atualizacao = datetime.now().strftime('%d/%m/%Y %H:%M')
ultima_atualizacao = '20/10/2024 10:00'  # Colocar a data manualmente por enquanto
st.write(f'Última atualização em: {ultima_atualizacao}')


# Leitura do arquivo com caminho relativo ao arquivo atual
BASE = Path(__file__).parent
xlsx_path = BASE / "lista-inscritos-dnj-2025-diocese-de-sao-jose-dos-pinhais-tratado.xlsx"

try:
    df = pd.read_excel(xlsx_path, engine="openpyxl")
except FileNotFoundError:
    st.error(f"Arquivo não encontrado: {xlsx_path}. Certifique-se que ele foi comitado no repositório ou faça upload via UI.")
    st.stop()
except ImportError:
    st.error("Dependência ausente para leitura de .xlsx (openpyxl). Adicione 'openpyxl' ao requirements.txt e redeploye.")
    st.stop()
except Exception as e:
    st.error(f"Erro ao ler o arquivo Excel: {e}")
    st.stop()



st.divider()

df = df.sort_values(by=['Paróquia', 'Nome'])


st.sidebar.title('Filtros')


modo_pesquisa = st.sidebar.radio("Modo de pesquisa:", ("Pesquisar por Paróquia", "Pesquisar por Nome"))

if modo_pesquisa == "Pesquisar por Paróquia":

    # Criar um filtro para a coluna "Paróquia"
    paroquias = df['Paróquia'].sort_values().unique()
    paroquias = np.insert(paroquias, 0, '')  # Adicionar uma opção vazia no início

    paroquia_selecionada = st.sidebar.selectbox('Selecione a Paróquia', paroquias)


    if paroquia_selecionada == '' or paroquia_selecionada is None:
        st.write('Nenhuma paróquia selecionada')
        st.stop()

    # Filtra por igualdade exata (mesma lógica que já tinha)
    df_filtrado = df[df['Paróquia'] == paroquia_selecionada]

else:  # Pesquisar por Nome
    nome_busca = st.sidebar.text_input('Digite o nome para pesquisar (parte do nome ou completo):', '')
    if nome_busca.strip() == '':
        st.write('Nenhum nome informado para pesquisa')
        st.stop()

    # Busca case-insensitive por substring na coluna "Nome"
    df_filtrado = df[df['Nome'].astype(str).str.contains(nome_busca, case=False, na=False)]

st.dataframe(df_filtrado)
st.write(f'Total de inscritos: {len(df_filtrado)}')

