__maintainer__ = "Jakub Wachal"
__team__ = "I_5GSC_SW_ENG_KRK_VRF_GMS"
__email__ = "I_5GSC_SW_ENG_KRK_VRF_GMS <I_5GSC_SW_ENG_KRK_VRF@internal.nsn.com>"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection
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

_cu = CU(
    backhaul_site_oam_ip="10.0.1.2",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.2", vlan_id=1650),
    x2u=NetworkAddress(v4="10.0.1.2", vlan_id=1650),
    s1u=NetworkAddress(v4="10.0.1.2", vlan_id=1650),
)
_pdu1 = FPFH(port_numbers=[5], addr="10.255.11.19", login="admin", password="admin")
_pdu2 = FPFH(port_numbers=[4], addr="10.255.11.19", login="admin", password="admin")
_abio1_du1 = CapacityUnit(addr="192.168.253.16")
_asib_du1 = CommonUnit(
    pdu_port=_pdu1.pdu_ports[5],
    lmp_connection=SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    hardware_type="ASIB",
    capacity_units=[
        CapacityUnit(addr="192.168.253.20", hardware_type="ABIO"),
        CapacityUnit(addr="192.168.253.24", hardware_type="ABIO"),
    ],
)
_du1 = DU(airscale=Airscale(common_units=[_asib_du1]))
_cbts = ClassicalBts(cu=_cu, dus=[_du1])
_ue = Airphone(
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    Airscale(
        [
            CommonUnit(
                pdu_port=_pdu2.pdu_ports[4],
                lmp_connection=SshServiceDetails(
                    addr="192.168.200.1", username="toor4nsn", password="oZPS0POrRieRtu"
                ),
                hardware_type="ASIL",
                capacity_units=[
                    CapacityUnit(addr="192.168.253.84", hardware_type="ABIO"),
                    CapacityUnit(addr="192.168.253.85", hardware_type="ABIO"),
                ],
            )
        ]
    ),
)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT2SK150.p02.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_cbts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        ),
        _ue,
    ],
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_X_XX_AP_",
    pdus=[_pdu1, _pdu2],
    ues=[_ue],
)

__all__ = ["tl"]
