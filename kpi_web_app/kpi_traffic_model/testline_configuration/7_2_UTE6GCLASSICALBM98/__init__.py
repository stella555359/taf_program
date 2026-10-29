__maintainer__ = "I_5G_AIRPHONE_PZ_CIT_CRT_TEAM_GMS"
__team__ = "I_5G_AIRPHONE_PZ_CIT_CRT_TEAM_GMS"
__email__ = "I_5G_AIRPHONE_PZ_CIT_CRT_TEAM@internal.nsn.com"
__owner_email__ = "I_5G_AIRPHONE_PZ_CIT_CRT_TEAM@internal.nsn.com"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (SshServiceDetails, HttpConnectionDetails)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline import Airphone
from taf.config.testline.pdu import ATEN

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_pdu = ATEN(addr='10.63.69.182', port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_pdus = [_pdu]


_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr='192.168.255.129',username='toor4nsn',password='oZPS0POrRieRtu'
    ),
    hardware_type='ASOE',
    capacity_units=[],
    pdu_port=_pdus[0].pdu_ports[4],
)

_airscale = Airscale([_common_unit])

_cu = CU(
         backhaul_site_oam_ip='10.0.1.2',
         oam_ssh_connection_details=SshServiceDetails(
            addr='192.168.255.129', username='toor4nsn', password='oZPS0POrRieRtu'
         ),
         oam_http_connection_details=HttpConnectionDetails(
            addr='192.168.255.129', username='Nemuadmin', password='nemuuser'
         ),
         x2c=NetworkAddress(v4='10.0.1.1', vlan_id=103),
         x2u=NetworkAddress(v4='10.0.1.2', vlan_id=103),
         s1u=NetworkAddress(v4='10.0.1.2', vlan_id=103),
         ngu=NetworkAddress(v4='10.0.1.2', vlan_id=103),
)

_du = DU(_airscale)

_cbts = ClassicalBts(cu=_cu, dus=[_du])

_ue = Airphone(
    egate=SshServiceDetails("", ""),
    l2_ssh_connection_details=SshServiceDetails("", ""),
    l3_ssh_connection_details=SshServiceDetails("", ""),
    l1=Airscale(
        common_units=[
            CommonUnit(
                lmp_connection=SshServiceDetails(
                    "192.168.200.1", "toor4nsn", password="oZPS0POrRieRtu"
                ),
                hardware_type='ASOE',
                capacity_units=[],
                pdu_port=_pdus[0].pdu_ports[3],
            )
        ]
    ),
)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr='10.63.80.4',
        username='ute',
        password='ute'
    ),
    connections=[_cbts.dus[0].airscale.common_units[0], _ue],
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_O_E_AP_E",
    ues=[_ue],
    pdus=_pdus,
    host_ip='10.63.80.3'
)

__all__ = ['tl']
