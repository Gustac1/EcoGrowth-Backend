import sys
import time
import board

sys.path.append("/home/TCCGustavo/Documents/TCCGUSTAVO")

# Importa os sensores
from SENSORES.LUMINOSIDADE.BH1750 import BH1750
from SENSORES.UMIDADE_DO_SOLO.DS18B20 import DS18B20
from SENSORES.UMIDADE_E_TEMPERATURA.DHT22 import DHT22

# Inicializa os sensores
bh1750 = BH1750()
ds18b20 = DS18B20()
dht22 = DHT22(pin=board.D17)  # Agora inicializa corretamente

while True:
    try:
        # Leitura dos sensores com tratamento de erro
        try:
            luminosidade = bh1750.ler_luminosidade()
            if luminosidade is not None and luminosidade > 0:
                luminosidade = f"{luminosidade:.2f}"
            else:
                raise ValueError("Leitura inválida do BH1750")
        except Exception as e:
            luminosidade = "Erro na leitura"
            print(f"Erro no BH1750: {e}")

        try:
            temperatura_solo = ds18b20.read_temp()
            if temperatura_solo is not None:
                temperatura_solo = f"{temperatura_solo:.2f}"
            else:
                raise ValueError("Leitura inválida do DS18B20")
        except Exception as e:
            temperatura_solo = "Erro na leitura"
            print(f"Erro no DS18B20: {e}")

        try:
            temperatura_ar, umidade_ar = dht22.ler_dados()
            if temperatura_ar is not None and umidade_ar is not None:
                temperatura_ar = f"{temperatura_ar:.2f}"
                umidade_ar = f"{umidade_ar:.2f}"
            else:
                raise ValueError("Falha na leitura do DHT22")
        except Exception as e:
            temperatura_ar, umidade_ar = "Erro na leitura", "Erro na leitura"
            print(f"Erro no DHT22: {e}")

        print(f"Luminosidade: {luminosidade} lux")
        print(f"Temperatura do Solo: {temperatura_solo}°C")
        print(f"Temperatura do Ar: {temperatura_ar}°C | Umidade do Ar: {umidade_ar}%")
        print("-" * 40)

        time.sleep(5)  # Ajuste o tempo para evitar falha no DHT22

    except KeyboardInterrupt:
        print("\nLeitura interrompida pelo usuário.")
        break
    except Exception as e:
        print(f"Erro ao executar loop principal: {e}")
