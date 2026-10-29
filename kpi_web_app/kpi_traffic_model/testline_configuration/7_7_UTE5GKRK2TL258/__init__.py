__maintainer__ = "Hubert Chrzan"
__team__ = "I_MN_RAN_RD_VRF_KRK_12"
__email__ = "I_MN_RAN_RD_VRF_KRK_12@internal.nsn.com"
__owner_email__ = "kacper.witek@nokia.com"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import NetworkAddress
from taf.config.testline.pdu import FPFH
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Airphone

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GKRK2TL258.bcu3.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_cu = CU(
    backhaul_site_oam_ip="192.168.255.129",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.1", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.1", vlan_id=1758),
    x2u=NetworkAddress(v4="10.0.1.1", vlan_id=1758),
    s1u=NetworkAddress(v4="10.0.1.1", vlan_id=1758),
)

_pdu1 = FPFH(port_numbers=[6], addr="10.253.167.11", login="admin", password="admin")
_pdu2 = FPFH(port_numbers=[5], addr="10.253.167.11", login="admin", password="admin")

_gnb_cu = CommonUnit(
    pdu_port=_pdu1.pdu_ports[6],
    lmp_connection=SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[
        CapacityUnit(addr="192.168.253.36"),
        CapacityUnit(addr="192.168.253.40"),
    ],
)

_cbts = ClassicalBts(cu=_cu, dus=[DU(airscale=Airscale(common_units=[_gnb_cu]))])

_ap_cu = CommonUnit(
    pdu_port=_pdu2.pdu_ports[5],
    lmp_connection=SshServiceDetails(
        addr="192.168.200.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[
        CapacityUnit(addr="192.168.253.84"),
        CapacityUnit(addr="192.168.253.88"),
    ],
)

_ue = Airphone(
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    Airscale([_ap_cu]),
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_BLL_AP_SA_L1B_CMWV",
    ues=[_ue],
)

__all__ = ["tl"]
