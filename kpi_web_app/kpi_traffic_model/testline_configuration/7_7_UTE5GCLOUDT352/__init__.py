__maintainer__ = "Marek Piotrowski"
__team__ = "I_5G_SW_MMW_PLKRK_04"
__email__ = "I_5G_SW_MMW_PLKRK_04 <I_5G_SW_MMW_PLKRK_04@nokia.com>"
__owner_email__ = "marek.piotrowski@nokia.com"

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
        addr="7-7-UTE5GCLOUDT352.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_cu = CU(
    backhaul_site_oam_ip="10.0.1.1",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    xnc=NetworkAddress(v4="10.0.1.1", vlan_id=1852),
    xnu=NetworkAddress(v4="10.0.1.1", vlan_id=1852),
    ngc=NetworkAddress(v4="10.0.1.1", vlan_id=1852),
    ngu=NetworkAddress(v4="10.0.1.1", vlan_id=1852),
    x2u=NetworkAddress(v4="10.0.1.1", vlan_id=1852),
    x2c=NetworkAddress(v4="10.0.1.1", vlan_id=1852),
    s1u=NetworkAddress(v4="10.0.1.1", vlan_id=1852),
)

_pdu1 = FPFH(
    port_numbers=[4],
    addr="FPFH-GA18-1.sc5g-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)
_pdu2 = FPFH(
    port_numbers=[3],
    addr="FPFH-GA18-1.sc5g-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)
_pdus = [_pdu1, _pdu2]

_abil1_du1 = CapacityUnit(addr="192.168.253.20")

_asik_du1 = CommonUnit(
    pdu_port=_pdu1.pdu_ports[4],
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
                pdu_port=_pdu2.pdu_ports[3],
                lmp_connection=SshServiceDetails(
                    addr="192.168.200.1", username="toor4nsn", password="oZPS0POrRieRtu"
                ),
                capacity_units=[CapacityUnit(addr="192.168.253.84")],
            )
        ]
    ),
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_AP",
    ues=[_ue],
    pdus=_pdus,
)

__all__ = ["tl"]
