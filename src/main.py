import machine
import dht
import time

## Configuração das Portas
PIN_DHT      = 15
PIN_BUZZER   = 13
PIN_BUTTON   = 18 
PIN_LED_RED  = 12
PIN_LED_YEL  = 14
PIN_LED_GRN  = 27
PIN_SCL      = 22
PIN_SDA      = 21

# Limiares de Engenharia (Ação Corretiva)
TEMP_CRITICA = 45.0 # Risco de fissura térmica (Calor de hidratação)
UMID_CRITICA = 60.0 # Risco de retração plástica (Secagem rápida)

# Limiares de Atenção (Ação Preventiva)
TEMP_AVISO = 40.0
UMID_AVISO = 65.0

INTERVALO = 2000 

class MiniLCD:
    def __init__(self, scl_pin, sda_pin, addr=0x27):
        self.i2c  = machine.SoftI2C(scl=machine.Pin(scl_pin), sda=machine.Pin(sda_pin), freq=100000)
        self.addr = addr
        time.sleep_ms(50)
        for cmd in (0x33, 0x32, 0x28, 0x0C, 0x06, 0x01):
            self._write(cmd, 0)
            time.sleep_ms(2)

    def _write(self, val, mode):
        h = mode | (val & 0xF0) | 0x08 
        l = mode | ((val << 4) & 0xF0) | 0x08
        self.i2c.writeto(self.addr, bytes([h | 0x04, h & ~0x04, l | 0x04, l & ~0x04]))

    def puts(self, text, line=0):
        text = text[:16]
        while len(text) < 16: text += " "
        self._write(0x80 if line == 0 else 0xC0, 0)
        for c in text: self._write(ord(c), 1)


lcd = MiniLCD(scl_pin=PIN_SCL, sda_pin=PIN_SDA)
sensor = dht.DHT22(machine.Pin(PIN_DHT))
led_r = machine.Pin(PIN_LED_RED, machine.Pin.OUT)
led_y = machine.Pin(PIN_LED_YEL, machine.Pin.OUT)
led_g = machine.Pin(PIN_LED_GRN, machine.Pin.OUT)
btn_mute = machine.Pin(PIN_BUTTON, machine.Pin.IN, machine.Pin.PULL_UP)

buzzer = machine.PWM(machine.Pin(PIN_BUZZER))
buzzer.duty(0)

proxima_leitura = 0
buzzer_silenciado = False
estado_critico = False

def atualizar_sinalizacao(r, y, g, som=False):
    led_r.value(r)
    led_y.value(y)
    led_g.value(g)
    if som and not buzzer_silenciado:
        buzzer.freq(1000)
        buzzer.duty(512)
    else:
        buzzer.duty(0)

while True:
    agora = time.ticks_ms()

    if time.ticks_diff(agora, proxima_leitura) >= 0:
        try:
            sensor.measure()
            t = sensor.temperature()
            h = sensor.humidity()
            
            # Verificação de ESTADO CRÍTICO (Vermelho)
            if t > TEMP_CRITICA or h < UMID_CRITICA:
                if not estado_critico: buzzer_silenciado = False
                estado_critico = True
                
                if t > TEMP_CRITICA and h < UMID_CRITICA:
                    msg = "MOLHAR E COBRIR!"
                elif t > TEMP_CRITICA:
                    msg = "COBRIR DO SOL"
                else:
                    msg = "MOLHAR CONCRETO"
                
                atualizar_sinalizacao(1, 0, 0, som=True)

            # Verificação de ESTADO DE ATENÇÃO (Amarelo)
            elif t > TEMP_AVISO or h < UMID_AVISO:
                estado_critico = False
                msg = "MONITORAR CURA"
                atualizar_sinalizacao(0, 1, 0, som=False)

            # ESTADO IDEAL (Verde)
            else:
                estado_critico = False
                msg = "CURA ADEQUADA"
                atualizar_sinalizacao(0, 0, 1, som=False)

            # Atualização do Display
            lcd.puts(f"T:{t:.1f}C U:{h:.1f}%", 0)
            lcd.puts(msg, 1)

        # Tratamento de Erro
        except Exception:
            lcd.puts("ERRO DE LEITURA", 0)
            lcd.puts("CHECAR SENSOR", 1)
        
        proxima_leitura = agora + INTERVALO

    # Lógica do Botão Mute
    if btn_mute.value() == 0 and estado_critico:
        buzzer_silenciado = True
        buzzer.duty(0)