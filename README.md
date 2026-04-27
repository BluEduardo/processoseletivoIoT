# 🚀 SmartCure IoT - Monitoramento de Cura de Concreto

### 👤 Identificação do Candidato
* **Nome completo:** Eduardo Roberto Pereira
* **Perfil:** Estudante de Engenharia Civil (UFCA) e Desenvolvedor Full-Stack
* **Objetivo:** Integração de Scientific Computing e IoT na Indústria da Construção Civil

---

### 1️⃣ Visão Geral da Solução
O **SmartCure IoT** nasce da intersecção entre a Engenharia Civil e a Tecnologia da Informação. A construção civil é uma indústria bilionária mundialmente, mas que ainda carece de digitalização no canteiro de obras. Falhas no processo de cura do concreto são responsáveis por patologias estruturais graves e acidentes que custam milhões em reparos e vidas humanas.

Este projeto aplica conceitos de **Internet das Coisas (IoT)** para garantir que o concreto atinja sua resistência de projeto, monitorando variáveis críticas que evitam a retração plástica e fissuras por dessecação.

O sistema atua de forma autônoma:
* **Monitoramento:** Captura temperatura e umidade superficial em tempo real.
* **Prevenção:** Identifica condições climáticas adversas que comprometem a hidratação do cimento.
* **Interface:** Alerta o operador via LCD 16x2 e sinais visuais/sonoros para intervenção imediata (molhagem ou cobertura).

---

### 2️⃣ Arquitetura do Sistema Embarcado
A arquitetura prioriza a **confiabilidade industrial**:

* **Fluxo Principal (main.py):** Desenvolvido com lógica não-bloqueante (`time.ticks_ms()`), permitindo que o sistema processe leituras de sensores e entradas de usuário (botão de silenciamento) simultaneamente, sem atrasos (*lags*).
* **Máquina de Estados Binária:** O sistema opera em dois estados claros: **ESTÁVEL** (Verde) e **CRÍTICO** (Vermelho). Essa decisão de design visa a usabilidade em campo, onde a tomada de decisão precisa ser rápida e sem ambiguidades.
* **Comunicação I2C:** Implementada via `SoftI2C` para garantir a integridade dos dados exibidos no LCD sob condições de oscilação de sinal.

---

### 3️⃣ Componentes Utilizados na Simulação
| Componente | Função Técnica | Pino (GPIO) |
| :--- | :--- | :--- |
| **ESP32** | Microcontrolador central com baixo consumo de energia | - |
| **DHT22** | Monitoramento de alta precisão de Temperatura e Umidade | 15 |
| **LCD 16x2 (I2C)** | Exibição em tempo real dos dados climáticos da face | 21, 22 |
| **Buzzer PWM** | Alerta sonoro de frequência constante (1000Hz) | 13 |
| **LEDs R/G** | Sinalização visual de status de conformidade térmica | 12, 27 |
| **Pushbutton** | Função de Acknowledge (Silenciamento do alarme sonoro) | 18 |

<img width="706" height="475" alt="image" src="https://github.com/user-attachments/assets/a4d4afff-5d50-4b6e-b3d6-7c91e499bdfa" />

Imagem do projeto SmartCure IoT

---

### 4️⃣ Decisões Técnicas Relevantes
* **Geração de Imagem Binária (LittleFS):** Para viabilizar a execução automatizada na esteira de CI/CD (GitHub Actions), foi necessário adicionar um processo de *build* que gera um sistema de arquivos binário utilizando a biblioteca `littlefs`. Isso permitiu empacotar o `main.py` e montá-lo diretamente na memória flash do ESP32 virtual, garantindo que o Wokwi CLI iniciasse o firmware corretamente durante os testes.
* **Eliminação do LED Amarelo:** Em um canteiro de obras, estados intermediários podem gerar dúvida. A interface foi simplificada para Vermelho (Intervenção Necessária) ou Verde (Cura Adequada).
* **Gestão de Alarme (Mute):** O botão silencia o buzzer para reduzir a poluição sonora, mas o LED vermelho permanece aceso até que as condições de umidade/temperatura voltem aos níveis seguros, garantindo que o alerta visual nunca seja ignorado.
* **Driver de Display Otimizado:** Criado para enviar comandos em *nibbles* de 4 bits, o que reduz erros de comunicação e caracteres fantasmas no LCD.

---

### 5️⃣ Resultados Obtidos e Limitações
**Resultados:**
* **Automação de CI/CD:** Pipeline validada com sucesso. O uso do binário LittleFS garantiu a estabilidade dos testes automatizados no Wokwi sempre que um novo commit é enviado.
* **Monitoramento Constante:** O sistema mantém um log de leitura estável, identificando riscos de dessecação (Umidade < 60%) e calor excessivo (Temp > 45°C).

**Limitações Atuais:**
* **Ponto Único de Leitura:** O protótipo utiliza apenas um sensor de face, não capturando variações em grandes áreas de concretagem.
* **Dependência de Energia:** O sistema ainda não possui modo de baixo consumo (*Deep Sleep*) para operação prolongada em locais sem rede elétrica estável.

---

### 6️⃣ Dificuldades e Melhorias Futuras
**Dificuldades Encontradas:**
O maior desafio técnico foi adequar o ambiente de simulação local para a esteira de integração contínua (CI). O Wokwi CLI exigia a pré-montagem do sistema de arquivos do ESP32 para executar o MicroPython no GitHub Actions, o que me obrigou a estudar e implementar o empacotamento do firmware via `littlefs`. Além disso, a calibração do barramento I2C no simulador exigiu o desenvolvimento de uma classe personalizada (`MiniLCD`) para controlar manualmente o tempo de pulso do sinal de *Enable*.

**Melhorias Planejadas (V2):**
* **Gradiente Térmico:** Reintegração do potenciômetro para simular sensores de núcleo, permitindo comparar a temperatura interna vs. externa (essencial para concreto de massa).
* **Expansão de Interface:** Upgrade para LCD 20x4 para exibição simultânea de mais métricas de engenharia.
* **Integração Mobile:** Envio de alertas via MQTT/Telegram para dispositivos móveis, permitindo que o engenheiro responsável monitore a cura à distância.
* **Análise de Maturação:** Implementação de algoritmos para cálculo da curva de maturidade do concreto diretamente no ESP32.
