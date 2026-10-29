__maintainer__ = "Bhanu Vamsi Krishna Gundlur"
__team__ = "I_5G_AIRPHONE_PZ_CIT_CRT_TEAM_GMS"
__email__ = "I_5G_AIRPHONE_PZ_CIT_CRT_TEAM@internal.nsn.com"
__owner_email__ = "I_5G_AIRPHONE_PZ_CIT_CRT_TEAM@internal.nsn.com"


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
from taf.config.testline.pdu import DELTA


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


_snmp_user = {
    "userName": "user",
    "authKey": "App1@pdu123",
    "privKey": "App1@privacy456",
    "authProtocol": "MD5",
    "privProtocol": "DES",
}


_pdu = DELTA(
    addr="10.62.93.172",
    port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
    snmp_user=_snmp_user,
    version="40288-1",
)
_pdus = [_pdu]

_capacity_unit = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIP",
)

_common_unit = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
    pdu_port=_pdus[0].pdu_ports[4],
    hardware_type="ASIM",
)

_airscale = Airscale([_common_unit])

_cu = CU(
    backhaul_site_oam_ip="192.168.255.129",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.2", vlan_id=303),
    x2u=NetworkAddress(v4="10.0.1.2", vlan_id=303),
    s1u=NetworkAddress(v4="10.0.1.2", vlan_id=303),
)

_du = DU(_airscale)

_cbts = ClassicalBts(cu=_cu, dus=[_du])


_ue = Airphone(
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    Airscale(
        [
            CommonUnit(
                SshServiceDetails(
                    "192.168.200.1", "toor4nsn", password="oZPS0POrRieRtu"
                ),
                capacity_units=[
                    CapacityUnit(addr="192.168.253.84", hardware_type="ABIO"),
                    CapacityUnit(addr="192.168.253.85", hardware_type="ABIO"),
                    CapacityUnit(addr="192.168.253.86", hardware_type="ABIO"),
                ],
                pdu_port=_pdus[0].pdu_ports[5],
                hardware_type="ASIL",
            )
        ]
    ),
)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.63.67.40", username="ute", password="ute"
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
    tl_cloud_topology="CLOUD_5G_I_MP_AP_LOOO_SANSA_FS_ECPRI_CMWV_TDD",
    ues=[_ue],
    pdus=_pdus,
)

__all__ = ["tl"]
