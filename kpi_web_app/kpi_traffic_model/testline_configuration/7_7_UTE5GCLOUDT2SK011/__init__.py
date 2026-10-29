__maintainer__ = "Anna Anzel"
__team__ = "I_5G_SW_MMW_PLKRK_04"
__email__ = "I_5G_SW_MMW_PLKRK_04 <I_5G_SW_MMW_PLKRK_04@nokia.com>"
__owner_email__ = "anna.anzel@nokia.com"

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
    backhaul_site_oam_ip="10.0.1.1",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    xnc=NetworkAddress(v4="10.0.1.1", vlan_id=1511),
    xnu=NetworkAddress(v4="10.0.1.1", vlan_id=1511),
    ngc=NetworkAddress(v4="10.0.1.1", vlan_id=1511),
    ngu=NetworkAddress(v4="10.0.1.1", vlan_id=1511),
    x2u=NetworkAddress(v4="10.0.1.1", vlan_id=1511),
    x2c=NetworkAddress(v4="10.0.1.1", vlan_id=1511),
    s1u=NetworkAddress(v4="10.0.1.1", vlan_id=1511),
)

_pdu1 = FPFH(
    port_numbers=[1, 2],
    addr="fpfh-hb01-46-p02.p02-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_pdus = [_pdu1]

_abil1_du1 = CapacityUnit(addr="192.168.253.84")

_asik_du1 = CommonUnit(
    pdu_port=_pdu1.pdu_ports[2],
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
                pdu_port=_pdu1.pdu_ports[1],
                lmp_connection=SshServiceDetails(
                    addr="192.168.200.1", username="toor4nsn", password="oZPS0POrRieRtu"
                ),
                capacity_units=[CapacityUnit(addr="192.168.253.20")],
            )
        ]
    ),
)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT2SK011.p02.ska-lab.nsn-rdnet.net",
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
    tl_cloud_topology="CLOUD_5G_O_E_AP_KL_SANSA_L1B_ECPRI_CMWV_TDD",
    ues=[_ue],
    pdus=_pdus,
)

__all__ = ["tl"]
