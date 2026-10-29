__maintainer__ = "Chen.yili"
__team__ = "I_MN_RAN_L3_SW_1_CN_BLUES_GMS"
__email__ = "I_MN_RAN_L3_SW_1_CN_BLUES@internal.nsn.com"
__owner_email__ = "yili.chen@nokia-sbell.com"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    HttpConnectionDetails,
    SshServiceDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import NetworkAddress
from taf.config.testline.pdu import TopYoung
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Airphone
from taf.config.testline import Connection

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


# pdu setting is adapted because local tl gnb1/gnb2/ap may be connected to different PDUs
# _pdu1 = FACOM(
#     port_numbers=[4, 5, 6],
#     addr="10.56.124.239",
# )
# _pdus = [_pdu1]

_pdu_gnb1 = TopYoung(
    port_numbers=[4],
    addr="10.56.124.236",
)

_pdu_gnb2 = TopYoung(
    port_numbers=[5],
    addr="10.56.124.236",
)

_pdu_ap = TopYoung(
    port_numbers=[6],
    addr="10.56.124.236",
)
_pdus = [_pdu_gnb1, _pdu_gnb2, _pdu_ap]

_capacity_unit_1 = CapacityUnit(addr="192.168.253.20", hardware_type='ABIP')
_common_unit_1 = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit_1],
    pdu_port=_pdus[0].pdu_ports[4],
    hardware_type="ASIM",
)
_airscale_1 = Airscale(common_units=[_common_unit_1])
_cu_1 = CU(
    backhaul_site_oam_ip="10.0.1.2",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.2", vlan_id=1634),
    x2u=NetworkAddress(v4="10.0.1.2", vlan_id=1634),
    s1u=NetworkAddress(v4="10.0.1.2", vlan_id=1634),
    ngu=NetworkAddress(v4="10.0.1.2", vlan_id=1634),
)

_du_1 = DU(airscale=_airscale_1)
_cbts_1 = ClassicalBts(cu=_cu_1, dus=[_du_1])
_capacity_unit_2 = CapacityUnit(addr="192.168.253.36", hardware_type='ABIP')

_common_unit_2 = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit_2],
    pdu_port=_pdus[1].pdu_ports[5],
    hardware_type="ASIM",
)

_airscale_2 = Airscale(common_units=[_common_unit_2])


_cu_2 = CU(
    backhaul_site_oam_ip="10.0.1.3",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.3", vlan_id=1634),
    x2u=NetworkAddress(v4="10.0.1.3", vlan_id=1634),
    s1u=NetworkAddress(v4="10.0.1.3", vlan_id=1634),
    ngu=NetworkAddress(v4="10.0.1.3", vlan_id=1634),
)



_du_2 = DU(airscale=_airscale_2)

_cbts_2 = ClassicalBts(cu=_cu_2, dus=[_du_2])

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
                [CapacityUnit(addr="192.168.253.84", hardware_type='ABIO'),
                CapacityUnit(addr="192.168.253.88", hardware_type='ABIO'),
                CapacityUnit(addr="192.168.253.92", hardware_type='ABIO'),],
                pdu_port=_pdus[2].pdu_ports[6],
                hardware_type="ASIL",
            )
        ]
    ),
)


_test_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.71.187.232",
        username="ute",
        password="tribe!L3SW1CN@",
    ),
    connections=[
        Connection(
           interface="eth1",
           interface_type="lmp",
           device=_cbts_1.dus[0].airscale.common_units[0]
        ),
        Connection(
            interface="eth2",
            interface_type="lmp",
            device=_ue
        )
    ]
)

_test_pc_2 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.71.187.230",
        username="ute",
        password="ute",
    ),
    connections=[
        Connection(
           interface="eth1",
           interface_type="lmp",
           device=_cbts_2.dus[0].airscale.common_units[0]
        ),
    ]
)
tl = TestLine(
    test_pc=_test_pc_1,
    test_pcs=[_test_pc_1, _test_pc_2],
    gnbs=[_cbts_1, _cbts_2],
    tl_cloud_topology="CLOUD_5G_I_[MP][MP]_AP_[LOOO]",
    ues=[_ue],
    pdus=_pdus,
)

__all__ = ["tl"]
