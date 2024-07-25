import streamlit as st
from supabase import create_client, Client
import datetime

# Configuração do Supabase
url = "https://erzycfiodrtrwthjtpdn.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVyenljZmlvZHJ0cnd0aGp0cGRuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjE1NzExMjUsImV4cCI6MjAzNzE0NzEyNX0.0O_m5WOjz0DsrDuzz0ChJfsZA_7v1pDP6vLQXl7YpNo"
supabase: Client = create_client(url, key)

# Função para buscar clientes do banco de dados
def fetch_clients():
    try:
        response = supabase.table('registro_cheques').select('clientes').execute()
        if response.data:
            return [client['clientes'] for client in response.data]
        else:
            st.error("Erro ao buscar clientes do banco de dados")
            return []
    except Exception as e:
        st.error(f"Erro ao buscar clientes: {e}")
        return []

# Função para inicializar chaves no session_state
def initialize_session_state(keys):
    for key in keys:
        if key not in st.session_state:
            st.session_state[key] = ''

initialize_session_state([
    'clientes', 'cheque', 'valor', 'agencia', 'cod', 'titular',
    'endereco', 'telefone', 'telefone2', 'telefone3', 'cpf', 'cep', 'email'
])

# Função para limpar os campos do formulário
def clear_form():
    for key in [
        'clientes', 'cheque', 'valor', 'agencia', 'cod', 'titular',
        'endereco', 'telefone', 'telefone2', 'telefone3', 'cpf', 'cep', 'email'
    ]:
        st.session_state[key] = ''

def insert_into_cheques(data):
    try:
        # Converte datas para strings no formato ISO
        if 'emissao' in data and isinstance(data['emissao'], datetime.date):
            data['emissao'] = data['emissao'].isoformat()
        if 'vencimento' in data and isinstance(data['vencimento'], datetime.date):
            data['vencimento'] = data['vencimento'].isoformat()

        response = supabase.table('registro_cheques').insert(data).execute()
        if response.status_code == 201:
            st.success("Cheque registrado com sucesso!")
        else:
            st.error(f"Erro ao registrar cheque: {response.status_code} - {response.data}")
    except Exception as e:
        st.error(f"Erro ao registrar cheque: {e}")

# Função para exibir a página de cadastro de cheques
def show_cheque_form():
    st.title('Cadastro de Cheques')
    with st.form(key='cheque_form', clear_on_submit=True):
        clientes = st.text_input("Nome do Cliente", key='clientes')
        cheque = st.text_input("Cheque", key='cheque')
        valor = st.text_input("Valor", key='valor')
        agencia = st.text_input("Agência", key='agencia')
        cod = st.text_input("Código", key='cod')
        emissao = st.date_input("Data de Emissão", key='emissao')
        vencimento = st.date_input("Data de Vencimento", key='vencimento')
        titular = st.text_input("Titular", key='titular')

        registrar = st.form_submit_button('Registrar', type="primary")

    # Lógica de confirmação
    if registrar:
        if clientes and cheque and valor and agencia and cod and emissao and vencimento and titular:
            with st.form(key='confirmation_form'):
                st.write("Você tem certeza de que deseja realizar esta ação?")
                col1, col2 = st.columns(2)
                with col1:
                    confirm = st.form_submit_button("Confirmar")
                with col2:
                    cancel = st.form_submit_button("Cancelar")

                if confirm:
                    data = {
                        'clientes': clientes,
                        'cheque': cheque,
                        'valor': valor,
                        'agencia': agencia,
                        'cod': cod,
                        'emissao': emissao,
                        'vencimento': vencimento,
                        'titular': titular
                    }
                    insert_into_cheques(data)
                    clear_form()
                    st.success('Dados salvos com sucesso !')
                elif cancel:
                    st.info("Ação cancelada.")
        else:
            st.error("Por favor, preencha todos os campos.")

def insert_into_clientes(data):
    try:
        # Converte datas para strings no formato ISO
        if 'data_cadastro' in data and isinstance(data['data_cadastro'], datetime.date):
            data['data_cadastro'] = data['data_cadastro'].isoformat()

        response = supabase.table('registro_clientes').insert(data).execute()
        if response.status_code == 201:
            st.success("Cliente registrado com sucesso!")
        else:
            st.error(f"Erro ao registrar cliente: {response.status_code}")
    except Exception as e:
        st.error(f"Erro ao registrar cliente: {e}")

# Função para exibir a página de cadastro de clientes
def show_cliente_form():
    st.title('Cadastro de Clientes')
    # Buscar clientes do banco de dados
    clientes = fetch_clients()
    
    with st.form(key='cliente_form', clear_on_submit=True):
        selected_cliente = st.selectbox('Selecionar cliente', options=clientes)
        cod = st.text_input("Código", key='cod')
        endereco = st.text_input("Endereço", key='endereco')
        telefone_comercial = st.text_input("Telefone comercial", placeholder="(xx) xxxxx-xxxx", key='telefone')
        telefone_residencial = st.text_input("Telefone residencial", placeholder="(xx) xxxxx-xxxx", key='telefone2')
        telefone_celular = st.text_input("Telefone celular", placeholder="(xx) xxxxx-xxxx", key='telefone3')
        cpf = st.text_input("Digite seu CPF", placeholder="000.000.000-00", key='cpf')
        cep = st.text_input("Digite seu CEP", placeholder="00000-000", key='cep')
        email = st.text_input("Digite seu Email", key='email')
        data_cadastro = st.date_input("Data do cadastro", key='data_cadastro')

        finalizar = st.form_submit_button('Registrar', type="primary")

        # Lógica de confirmação
        if finalizar:
            if selected_cliente and cod and telefone_comercial and telefone_residencial and telefone_celular and endereco and cpf and cep and email and data_cadastro:
                with st.form(key='confirmation_form'):
                    st.write("Você tem certeza de que deseja realizar esta ação?")
                    col1, col2 = st.columns(2)
                    with col1:
                        confirm = st.form_submit_button("Confirmar")
                    with col2:
                        cancel = st.form_submit_button("Cancelar")

                    if confirm:
                        data = {
                            'cliente': selected_cliente,
                            'cod': cod,
                            'endereco': endereco,
                            'telefone_comercial': telefone_comercial,
                            'telefone_residencial': telefone_residencial,
                            'telefone_celular': telefone_celular,
                            'cpf': cpf,
                            'cep': cep,
                            'email': email,
                            'data_cadastro': data_cadastro
                        }
                        insert_into_clientes(data)
                        clear_form()
                        st.success('Dados salvos com sucesso !')
                    elif cancel:
                        st.info("Ação cancelada.")
            else:
                st.error("Por favor, preencha todos os campos.")

# Função para exibir a página inicial
def show_home_page():
    st.title('Teste')

# Função para exibir a sidebar
def show_sidebar():
    st.sidebar.title('Registros')
    if st.sidebar.button('Página inicial'):
        st.session_state.current_page = 'home'
    if st.sidebar.button('Cheques'):
        st.session_state.current_page = 'cheque_form'
    if st.sidebar.button('Clientes'):
        st.session_state.current_page = 'cliente_form'

# Verifica se o estado 'current_page' existe no session_state, caso contrário, define como 'home'
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Exibe a sidebar e o conteúdo principal
show_sidebar()

# Navegação entre páginas
if st.session_state.current_page == 'cliente_form': 
    show_cliente_form()
elif st.session_state.current_page == 'cheque_form':
    show_cheque_form()
else:
    show_home_page()
