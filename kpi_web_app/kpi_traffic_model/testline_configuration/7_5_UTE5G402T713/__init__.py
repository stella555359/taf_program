__maintainer__ = "Michal Kowalski"
__team__ = "MN RAN L2 SW 1 KRK Vrf"
__email__ = "I_KRK_UTE_CLOUD_ADMINS@internal.nsn.com"
__owner_email__ = "michal.1.kowalski@nokia.com"


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
from taf.config.testline.pdu import FPFH, HBTE, TopYoung
from taf.config.testline.attenuator import (
    AttenuationPort,
)  # added in taf.meta 5.4


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# _pdu = FPFH(port_numbers=[3, 4], addr="10.255.17.8", login="admin", password="admin")
_ap_pdu = TopYoung(addr="10.57.172.165", port_numbers=[1])
_gnb_pdu = TopYoung(addr="10.57.172.165", port_numbers=[3])

_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[
        CapacityUnit(addr="192.168.253.36", hardware_type="ABIO"),
    ],
    hardware_type="ASIL",
    pdu_port=_gnb_pdu.pdu_ports[3],
)

_airscale = Airscale([_common_unit])

_cu = CU(
    backhaul_site_oam_ip="192.168.255.129",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.1", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.1", vlan_id=1252),
    x2u=NetworkAddress(v4="10.0.1.1", vlan_id=1252),
    s1u=NetworkAddress(v4="10.0.1.1", vlan_id=1252),
)

_du = DU(_airscale, f1_m_ip_addr="10.57.224.204")

_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id="1", global_bts_id="1")


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
                ],
                pdu_port=_ap_pdu.pdu_ports[1],
            )
        ]
    ),
)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.91",
        username="ute",
        password="iW_K#8.ute%A10h0m0ra",
    ),
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    ues=[_ue],
    pdus=[_ap_pdu, _gnb_pdu],
)

__all__ = ["tl"]
