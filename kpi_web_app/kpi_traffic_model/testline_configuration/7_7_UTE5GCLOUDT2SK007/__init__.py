__maintainer__ = "Tomasz Pyrek"
__team__ = "I_MN_RAN_RD_VRF_KRK_1"
__email__ = "I_MN_RAN_RD_VRF_KRK_1@internal.nsn.com"
__owner_email__ = "tomasz.pyrek@nokia.com"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline import Airphone
from taf.config.testline import Connection
from taf.config.testline.pdu import FPFH

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_pdu = FPFH(
    addr="10.255.11.18",
    port_numbers=[1, 2, 3, 4, 5, 6],
    login="admin",
    password="admin",
)

_common_unit = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_pdu.pdu_ports[3],
    hardware_type="ASOE",
)

_airscale = Airscale([_common_unit])

_cu = CU(
    backhaul_site_oam_ip="192.168.255.129",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.1", vlan_id=1507),
    x2u=NetworkAddress(v4="10.0.1.1", vlan_id=1507),
    s1u=NetworkAddress(v4="10.0.1.1", vlan_id=1507),
    ngu=NetworkAddress(v4="10.0.1.1", vlan_id=1507),
)

_du = DU(_airscale)

_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=770000071)

_ABIO1 = CapacityUnit(addr="192.168.253.84", hardware_type="ABIO")
_ABIO2 = CapacityUnit(addr="192.168.253.84", hardware_type="ABIO")
_ABIO3 = CapacityUnit(addr="192.168.253.84", hardware_type="ABIO")
_ABIO4 = CapacityUnit(addr="192.168.253.84", hardware_type="ABIO")
_ABIO5 = CapacityUnit(addr="192.168.253.84", hardware_type="ABIO")
_ABIO6 = CapacityUnit(addr="192.168.253.84", hardware_type="ABIO")


_ue1 = Airphone(
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    Airscale(
        [
            CommonUnit(
                SshServiceDetails(
                    "192.168.200.1", "toor4nsn", password="oZPS0POrRieRtu"
                ),
                capacity_units=[_ABIO1, _ABIO2, _ABIO3],
                pdu_port=_pdu.pdu_ports[2],
                hardware_type="ASIL",
            )
        ]
    ),
)

_ue2 = Airphone(
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    Airscale(
        [
            CommonUnit(
                SshServiceDetails(
                    "192.168.200.2", "toor4nsn", password="oZPS0POrRieRtu"
                ),
                capacity_units=[_ABIO4, _ABIO5, _ABIO6],
                pdu_port=_pdu.pdu_ports[4],
                hardware_type="ASIL",
            )
        ]
    ),
)

_test_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT2SK007.p02.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    ),
    connections=[
        Connection(
            interface="eth1",
            interface_type="lmp",
            device=_cbts.dus[0].airscale.common_units[0],
        ),
        Connection(interface="eth2", interface_type="lmp", device=_ue1),
        Connection(interface="eth5", interface_type="lmp", device=_ue2),
    ],
)

tl = TestLine(
    test_pc=_test_pc_1,
    test_pcs=[_test_pc_1],
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_O_E_AP_2LOOO",
    ues=[_ue1, _ue2],
    pdus=_pdu,
)

__all__ = ["tl"]
