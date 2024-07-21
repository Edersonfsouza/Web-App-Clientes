import streamlit as st
from supabase import create_client, Client
import secrets
from datetime import datetime

# Gera uma chave segura de 32 bytes e a converte para uma string hexadecimal
cookie_key = secrets.token_hex(32)

# Configuração do Supabase
url = "https://erzycfiodrtrwthjtpdn.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVyenljZmlvZHJ0cnd0aGp0cGRuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjE1NzExMjUsImV4cCI6MjAzNzE0NzEyNX0.0O_m5WOjz0DsrDuzz0ChJfsZA_7v1pDP6vLQXl7YpNo"
supabase: Client = create_client(url, key)

# Função para salvar os dados no Supabase
def salvar_dados(clientes, cheque, valor, agencia, cod, emissao, vencimento, titular):
    # Converte as datas para formato de string
    emissao_str = emissao.strftime('%Y-%m-%d') if emissao else None
    vencimento_str = vencimento.strftime('%Y-%m-%d') if vencimento else None
    
    data = {
        "clientes": clientes,
        "cheque": cheque,
        "valor": valor,
        "agencia": agencia,
        "cod": cod,
        "emissao": emissao_str,
        "vencimento": vencimento_str,
        "titular": titular
    }

    response = supabase.table('registro_clientes').insert(data).execute()
    
    if response == True:
        st.success("Dados enviados com sucesso!")
    else:
        st.success("Dados enviados com sucesso!")

# Tela de Cadastro
st.title("Cadastro de Cheques")

with st.form("signup_form"):
    clientes = st.text_input("Cliente")
    cheque = st.text_input("Cheque")
    valor = st.text_input("Valor")
    agencia = st.text_input("Agência")
    cod = st.text_input("Código")
    emissao = st.date_input("Data de Emissão")
    vencimento = st.date_input("Data de Vencimento")
    titular = st.text_input("Titular")

    submit_button = st.form_submit_button("Registrar")

if submit_button:
    if clientes and cheque and valor and agencia and cod and emissao and vencimento and titular:
        salvar_dados(clientes, cheque, valor, agencia, cod, emissao, vencimento, titular)
    else:
        st.error("Por favor, preencha todos os campos.")
