__maintainer__ = "Mateusz Lesniak"
__team__ = "MN RAN L2 SW 2 KRK CntDlv SG"
__email__ = "I_6064_KRK_TEAM_GMS <I_6064_KRK_TEAM@internal.nsn.com>"
__owner_email__ = "mateusz.lesniak@nokia.com"

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
        addr="7-7-UTE5GCLOUDT168.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_cu = CU(
    backhaul_site_oam_ip="10.0.1.2",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.1", vlan_id=4093),
    x2u=NetworkAddress(v4="10.0.1.2", vlan_id=1506),
    s1u=NetworkAddress(v4="10.0.1.2", vlan_id=1506),
    ngu=NetworkAddress(v4="10.0.1.2", vlan_id=1506),
)

_pdu2 = FPFH(port_numbers=[6], addr="10.253.166.7", login="admin", password="admin")
_pdu1 = FPFH(port_numbers=[5], addr="10.253.166.7", login="admin", password="admin")

_abil1_du1 = CapacityUnit(addr="192.168.253.36")

_asik_du1 = CommonUnit(
    pdu_port=_pdu1.pdu_ports[5],
    lmp_connection=SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil1_du1],
)

_du1 = DU(airscale=Airscale(common_units=[_asik_du1]))

_cbts = ClassicalBts(cu=_cu, dus=[_du1])

_ue = Airphone(
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    Airscale(
        [
            CommonUnit(
                pdu_port=_pdu2.pdu_ports[6],
                lmp_connection=SshServiceDetails(
                    addr="192.168.200.1", username="toor4nsn", password="oZPS0POrRieRtu"
                ),
                capacity_units=[CapacityUnit(addr="192.168.253.84")],
            )
        ]
    ),
)


tl = TestLine(
    test_pc=_test_pc, gnbs=[_cbts], tl_cloud_topology="CLOUD_5G_CLASSICAL_AP", ues=[_ue]
)

__all__ = ["tl"]
