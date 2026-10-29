# KPI Anomaly Detector Package
# Version: 2.3.0 (ivy0203)
# Date: 2026-02-03
# Features: Reclassified strategies (IQR/Poisson/Relative/Z-Score/KS-Test)
#           Legacy strategies mapped to core strategies

from .detector import KPIAnomalyDetector
from .config import PATHS, COLORS
from .kpi_types import (
    KPIType, DetectionStrategy, 
    KPITypeClassifier, TypeBasedAnomalyDetector,
    StrategyBasedDetector, StrategyConfig,
    get_classifier, get_type_based_detector, get_strategy_based_detector,
    normalize_strategy, LEGACY_STRATEGY_MAP
)

__version__ = "2.3.0"
__all__ = [
    'KPIAnomalyDetector', 
    'PATHS', 
    'COLORS',
    'KPIType',
    'DetectionStrategy',
    'KPITypeClassifier',
    'TypeBasedAnomalyDetector',
    'StrategyBasedDetector',
    'StrategyConfig',
    'get_classifier',
    'get_type_based_detector',
    'get_strategy_based_detector',
    'normalize_strategy',
    'LEGACY_STRATEGY_MAP',
]
