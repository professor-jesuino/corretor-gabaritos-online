import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Corretor de Provas", page_icon="📝")

st.title("📝 Portal do Aluno")
st.markdown("Preencha seu nome e marque as respostas da prova.")

# Conexão com a planilha (usando os secrets configurados)
conn = st.connection("gsheets", type=GSheetsConnection)

# --- CONFIGURAÇÃO DA PROVA ---
gabarito_oficial = ['A', 'B', 'C', 'D', 'E'] 

nome = st.text_input("Nome Completo do Aluno:")

# Interface para as questões
respostas = []
cols = st.columns(len(gabarito_oficial))
for i, col in enumerate(cols):
    res = col.selectbox(f"Q{i+1}", ["", "A", "B", "C", "D", "E"], key=f"q{i}")
    respostas.append(res)

if st.button("Enviar Respostas"):
    if not nome or "" in respostas:
        st.error("Por favor, preencha o nome e todas as questões.")
    else:
        # Cálculo do resultado
        acertos = sum(1 for r, g in zip(respostas, gabarito_oficial) if r == g)
        nota = (acertos / len(gabarito_oficial)) * 10
        
        # 1. Ler os dados atuais da planilha
        dados_atuais = conn.read(spreadsheet="SUA_URL_DA_PLANILHA_OU_NOME")
        
        # 2. Criar a nova linha
        nova_linha = pd.DataFrame([{
            "Nome": nome,
            "Acertos": acertos,
            "Nota": nota
        }])
        
        # 3. Juntar o novo dado aos antigos
        dados_atualizados = pd.concat([dados_atuais, nova_linha], ignore_index=True)
        
        # 4. Salvar de volta na planilha
        conn.update(spreadsheet="SUA_URL_DA_PLANILHA_OU_NOME", data=dados_atualizados)
        
        st.success(f"Parabéns, {nome}! Suas respostas foram enviadas com sucesso.")
        st.balloons()