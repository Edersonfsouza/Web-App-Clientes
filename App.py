import streamlit as st
from supabase import create_client, Client
import datetime

# Configuração do Supabase
url = "https://erzycfiodrtrwthjtpdn.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVyenljZmlvZHJ0cnd0aGp0cGRuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjE1NzExMjUsImV4cCI6MjAzNzE0NzEyNX0.0O_m5WOjz0DsrDuzz0ChJfsZA_7v1pDP6vLQXl7YpNo"
supabase: Client = create_client(url, key)

# Inicializando o estado da aplicação
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}
if 'show_confirmation' not in st.session_state:
    st.session_state.show_confirmation = False

# Função para buscar clientes do banco de dados (a partir da tabela de cheques)
def fetch_clients_from_cheques():
    try:
        response = supabase.table('registro_cheques').select('clientes').execute()
        if response.data:
            return list(set(client['clientes'] for client in response.data))
        else:
            st.error("Erro ao buscar clientes do banco de dados")
            return []
    except Exception as e:
        st.error(f"Erro ao buscar clientes: {e}")
        return []

# Função para verificar duplicação na tabela de cheques
def check_duplicate_check(clientes, cheque, valor, agencia, cod, emissao, vencimento, titular):
    try:
        response = supabase.table('registro_cheques').select('*').eq('clientes', clientes).eq('cheque', cheque).eq('valor', valor).eq('agencia', agencia).eq('cod', cod).eq('emissao', emissao).eq('vencimento', vencimento).eq('titular', titular).execute()
        if response.data:
            return True  # Duplicata encontrada
        return False
    except Exception as e:
        st.error(f"Erro ao verificar duplicação: {e}")
        return True

# Função para verificar duplicação na tabela de clientes
def check_duplicate_client(cod, cpf, email):
    try:
        response = supabase.table('registro_clientes').select('*').eq('cod', cod).eq('cpf', cpf).eq('email', email).execute()
        if response.data:
            return True  # Duplicata encontrada
        return False
    except Exception as e:
        st.error(f"Erro ao verificar duplicação: {e}")
        return True

# Função para salvar dados na tabela de cheques
def save_check_data(clientes, cheque, valor, agencia, cod, emissao, vencimento, titular):
    if check_duplicate_check(clientes, cheque, valor, agencia, cod, emissao, vencimento, titular):
        st.error("Erro: Este cheque já está registrado no sistema.")
        return False
    
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

    try:
        response = supabase.table('registro_cheques').insert(data).execute()
        if response.data:
            return True
        else:
            st.error(f"Erro ao salvar dados: {response}")
            return False
    except Exception as e:
        st.error(f"Erro ao salvar dados: {e}")
        return False

# Função para salvar dados na tabela de clientes
def save_client_data(cliente_selecionado, cod, endereco, telefone_comercial, telefone_residencial, telefone_celular, cpf, cep, email, data_cadastro):
    if check_duplicate_client(cod, cpf, email):
        st.error("Erro: Este cliente já está registrado no sistema.")
        return False
    
    data_cadastro_str = data_cadastro.strftime('%Y-%m-%d') if data_cadastro else None
    
    data = {
        "cliente": cliente_selecionado,
        "cod": cod,
        "endereco": endereco,
        "telefone_comercial": telefone_comercial,
        "telefone_residencial": telefone_residencial,
        "telefone_celular": telefone_celular,
        "cpf": cpf,
        "cep": cep,
        "email": email,
        "data_cadastro": data_cadastro_str
    }

    try:
        response = supabase.table('registro_clientes').insert(data).execute()
        if response.data:
            return True
        else:
            st.error(f"Erro ao salvar cliente: {response}")
            return False
    except Exception as e:
        st.error(f"Erro ao salvar cliente: {e}")
        return False

# Função para exibir a página de cadastro de cheques
def show_check_form():
    st.title('Cadastro de Cheques')
    with st.form(key='check_form', clear_on_submit=True):
        clientes = st.text_input("Nome do Cliente", key='clientes')
        cheque = st.text_input("Cheque", key='cheque')
        valor = st.text_input("Valor", key='valor')
        agencia = st.text_input("Agência", key='agencia')
        cod = st.text_input("Código", key='cod')
        emissao = st.date_input("Data de Emissão", key='emissao')
        vencimento = st.date_input("Data de Vencimento", key='vencimento')
        titular = st.text_input("Titular", key='titular')

        registrar = st.form_submit_button('Registrar', type="primary")

    if registrar:
        if clientes and cheque and valor and agencia and cod and emissao and vencimento and titular:
            st.session_state.form_data = {
                'clientes': clientes, 'cheque': cheque, 'valor': valor, 
                'agencia': agencia, 'cod': cod, 'emissao': emissao, 
                'vencimento': vencimento, 'titular': titular
            }
            st.session_state.show_confirmation = True
        else:
            st.error("Por favor, preencha todos os campos.")

    if st.session_state.show_confirmation:
        with st.form(key='confirmation_form'):
            st.write("Você tem certeza de que deseja realizar esta ação?")
            col1, col2 = st.columns(2)
            with col1:
                confirm = st.form_submit_button("Confirmar",  type="primary")
            with col2:
                cancel = st.form_submit_button("Cancelar")

            if confirm:
                form_data = st.session_state.form_data
                success = save_check_data(
                    form_data['clientes'], form_data['cheque'], form_data['valor'], 
                    form_data['agencia'], form_data['cod'], form_data['emissao'], 
                    form_data['vencimento'], form_data['titular']
                )
                st.session_state.show_confirmation = False
                if success:
                    st.success('Dados salvos com sucesso', icon="✅")
                clear_form()
            elif cancel:
                st.info("Ação cancelada.")
                st.session_state.show_confirmation = False

