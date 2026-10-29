from __future__ import annotations

from typing import Any

from .models import NormalizedUe


class UeExtractor:
    def extract(self, tl: Any) -> list[NormalizedUe]:
        raw_ues = list(getattr(tl, 'ues', []) or [])
        normalized_ues: list[NormalizedUe] = []
        for ue_index, ue in enumerate(raw_ues):
            normalized_ues.append(self.normalize_ue(ue, ue_index))
        return normalized_ues

    def normalize_ue(self, ue: Any, ue_index: int) -> NormalizedUe:
        ue_type = str(getattr(ue, 'ue_type', '') or ue.__class__.__name__).strip().lower()
        ue_ip = self._detect_ue_ip(ue)
        label = self._build_label(ue_index, ue_type, ue_ip)
        capabilities = list(getattr(ue, 'capabilities', []) or [])
        serial_number = getattr(ue, 'serial_number', None)
        return NormalizedUe(
            ue_index=ue_index,
            ue_type=ue_type,
            ue_ip=ue_ip,
            label=label,
            serial_number=str(serial_number) if serial_number not in (None, '') else None,
            capabilities=[str(capability) for capability in capabilities],
            raw_object=ue,
        )

    def extract_summary(self, tl: Any) -> dict[str, Any]:
        return {
            'ue_count': len(getattr(tl, 'ues', []) or []),
            'gnb_count': len(getattr(tl, 'gnbs', []) or []),
            'enb_count': len(getattr(tl, 'enbs', []) or []),
            'has_appserver': getattr(tl, 'appserver', None) is not None,
            'has_test_pc': getattr(tl, 'test_pc', None) is not None,
            'topology_id': getattr(tl, 'tl_cloud_topology', None),
        }

    def _detect_ue_ip(self, ue: Any) -> str | None:
        direct_ip = getattr(ue, 'ue_pc_address', None)
        if direct_ip:
            return str(direct_ip)

        ssh_details = getattr(ue, 'ssh_connection_details', None)
        ssh_addr = getattr(ssh_details, 'addr', None)
        if ssh_addr:
            return str(ssh_addr)

        generic_addr = getattr(ue, 'addr', None)
        if generic_addr:
            return str(generic_addr)
        return None

    def _build_label(self, ue_index: int, ue_type: str, ue_ip: str | None) -> str:
        suffix = ue_ip or 'unknown_ip'
        return f'{ue_index}_{ue_type}_{suffix}'
