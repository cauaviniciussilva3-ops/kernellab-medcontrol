# KernelLab - Simulador de Gerenciamento de CPU, Memória e Dispositivos (MedControl)

> **Projeto Acadêmico - Disciplina de Sistemas Operacionais**  
> **Instituição:** UniFECAF  
> **Aluno:** Cauã Vinícius Porto Silva  
> **Tutora:** Patrícia Ampese  

---

## 📌 Contexto, Problema e Objetivos

O **MedControl** é um sistema embarcado para monitoramento de pacientes em Unidade de Terapia Intensiva (UTI). 
* **Problema Identificado:** O sistema apresentava atraso no disparo de alarmes de emergência médica (Processo P4 - parada cardíaca). No momento em que o alarme chegava ($t=3$), a CPU permanecia ocupada por tarefas secundárias não preemptivas (como geração de relatórios), colocando em risco a vida dos pacientes.
* **Objetivo:** Simular, analisar e otimizar a gestão dos recursos do SO (Escalonamento de CPU, Memória Virtual e Dispositivos de E/S), implementando soluções para garantir o atendimento instantâneo de emergências médicas.

---

## 🏗️ Arquitetura do Simulador e Módulos

O KernelLab foi construído de forma modular em Python para simular os subsistemas do Kernel de um Sistema Operacional:

```text
kernellab-medcontrol/
├── data/
│   └── processes.json          # Formato de entrada: tabela de dados dos processos da MedControl
├── src/
│   ├── __init__.py             # Identificador de pacote Python
│   ├── schedulers.py           # Algoritmos de Escalonamento de CPU (FCFS, SJF, RR, Prioridade)
│   ├── memory.py               # Algoritmos de Substituição de Páginas (FIFO, LRU, Optimal)
│   ├── devices.py              # Matriz de Controle de Acesso (DAC) e Concorrência (Mutex/Semáforo)
│   └── main.py                 # Script principal de execução da simulação e relatórios
├── tests/
│   ├── __init__.py             # Identificador de pacote para testes unitários
│   └── test_kernellab.py       # Suíte de testes automatizados com pytest
└── README.md                   # Documentação completa e relatório técnico
```
## Algoritmos Implementados

Escalonamento de CPU: FCFS (First-Come, First-Served), SJF Não-Preemptivo (Shortest Job First), Round Robin ($q=3$) e Prioridade Preemptiva.
Gerenciamento de Memória Virtual: Substituição de páginas com algoritmos FIFO, LRU e Optimal.
Concorrência e Segurança de E/S: Matriz de Controle de Acesso (DAC), Mutex (threading.Lock) e Semáforo (threading.Semaphore).

## Instruções de Instalação e Execução

Pré-requisitos
Python 3.10 ou superior
Biblioteca pytest para testes
```text
pip install pytest
```

# Executando os Testes Automatizados
```text
pytest tests/
```

## Formato dos Dados de Entrada (data/processes.json)
Os processos da MedControl são definidos em um arquivo JSON contendo:

- id: Identificador único do processo (ex.: P1 a P6).
- func: Descrição da tarefa hospitalar.
- arrival: Tempo de chegada do processo na fila de prontos.
- burst: Tempo total de execução necessário na CPU.
- priority: Nível de prioridade (menor número = maior prioridade).

# Exemplos de Uso e Saída Esperada
Ao executar python src/main.py, o terminal exibe:

- Gráficos de Gantt e Métricas da CPU: Demostrando que no algoritmo de Prioridade Preemptiva, o processo P4 (Alarme Crítico) interrompe a CPU no instante $t=3$ e é atendido imediatamente (Espera = 0 u.t.).
- Contagem de Páginas: Demonstrando que o algoritmo LRU obtém menos falhas de página (10 Page Faults) em comparação ao FIFO (12 Page Faults).
- Validação de Segurança: Bloqueio de acessos não autorizados ([ACESSO NEGADO]) e sincronização por Mutex e Semáforo.

## RELATÓRIO TÉCNICO E MÉTRICAS COMPARATIVAS
1. Escalonamento de CPU
Algoritmo: FCFS

- Tempo Médio de Espera (TME): 13.67 u.t.
- Tempo Médio de Retorno (TMR): 20.50 u.t.
- Tempo Médio de Resposta (TMResp): 13.67 u.t.
- Trocas de Contexto: 5
- Atendimento ao Alarme (P4): Início no tempo t=21 (Crítico)

Algoritmo: SJF (Não-Preemptivo)

- Tempo Médio de Espera (TME): 10.67 u.t.
- Tempo Médio de Retorno (TMR): 17.50 u.t.
- Tempo Médio de Resposta (TMResp): 10.67 u.t.
- Trocas de Contexto: 5
- Atendimento ao Alarme (P4): Início no tempo t=8 (Atrasado)

Algoritmo: Round Robin (q=3)

- Tempo Médio de Espera (TME): 18.00 u.t.
- Tempo Médio de Retorno (TMR): 24.83 u.t.
- Tempo Médio de Resposta (TMResp): 5.33 u.t.
- Trocas de Contexto: 13
- Atendimento ao Alarme (P4): Início no tempo t=9 (Inaceitável)

Algoritmo: Prioridade Preemptiva

- Tempo Médio de Espera (TME): 10.17 u.t.
- Tempo Médio de Retorno (TMR): 17.00 u.t.
- Tempo Médio de Resposta (TMResp): 9.83 u.t.
- Trocas de Contexto: 6
- Atendimento ao Alarme (P4): Início no tempo t=3 (Imediato - Espera 0 u.t.)

2. Memória Virtual (Sequência de 17 Referências, 4 Frames)

- FIFO: 12 Page Faults (70.59% de faltas)
- LRU: 10 Page Faults (58.82% de faltas)
- Optimal: 7 Page Faults (41.18% de faltas)

⚠️ Limitações do Simulador e Possíveis Melhorias
- Limitação 1 (Risco de Starvation): No algoritmo de Prioridade Preemptiva, processos com prioridade baixa (ex.: P5 - Backup) podem sofrer postergação indefinida caso ocorram sucessivas chegadas de processos de maior prioridade.
- Melhoria Propagada: Implementar a técnica de Aging (Envelhecimento), que aumenta gradualmente a prioridade de processos que permanecem muito tempo na fila de prontos.
- Limitação 2 (Estático): Os tempos de execução e sequências de páginas são fixos.
Melhoria Propagada: Integrar geradores dinâmicos de carga em tempo real.

# Referências Bibliográficas e Fontes de Pesquisa

- SILBERSCHATZ, Abraham; GALVIN, Peter Baer; GAGNE, Greg. Sistemas Operacionais com Java. 9. ed. Rio de Janeiro: LTC, 2015.
- TANENBAUM, Andrew S.; BOS, Herbert. Sistemas Operacionais Modernos. 4. ed. São Paulo: Pearson Education do Brasil, 2016.
- STALLINGS, William. Operating Systems: Internals and Design Principles. 9th ed. Pearson, 2018.

---

### 2. Atualização dos Comandos no Terminal (VS Code)

Para enviar o `README.md` atualizado ao GitHub, execute no terminal:

```powershell
git commit -am "Atualiza README com referencias e limites exigidos pelo edital"
git push origin main