# Função para exibir a página de cadastro de clientes
def show_client_form():
    st.title('Cadastro de Clientes')
    clientes = fetch_clients_from_cheques()
    
    with st.form(key='client_form', clear_on_submit=True):
        cliente_selecionado = st.selectbox('Nome do Cliente', options=clientes, key='cliente_selecionado')
        cod = st.text_input("Código", key='cod')
        endereco = st.text_input("Endereço", key='endereco')
        telefone_comercial = st.text_input("Telefone Comercial", placeholder="(xx) xxxxx-xxxx", key='telefone')
        telefone_residencial = st.text_input("Telefone Residencial", placeholder="(xx) xxxxx-xxxx", key='telefone2')
        telefone_celular = st.text_input("Telefone Celular", placeholder="(xx) xxxxx-xxxx", key='telefone3')
        cpf = st.text_input("CPF", placeholder="000.000.000-00", key='cpf')
        cep = st.text_input("CEP", placeholder="00000-000", key='cep')
        email = st.text_input("Email", key='email')
        data_cadastro = st.date_input("Data do Cadastro", key='data_cadastro')

        finalizar = st.form_submit_button('Registrar',  type="primary")

        if finalizar:
            if cod and endereco and telefone_comercial and telefone_residencial and telefone_celular and cpf and cep and email and data_cadastro:
                st.session_state.form_data = {
                    'cliente_selecionado': cliente_selecionado, 'cod': cod, 'endereco': endereco, 
                    'telefone_comercial': telefone_comercial, 'telefone_residencial': telefone_residencial, 
                    'telefone_celular': telefone_celular, 'cpf': cpf, 'cep': cep, 
                    'email': email, 'data_cadastro': data_cadastro
                }
                st.session_state.show_confirmation = True
            else:
                st.error("Por favor, preencha todos os campos.")

    if st.session_state.show_confirmation:
        with st.form(key='confirmation_form'):
            st.write("Você tem certeza de que deseja realizar esta ação?")
            col1, col2 = st.columns(2)
            with col1:
                confirm = st.form_submit_button("Confirmar",  type="primary")
            with col2:
                cancel = st.form_submit_button("Cancelar")

            if confirm:
                form_data = st.session_state.form_data
                success = save_client_data(
                    form_data['cliente_selecionado'], form_data['cod'], form_data['endereco'], 
                    form_data['telefone_comercial'], form_data['telefone_residencial'], 
                    form_data['telefone_celular'], form_data['cpf'], form_data['cep'], 
                    form_data['email'], form_data['data_cadastro']
                )
                st.session_state.show_confirmation = False
                if success:
                    st.success('Dados salvos com sucesso', icon="✅")
                clear_form()
            elif cancel:
                st.info("Ação cancelada.")
                st.session_state.show_confirmation = False

# Função para limpar os campos do formulário
def clear_form():
    keys_to_clear = [
        'cliente', 'clientes', 'cheque', 'valor', 'agencia', 'cod', 'titular',
        'endereco', 'telefone', 'telefone2', 'telefone3', 'cpf', 'cep', 'email'
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

# Função para exibir a página inicial
def show_home_page():
    st.title('Página Inicial')

# Função para exibir a sidebar
def show_sidebar():
    st.sidebar.title('Registros')
    if st.sidebar.button('Página Inicial'):
        st.session_state.current_page = 'home'
    if st.sidebar.button('Cheques'):
        st.session_state.current_page = 'check_form'
    if st.sidebar.button('Clientes'):
        st.session_state.current_page = 'client_form'

# Exibe a sidebar e o conteúdo principal
show_sidebar()

# Navegação entre páginas
if st.session_state.current_page == 'client_form':
    show_client_form()
elif st.session_state.current_page == 'check_form':
    show_check_form()
else:
    show_home_page()
