__maintainer__ = 'Katarzyna Wisniewska'
__team__ = 'MN RAN RD VRF WRO2 5'
__email__ = 'I_MN_RAN_RD_VRF_WRO2_5@nokia.com'
__owner_email__ = 'katarzyna.wisniewska@nokia.com'


import os
from taf.config.testline.testline import TestLine
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline import Airphone
from taf.config.testline.pdu import ATEN, Gude
from taf.config.testline import Connection

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# PDU  port_1 = GNB_5,  port_2 = GNB_6,   port_3 = GNB_3,  port_4 = GNB_4,  port_5 = GNB_1,  port_6 = GNB_2,   port_7 = Airphone
_pdu = Gude(
    addr="10.44.206.156",
    port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    model="EPC",
    version="8220-1",
)

_cu1 = CU(
    backhaul_site_oam_ip="10.0.1.2",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.2", vlan_id=1303),
    x2u=NetworkAddress(v4="10.0.1.2", vlan_id=1303),
    s1u=NetworkAddress(v4="10.0.1.2", vlan_id=1303),
    ngu=NetworkAddress(v4="10.0.1.2", vlan_id=1303),
)

_abio_du1 = CapacityUnit(addr="192.168.253.20", hardware_type="ABIO")

_asil_du1 = CommonUnit(
    pdu_port=_pdu.pdu_ports[5],
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    hardware_type="ASIL",
    capacity_units=[_abio_du1],
)

_du1 = DU(airscale=Airscale(common_units=[_asil_du1]))

_gnb1 = ClassicalBts(cu=_cu1, dus=[_du1], instance_id=716000071)

_cu2 = CU(
    backhaul_site_oam_ip="10.0.1.3",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.3", vlan_id=1303),
    x2u=NetworkAddress(v4="10.0.1.3", vlan_id=1303),
    s1u=NetworkAddress(v4="10.0.1.3", vlan_id=1303),
    ngu=NetworkAddress(v4="10.0.1.3", vlan_id=1303),
)

_abio_du2 = CapacityUnit(addr="192.168.253.20", hardware_type="ABIO")

_asil_du2 = CommonUnit(
    pdu_port=_pdu.pdu_ports[6],
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    hardware_type="ASIL",
    capacity_units=[_abio_du2],
)

_du2 = DU(airscale=Airscale(common_units=[_asil_du2]))

_gnb2 = ClassicalBts(cu=_cu2, dus=[_du2], instance_id=716000072)

_cu3 = CU(
    backhaul_site_oam_ip="10.0.1.4",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.4", vlan_id=1303),
    x2u=NetworkAddress(v4="10.0.1.4", vlan_id=1303),
    s1u=NetworkAddress(v4="10.0.1.4", vlan_id=1303),
    ngu=NetworkAddress(v4="10.0.1.4", vlan_id=1303),
)

_abio_du3 = CapacityUnit(addr="192.168.253.20", hardware_type="ABIO")

_asil_du3 = CommonUnit(
    pdu_port=_pdu.pdu_ports[3],
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    hardware_type="ASIL",
    capacity_units=[_abio_du3],
)

_du3 = DU(airscale=Airscale(common_units=[_asil_du3]))

_gnb3 = ClassicalBts(cu=_cu3, dus=[_du3], instance_id=716000073)

_cu4 = CU(
    backhaul_site_oam_ip="10.0.1.5",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.5", vlan_id=1303),
    x2u=NetworkAddress(v4="10.0.1.5", vlan_id=1303),
    s1u=NetworkAddress(v4="10.0.1.5", vlan_id=1303),
    ngu=NetworkAddress(v4="10.0.1.5", vlan_id=1303),
)

_abio_du4 = CapacityUnit(addr="192.168.253.20", hardware_type="ABIO")

_asil_du4 = CommonUnit(
    pdu_port=_pdu.pdu_ports[4],
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    hardware_type="ASIL",
    capacity_units=[_abio_du4],
)

_du4 = DU(airscale=Airscale(common_units=[_asil_du4]))

_gnb4 = ClassicalBts(cu=_cu4, dus=[_du4], instance_id=716000074)

