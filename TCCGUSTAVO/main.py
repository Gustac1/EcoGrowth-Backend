import time
import threading
import board
from SENSORES.LUMINOSIDADE.BH1750 import BH1750
from SENSORES.UMIDADE_DO_SOLO.DS18B20 import DS18B20
from SENSORES.UMIDADE_E_TEMPERATURA.DHT22 import DHT22
from FIREBASE.firebase_config import enviar_dados  # Importa a função de envio de dados para o Firebase

# Identificador da estufa (pode ser alterado para "EG002", "EG003", etc.)
estufa_id = "EG001"

# Inicializa os sensores
luminosidade_sensor = BH1750()
temperatura_solo_sensor = DS18B20()
temperatura_ar_sensor = DHT22(pin=board.D17)

def coletar_dados():
    """ Coleta os dados dos sensores e envia para o Firebase """
    while True:
        try:
            # Leitura dos sensores
            lux = luminosidade_sensor.ler_luminosidade()
            temperatura_solo = temperatura_solo_sensor.read_temp()
            temperatura_ar, umidade_ar = temperatura_ar_sensor.ler_dados()
            
            # Validação das leituras e formatação para duas casas decimais
            lux = round(lux, 2) if lux is not None else None
            temperatura_solo = round(temperatura_solo, 2) if temperatura_solo is not None else None
            temperatura_ar = round(temperatura_ar, 2) if temperatura_ar is not None else None
            umidade_ar = round(umidade_ar, 2) if umidade_ar is not None else None
            
            # Dados a serem enviados ao Firebase
            dados_sensor = {
                'estufa_id': estufa_id,
                'lux': lux,
                'temperatura_solo': temperatura_solo,
                'temperatura_ar': temperatura_ar,
                'umidade_ar': umidade_ar,
                'timestamp': round(time.time(), 2)
            }
            
            # Enviar os dados para o Firebase
            enviar_dados(dados_sensor)
            print(f"Dados enviados: {dados_sensor}")
        
        except Exception as e:
            print(f"Erro ao coletar dados dos sensores: {e}")
        
        # Aguardar 5 segundos antes da próxima leitura
        time.sleep(5)

if __name__ == "__main__":
    thread_coleta = threading.Thread(target=coletar_dados)
    thread_coleta.start()
