import firebase_admin
from firebase_admin import credentials, firestore

# Caminho para o arquivo de credenciais do Firebase
CREDENCIAIS_PATH = "TCCGUSTAVO/CREDENCIAIS/ecogrowth-772d4-firebase-adminsdk-ubo79-eef9fa5c2f.json"

# Inicializa o Firebase apenas se ainda não estiver inicializado
if not firebase_admin._apps:
    cred = credentials.Certificate(CREDENCIAIS_PATH)
    firebase_admin.initialize_app(cred)

# Conecta ao Firestore
db = firestore.client()

def enviar_dados(dados):
    """
    Envia os dados dos sensores para o Firebase Firestore.
    
    :param dados: Dicionário contendo os valores de luminosidade, temperatura e umidade.
    """
    try:
        estufa_id = dados.get("estufa_id", "EG001")  # Usa um ID padrão se não informado
        
        # Mapeamento correto dos nomes das variáveis
        sensores = {
            "Luminosidade": ("lux", "LuminosidadeAtual"),
            "Temperatura": ("temperatura_ar", "TemperaturaDoArAtual"),
            "Umidade": ("umidade_ar", "UmidadeDoArAtual"),
            "TemperaturaDoSolo": ("temperatura_solo", "TemperaturaDoSoloAtual")
        }

        for sensor, (campo_dado, campo_firebase) in sensores.items():
            valor = dados.get(campo_dado)

            if valor is not None:
                # Atualiza os dados mais recentes no documento correspondente
                doc_ref = db.collection("Dispositivos").document(estufa_id).collection("Dados").document(sensor)
                doc_ref.set({campo_firebase: valor}, merge=True)

                # Salva o histórico dentro de "Dados/{Sensor}/Historico"
                historico_ref = db.collection("Dispositivos").document(estufa_id).collection("Dados").document(sensor).collection("Historico").document()
                historico_ref.set({
                    campo_firebase: valor,
                    "timestamp": firestore.SERVER_TIMESTAMP  # Adiciona timestamp automático
                })

        print("✅ Dados enviados ao Firebase com sucesso!")

    except Exception as e:
        print(f"⚠️ Erro ao enviar dados para o Firebase: {e}")
