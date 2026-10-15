# KernelLab - Simulador de Gerenciamento de CPU, Memória e Dispositivos (MedControl)

> **Projeto Acadêmico - Disciplina de Sistemas Operacionais**  
> **Instituição:** UniFECAF  

---

## 📌 Contexto e Objetivo do Trabalho

O **MedControl** é um sistema embarcado crítico projetado para monitorar pacientes em Unidades de Terapia Intensiva (UTIs). O objetivo deste projeto é simular, analisar e otimizar a gestão dos recursos do sistema operacional (Processador, Memória Virtual e Dispositivos de E/S), resolvendo gargalos críticos como o atraso no disparo de alarmes de emergência médica (Processo P4).

---

## 🛠️ Pré-requisitos de Instalação

Para executar este simulador e rodar a suíte de testes, certifique-se de ter instalado:

1. **Python 3.10 ou superior**
2. **Biblioteca `pytest`** (opcional para testes unitários):

   pip install pytest

## Como Executar o Simulador
Executando a Simulação Completa
Abra o terminal na pasta raiz do projeto (kernellab-medcontrol) e execute:

python src/main.py

## Executando os Testes Unitários
Para validar a integridade dos módulos do KernelLab:

pytest tests/

# Estrutura do Projeto e Módulos
'''
kernellab-medcontrol/
├── data/
│   └── processes.json          # Tabela de dados dos processos da MedControl (P1 a P6)
├── src/
│   ├── __init__.py             # Identificador de pacote Python
│   ├── schedulers.py           # Algoritmos de Escalonamento de CPU (FCFS, SJF, RR, Prioridade)
│   ├── memory.py               # Algoritmos de Substituição de Páginas (FIFO, LRU, Optimal)
│   ├── devices.py              # Matriz de Controle de Acesso e Concorrência (Mutex/Semáforo)
│   └── main.py                 # Script principal de execução dos relatórios e simulação
├── tests/
│   ├── __init__.py             # Identificador de pacote Python para testes
│   └── test_kernellab.py       # Testes unitários do simulador
└── README.md                   # Documentação detalhada e relatório completo do projeto


# RELATÓRIO TÉCNICO DE RESULTADOS E ANÁLISE

1. Diagnóstico do Problema no MedControl
O sistema apresentou falhas graves, incluindo o atraso na emissão de alarmes de parada cardíaca (Processo P4).

Causa: O uso de escalonamento sem preempção mantinha a CPU ocupada com tarefas secundárias no momento em que o alarme emergencial chegava.

2. Ciclo de Vida dos Processos
Os processos transitam pelos estados:

Novo (New): Carregado a partir do arquivo JSON.
Pronto (Ready): Aguardando alocação de CPU na fila.
Executando (Running): Processo em execução na CPU.
Esperando (Waiting/Blocked): Aguardando liberação de recurso de E/S por Mutex ou Semáforo.
Terminado (Terminated): Execução concluída.

3. Escalonamento de CPU - Resultados Comparativos

Algoritmo: FCFS

Tempo Médio de Espera (TME): 13.67 u.t.
Tempo Médio de Retorno (TMR): 20.50 u.t.
Tempo Médio de Resposta (TMResp): 13.67 u.t.
Trocas de Contexto: 5
Atendimento ao Alarme (P4): Início no tempo t=21 (Crítico)

Algoritmo: SJF (Não-Preemptivo)

Tempo Médio de Espera (TME): 10.67 u.t.
Tempo Médio de Retorno (TMR): 17.50 u.t.
Tempo Médio de Resposta (TMResp): 10.67 u.t.
Trocas de Contexto: 5
Atendimento ao Alarme (P4): Início no tempo t=8 (Atrasado)

Algoritmo: Round Robin (q=3)

Tempo Médio de Espera (TME): 18.00 u.t.
Tempo Médio de Retorno (TMR): 24.83 u.t.
Tempo Médio de Resposta (TMResp): 5.33 u.t.
Trocas de Contexto: 13
Atendimento ao Alarme (P4): Início no tempo t=9 (Inaceitável)

Algoritmo: Prioridade Preemptiva

Tempo Médio de Espera (TME): 10.17 u.t.
Tempo Médio de Retorno (TMR): 17.00 u.t.
Tempo Médio de Resposta (TMResp): 9.83 u.t.
Trocas de Contexto: 6
Atendimento ao Alarme (P4): Início no tempo t=3 (Imediato)

Resumo da Análise de CPU:

Menor Tempo Médio de Espera: Prioridade Preemptiva (10.17 u.t.).
Atendimento do Alarme (P4): O algoritmo de Prioridade Preemptiva interrompe imediatamente a tarefa em execução no instante t=3, garantindo tempo de espera 0 u.t. para a emissão do alarme.
Risco de Starvation: Presente em Prioridade e SJF para processos de baixa prioridade (exemplo: P5 - Backup).
Justiça: Round Robin distribui fatias iguais de tempo entre os processos na fila circular.

4. Gerenciamento de Memória Virtual
Análise para a sequência de 17 referências com 4 quadros (frames) de memória ([1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5, 2, 1, 5, 3, 2]):

FIFO (First-In, First-Out): 12 Page Faults (Taxa de Faltas: 70.59%)
LRU (Least Recently Used): 10 Page Faults (Taxa de Faltas: 58.82%)
Optimal (Teórico): 7 Page Faults (Taxa de Faltas: 41.18%)
Conclusão: O LRU superou o FIFO aproveitando o princípio da localidade temporal das páginas de monitoramento.

5. Dispositivos de Entrada/Saída e Segurança
Matriz de Controle de Acesso (DAC): Define permissões explícitas por processo (ex.: P4 possui acesso exclusivo a Áudio e Rede; P1 não tem permissão no Disco).

Mecanismos de Sincronização:
Mutex (threading.Lock): Garante a posse exclusiva do dispositivo de áudio para o processo P4.
Semáforo (threading.Semaphore): Limita a 2 acessos simultâneos ao barramento de rede.

6. Recomendação Final para o MedControl
Recomenda-se a adoção do Escalonador de Prioridade Preemptiva com mecanismo de Aging (Envelhecimento) para evitar starvation, combinado com o Algoritmo LRU para o gerenciamento de memória virtual.