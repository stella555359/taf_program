__maintainer__ = "Vijay"
__team__ = "I_CNP_AP_ABIL_ABIO_GMS"
__email__ = "I_CNP_AP_ABIL_ABIO@internal.nsn.com"
__owner_email__ = "vijay.sansuddi@nokia.com"


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
from taf.config.testline.pdu import RRB


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


_pdu = RRB(addr="10.63.69.176", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_pdus = [_pdu]

_capacity_unit = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIO",
)

_common_unit = CommonUnit(
    SshServiceDetails(
        addr="192.168.254.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
    pdu_port=_pdus[0].pdu_ports[1],
    hardware_type="ASIL",
)

_common_unit2 = CommonUnit(
    SshServiceDetails(
        addr="192.168.254.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
    pdu_port=_pdus[0].pdu_ports[7],
    hardware_type="ASIL",
)
_airscale = Airscale([_common_unit])
_airscale2 = Airscale([_common_unit2])

_cu = CU(
    backhaul_site_oam_ip="192.168.254.1",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.254.1", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.1", vlan_id=403),
    x2u=NetworkAddress(v4="10.0.1.2", vlan_id=403),
    s1u=NetworkAddress(v4="10.0.1.2", vlan_id=403),
)

_cu_2 = CU(
    backhaul_site_oam_ip="10.0.1.3",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.254.2", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.1", vlan_id=403),
    x2u=NetworkAddress(v4="10.0.1.1", vlan_id=403),
    s1u=NetworkAddress(v4="10.0.1.1", vlan_id=403),
    ngu=NetworkAddress(v4="10.0.1.1", vlan_id=403),
)

_du = DU(_airscale)
_du2 = DU(_airscale2)

_cbts = ClassicalBts(cu=_cu, dus=[_du])
_cbts2 = ClassicalBts(cu=_cu_2, dus=[_du2])

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
                [
                    CapacityUnit(
                        addr="192.168.253.22",
                        hardware_type="ABIO",
                    ),
                ],
                pdu_port=_pdus[0].pdu_ports[2],
                hardware_type="ASIL",
            )
        ]
    ),
)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.63.69.115", username="ute", password="Ut3pa5s#4da1115"
    ),
    connections=[Connection(interface="eth1", device=_cbts.dus[0].airscale.common_units[0], interface_type="lmp"), Connection(interface="eth1", device=_cbts2.dus[0].airscale.common_units[0], interface_type="lmp"), _ue],
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts, _cbts2],
    tl_cloud_topology="CLOUD_5G_I_LO_AP_LO_SANSA_FS_ECPRI_CMWV_TDD",
    ues=[_ue],
    pdus=_pdus,
)

__all__ = ["tl"]