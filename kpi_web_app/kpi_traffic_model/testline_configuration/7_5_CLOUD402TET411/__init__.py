__maintainer__ = "Zhang xiaping"
__team__ = (
    "I_MN_5GSC_SW_ENG_1_CN_06_SG_GMS <I_MN_5GSC_SW_ENG_1_CN_06_SG@internal.nsn.com>"
)
__email__ = "xiaping.zhang@nokia-sbell.com"
__owner_email__ = "xiaping.zhang@nokia-sbell.com"

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
from taf.config.testline.pdu import FACOM

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.205.19", username="ute", password="ute"
    )
)

_pdu1 = FACOM(addr="10.57.247.220", port_numbers=[3, 4], model="FACOM", version=None)

_capacity_unit = CapacityUnit(addr="192.168.253.22")

_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
    pdu_port=_pdu1.pdu_ports[3],
)

_airscale = Airscale(common_units=[_common_unit])

_cu = CU(
    backhaul_site_oam_ip="192.168.255.129",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu", port=443
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.1", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.1.1.1", vlan_id=902),
)

_du = DU(airscale=_airscale)

_cbts = ClassicalBts(cu=_cu, dus=[_du])

_airphone = Airphone(
    egate=SshServiceDetails("", ""),
    l3_ssh_connection_details=SshServiceDetails("", ""),
    l2_ssh_connection_details=SshServiceDetails("", ""),
    l1=Airscale(
        common_units=[
            CommonUnit(
                lmp_connection=SshServiceDetails(
                    addr="192.168.200.1", username="toor4nsn", password="oZPS0POrRieRtu"
                ),
                capacity_units=[CapacityUnit(addr="192.168.253.22")],
                pdu_port=_pdu1.pdu_ports[4],
            )
        ]
    ),
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_AP",
    ues=[_airphone],
    pdus=[_pdu1],
)

_dcap_server = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.209.251", username="dcapuser", password="dcapuser123"
    )
)
dcap_server = _dcap_server

__all__ = ["tl"]
