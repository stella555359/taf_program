from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from ..adapters.base import ModuleRepository


PORTAL_ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_ROOT = PORTAL_ROOT.parent


REPOSITORIES: Dict[str, ModuleRepository] = {
    'kpi-anomaly-detector': ModuleRepository(
        key='kpi-anomaly-detector',
        title='KPI Anomaly Detector',
        summary='Upload KPI Excel data, compare with history, and generate HTML or Excel anomaly reports.',
        route_name='kpi_detector.index',
        repo_path=WORKSPACE_ROOT / 'kpi-anomaly-detector',
        readme_path=WORKSPACE_ROOT / 'kpi-anomaly-detector' / 'README.md',
        entry_candidates=[
            WORKSPACE_ROOT / 'kpi-anomaly-detector' / 'scripts' / 'run_detector.py',
            WORKSPACE_ROOT / 'kpi-anomaly-detector' / 'scripts' / 'kpi_detector' / 'detector.py',
        ],
    ),
    'kpi-generator': ModuleRepository(
        key='kpi-generator',
        title='KPI Generator',
        summary='Generate Compass KPI reports from timestamp ranges, then finalize them with analysis, compare, or horizontal merge.',
        route_name='kpi_generator.index',
        repo_path=WORKSPACE_ROOT / 'kpi-generator',
        readme_path=WORKSPACE_ROOT / 'kpi-generator' / 'README.md',
        entry_candidates=[
            WORKSPACE_ROOT / 'kpi-generator' / 'kpi_generator.py',
        ],
    ),
    'kpi-traffic-model': ModuleRepository(
        key='kpi-traffic-model',
        title='KPI Traffic Model',
        summary='Run testline-driven KPI traffic workflows with env resolution, UE selection, and a schema-first orchestrator.',
        route_name='kpi_traffic_model.index',
        repo_path=WORKSPACE_ROOT / 'kpi_traffic_model',
        readme_path=WORKSPACE_ROOT / 'kpi_traffic_model' / 'testline_configuration' / 'README.md',
        entry_candidates=[
            WORKSPACE_ROOT / 'kpi_traffic_model' / 'orchestrator' / 'request_loader.py',
            WORKSPACE_ROOT / 'kpi_traffic_model' / 'orchestrator' / 'config_resolver.py',
            WORKSPACE_ROOT / 'kpi_traffic_model' / 'orchestrator' / 'runner.py',
        ],
    ),
}


def get_repository(key: str) -> ModuleRepository:
    return REPOSITORIES[key]


def get_module_cards() -> List[dict]:
    cards: List[dict] = []
    for repository in REPOSITORIES.values():
        cards.append(
            {
                'key': repository.key,
                'title': repository.title,
                'summary': repository.summary,
                'route_name': repository.route_name,
                'repo_exists': repository.repo_path.exists(),
                'readme_exists': repository.readme_path.exists(),
                'entry_count': sum(1 for path in repository.entry_candidates if path.exists()),
                'repo_path': str(repository.repo_path),
            }
        )
    return cards