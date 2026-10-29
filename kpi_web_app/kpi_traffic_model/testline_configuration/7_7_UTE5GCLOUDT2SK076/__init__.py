__maintainer__ = "MN RAN L2 SW 2 KRK Vrf SG"
__team__ = "I_5GSC_SW_ENG_KRK_VRF_GMS"
__email__ = "I_5GSC_SW_ENG_KRK_VRF_GMS <I_5GSC_SW_ENG_KRK_VRF@internal.nsn.com>"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import NetworkAddress, Connection
from taf.config.testline.pdu import FPFH
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Airphone

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_cu = CU(
    backhaul_site_oam_ip="192.168.255.129",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.0.1.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.1", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.2", vlan_id=1576),
    x2u=NetworkAddress(v4="10.0.1.2", vlan_id=1576),
    s1u=NetworkAddress(v4="10.0.1.2", vlan_id=1576),
)

_pdu1 = FPFH(
    port_numbers=[1],
    addr="fpfh-hc02-34-p02.p02-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)
_pdu2 = FPFH(
    port_numbers=[1],
    addr="fpfh-hc02-46-p02.p02-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_abio1_du1 = CapacityUnit(addr="192.168.253.36", hardware_type="ABIO")

_common_unit = CommonUnit(
    pdu_port=_pdu1.pdu_ports[1],
    lmp_connection=SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    hardware_type="ASOE",
)

_du1 = DU(airscale=Airscale(common_units=[_common_unit]))

_cbts = ClassicalBts(cu=_cu, dus=[_du1])

_ue = Airphone(
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    Airscale(
        [
            CommonUnit(
                pdu_port=_pdu2.pdu_ports[1],
                lmp_connection=SshServiceDetails(
                    addr="192.168.200.1", username="toor4nsn", password="oZPS0POrRieRtu"
                ),
                hardware_type="ASIL",
                capacity_units=[
                    CapacityUnit(addr="192.168.253.84", hardware_type="ABIO"),
                    CapacityUnit(addr="192.168.253.88", hardware_type="ABIO"),
                ],
            )
        ]
    ),
)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT2SK076.p02.ska-lab.nsn-rdnet.net",
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
    test_pc=_test_pc, gnbs=[_cbts], tl_cloud_topology="CLOUD_5G_CLASSICAL_AP", ues=[_ue]
)

__all__ = ["tl"]
