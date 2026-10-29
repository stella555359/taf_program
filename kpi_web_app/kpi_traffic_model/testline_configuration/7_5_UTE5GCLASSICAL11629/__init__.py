__maintainer__ = "yuema"
__team__ = "I_EXT_MN_RAN_L2_SW_1_CN_09_SG_GMS"
__email__ = "I_EXT_MN_RAN_L2_SW_1_CN_09_SG@internal.nsn.com"
__owner_email__ = "yue.4.ma@nokia-sbell.com"


import os
from taf.config.testline.testline import TestLine
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import NetworkAddress
from taf.config.testline import Airphone
from taf.config.testline.pdu import HBTE


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_pdu1 = HBTE(addr="10.64.49.29", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_pdu2 = HBTE(addr="10.64.49.29", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_pdus = [_pdu1, _pdu2]


_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr='192.168.255.1', username='toor4nsn', password='oZPS0POrRieRtu'
        ),
        hardware_type='ASIL',
        capacity_units=[
            CapacityUnit(addr='192.168.253.20', hardware_type='ABIO')],
            pdu_port=_pdus[0].pdu_ports[4],
)

_airscale = Airscale([_common_unit])

_cu = CU(
    backhaul_site_oam_ip='192.168.255.129',
    oam_ssh_connection_details=SshServiceDetails(
        addr='192.168.255.1', username='toor4nsn', password='oZPS0POrRieRtu'
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr='192.168.255.1', username='Nemuadmin', password='nemuuser'
    ),
    x2c=NetworkAddress(v4='10.1.1.1', vlan_id=2298),
    x2u=NetworkAddress(v4='10.1.1.1', vlan_id=2298),
    s1u=NetworkAddress(v4='10.1.1.1', vlan_id=2298),
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
                    '192.168.200.1', 'toor4nsn', password='oZPS0POrRieRtu'
                ),
                hardware_type='ASIL',
                capacity_units=[
                   CapacityUnit(addr='192.168.253.84', hardware_type='ABIO')],
                pdu_port=_pdus[1].pdu_ports[5],
                        )
                ] 
    ),
)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr='10.57.208.33', 
        username='ute', 
        password='ute'
        ),
        connections=[_cbts.dus[0].airscale.common_units[0], _ue],
)



tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_I_LO_AP_LO",
    ues=[_ue],
    pdus=_pdus,
)

__all__ = ['tl']
