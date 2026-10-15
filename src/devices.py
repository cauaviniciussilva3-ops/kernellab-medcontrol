import threading
import time
from typing import Dict, List, Tuple

class DeviceManager:
    def __init__(self):
        self.access_matrix: Dict[str, Dict[str, List[str]]] = {
            "P1": {"Disco": [], "Rede": ["Ler", "Gravar", "Usar"], "Áudio": [], "Logs": ["Gravar"]},
            "P2": {"Disco": [], "Rede": ["Ler", "Gravar", "Usar"], "Áudio": [], "Logs": ["Gravar"]},
            "P3": {"Disco": ["Ler", "Gravar", "Exclusivo"], "Rede": [], "Áudio": [], "Logs": ["Gravar"]},
            "P4": {"Disco": [], "Rede": ["Usar", "Exclusivo"], "Áudio": ["Usar", "Exclusivo"], "Logs": ["Gravar"]},
            "P5": {"Disco": ["Ler", "Gravar", "Exclusivo"], "Rede": [], "Áudio": [], "Logs": ["Gravar"]},
            "P6": {"Disco": ["Ler", "Gravar"], "Rede": ["Usar"], "Áudio": [], "Logs": ["Gravar"]},
        }
        self.mutex_device = threading.Lock()
        self.semaphore_network = threading.Semaphore(2)
        self.log_history: List[str] = []

    def check_permission(self, process_id: str, device_name: str, action: str) -> bool:
        allowed = self.access_matrix.get(process_id, {}).get(device_name, [])
        return action in allowed

    def request_exclusive_access(self, process_id: str, device_name: str, action: str) -> Tuple[bool, str]:
        if not self.check_permission(process_id, device_name, action):
            msg = f"[ACESSO NEGADO] Processo {process_id} sem permissão de '{action}' no dispositivo '{device_name}'."
            self.log_history.append(msg)
            return False, msg

        acquired = self.mutex_device.acquire(timeout=1.0)
        if acquired:
            try:
                msg = f"[OK EXCLUSIVO] {process_id} obteve o Mutex para {action} em '{device_name}'."
                self.log_history.append(msg)
                time.sleep(0.05)
                return True, msg
            finally:
                self.mutex_device.release()
        else:
            msg = f"[BLOQUEADO] {process_id} sofreu timeout ao tentar acessar '{device_name}'."
            self.log_history.append(msg)
            return False, msg

    def request_shared_network(self, process_id: str, action: str) -> Tuple[bool, str]:
        if not self.check_permission(process_id, "Rede", action):
            msg = f"[ACESSO NEGADO] Processo {process_id} sem permissão na Rede."
            self.log_history.append(msg)
            return False, msg

        acquired = self.semaphore_network.acquire(timeout=1.0)
        if acquired:
            try:
                msg = f"[OK COMPARTILHADO] {process_id} usando vaga do Semáforo na Rede."
                self.log_history.append(msg)
                time.sleep(0.05)
                return True, msg
            finally:
                self.semaphore_network.release()
        else:
            msg = f"[BLOQUEADO] {process_id} sofreu timeout na Rede."
            self.log_history.append(msg)
            return False, msg