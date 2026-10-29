###############################
#    TL068 Classical AP NPS   #
###############################
__maintainer__ = "Leandre Hueber"
__team__ = "MN_5G_SC_NPS_ET"
__email__ = "leandre.hueber@nokia.com"

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
from taf.config.testline.pdu import ATEN

# PDU  port4= GNB  port3= Airphone
_pdu = ATEN(addr="10.5.113.94", port_numbers=[1, 2])

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

##ASIK
_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[
        CapacityUnit(addr="192.168.253.20", hardware_type="ABIO"),
        CapacityUnit(addr="192.168.253.24", hardware_type="ABIO"),
    ],
    pdu_port=_pdu.pdu_ports[2],
    hardware_type="ASIB",
)

_airscale = Airscale(common_units=[_common_unit])

##GNB
_cu = CU(
    backhaul_site_oam_ip="192.168.255.129",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.1", vlan_id=3068),
    x2u=NetworkAddress(v4="10.0.1.1", vlan_id=3068),
    s1u=NetworkAddress(v4="10.0.1.1", vlan_id=3068),
)

_du = DU(_airscale)

_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=720000681)

##AirPhone
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
                ],
                pdu_port=_pdu.pdu_ports[1],
                hardware_type="ASIL",
            )
        ]
    ),
)

# TestPC
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.0.108.8", username="ute", password="ute"
    ),
    connections=[_cbts.dus[0].airscale.common_units[0], _ue],
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_I_BOO_AP_LOO",
    ues=[_ue],
    pdus=[_pdu],
)

__all__ = ["tl"]
