import streamlit as st
import mysql.connector
import random
import requests
import json

# Lista de exames
EXAMES = [
    {"ID": "69347473316204", "Grupo": "BETA-HCG", "Nome": "BETA HCG"},
    {"ID": "161308206689966", "Grupo": "BIOQUÍMICA", "Nome": "FOSFATASE ALCALINA"},
    {"ID": "218896270091674", "Grupo": "BIOQUÍMICA", "Nome": "BILIRRUBINA DIRETA"},
    {"ID": "309865185389874", "Grupo": "BIOQUÍMICA", "Nome": "PROTEINA ALBUMINA"},
    {"ID": "32027115566935", "Grupo": "BIOQUÍMICA", "Nome": "PROTEINA GLOBULINA"},
    {"ID": "470607304467166", "Grupo": "BIOQUÍMICA", "Nome": "COLESTEROL TOTAL"},
    {"ID": "48167560717928", "Grupo": "BIOQUÍMICA", "Nome": "CREATININA"},
    {"ID": "501205959999498", "Grupo": "BIOQUÍMICA", "Nome": "ÁCIDO ÚRICO"},
    {"ID": "543176137635437", "Grupo": "BIOQUÍMICA", "Nome": "PROTEINAS TOTAIS"},
    {"ID": "563916064994522", "Grupo": "BIOQUÍMICA", "Nome": "BILIRRUBINA TOTAL"},
    {"ID": "572378907359477", "Grupo": "BIOQUÍMICA", "Nome": "UREIA"},
    {"ID": "647041511788721", "Grupo": "BIOQUÍMICA", "Nome": "PROTEINA RELAÇÃO A/G"},
    {"ID": "702599471081534", "Grupo": "BIOQUÍMICA", "Nome": "TRANSAMINASE PIRÚVICA - TGP"},
    {"ID": "712563827129545", "Grupo": "BIOQUÍMICA", "Nome": "BILIRRUBINA INDIRETA"},
    {"ID": "740049542317069", "Grupo": "BIOQUÍMICA", "Nome": "GLICEMIA"},
    {"ID": "874680618035055", "Grupo": "BIOQUÍMICA", "Nome": "TRANSAMINASE OXALACÉTICA - TGO"},
    {"ID": "916033777182842", "Grupo": "BIOQUÍMICA", "Nome": "TRIGLICÉRIDES"},
    {"ID": "180514982556270", "Grupo": "COAGULOGRAMA", "Nome": "COAGULOGRAMA RNI"},
    {"ID": "664919430870437", "Grupo": "COAGULOGRAMA", "Nome": "COAGULOGRAMA TEMPO DE PROTROMBINA (TAP)"},
    {"ID": "726177468482074", "Grupo": "COAGULOGRAMA", "Nome": "COAGULOGRAMA - RATIO"},
    {"ID": "75436436489072", "Grupo": "COAGULOGRAMA", "Nome": "COAGULOGRAMA TTPA"},
    {"ID": "975713350212038", "Grupo": "COAGULOGRAMA", "Nome": "COAGULOGRAMA ATIVIDADE DE PROTROMBINA"},
    {"ID": "194842003318165", "Grupo": "ELETROLITOS", "Nome": "CÁLCIO"},
    {"ID": "336533884498622", "Grupo": "ELETROLITOS", "Nome": "MAGNÉSIO"},
    {"ID": "340188762721737", "Grupo": "ELETROLITOS", "Nome": "SÓDIO"},
    {"ID": "454046226735374", "Grupo": "ELETROLITOS", "Nome": "POTÁSSIO"},
    {"ID": "239944994700252", "Grupo": "ERITROGRAMA", "Nome": "HCM"},
    {"ID": "320850121297525", "Grupo": "ERITROGRAMA", "Nome": "RDW"},
    {"ID": "675375492818318", "Grupo": "ERITROGRAMA", "Nome": "HEMATÓCRITO"},
    {"ID": "687080049427143", "Grupo": "ERITROGRAMA", "Nome": "CHCM"},
    {"ID": "709531324356465", "Grupo": "ERITROGRAMA", "Nome": "HEMOGLOBINA"},
    {"ID": "88351644527716", "Grupo": "ERITROGRAMA", "Nome": "HEMÁCIAS"},
    {"ID": "88994936389408", "Grupo": "ERITROGRAMA", "Nome": "VCM"},
    {"ID": "4111568332466", "Grupo": "FSH E ESTRADIOL", "Nome": "ESTRADIOL"},
    {"ID": "57096196972666", "Grupo": "FSH E ESTRADIOL", "Nome": "HORMÔNIO FOLÍCULO ESTIMULANTE - FSH"},
    {"ID": "12987826865678", "Grupo": "LEUCOGRAMA", "Nome": "MIELÓCITOS"},
    {"ID": "151203726417434", "Grupo": "LEUCOGRAMA", "Nome": "SEGMENTADOS"},
    {"ID": "252535059860071", "Grupo": "LEUCOGRAMA", "Nome": "MONÓCITOS"},
    {"ID": "26064283589319", "Grupo": "LEUCOGRAMA", "Nome": "BLASTOS"},
    {"ID": "46466895430103", "Grupo": "LEUCOGRAMA", "Nome": "BASÓFILOS"},
    {"ID": "486983854837953", "Grupo": "LEUCOGRAMA", "Nome": "LINFÓCITOS"},
    {"ID": "532306573295376", "Grupo": "LEUCOGRAMA", "Nome": "LINFÓCITOS ATÍPICOS"},
    {"ID": "58760558082170", "Grupo": "LEUCOGRAMA", "Nome": "BASTONETES"},
    {"ID": "728263932971656", "Grupo": "LEUCOGRAMA", "Nome": "LEUCÓCITOS"},
    {"ID": "770665478658018", "Grupo": "LEUCOGRAMA", "Nome": "PROMIELÓCITOS"},
    {"ID": "782074853964320", "Grupo": "LEUCOGRAMA", "Nome": "METAMIELÓCITOS"},
    {"ID": "9003121926942", "Grupo": "LEUCOGRAMA", "Nome": "EOSINÓFILOS"},
    {"ID": "95527918101395", "Grupo": "LEUCOGRAMA", "Nome": "NEUTRÓFILOS"},
    {"ID": "17015142045720", "Grupo": "OUTROS", "Nome": "TESTOSTERONA TOTAL"},
    {"ID": "465847456650166", "Grupo": "OUTROS", "Nome": "CREATINOFOSFOQUINASE - CPK"},
    {"ID": "90688435037507", "Grupo": "OUTROS", "Nome": "GAMA GLUTAMIL TRANSFERASE"},
    {"ID": "64524974674735", "Grupo": "PLAQUETAS", "Nome": "CONTAGEM DE PLAQUETAS"},
    {"ID": "618968867654597", "Grupo": "SOROLOGIA", "Nome": "HIV I + II ANTICORPO ANTI-PESQUISA"},
    {"ID": "833256258716987", "Grupo": "SOROLOGIA", "Nome": "ANTICORPO ANTI-HCV"},
    {"ID": "926602988933154", "Grupo": "SOROLOGIA", "Nome": "HEPATITE B HBSAG"},
    {"ID": "966742333908652", "Grupo": "SOROLOGIA", "Nome": "HBC IGM-ANTI"},
    {"ID": "145249020678016", "Grupo": "URINA TIPO I", "Nome": "URINA TIPO I - GLICOSE"},
    {"ID": "190364983573151", "Grupo": "URINA TIPO I", "Nome": "URINA TIPO I - DENSIDADE"},
    {"ID": "27665274546861", "Grupo": "URINA TIPO I", "Nome": "URINA TIPO I - CETONAS"},
    {"ID": "34088485628205", "Grupo": "URINA TIPO I", "Nome": "URINA TIPO I - CILINDROS"},
    {"ID": "350554347265881", "Grupo": "URINA TIPO I", "Nome": "URINA TIPO I - CRISTAIS"},
    {"ID": "514815544639654", "Grupo": "URINA TIPO I", "Nome": "URINA  TIPO I - SANGUE OCULTO"},
    {"ID": "70848222330219", "Grupo": "URINA TIPO I", "Nome": "URINA TIPO I - PH"},
    {"ID": "791367154216307", "Grupo": "URINA TIPO I", "Nome": "URINA TIPO I - LEUCÓCITOS"},
    {"ID": "827897628405054", "Grupo": "URINA TIPO I", "Nome": "URINA TIPO I - UROBILINOGÊNIO"},
    {"ID": "846263766068434", "Grupo": "URINA TIPO I", "Nome": "URINA TIPO I - PROTEÍNAS"},
    {"ID": "93685258983146", "Grupo": "URINA TIPO I", "Nome": "URINA TIPO I - BILIRRUBINAS"},
    {"ID": "938340491088770", "Grupo": "URINA TIPO I", "Nome": "URINA TIPO I - NITRITO"},
    {"ID": "99252312640714", "Grupo": "URINA TIPO I", "Nome": "URINA TIPO I - HEMÁCIAS"},
]

