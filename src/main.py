import json
import os
from schedulers import CPUScheduler
from memory import MemorySimulator
from devices import DeviceManager

def load_processes():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_path, "data", "processes.json")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_cpu_benchmarks():
    data = load_processes()
    scheduler = CPUScheduler(data)

    algorithms = [
        ("FCFS", scheduler.fcfs()),
        ("SJF (Não-Preemptivo)", scheduler.sjf_non_preemptive()),
        ("Round Robin (q=3)", scheduler.round_robin(quantum=3)),
        ("Prioridade Preemptiva", scheduler.priority_preemptive())
    ]

    print("=" * 85)
    print("                      RELATÓRIO DE ESCALONAMENTO DE CPU                     ")
    print("=" * 85)

    for name, (procs, gantt, switches) in algorithms:
        avg_wait = sum(p.waiting_time for p in procs) / len(procs)
        avg_turnaround = sum(p.turnaround_time for p in procs) / len(procs)
        avg_response = sum(p.response_time for p in procs) / len(procs)

        print(f"\n>>> Algoritmo: {name}")
        print(f"Gantt: {gantt}")
        print(f"Trocas de Contexto: {switches}")
        print(f"Métricas Médias -> Espera (TME): {avg_wait:.2f} | Retorno (TMR): {avg_turnaround:.2f} | Resposta (TMResp): {avg_response:.2f}")
        print("-" * 85)
        print(f"{'ID':<5}{'Função':<30}{'Espera':<10}{'Retorno':<10}{'Resposta':<10}")
        print("-" * 85)
        for p in procs:
            print(f"{p.id:<5}{p.function:<30}{p.waiting_time:<10}{p.turnaround_time:<10}{p.response_time:<10}")

def run_memory_benchmarks():
    pages = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5, 2, 1, 5, 3, 2]
    mem = MemorySimulator(num_frames=4)

    fifo_hist, fifo_hits, fifo_faults, fifo_rate = mem.fifo(pages)
    lru_hist, lru_hits, lru_faults, lru_rate = mem.lru(pages)
    opt_hist, opt_hits, opt_faults, opt_rate = mem.optimal(pages)

    print("\n" + "=" * 85)
    print("                  RELATÓRIO DE GERENCIAMENTO DE MEMÓRIA VIRTUAL             ")
    print("=" * 85)
    print(f"Sequência de Páginas (17 refs): {pages}\n")

    print(f"{'Algoritmo':<20}{'Page Hits':<12}{'Page Faults':<14}{'Taxa de Faltas (%)':<20}")
    print("-" * 85)
    print(f"{'FIFO':<20}{fifo_hits:<12}{fifo_faults:<14}{fifo_rate:.2f}%")
    print(f"{'LRU':<20}{lru_hits:<12}{lru_faults:<14}{lru_rate:.2f}%")
    print(f"{'Optimal':<20}{opt_hits:<12}{opt_faults:<14}{opt_rate:.2f}%")

def run_device_benchmarks():
    dev = DeviceManager()
    print("\n" + "=" * 85)
    print("              SIMULAÇÃO DE CONCORRÊNCIA E CONTROLE DE ACESSO                ")
    print("=" * 85)

    res1, msg1 = dev.request_exclusive_access("P4", "Áudio", "Usar")
    res2, msg2 = dev.request_exclusive_access("P3", "Disco", "Exclusivo")
    res3, msg3 = dev.request_exclusive_access("P1", "Disco", "Gravar")
    res4, msg4 = dev.request_shared_network("P1", "Usar")
    res5, msg5 = dev.request_shared_network("P2", "Usar")

    for log in dev.log_history:
        print(log)

if __name__ == "__main__":
    run_cpu_benchmarks()
    run_memory_benchmarks()
    run_device_benchmarks()