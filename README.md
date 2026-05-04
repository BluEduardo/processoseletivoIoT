# 🚀 SmartCure IoT - Monitoramento de Cura de Concreto

### 👤 Identificação do Candidato
* **Nome Completo:** Eduardo Roberto Pereira
* **Perfil:** Estudante de Engenharia Civil e Desenvolvedor Full-Stack
* **Objetivo:** Integração de Sistemas Embarcados e IoT na Indústria da Construção Civil

---

### 1️⃣ Visão Geral da Solução
O **SmartCure IoT** é um sistema embarcado voltado para a digitalização do canteiro de obras, que nasce da intersecção entre a Engenharia Civil e a Tecnologia da Informação. A construção civil é uma indústria bilionária mundialmente, mas que ainda carece de digitalização na sua rotina. Falhas no processo de cura do concreto são responsáveis por patologias estruturais graves e acidentes que custam milhões em reparos e vidas humanas.

Este projeto aplica conceitos de **Internet das Coisas (IoT)** para garantir que o concreto atinja sua resistência de projeto, monitorando variáveis críticas que evitam a retração plástica e fissuras por dessecação.

O sistema atua em três níveis:
* **Monitoramento:** Captura contínua de temperatura e umidade via sensor DHT22.
* **Análise de Risco:** Processamento local de limiares técnicos de engenharia.
* **Interface de Ação:** Alertas visuais (Semáforo LED), sonoros (Buzzer) e textuais (LCD) com instruções de intervenção (molhagem e/ou cobertura).

---

### 2️⃣ Arquitetura do Sistema Embarcado
A arquitetura prioriza a **confiabilidade industrial**:

* **Fluxo Principal (main.py):** Desenvolvido com lógica não-bloqueante (`time.ticks_ms()`), permitindo que o sistema processe leituras de sensores e entradas de usuário (botão de silenciamento) simultaneamente, sem atrasos (*lags*).
* **Hierarquia de Alertas:** O sistema categoriza o ambiente em três zonas (Ideal, Atenção e Crítica), garantindo que o operador saiba a urgência da ação necessária.
* **Comunicação I2C:** Implementada via `SoftI2C` para garantir a integridade dos dados exibidos no LCD sob condições de oscilação de sinal.

---

### 3️⃣ Componentes Utilizados na Simulação
| Componente | Função Técnica | Pino (GPIO) |
| :--- | :--- | :--- |
| **ESP32** | Microcontrolador central com baixo consumo de energia | - |
| **DHT22** | Monitoramento de alta precisão de Temperatura e Umidade | 15 |
| **LCD 16x2 (I2C)** | Interface textual para dados e instruções de engenharia | 21, 22 |
| **Buzzer PWM** | Alerta sonoro para estados críticos de emergência | 13 |
| **LEDs (R/Y/G)** | Semáforo de status (Crítico, Atenção, Ideal) | 12, 14, 27 |
| **Pushbutton** | Silenciamento (Mute) do alarme sonoro | 18 |

---

### 4️⃣ Decisões Técnicas Relevantes

* **Sinalização Preventiva (LED Amarelo):** Diferente de sistemas binários, o SmartCure introduz a "Zona de Atenção". Isso permite uma gestão proativa na obra, avisando que os limites de segurança estão próximos antes que o dano ocorra, prevenindo danos irreversíveis a estrutura do concreto.
* **Instruções Técnicas de Campo:** O LCD não exibe apenas números, ele fornece instruções de engenharia como **"MOLHAR CONCRETO"** ou **"COBRIR DO SOL"**, traduzindo dados brutos em ações práticas de canteiro, minimizando o tempo de pensamento do responsável e agilizando a tomada de decisão.
* **Gestão de Alarme (Anti-Fadiga):** O buzzer é acionado apenas no estado **Vermelho (Crítico)**. No estado amarelo, a sinalização é apenas visual, evitando a poluição sonora desnecessária que leva os operadores a ignorarem alarmes em ambiente real.
* **Compatibilidade CI/CD:** O firmware foi adaptado para execução automatizada via **GitHub Actions** e **Wokwi CLI**, garantindo que cada commit seja validado tecnicamente na nuvem.
* **Geração de Imagem Binária (LittleFS):** Para viabilizar a execução automatizada na esteira de CI/CD (GitHub Actions), foi necessário adicionar um processo de *build* que gera um sistema de arquivos binário utilizando a biblioteca `littlefs`. Isso permitiu empacotar o `main.py` e montá-lo diretamente na memória flash do ESP32 virtual, garantindo que o Wokwi CLI iniciasse o firmware corretamente durante os testes.
>[!IMPORTANT]
Nota de Desenvolvimento: Toda vez que o arquivo main.py for modificado, o script build.py deve ser executado para atualizar o binário. Caso contrário, as alterações não serão refletidas nas GitHub Actions.

