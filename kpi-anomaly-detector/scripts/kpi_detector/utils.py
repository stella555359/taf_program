# -*- coding: utf-8 -*-
"""
Utility functions for KPI Anomaly Detector
"""

import re
from typing import Any, Dict, Optional

import numpy as np
import pandas as pd


HISTORY_CONTEXT_PATTERN = re.compile(
    r'(?P<test_config>T\d+(?:\.[^_]+)*)_(?P<scenario>.+?)_(?P<run>\d+csv(?:\d+run|\d+)?)',
    re.IGNORECASE,
)
ENVIRONMENT_PATTERN = re.compile(r'^(T\d+)', re.IGNORECASE)
UE_TOKEN_PATTERN = re.compile(r'^(?P<ue>\d+ue)s?(?:[_\-.]+(?P<label>.*))?$', re.IGNORECASE)
RUN_TOKEN_PATTERN = re.compile(r'^\d+csv(?:\d+run|\d+)?$', re.IGNORECASE)


def classify_code(code: str) -> str:
    """Classify Code as Counter or KPI type
    
    Args:
        code: The code string to classify
        
    Returns:
        'Counter', 'KPI', or 'Other'
    """
    code = str(code).strip()
    if re.match(r'^M\d{5}C\d{1,5}$', code, re.IGNORECASE):
        return 'Counter'
    elif re.search(r'NR', code, re.IGNORECASE):
        return 'KPI'
    else:
        return 'Other'


def generate_sparkline(raw_data: str) -> str:
    """Generate text-based sparkline using Unicode bar characters
    
    Args:
        raw_data: Comma-separated numeric values
        
    Returns:
        Unicode sparkline string
    """
    if not raw_data:
        return ''
    
    try:
        values = [float(x) for x in raw_data.split(',') if x.strip()]
        if not values:
            return ''
        
        # Unicode bar characters (low to high)
        bars = '\u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588'
        
        min_val = min(values)
        max_val = max(values)
        
        if max_val == min_val:
            # All values are the same, use middle height
            return bars[4] * len(values)
        
        # Normalize to 0-7 range
        sparkline = ''
        for v in values:
            normalized = (v - min_val) / (max_val - min_val)
            bar_idx = int(normalized * 7)
            bar_idx = min(7, max(0, bar_idx))
            sparkline += bars[bar_idx]
        
        return sparkline
    except:
        return ''


def parse_raw_data(raw_data: str) -> list:
    """Parse comma-separated raw data string to list of floats
    
    Args:
        raw_data: Comma-separated numeric values
        
    Returns:
        List of float values
    """
    if not raw_data:
        return []
    try:
        return [float(x) for x in raw_data.split(',') if x.strip()]
    except:
        return []


def calculate_cv(values: list) -> tuple:
    """Calculate coefficient of variation
    
    Args:
        values: List of numeric values
        
    Returns:
        Tuple of (mean, std, cv_percentage)
    """
    if not values:
        return np.nan, np.nan, np.nan
    
    arr = np.array(values)
    mean_val = np.mean(arr)
    std_val = np.std(arr, ddof=0)
    
    if abs(mean_val) < 0.001:
        cv = np.nan
    else:
        cv = (std_val / mean_val) * 100
    
    return mean_val, std_val, cv


def calculate_trimmed_cv(values: list) -> tuple:
    """Calculate CV after removing min and max values
    
    Args:
        values: List of numeric values (must have >= 5 elements)
        
    Returns:
        Tuple of (trimmed_mean, trimmed_std, trimmed_cv)
    """
    if len(values) < 5:
        return np.nan, np.nan, np.nan
    
    sorted_vals = sorted(values)
    trimmed = sorted_vals[1:-1]  # Remove min and max
    
    return calculate_cv(trimmed)


def is_kpi_pattern(code: str) -> bool:
    """Check if code matches KPI pattern (NR_XXXXx or SCOUT_NR_XXXXx)
    
    Args:
        code: Code string to check
        
    Returns:
        True if matches KPI pattern
    """
    pattern = r'((?:SCOUT_)?NR_\d{2,4})([a-zA-Z])'
    return bool(re.search(pattern, code, re.IGNORECASE))