# Agrupa os exames por grupo
exames_por_grupo = {}
for exame in EXAMES:
    grupo = exame["Grupo"]
    exames_por_grupo.setdefault(grupo, []).append(exame)

# Conexão com banco
def get_db_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        database=st.secrets["mysql"]["database"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        port=st.secrets["mysql"]["port"]
    )

def generate_service_order():
    return str(random.randint(10000000, 99999999))

def get_par_exam_request(cpf_participant):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID_PARTICIPANT FROM PARTICIPANT WHERE CPF = %s", (cpf_participant,))
    participant_id = cur.fetchone()
    
    if not participant_id:
        return None, "❌ Participante não encontrado."
    
    cur.execute("""
        SELECT PAR_EXAM_REQUEST FROM PAR_EXAM_REQUEST
        WHERE ID_PARTICIPANT = %s AND STATUS = 'REQUESTED'
        ORDER BY CREATED_AT DESC LIMIT 1
    """, (participant_id[0],))
    par_exam_request = cur.fetchone()
    
    cur.close()
    conn.close()

    if not par_exam_request:
        return None, "❌ Nenhuma solicitação de exame pendente."
    
    return par_exam_request[0], None

def get_or_update_service_order(parExamRequestId):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT SERVICE_ORDER FROM PAR_EXAM_REQUEST WHERE PAR_EXAM_REQUEST = %s", (parExamRequestId,))
    service_order = cur.fetchone()

    if service_order and service_order[0]:
        cur.close()
        conn.close()
        return service_order[0]

    new_service_order = generate_service_order()
    cur.execute("UPDATE PAR_EXAM_REQUEST SET SERVICE_ORDER = %s WHERE PAR_EXAM_REQUEST = %s", (new_service_order, parExamRequestId))
    conn.commit()
    cur.close()
    conn.close()

    return new_service_order