---

### 5️⃣ Demonstração da Simulação

#### 🟢 Estado Ideal
<img width="764" height="476" alt="image" src="https://github.com/user-attachments/assets/8ecd1d94-2ecc-4651-88fd-e100c0a8e375" />

*Estado de Conformidade: Parâmetros dentro da normalidade, garantindo uma cura lenta e eficaz sem riscos imediatos.*

#### 🟡 Estado de Atenção
<img width="765" height="478" alt="image" src="https://github.com/user-attachments/assets/53a83670-eea4-477e-982a-49670b874f21" />

*Monitoramento Preventivo: O sistema identifica que os níveis de umidade ou temperatura estão se aproximando dos limites críticos de projeto.*

#### 🔴 Estado Crítico
<img width="750" height="489" alt="image" src="https://github.com/user-attachments/assets/49f7b2ae-c20c-43a4-87bd-2d7ffdea344c" />

*Intervenção Urgente: Alerta visual e sonoro acionados. O LCD instrui a ação corretiva imediata para evitar fissuras e perda de resistência.*

---

### 6️⃣ Resultados Obtidos e Limitações
**Resultados:**
* **Automação de CI/CD:** Pipeline validada com sucesso. O uso do binário LittleFS garantiu a estabilidade dos testes automatizados no Wokwi sempre que um novo commit é enviado.
* **Monitoramento Constante:** O sistema mantém um log de leitura estável, identificando riscos de dessecação (Umidade < 60%) e calor excessivo (Temp > 45°C).
* **Interface de usuário (UI):** Implementação de uma interface simples focada na tomada de decisão rápida no canteiro de obras.
* **Lógica Robusta:** Lógica de firmware robusta e resiliente a erros de leitura de sensores.

**Limitações Atuais:**
* **Ponto Único de Leitura:** O protótipo utiliza apenas um sensor de face, não capturando variações em grandes áreas de concretagem.
* **Dependência de Energia:** O sistema ainda não possui modo de baixo consumo (*Deep Sleep*) para operação prolongada em locais sem rede elétrica estável.

---

### 7️⃣ Dificuldades e Melhorias Futuras
**Dificuldades Encontradas:**
O maior desafio técnico foi adequar o ambiente de simulação local para a esteira de integração contínua (CI). O Wokwi CLI exigia a pré-montagem do sistema de arquivos do ESP32 para executar o MicroPython no GitHub Actions, o que me obrigou a estudar e implementar o empacotamento do firmware via `littlefs`. Além disso, a calibração do barramento I2C no simulador exigiu o desenvolvimento de uma classe personalizada (`MiniLCD`) para controlar manualmente o tempo de pulso do sinal de *Enable*.

**Melhorias Planejadas (V2):**
* **Deep Sleep:** Implementação de modos de economia de energia para operação via bateria em obras remotas.
* **Gradiente Térmico:** Integração de um potenciômetro para simular um sensor de temperatura no núcleo do concreto, permitindo comparar a temperatura interna vs. externa (essencial para concreto de massa).
* **Expansão de Interface:** Upgrade para LCD 20x4 para exibição simultânea de mais métricas de engenharia.
* **Integração Mobile:** Envio de alertas via MQTT/Telegram para dispositivos móveis, permitindo que o engenheiro responsável monitore a cura à distância.
* **Análise de Maturação:** Implementação de algoritmos para cálculo da curva de maturidade do concreto diretamente no ESP32.
