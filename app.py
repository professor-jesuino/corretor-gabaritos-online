import streamlit as st

st.title("📝 Portal do Aluno - Gabarito")

nome = st.text_input("Digite seu nome completo:")
gabarito_oficial = ['A', 'B', 'C', 'D', 'E']
respostas = []

# Cria colunas para as questões ficarem bonitas lado a lado
cols = st.columns(len(gabarito_oficial))

for i, col in enumerate(cols):
    res = col.selectbox(f"Q{i+1}", ["", "A", "B", "C", "D", "E"], key=i)
    respostas.append(res)

if st.button("Enviar Respostas"):
    if "" in respostas:
        st.warning("Por favor, responda todas as questões.")
    else:
        acertos = sum(1 for r, g in zip(respostas, gabarito_oficial) if r == g)
        st.success(f"Obrigado, {nome}! Você acertou {acertos} questões.")
        
        # Aqui você poderia integrar com uma planilha do Google para salvar!