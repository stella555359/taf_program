from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Callable, Dict, Tuple


@dataclass(frozen=True)
class RunnerJobKey:
    module_key: str
    job_id: str


class UnifiedRunner:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._threads: Dict[RunnerJobKey, threading.Thread] = {}
        self._dispatchers: Dict[str, threading.Thread] = {}

    def submit_threaded_job(self, module_key: str, job_id: str, target: Callable[[], None]) -> bool:
        job_key = RunnerJobKey(module_key=module_key, job_id=job_id)
        with self._lock:
            existing = self._threads.get(job_key)
            if existing is not None and existing.is_alive():
                return False
            thread = threading.Thread(target=self._run_and_cleanup, args=(job_key, target), daemon=True)
            self._threads[job_key] = thread
            thread.start()
            return True

    def submit_module_dispatcher(self, module_key: str, target: Callable[[], None]) -> bool:
        with self._lock:
            existing = self._dispatchers.get(module_key)
            if existing is not None and existing.is_alive():
                return False
            thread = threading.Thread(target=self._run_dispatcher_and_cleanup, args=(module_key, target), daemon=True)
            self._dispatchers[module_key] = thread
            thread.start()
            return True

    def is_job_running(self, module_key: str, job_id: str) -> bool:
        job_key = RunnerJobKey(module_key=module_key, job_id=job_id)
        with self._lock:
            thread = self._threads.get(job_key)
            return bool(thread is not None and thread.is_alive())

    def active_jobs(self) -> list[Tuple[str, str]]:
        with self._lock:
            return [
                (job_key.module_key, job_key.job_id)
                for job_key, thread in self._threads.items()
                if thread.is_alive()
            ]

    def active_dispatchers(self) -> list[str]:
        with self._lock:
            return [module_key for module_key, thread in self._dispatchers.items() if thread.is_alive()]

    def _run_and_cleanup(self, job_key: RunnerJobKey, target: Callable[[], None]) -> None:
        try:
            target()
        finally:
            with self._lock:
                current = self._threads.get(job_key)
                if current is threading.current_thread():
                    self._threads.pop(job_key, None)

    def _run_dispatcher_and_cleanup(self, module_key: str, target: Callable[[], None]) -> None:
        try:
            target()
        finally:
            with self._lock:
                current = self._dispatchers.get(module_key)
                if current is threading.current_thread():
                    self._dispatchers.pop(module_key, None)


_UNIFIED_RUNNER = UnifiedRunner()


def get_unified_runner() -> UnifiedRunner:
    return _UNIFIED_RUNNER