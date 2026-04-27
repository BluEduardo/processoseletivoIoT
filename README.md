<<<<<<< HEAD
=======
# 🚀 SmartCure IoT - Monitoramento de Cura de Concreto

>>>>>>> 22a654921d1ee26cc1eecf02b56c74c3d353bc3b
### 👤 Identificação do Candidato
* **Nome completo:** Eduardo Roberto Pereira
---

### 1️⃣ Visão Geral da Solução
O **SmartCure IoT** é um sistema de monitoramento de baixo custo projetado para garantir a qualidade do concreto durante o estágio de cura. O objetivo é evitar manifestações patológicas, como fissuras por retração plástica ou térmica, através da vigilância contínua da temperatura e umidade superficial.

O sistema atua de forma autônoma:
* **Monitoramento:** Captura dados ambientais em tempo real.
* **Decisão:** Compara os dados com limiares normativos técnicos.
* **Interface:** Informa o operador via LCD 16x2 e alertas visuais/sonoros.

---

### 2️⃣ Arquitetura do Sistema Embarcado
A arquitetura lógica foi desenhada para priorizar a estabilidade e a facilidade de leitura no canteiro de obras:

* **Fluxo Principal (main.py):** O programa opera em um loop infinito com temporização não-bloqueante (`time.ticks_ms()`), garantindo que o sensor DHT22 seja consultado a cada 2 segundos sem travar a resposta do botão de mute.
* **Máquina de Estados:** O sistema alterna entre os estados **NORMAL** (Verde) e **CRÍTICO** (Vermelho), onde qualquer desvio de umidade ou temperatura aciona o protocolo de segurança.
* **Comunicação I2C:** Utiliza o protocolo `SoftI2C` para gerenciar o display LCD 20x4, garantindo resiliência na transmissão de dados no ambiente de simulação.

---

### 3️⃣ Componentes Utilizados na Simulação
Conforme definido no `diagram.json`, os componentes principais são:

| Componente | Função Técnica | Pino (GPIO) |
| :--- | :--- | :--- |
| **ESP32** | Microcontrolador central da solução  | - |
| **DHT22** | Medição de Temperatura e Umidade da face do Concreto | 15 |
| **LCD 16x2 (I2C)** | Interface detalhada para o operador  | 21, 22 |
| **Buzzer PWM** | Alerta sonoro para chamar atenção do responsável pela obra  | 13 |
| **LEDs R/G** | Sinalização visual binária de status | 12, 27 |
| **Pushbutton** | Função de Acknowledge (Silenciar Alarme) | 18 |

---

### 4️⃣ Decisões Técnicas Relevantes
* **Driver MiniLCD Personalizado:** Implementado para gerenciar a escrita de nibbles de forma atômica, evitando caracteres corrompidos durante flutuações na simulação.
* **Interface Binária:** Optou-se por remover o LED amarelo e utilizar apenas **Verde/Vermelho**. Esta decisão justifica-se pela necessidade de clareza absoluta em ambientes industriais: se está vermelho, o operador precisa intervir.
* **Silenciamento (Mute):** O botão de mute desativa apenas o som, mantendo o LED vermelho aceso. Isso garante que o alarme sonoro não cause poluição auditiva desnecessária após o problema ser identificado, mas mantém o alerta visual até a normalização.
* **Uso de Constantes:** Todos os limiares (`TEMP_MAX`, `UMID_MIN`) estão centralizados no topo do código para facilitar a manutenção técnica.

---

### 5️⃣ Resultados Obtidos
O sistema demonstrou total funcionalidade no ambiente Wokwi:
* **Estabilidade:** A pipeline de CI/CD foi validada com sucesso através de commits semânticos e uso de Secrets para chaves de API.
* **Conformidade:** O sistema identifica corretamente quando a umidade cai abaixo de 60% ou a temperatura sobe acima de 45°C, emitindo alertas imediatos.
* **Interface:** O LCD 16x2 exibe constantemente os valores de umidade e temperatura da face do concreto, promovendo melhor acompanhamento pelo responsável técnico da obra.

---

### 6️⃣ Comentários Adicionais
* **Aprendizados:** O projeto reforçou a importância do versionamento semântico e da proteção de chaves sensíveis em ambientes de nuvem.
* **Dificuldades:** A calibração da comunicação I2C no simulador exigiu a implementação de um driver robusto baseado em temporização manual de pulsos.
* **Melhorias:** Em uma versão futura, seria ideal implementar o envio de dados via protocolo MQTT para monitoramento remoto via dashboard em nuvem.
