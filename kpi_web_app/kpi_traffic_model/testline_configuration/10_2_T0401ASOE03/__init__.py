__maintainer__ = 'Meghana J'
__team__ = 'I_MI_MN_RAN_RD_VRF_BLR2_INVICTUS'
__email__ = 'I_MI_MN_RAN_RD_VRF_BLR2_INVICTUS@internal.nsn.com'
__owner_email__ = 'meghana.j@nokia.com'

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (SshServiceDetails, HttpConnectionDetails)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline import Airphone
from taf.config.testline.pdu import Gude, FACOM, PduPort, Pdu, HBTE, RRB
#from taf.config.testline.pdu import ATEN


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


_pdu_1 = RRB(addr='10.71.247.5', port_numbers=[6])
_pdu_3 = RRB(addr='10.71.247.3', port_numbers=[1])    
_pdus = [_pdu_1, _pdu_3]



_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr='192.168.255.129',username='toor4nsn',password='oZPS0POrRieRtu'
    ),
    hardware_type='ASOE',
    capacity_units=[],
        pdu_port=_pdu_1.pdu_ports[6],
)
		
_airscale = Airscale([_common_unit])

_cu = CU(backhaul_site_oam_ip='192.168.255.129',
    oam_ssh_connection_details=SshServiceDetails(
        addr='192.168.255.129', username='toor4nsn', password='oZPS0POrRieRtu'),
    oam_http_connection_details=HttpConnectionDetails(
        addr='192.168.255.129', username='Nemuadmin', password='nemuuser'),
    x2c=NetworkAddress(v4='10.0.1.2', vlan_id=1),
    x2u=NetworkAddress(v4='10.0.1.2', vlan_id=1),
    s1u=NetworkAddress(v4='10.0.1.2', vlan_id=1),
)

_du = DU(_airscale)

_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=720001205)


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
                    CapacityUnit(addr='192.168.253.80', hardware_type='ABIO')],
                pdu_port=_pdu_3.pdu_ports[1],
			)
		]
	),
)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr='10.45.141.178',
        username='ute',
        password='UTE.debian12'
        ),
        connections=[_cbts.dus[0].airscale.common_units[0], _ue],
)

tl = TestLine(test_pc=_test_pc,
              gnbs=[_cbts],
               tl_cloud_topology='CLOUD_5G_O_E_AP_LO',
              ues=[_ue],
              pdus=_pdus)

__all__ = ['tl']