_cu5 = CU(
    backhaul_site_oam_ip="10.0.1.6",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.6", vlan_id=1303),
    x2u=NetworkAddress(v4="10.0.1.6", vlan_id=1303),
    s1u=NetworkAddress(v4="10.0.1.6", vlan_id=1303),
    ngu=NetworkAddress(v4="10.0.1.6", vlan_id=1303),
)

_abio_du5 = CapacityUnit(addr="192.168.253.20", hardware_type="ABIO")

_asil_du5 = CommonUnit(
    pdu_port=_pdu.pdu_ports[1],
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    hardware_type="ASIL",
    capacity_units=[_abio_du5],
)

_du5 = DU(airscale=Airscale(common_units=[_asil_du5]))

_gnb5 = ClassicalBts(cu=_cu5, dus=[_du5], instance_id=716000075)

_cu6 = CU(
    backhaul_site_oam_ip="10.0.1.7",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.7", vlan_id=1303),
    x2u=NetworkAddress(v4="10.0.1.7", vlan_id=1303),
    s1u=NetworkAddress(v4="10.0.1.7", vlan_id=1303),
    ngu=NetworkAddress(v4="10.0.1.7", vlan_id=1303),
)

_abio_du6 = CapacityUnit(addr="192.168.253.20", hardware_type="ABIO")

_asil_du6 = CommonUnit(
    pdu_port=_pdu.pdu_ports[2],
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    hardware_type="ASIL",
    capacity_units=[_abio_du6],
)

_du6 = DU(airscale=Airscale(common_units=[_asil_du6]))

_gnb6 = ClassicalBts(cu=_cu6, dus=[_du6], instance_id=716000076)

_ue = Airphone(
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    Airscale(
        [
            CommonUnit(
                pdu_port=_pdu.pdu_ports[7],
                lmp_connection=SshServiceDetails(
                    addr="192.168.200.1", username="toor4nsn", password="oZPS0POrRieRtu"
                ),
                hardware_type="ASIL",
                capacity_units=[
                    CapacityUnit(addr="192.168.253.84", hardware_type="ABIO"),
                    CapacityUnit(addr="192.168.253.85", hardware_type="ABIO"),
                    CapacityUnit(addr="192.168.253.86", hardware_type="ABIO")
                ],
            )
        ]
    ),
)


_test_pc1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.42.231.87",
        username="ute",
        password="UTE.debian12",
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_gnb1.dus[0].airscale.common_units[0],
            interface_type="lmp",
        ),
        _ue,
    ],
)

_test_pc2 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.42.231.88",
        username="ute",
        password="UTE.debian12",
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_gnb2.dus[0].airscale.common_units[0],
            interface_type="lmp",
        ),
    ],
)

_test_pc3 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.42.231.89",
        username="ute",
        password="UTE.debian12",
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_gnb3.dus[0].airscale.common_units[0],
            interface_type="lmp",
        ),
    ],
)

_test_pc4 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.42.231.90",
        username="ute",
        password="UTE.debian12",
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_gnb4.dus[0].airscale.common_units[0],
            interface_type="lmp",
        ),
    ],
)

_test_pc5 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.42.231.91",
        username="ute",
        password="UTE.debian12",
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_gnb5.dus[0].airscale.common_units[0],
            interface_type="lmp",
        ),
    ],
)

_test_pc6 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.42.231.92",
        username="ute",
        password="UTE.debian12",
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_gnb6.dus[0].airscale.common_units[0],
            interface_type="lmp",
        ),
    ],
)

tl = TestLine(
    test_pc=_test_pc1,
    test_pcs=[_test_pc1, _test_pc2, _test_pc4, _test_pc4, _test_pc5, _test_pc6],
    gnbs=[_gnb1, _gnb2, _gnb3, _gnb4, _gnb5, _gnb6],
    tl_cloud_topology="CLOUD_5G_I_[LO][LO][LO][LO][LO][LO]_AP_[LOOO]",
    ues=[_ue],
    pdus=[_pdu],
)

__all__ = ["tl"]
