from __future__ import annotations

import threading
import unittest

from portal.runners.unified_runner import UnifiedRunner


class UnifiedRunnerTests(unittest.TestCase):
    def test_submit_threaded_job_prevents_duplicate_running_job(self) -> None:
        runner = UnifiedRunner()
        started = threading.Event()
        release = threading.Event()

        def target() -> None:
            started.set()
            release.wait(timeout=5)

        first = runner.submit_threaded_job('kpi-generator', 'job-1', target)
        self.assertTrue(first)
        self.assertTrue(started.wait(timeout=2))

        second = runner.submit_threaded_job('kpi-generator', 'job-1', target)
        self.assertFalse(second)
        self.assertTrue(runner.is_job_running('kpi-generator', 'job-1'))

        release.set()
        for _ in range(50):
            if not runner.is_job_running('kpi-generator', 'job-1'):
                break
            threading.Event().wait(0.02)

        self.assertFalse(runner.is_job_running('kpi-generator', 'job-1'))

    def test_submit_module_dispatcher_prevents_duplicate_dispatcher(self) -> None:
        runner = UnifiedRunner()
        started = threading.Event()
        release = threading.Event()

        def target() -> None:
            started.set()
            release.wait(timeout=5)

        first = runner.submit_module_dispatcher('kpi-generator', target)
        self.assertTrue(first)
        self.assertTrue(started.wait(timeout=2))

        second = runner.submit_module_dispatcher('kpi-generator', target)
        self.assertFalse(second)
        self.assertIn('kpi-generator', runner.active_dispatchers())

        release.set()
        for _ in range(50):
            if 'kpi-generator' not in runner.active_dispatchers():
                break
            threading.Event().wait(0.02)

        self.assertNotIn('kpi-generator', runner.active_dispatchers())