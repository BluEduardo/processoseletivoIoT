import machine
import dht
import time


## Configuração das Portas
PIN_DHT      = 15
PIN_BUZZER   = 13
PIN_BUTTON   = 18  # Mute
PIN_LED_RED  = 12
PIN_LED_YEL  = 14
PIN_LED_GRN  = 27
PIN_SCL      = 22
PIN_SDA      = 21

# Limiares técnicos
TEMP_MAX     = 45.0
UMID_MIN     = 60.0
INTERVALO    = 2000 

print("Teste")

class MiniLCD:
    def __init__(self, scl_pin, sda_pin, addr=0x27):
        self.i2c  = machine.SoftI2C(scl=machine.Pin(scl_pin), sda=machine.Pin(sda_pin), freq=100000)
        self.addr = addr
        time.sleep_ms(50)

        for cmd in (0x33, 0x32, 0x28, 0x0C, 0x06, 0x01):
            self._write(cmd, 0)
            time.sleep_ms(2)

    def _write(self, val, mode):
        h = mode | (val & 0xF0) | 0x08 # Backlight sempre ON
        l = mode | ((val << 4) & 0xF0) | 0x08
        self.i2c.writeto(self.addr, bytes([h | 0x04, h & ~0x04, l | 0x04, l & ~0x04]))

    def puts(self, text, line=0):
        # 16 chars por linha
        text = text[:16]
        while len(text) < 16: text += " "
        self._write(0x80 if line == 0 else 0xC0, 0)
        for c in text: self._write(ord(c), 1)


# Inicialização de periféricos
lcd = MiniLCD(scl_pin=PIN_SCL, sda_pin=PIN_SDA)
lcd.puts("SISTEMA INICIADO", 0)
sensor = dht.DHT22(machine.Pin(PIN_DHT))
led_r = machine.Pin(PIN_LED_RED, machine.Pin.OUT)
led_y = machine.Pin(PIN_LED_YEL, machine.Pin.OUT)
led_g = machine.Pin(PIN_LED_GRN, machine.Pin.OUT)
btn_mute = machine.Pin(PIN_BUTTON, machine.Pin.IN, machine.Pin.PULL_UP)

buzzer = machine.PWM(machine.Pin(PIN_BUZZER))
buzzer.duty(0)

proxima_leitura = 0
buzzer_silenciado = False
foi_critico_antes = False


while True:
    agora = time.ticks_ms()

    if time.ticks_diff(agora, proxima_leitura) >= 0:
        try:
            sensor.measure()
            t = sensor.temperature()
            h = sensor.humidity()

            # Lógica de Alertas
            if t > TEMP_MAX or h < UMID_MIN:
                led_r.value(1); led_g.value(0)
                if not foi_critico_antes: buzzer_silenciado = False
                if not buzzer_silenciado:
                    buzzer.freq(1000); buzzer.duty(512)
                else:
                    buzzer.duty(0)
                foi_critico_antes = True            
            else:
                led_r.value(0); led_g.value(1)
                buzzer.duty(0); foi_critico_antes = False

            lcd.puts(f"TEMP: {t:.1f} C", 0)
            lcd.puts(f"UMID: {h:.1f} %", 1)
          

        except Exception as e:
            lcd.puts("ERRO NO SENSOR", 0)
        
        proxima_leitura = agora + INTERVALO

    # Botão Mute
    if btn_mute.value() == 0 and foi_critico_antes:
        buzzer_silenciado = True
        buzzer.duty(0)