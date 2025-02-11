import time
import threading
import board
from SENSORES.LUMINOSIDADE.BH1750 import BH1750
from SENSORES.UMIDADE_DO_SOLO.DS18B20 import DS18B20
from SENSORES.UMIDADE_E_TEMPERATURA.DHT22 import DHT22
from FIREBASE.firebase_config import enviar_dados_realtime, enviar_dados_firestore

# 🔥 Identificador da estufa
estufa_id = "EG001"

# 🔥 Inicializa os sensores
luminosidade_sensor = BH1750()
temperatura_solo_sensor = DS18B20()
temperatura_ar_sensor = DHT22(pin=board.D17)

# 🔥 Buffer para armazenar leituras antes do envio ao Firestore (histórico)
buffer_sensores = {
    "Luminosidade": [],
    "TemperaturaDoSolo": [],
    "Temperatura": [],
    "Umidade": []
}

def coletar_dados():
    """ Coleta os dados dos sensores e envia os valores atuais para o Realtime Database. """
    while True:
        try:
            # 🔥 Leitura dos sensores
            lux = luminosidade_sensor.ler_luminosidade()
            temperatura_solo = temperatura_solo_sensor.read_temp()
            temperatura_ar, umidade_ar = temperatura_ar_sensor.ler_dados()
            
            # 🔥 Validação e arredondamento
            lux = round(lux, 2) if lux is not None else None
            temperatura_solo = round(temperatura_solo, 2) if temperatura_solo is not None else None
            temperatura_ar = round(temperatura_ar, 2) if temperatura_ar is not None else None
            umidade_ar = round(umidade_ar, 2) if umidade_ar is not None else None
            
            # 🔥 Atualiza os valores atuais no Realtime Database
            dados_atuais = {
                "LuminosidadeAtual": lux,
                "TemperaturaDoArAtual": temperatura_ar,
                "UmidadeDoArAtual": umidade_ar,
                "TemperaturaDoSoloAtual": temperatura_solo,
                "timestamp": round(time.time(), 2)
            }

            enviar_dados_realtime(estufa_id, dados_atuais)  # 🔥 Atualiza valores em tempo real

            # 🔥 Armazena os valores no buffer para histórico
            if lux is not None: buffer_sensores["Luminosidade"].append(lux)
            if temperatura_solo is not None: buffer_sensores["TemperaturaDoSolo"].append(temperatura_solo)
            if temperatura_ar is not None: buffer_sensores["Temperatura"].append(temperatura_ar)
            if umidade_ar is not None: buffer_sensores["Umidade"].append(umidade_ar)

        except Exception as e:
            print(f"⚠️ Erro ao coletar dados dos sensores: {e}")
        
        time.sleep(30)  # 🔥 Aguardar 30 segundos antes da próxima leitura

def enviar_dados_periodicamente():
    """ A cada 5 minutos, calcula a média dos sensores e envia para o Firestore. """
    while True:
        try:
            if len(buffer_sensores["Luminosidade"]) >= 5:
                media_dados = {
                    "Luminosidade": sum(buffer_sensores["Luminosidade"]) / len(buffer_sensores["Luminosidade"]),
                    "TemperaturaDoSolo": sum(buffer_sensores["TemperaturaDoSolo"]) / len(buffer_sensores["TemperaturaDoSolo"]),
                    "Temperatura": sum(buffer_sensores["Temperatura"]) / len(buffer_sensores["Temperatura"]),
                    "Umidade": sum(buffer_sensores["Umidade"]) / len(buffer_sensores["Umidade"]),
                    "timestamp": round(time.time(), 2)
                }

                for key in buffer_sensores:
                    buffer_sensores[key].clear()  # 🔥 Limpa buffers após envio

                enviar_dados_firestore(estufa_id, media_dados)  # 🔥 Envia ao Firestore
                print(f"✅ Média enviada ao Firestore: {media_dados}")

        except Exception as e:
            print(f"⚠️ Erro ao enviar dados para o Firestore: {e}")

        time.sleep(300)  # 🔥 Enviar a cada 5 minutos

if __name__ == "__main__":
    thread_coleta = threading.Thread(target=coletar_dados)
    thread_envio = threading.Thread(target=enviar_dados_periodicamente)

    thread_coleta.start()
    thread_envio.start()
