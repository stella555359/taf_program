__maintainer__ = "Kamil Pokusa"
__team__ = "MN RAN L2 SW 2 KRK CntDlv SG"
__email__ = "I_CD_ET_TESTERS_GMS <I_CD_ET_TESTERS@internal.nsn.com>"
__owner_email__ = "kamil.pokusa@nokia.com"

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

_pdu = FPFH(
    port_numbers=[3, 4],
    addr="fpfh-hc07-48-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    hardware_type="ASIB",
    capacity_units=[
        CapacityUnit(addr="192.168.253.36", hardware_type="ABIO"),
        CapacityUnit(addr="192.168.253.40", hardware_type="ABIO"),
    ],
    pdu_port=_pdu.pdu_ports[4],
)

_airscale = Airscale([_common_unit])

_cu = CU(
    backhaul_site_oam_ip="10.0.1.2",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.1",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.1",
        username="Nemuadmin",
        password="nemuuser",
    ),
    x2c=NetworkAddress(v4="10.0.1.1", vlan_id=1532),
    x2u=NetworkAddress(v4="10.0.1.1", vlan_id=1532),
    s1u=NetworkAddress(v4="10.0.1.1", vlan_id=1532),
)

_du = DU(_airscale)

_cbts = ClassicalBts(cu=_cu, dus=[_du])

_ue = Airphone(
    egate=SshServiceDetails("", ""),
    l2_ssh_connection_details=SshServiceDetails("", ""),
    l3_ssh_connection_details=SshServiceDetails("", ""),
    l1=Airscale(
        common_units=[
            CommonUnit(
                lmp_connection=SshServiceDetails(
                    "192.168.200.1", "toor4nsn", password="oZPS0POrRieRtu"
                ),
                hardware_type="ASIL",
                capacity_units=[
                    CapacityUnit(addr="192.168.253.84", hardware_type="ABIO"),
                    CapacityUnit(addr="192.168.253.85", hardware_type="ABIO"),
                ],
                pdu_port=_pdu.pdu_ports[3],
            )
        ]
    ),
)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT8SK032.p08.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    ),
    connections=[_cbts.dus[0].airscale.common_units[0], _ue],
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_I_BOO_AP_LOO",
    pdus=[_pdu],
    ues=[_ue],
)

__all__ = ["tl"]
