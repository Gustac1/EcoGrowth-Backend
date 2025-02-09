import random
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Caminho para o arquivo de credenciais do Service Account
cred = credentials.Certificate("/home/TCCGustavo/Documents/TCCGustavo - Raspberry/credentials/ecogrowth-772d4-firebase-adminsdk-ubo79-eef9fa5c2f.json")

# Inicialize o Firebase Admin SDK com as configurações e credenciais
firebase_admin.initialize_app(cred)

# Inicialize o Firestore
db = firestore.client()

# Função para gerar valor aleatório
def generate_random_value():
    return random.randint(0, 100)  # Altere o intervalo conforme necessário

# ID do documento que você deseja atualizar (pode ser gerado automaticamente)
document_id = "EG001"  # Substitua pelo ID correto ou gere dinamicamente

while True:
    # Gera um valor aleatório
    random_value = generate_random_value()

    # Referência ao documento no Firestore
    doc_ref = db.collection("Dispositivos").document(document_id)

    # Atualiza o valor no Firestore
    try:
        doc_ref.update({"numeroAleatorio": random_value})
        print(f"Valor atualizado para o documento {document_id}: {random_value}")
    except Exception as e:
        print(f"Erro ao atualizar valor: {str(e)}")

    # Espera 10 segundos antes da próxima atualização
    time.sleep(1)