__maintainer__ = "Anna Anzel"
__team__ = "MN_RAN_L2_SW_2_KRK_SG04"
__email__ = (
    "I_MN_RAN_L2_SW_2_KRK_SG04_ET_GMS <I_MN_RAN_L2_SW_2_KRK_SG04_ET@internal.nsn.com>"
)
__owner_email__ = "anna.anzel@nokia.com"

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
    xnc=NetworkAddress(v4="10.0.1.2", vlan_id=1635),
    xnu=NetworkAddress(v4="10.0.1.2", vlan_id=1635),
    ngc=NetworkAddress(v4="10.0.1.2", vlan_id=1635),
    ngu=NetworkAddress(v4="10.0.1.2", vlan_id=1635),
    x2u=NetworkAddress(v4="10.0.1.2", vlan_id=1635),
    x2c=NetworkAddress(v4="10.0.1.2", vlan_id=1635),
    s1u=NetworkAddress(v4="10.0.1.2", vlan_id=1635),
)

_pdu = FPFH(
    port_numbers=[3, 4],
    addr="fpfh-hb02-34-p02.p02-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_pdus = [_pdu]

_abio1_du1 = CapacityUnit(addr="192.168.253.36", hardware_type="ABIO")

_asil_du1 = CommonUnit(
    pdu_port=_pdu.pdu_ports[4],
    lmp_connection=SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    hardware_type="ASIL",
    capacity_units=[_abio1_du1],
)

_du1 = DU(airscale=Airscale(common_units=[_asil_du1]))

_cbts = ClassicalBts(cu=_cu, dus=[_du1])

_ue = Airphone(
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    Airscale(
        [
            CommonUnit(
                pdu_port=_pdu.pdu_ports[3],
                lmp_connection=SshServiceDetails(
                    addr="192.168.200.1", username="toor4nsn", password="oZPS0POrRieRtu"
                ),
                hardware_type="ASIL",
                capacity_units=[
                    CapacityUnit(addr="192.168.253.84", hardware_type="ABIO")
                ],
            )
        ]
    ),
)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT2SK135.p02.ska-lab.nsn-rdnet.net",
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
    tl_cloud_topology="CLOUD_5G_I_LO_AP_LO_SANSA_FS_ECPRI_CMWV_TDD",
    ues=[_ue],
    pdus=_pdus,
)

__all__ = ["tl"]
