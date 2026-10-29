__maintainer__ = "Hubert Chrzan"
__team__ = "I_MN_RAN_RD_VRF_KRK_12"
__email__ = "OU_MN_RAN_L3_SW_2_KRK_3_SG_53004197 <OU_MN_RAN_L3_SW_2_KRK_3_SG_53004197@internal.nsn.com>"
__owner_email__ = "hubert.chrzan@nokia.com"

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

_pdus = [
    FPFH(
        port_numbers=[1, 2, 3, 4, 5, 6],
        addr="10.253.167.15",
        login="admin",
        password="admin",
    )
]

_cu = CU(
    backhaul_site_oam_ip="192.168.255.129",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.1", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.1", vlan_id=1766),
    x2u=NetworkAddress(v4="10.0.1.1", vlan_id=1766),
    s1u=NetworkAddress(v4="10.0.1.1", vlan_id=1766),
)

_common_unit = CommonUnit(
    pdu_port=_pdus[0].pdu_ports[2],
    lmp_connection=SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[CapacityUnit(
        addr="192.168.253.36",
        hardware_type="ABIO"
    )],
    hardware_type="ASIL"
)

_du = DU(Airscale([_common_unit]))

_cbts = ClassicalBts(cu=_cu, dus=[_du])

_ue = Airphone(
    egate=SshServiceDetails("", ""),
    l2_ssh_connection_details=SshServiceDetails("", ""),
    l3_ssh_connection_details=SshServiceDetails("", ""),
    l1=Airscale(
        common_units=[
            CommonUnit(
                pdu_port=_pdus[0].pdu_ports[1],
                lmp_connection=SshServiceDetails(
                    addr="192.168.200.1", username="toor4nsn", password="oZPS0POrRieRtu"
                ),
                hardware_type="ASIL",
                capacity_units=[CapacityUnit(addr="192.168.253.84", hardware_type="ABIO")],
            )
        ]
    ),
)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GKRK2TL266.bcu3.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    ),
    connections=[_cbts.dus[0].airscale.common_units[0], _ue],
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_AP",
    ues=[_ue],
    pdus=_pdus,
)

__all__ = ["tl"]
