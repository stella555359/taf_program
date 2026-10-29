###########################################################
#          TL312 AEP CLOUD_5G_I_MPPP_AP_3[LOOO]           #
###########################################################
#  Template https://docs.uca.nsn-rdnet.net/docs/documentation/maintainer-guides/001-docs-configuration-files/ #
#  Template https://confluence.ext.net.nokia.com/display/AirPhoneWTS/UTE+Compatible+Variant+Naming+Convention+for+multi-AP+multi-WTS+TL+Configuration/ #

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
from taf.config.testline import Connection

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_pdu1 = FPFH(addr="10.0.96.66", port_numbers=[1, 3, 5])
_pdu2 = FPFH(addr="10.0.96.67", port_numbers=[1])
_pdus = [_pdu1,_pdu2]

_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"),
    hardware_type="ASIM",
    capacity_units=[
        CapacityUnit(addr="192.168.253.20", hardware_type="ABIP"),
        CapacityUnit(addr="192.168.253.24", hardware_type="ABIP"),
        CapacityUnit(addr="192.168.253.28", hardware_type="ABIP")],
    pdu_port=_pdus[0].pdu_ports[1],
)
_airscale = Airscale([_common_unit])
_du = DU(_airscale)

_cu = CU(backhaul_site_oam_ip="192.168.255.129",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser", port=443),
    x2c=NetworkAddress(v4="10.0.1.2", vlan_id=3312),
    x2u=NetworkAddress(v4="10.0.1.2", vlan_id=3312),
    s1u=NetworkAddress(v4="10.0.1.2", vlan_id=3312),
)

_gnb_master_Left = ClassicalBts(cu=_cu, dus=[_du])

_ABIO1 = CapacityUnit(addr="192.168.253.84", hardware_type="ABIO")
_ABIO2 = CapacityUnit(addr="192.168.253.88", hardware_type="ABIO")
_ABIO3 = CapacityUnit(addr="192.168.253.92", hardware_type="ABIO")

_ABIO4 = CapacityUnit(addr="192.168.253.84", hardware_type="ABIO")
_ABIO5 = CapacityUnit(addr="192.168.253.88", hardware_type="ABIO")
_ABIO6 = CapacityUnit(addr="192.168.253.92", hardware_type="ABIO")

_ABIO7 = CapacityUnit(addr="192.168.253.84", hardware_type="ABIO")
_ABIO8 = CapacityUnit(addr="192.168.253.88", hardware_type="ABIO")
_ABIO9 = CapacityUnit(addr="192.168.253.92", hardware_type="ABIO")

_ue1 = Airphone(
     egate=SshServiceDetails("", ""),
     l2_ssh_connection_details=SshServiceDetails("", ""),
     l3_ssh_connection_details=SshServiceDetails("", ""),
     l1=Airscale(
         common_units=[
             CommonUnit(
                 lmp_connection=SshServiceDetails("192.168.200.1", "toor4nsn", password="oZPS0POrRieRtu"),
                 hardware_type="ASIL",
                 capacity_units=[_ABIO1, _ABIO2, _ABIO3],
                 pdu_port=_pdus[0].pdu_ports[3],
             )
         ]
     ),
)

_ue2 = Airphone(
     egate=SshServiceDetails("", ""),
     l2_ssh_connection_details=SshServiceDetails("", ""),
     l3_ssh_connection_details=SshServiceDetails("", ""),
     l1=Airscale(
         common_units=[
             CommonUnit(
                 lmp_connection=SshServiceDetails("192.168.200.1", "toor4nsn", password="oZPS0POrRieRtu"),
                 hardware_type="ASIL",
                 capacity_units=[_ABIO4, _ABIO5, _ABIO6],
                 pdu_port=_pdus[0].pdu_ports[5],
             )
         ]
     ),
)

_ue3 = Airphone(
     egate=SshServiceDetails("", ""),
     l2_ssh_connection_details=SshServiceDetails("", ""),
     l3_ssh_connection_details=SshServiceDetails("", ""),
     l1=Airscale(
         common_units=[
             CommonUnit(
                 lmp_connection=SshServiceDetails("192.168.200.1", "toor4nsn", password="oZPS0POrRieRtu"),
                 hardware_type="ASIL",
                 capacity_units=[_ABIO7, _ABIO8, _ABIO9],
                 pdu_port=_pdus[1].pdu_ports[1],
             )
         ]
     ),
)
					   


_test_pc1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.0.108.241", username="ute", password="UTE.debian12"
    ),
    connections=[
        Connection(
            interface="eth1",
            interface_type="lmp",
            device=_gnb_master_Left.dus[0].airscale.common_units[0]
        ),
        Connection(
            interface="eth2",
            interface_type="lmp",
            device=_ue1
        )
    ]
)

_test_pc2 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.0.108.242", username="ute", password="UTE.debian12"
    ),
    connections=[
        Connection(
            interface="eth2",
            interface_type="lmp",
            device=_ue2
        )
    ]
)

_test_pc3 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.0.108.243", username="ute", password="UTE.debian12"
    ),
    connections=[
        Connection(
            interface="eth2",
            interface_type="lmp",
            device=_ue3
        )
    ]
)

tl = TestLine(
    test_pc=_test_pc1,
    test_pcs = [_test_pc1, _test_pc2, _test_pc3],
    gnbs=[_gnb_master_Left],
    tl_cloud_topology="CLOUD_5G_I_MPPP_AP_3[LOOO]",
    ues=[_ue1, _ue2, _ue3],
    pdus=_pdus,
)
__all__ = ["tl"]