def is_counter_pattern(code: str) -> bool:
    """Check if code matches Counter pattern (MxxxxxCxxxxx)
    
    Args:
        code: Code string to check
        
    Returns:
        True if matches Counter pattern
    """
    return bool(re.match(r'^M\d{5}C\d{1,5}$', code, re.IGNORECASE))


def normalize_scenario_key(scenario: str) -> str:
    """Normalize scenario text for reliable history matching."""
    normalized = re.sub(r'[^0-9A-Za-z]+', '_', str(scenario).strip()).strip('_').lower()
    normalized = re.sub(r'(?<=\d)ues?(?=_|$)', 'ue', normalized)
    return normalized


def build_history_context_payload(test_config: str, scenario: str) -> Optional[Dict[str, Any]]:
    environment_match = ENVIRONMENT_PATTERN.search(test_config)
    environment = environment_match.group(1).upper() if environment_match else None
    scenario = str(scenario).strip(' _.')
    if not environment or not scenario:
        return None

    scenario_key = normalize_scenario_key(scenario)

    ue_count = None
    scenario_label = scenario
    ue_match = UE_TOKEN_PATTERN.match(scenario_key)
    if ue_match:
        ue_count = ue_match.group('ue').upper()
        label = ue_match.group('label')
        if label:
            scenario_label = label.replace('_', ' ')

    return {
        'environment': environment,
        'test_config': test_config.strip(),
        'scenario': scenario,
        'scenario_key': scenario_key,
        'scenario_label': scenario_label,
        'ue_count': ue_count,
        'history_key': f'{environment}:{scenario_key}',
    }


def extract_history_context_from_tokens(stem: str) -> Optional[Dict[str, Any]]:
    tokens = [token.strip() for token in str(stem).split('_') if token.strip()]
    if not tokens:
        return None

    env_index = next((index for index, token in enumerate(tokens) if ENVIRONMENT_PATTERN.match(token)), None)
    if env_index is None:
        return None

    run_index = next(
        (index for index in range(env_index + 1, len(tokens)) if RUN_TOKEN_PATTERN.match(tokens[index])),
        None,
    )
    if run_index is None:
        return None

    scenario_start = next(
        (
            index for index in range(env_index + 1, run_index)
            if UE_TOKEN_PATTERN.match(normalize_scenario_key(tokens[index]))
        ),
        None,
    )
    if scenario_start is None:
        scenario_start = env_index + 1

    scenario_tokens = tokens[scenario_start:run_index]
    if not scenario_tokens:
        return None

    return build_history_context_payload(tokens[env_index], '_'.join(scenario_tokens))


def extract_history_context(filename: str) -> Optional[Dict[str, Any]]:
    """Extract environment and scenario context from supported KPI report filenames."""
    if not filename:
        return None

    basename = str(filename).rsplit('/', 1)[-1].rsplit('\\', 1)[-1]
    stem = basename.rsplit('.', 1)[0]

    token_context = extract_history_context_from_tokens(stem)
    if token_context is not None:
        return token_context

    match = HISTORY_CONTEXT_PATTERN.search(stem)
    if not match:
        return None

    return build_history_context_payload(match.group('test_config').strip(), match.group('scenario'))


def extract_history_context_from_record(record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Read history context from a record, falling back to filename parsing."""
    if not record:
        return None

    environment = record.get('environment')
    test_config = record.get('test_config')
    scenario = record.get('scenario')
    scenario_key = record.get('scenario_key')
    history_key = record.get('history_key')

    if environment and scenario_key:
        normalized_key = normalize_scenario_key(str(scenario_key))
        return {
            'environment': str(environment).upper(),
            'test_config': test_config,
            'scenario': scenario or scenario_key,
            'scenario_key': normalized_key,
            'scenario_label': record.get('scenario_label') or scenario or scenario_key,
            'ue_count': record.get('ue_count'),
            'history_key': history_key or f"{str(environment).upper()}:{normalized_key}",
        }

    return extract_history_context(record.get('filename', ''))
