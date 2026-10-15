from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

@dataclass
class Process:
    id: str
    function: str
    arrival: int
    burst: int
    priority: int
    memory: int
    device: str
    remaining_burst: int = 0
    start_time: int = -1
    completion_time: int = 0
    waiting_time: int = 0
    turnaround_time: int = 0
    response_time: int = -1

    def __post_init__(self):
        self.remaining_burst = self.burst

class CPUScheduler:
    def __init__(self, processes_data: List[Dict[str, Any]]):
        self.raw_data = processes_data

    def _get_fresh_processes(self) -> List[Process]:
        return [Process(**p) for p in self.raw_data]

    def fcfs(self) -> Tuple[List[Process], List[Tuple[str, int, int]], int]:
        procs = sorted(self._get_fresh_processes(), key=lambda x: x.arrival)
        current_time = 0
        gantt = []
        context_switches = 0
        last_proc = None

        for p in procs:
            if current_time < p.arrival:
                gantt.append(("IDLE", current_time, p.arrival))
                current_time = p.arrival

            if last_proc is not None and last_proc != p.id:
                context_switches += 1

            p.start_time = current_time
            p.response_time = p.start_time - p.arrival
            current_time += p.burst
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival
            p.waiting_time = p.turnaround_time - p.burst

            gantt.append((p.id, p.start_time, p.completion_time))
            last_proc = p.id

        return procs, gantt, context_switches

    def sjf_non_preemptive(self) -> Tuple[List[Process], List[Tuple[str, int, int]], int]:
        procs = self._get_fresh_processes()
        current_time = 0
        completed = []
        gantt = []
        context_switches = 0
        last_proc = None

        while len(completed) < len(procs):
            ready = [p for p in procs if p.arrival <= current_time and p not in completed]
            if not ready:
                next_arrival = min(p.arrival for p in procs if p not in completed)
                gantt.append(("IDLE", current_time, next_arrival))
                current_time = next_arrival
                continue

            ready.sort(key=lambda x: (x.burst, x.arrival))
            p = ready[0]

            if last_proc is not None and last_proc != p.id:
                context_switches += 1

            p.start_time = current_time
            p.response_time = p.start_time - p.arrival
            current_time += p.burst
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival
            p.waiting_time = p.turnaround_time - p.burst

            gantt.append((p.id, p.start_time, p.completion_time))
            last_proc = p.id
            completed.append(p)

        return procs, gantt, context_switches

    def round_robin(self, quantum: int = 3) -> Tuple[List[Process], List[Tuple[str, int, int]], int]:
        procs = self._get_fresh_processes()
        procs.sort(key=lambda x: x.arrival)
        current_time = 0
        queue = []
        gantt = []
        context_switches = 0
        last_proc = None
        completed_count = 0
        visited = set()

        def add_arrived():
            for p in procs:
                if p.arrival <= current_time and p.id not in visited and p.remaining_burst > 0:
                    queue.append(p)
                    visited.add(p.id)

        add_arrived()
        if not queue:
            current_time = procs[0].arrival
            add_arrived()

        while completed_count < len(procs):
            if not queue:
                uncompleted = [p for p in procs if p.remaining_burst > 0]
                if not uncompleted:
                    break
                next_p = min(uncompleted, key=lambda x: x.arrival)
                gantt.append(("IDLE", current_time, next_p.arrival))
                current_time = next_p.arrival
                add_arrived()
                continue

            p = queue.pop(0)

            if last_proc is not None and last_proc != p.id:
                context_switches += 1

            if p.response_time == -1:
                p.response_time = current_time - p.arrival

            exec_time = min(quantum, p.remaining_burst)
            start = current_time
            current_time += exec_time
            p.remaining_burst -= exec_time

            gantt.append((p.id, start, current_time))
            last_proc = p.id

            add_arrived()

            if p.remaining_burst > 0:
                queue.append(p)
            else:
                p.completion_time = current_time
                p.turnaround_time = p.completion_time - p.arrival
                p.waiting_time = p.turnaround_time - p.burst
                completed_count += 1

        return procs, gantt, context_switches

    def priority_preemptive(self) -> Tuple[List[Process], List[Tuple[str, int, int]], int]:
        procs = self._get_fresh_processes()
        current_time = 0
        completed = 0
        n = len(procs)
        gantt = []
        context_switches = 0
        last_proc = None

        while completed < n:
            ready = [p for p in procs if p.arrival <= current_time and p.remaining_burst > 0]
            if not ready:
                uncompleted = [p for p in procs if p.remaining_burst > 0]
                if not uncompleted:
                    break
                next_arr = min(p.arrival for p in uncompleted)
                gantt.append(("IDLE", current_time, next_arr))
                current_time = next_arr
                continue

            ready.sort(key=lambda x: (x.priority, x.arrival))
            p = ready[0]

            if last_proc is not None and last_proc != p.id:
                context_switches += 1

            if p.response_time == -1:
                p.response_time = current_time - p.arrival

            start = current_time
            current_time += 1
            p.remaining_burst -= 1

            if gantt and gantt[-1][0] == p.id:
                gantt[-1] = (p.id, gantt[-1][1], current_time)
            else:
                gantt.append((p.id, start, current_time))

            last_proc = p.id

            if p.remaining_burst == 0:
                p.completion_time = current_time
                p.turnaround_time = p.completion_time - p.arrival
                p.waiting_time = p.turnaround_time - p.burst
                completed += 1

        return procs, gantt, context_switches