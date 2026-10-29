############################################
#    TL306D02 AEP CLOUD_5G_I_MP_AP_LOOO    #
############################################
#  https://confluence.ext.net.nokia.com/display/MNRANVRFNPS/7-20-UTE5GVMTL306D-02

__maintainer__ = 'Philippe Fressard'
__team__ = 'MN_5G_SC_NPS_ET'
__email__ = 'philippe.fressard@nokia.com'


import os
from taf.config.testline.testline import TestLine
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (SshServiceDetails, HttpConnectionDetails)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline import Airphone
from taf.config.testline.pdu import FPFH

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_pdu1 = FPFH(addr='10.0.116.207',port_numbers=[2, 4], protocol="http")
_pdus = [_pdu1]

_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr='192.168.255.129',username='toor4nsn',password='oZPS0POrRieRtu'
    ),
    hardware_type='ASIM',
    capacity_units=[
        CapacityUnit(addr="192.168.253.36", hardware_type='ABIP')],
    pdu_port=_pdu1.pdu_ports[2],
)

_airscale = Airscale([_common_unit])

_cu = CU(backhaul_site_oam_ip='192.168.255.129',
    oam_ssh_connection_details=SshServiceDetails(
        addr='192.168.255.129', username='toor4nsn', password='oZPS0POrRieRtu'),
    oam_http_connection_details=HttpConnectionDetails(
        addr='192.168.255.129', username='Nemuadmin', password='nemuuser', port=443),
    x2c=NetworkAddress(v4='10.0.1.60', vlan_id=3307),
    x2u=NetworkAddress(v4='10.0.1.60', vlan_id=3307),
    s1u=NetworkAddress(v4='10.0.1.60', vlan_id=3307),
)

_du = DU(_airscale)

_cbts = ClassicalBts(cu=_cu, dus=[_du])

_ABIO1 = CapacityUnit(addr='192.168.253.100', hardware_type='ABIO')
_ABIO2 = CapacityUnit(addr='192.168.253.104', hardware_type='ABIO')
_ABIO3 = CapacityUnit(addr='192.168.253.108', hardware_type='ABIO')


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
                capacity_units=[_ABIO1,_ABIO2,_ABIO3],
                pdu_port=_pdu1.pdu_ports[4],
			)
		]
	),
)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr='10.0.108.232',
        username='ute',
        password='UTE.debian12'
        ),
    connections=[_cbts.dus[0].airscale.common_units[0],_ue],
)

#CLOUD_5G_I_[LP]_AP_1x[LOOO]
tl = TestLine(test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology='CLOUD_5G_I_MP_AP_LOOO',
    ues=[_ue],
    pdus=_pdus,
)
__all__ = ["tl"]