# Login com secrets
def login():
    if "tentativa_login" not in st.session_state:
        st.session_state["tentativa_login"] = False

    with st.form("login_form"):
        st.markdown("## 🔐 Acesso Restrito")
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        entrar = st.form_submit_button("Entrar")

        if entrar:
            usuario_valido = st.secrets["auth"]["usuario"]
            senha_valida = st.secrets["auth"]["senha"]
            if usuario == usuario_valido and senha == senha_valida:
                st.session_state["logado"] = True
            else:
                st.session_state["tentativa_login"] = True

    if st.session_state["tentativa_login"] and not st.session_state.get("logado", False):
        st.error("Usuário ou senha incorretos.")

# App principal
def main():
    st.title("🩺 Resultados de Exames do CDL")
    cpf = st.text_input("CPF do PP (somente números)", max_chars=11)

    if cpf:
        par_exam_request, erro = get_par_exam_request(cpf)
        if erro:
            st.error(erro)
            st.stop()

        service_order = get_or_update_service_order(par_exam_request)

        st.success("✅ Dados recuperados com sucesso.")
        st.markdown(f"**📄 parExamRequestId:** `{par_exam_request}`")
        st.markdown(f"**📄 serviceOrder:** `{service_order}`")

        st.markdown("### 🧪 Selecione os grupos de exame:")
        grupos_selecionados = {}
        for grupo in exames_por_grupo:
            grupos_selecionados[grupo] = st.checkbox(grupo)

        with st.form("form_exames"):
            st.markdown("### ✍️ Preencha os resultados:")
            resultados = []

            for grupo, selecionado in grupos_selecionados.items():
                if selecionado:
                    st.subheader(grupo)
                    for exame in exames_por_grupo[grupo]:
                        resultado = st.text_input(f"{exame['Nome']}", key=exame["ID"])
                        if resultado:
                            resultados.append({
                                "examId": exame["ID"],
                                "result": resultado
                            })

            enviado = st.form_submit_button("Salvar e Enviar para a API")

        if enviado:
            if not resultados:
                st.warning("⚠️ Nenhum exame preenchido.")
            else:
                dados_json = [{
                    "parExamRequestId": par_exam_request,
                    "serviceOrder": service_order,
                    "results": resultados
                }]

                st.info("📡 Enviando dados para a API...")

                try:
                    response = requests.put(
                        url=st.secrets["api"]["url"],
                        json=dados_json,
                        headers={
                            "Content-Type": "application/json",
                            "x-api-key": st.secrets["api"]["key"]
                        },
                        timeout=15
                    )

                    if response.status_code == 200:
                        st.success("✅ Resultados enviados com sucesso!")
                        try:
                            st.json(response.json())
                        except:
                            st.info("Resposta recebida da API:")
                            st.text(response.text)
                    else:
                        st.error(f"❌ Erro ao enviar dados. Código {response.status_code}")
                        st.text(response.text)

                except Exception as e:
                    st.error(f"Erro de comunicação com a API: {str(e)}")

                st.stop()
    else:
        st.info("🔐 Por favor, insira o CPF e aperte Enter ↵ para continuar.")

# Controle de sessão
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if st.session_state["logado"]:
    main()
else:
    login()
