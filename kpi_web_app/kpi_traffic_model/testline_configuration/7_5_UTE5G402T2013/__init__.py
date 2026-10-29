__maintainer__ = 'Li Chun'
__team__ = 'RAN VRF HAZ3 T05'
__email__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05@internal.nsn.com>"
)
__owner_email__ = 'chun.li@nokia.com'

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (SshServiceDetails, HttpConnectionDetails)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline import Airphone
from taf.config.testline.pdu import HBTE


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


_pdu = HBTE(addr='10.71.195.42', port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_pdus = [_pdu]



_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr='192.168.255.1',username='toor4nsn',password='oZPS0POrRieRtu'
    ),
    hardware_type='ASIL',
    capacity_units=[
        CapacityUnit(addr="192.168.253.20", hardware_type='ABIO')],
        pdu_port=_pdus[0].pdu_ports[2],
)
		
_airscale = Airscale([_common_unit])

_cu = CU(backhaul_site_oam_ip='192.168.255.129',
    oam_ssh_connection_details=SshServiceDetails(
        addr='192.168.255.1', username='toor4nsn', password='oZPS0POrRieRtu'),
    oam_http_connection_details=HttpConnectionDetails(
        addr='192.168.255.1', username='Nemuadmin', password='nemuuser', port=443),
    x2c=NetworkAddress(v4='10.0.1.1', vlan_id=2507),
    x2u=NetworkAddress(v4='10.0.1.1', vlan_id=2507),
    s1u=NetworkAddress(v4='10.0.1.1', vlan_id=2507),
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
                hardware_type='ASIL',
                capacity_units=[
                    CapacityUnit(addr='192.168.253.84', hardware_type='ABIO')],
                pdu_port=_pdus[0].pdu_ports[6],
			)
		]
	),
)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr='10.101.60.100',
        username='ute',
        password='iW_K#8.ute%A10h0m0ra'
        ),
        connections=[_cbts.dus[0].airscale.common_units[0], _ue],
)

tl = TestLine(test_pc=_test_pc,
              gnbs=[_cbts],
              tl_cloud_topology='CLOUD_5G_I_LO_AP_LO',
              ues=[_ue],
              pdus=_pdus)

__all__ = ['tl']