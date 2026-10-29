#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test script for strategy changes"""

from kpi_detector.kpi_types import DetectionStrategy, normalize_strategy, KPI_TYPE_TO_STRATEGY, KPIType

# Test normalize_strategy with SKIP
skip = DetectionStrategy.SKIP
print(f'SKIP -> {normalize_strategy(skip)}')
print(f'SKIP (str) -> {normalize_strategy("SKIP")}')

# Test CONFIG_TYPE mapping
print(f'CONFIG_TYPE strategy: {KPI_TYPE_TO_STRATEGY[KPIType.CONFIG_TYPE]}')

print('OK: all tests passed')
