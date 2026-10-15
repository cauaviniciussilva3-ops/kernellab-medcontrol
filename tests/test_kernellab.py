import pytest
from src.schedulers import CPUScheduler
from src.memory import MemorySimulator
from src.devices import DeviceManager

@pytest.fixture
def sample_processes():
    return [
        {"id": "P1", "function": "Teste 1", "arrival": 0, "burst": 5, "priority": 1, "memory": 100, "device": "Rede"},
        {"id": "P2", "function": "Teste 2", "arrival": 1, "burst": 2, "priority": 0, "memory": 50, "device": "Disco"}
    ]

def test_fcfs_scheduler(sample_processes):
    sched = CPUScheduler(sample_processes)
    procs, gantt, switches = sched.fcfs()
    assert len(procs) == 2
    assert procs[0].completion_time == 5
    assert procs[1].completion_time == 7

def test_memory_lru():
    mem = MemorySimulator(num_frames=3)
    pages = [1, 2, 3, 1, 4, 1]
    hist, hits, faults, rate = mem.lru(pages)
    assert hits + faults == len(pages)
    assert faults > 0

def test_device_security():
    dev = DeviceManager()
    allowed, msg = dev.request_exclusive_access("P4", "Áudio", "Usar")
    assert allowed is True
    denied, msg_denied = dev.request_exclusive_access("P1", "Disco", "Exclusivo")
    assert denied is False