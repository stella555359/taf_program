__maintainer__ = "Damian Piasecki"
__team__ = "MN RAN L2 SW 2 KRK CntDlv SG"
__email__ = "I_CD_ET_TESTERS <I_CD_ET_TESTERS@internal.nsn.com>"
__owner_email__ = "damian.piasecki@nokia.com"

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
        addr="7-7-UTE5GCLOUDT2SK116.p02.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_pdu = FPFH(
    port_numbers=[5],
    addr="fpfh-hc11-46-p02.p02-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    hardware_type="ASIL",
    capacity_units=[CapacityUnit(addr="192.168.253.36")],
    pdu_port=_pdu.pdu_ports[5],
)

_airscale = Airscale([_common_unit])

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

_du = DU(_airscale)

_cbts = ClassicalBts(cu=_cu, dus=[_du])

_ue = Airphone(
    egate=SshServiceDetails("", ""),
    l2_ssh_connection_details=SshServiceDetails("", ""),
    l3_ssh_connection_details=SshServiceDetails("", ""),
    l1=Airscale(
        [
            CommonUnit(
                lmp_connection=SshServiceDetails(
                    addr="192.168.200.1", username="toor4nsn", password="oZPS0POrRieRtu"
                ),
                hardware_type="ASIL",
                capacity_units=[CapacityUnit(addr="192.168.253.84")],
                pdu_port=_pdu.pdu_ports[5],
            )
        ]
    ),
)


tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_AP",
    pdus=[_pdu],
    ues=[_ue],
)

__all__ = ["tl"]
