__maintainer__ = "wu hongmei"
__team__ = "I_EXT_MN_RAN_L2_SW_1_CN_06_SG_GMS"
__email__ = "I_EXT_MN_RAN_L2_SW_1_CN_06_SG@internal.nsn.com"
__owner_email__ = "hongmei.m.wu@nokia-sbell.com"



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
from taf.config.testline.pdu import HBTE
from taf.config.testline import Connection

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_pdu = HBTE(addr="10.68.4.235", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_pdus = [_pdu]

_pdu_ap = HBTE(addr="10.68.4.234", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_pdus_ap = [_pdu_ap]

_capacity_unit = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIN",
)

_common_unit = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
    pdu_port=_pdus[0].pdu_ports[4],
    hardware_type="ASIL",
)

_airscale = Airscale(common_units=[_common_unit])

_cu = CU(
    backhaul_site_oam_ip="192.168.255.129",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.1", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.1", vlan_id=1834),
    x2u=NetworkAddress(v4="10.0.1.1", vlan_id=1834),
    s1u=NetworkAddress(v4="10.0.1.1", vlan_id=1834),
    ngu=NetworkAddress(v4="10.0.1.1", vlan_id=1834),
)

_du = DU(airscale=_airscale)

_cbts = ClassicalBts(cu=_cu, dus=[_du])


_ue = Airphone(
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    Airscale(
        [
            CommonUnit(
                SshServiceDetails(
                    "192.168.200.1", "toor4nsn", password="oZPS0POrRieRtu"
                ),
                [CapacityUnit(addr="192.168.253.84", hardware_type="ABIO")],
                pdu_port=_pdus_ap[0].pdu_ports[4],
                hardware_type="ASIL",
            )
        ]
    ),
)


_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.4.14", username="ute", password="ute"
    ),
    connections=[
        Connection(
           interface="eth1",
           interface_type="lmp",
           device=_cbts.dus[0].airscale.common_units[0]
        ),
        Connection(
            interface="eth2",
            interface_type="lmp",
            device=_ue
        )
    ]
)


tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_I_LN_AP_LO",
    ues=[_ue],
    pdus=_pdus,
)

__all__ = ["tl"]
