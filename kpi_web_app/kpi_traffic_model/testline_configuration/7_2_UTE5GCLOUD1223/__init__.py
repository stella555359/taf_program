__maintainer__ = "AMBATI SUNIL KUMAR"
__team__ = "I_MN_RAN_RD_VRF_BLR1_T08_GMS"
__email__ = "ambati.sunil_kumar@nokia.com"
__owner_email__ = "ambati.sunil_kumar@nokia.com"

import os

from typing import Optional, List, Union
from enum import Enum


from taf.config.testline.testline import TestLine
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline import Airphone
from taf.config.testline.pdu import Gude, RRB
from taf.config.testline import RU, RadioTypes, FujitsuRU, FujitsuRadioTypes
from taf.config.testline.testpc import Connection, TestPc
from taf.config.testline.connection_details import SshServiceDetails, TelnetConnectionDetails
from taf.config.testline.connection_details import (
    SshServiceDetails,
    TelnetConnectionDetails,
    HttpConnectionDetails,
)




_test_pc_master = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.41.209.152", username="ute", password="ute"
    ),
    connections=[NetworkAddress(v4="192.168.255.129")],
)


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))
_du_pdu = RRB("10.53.252.19", [2])
_ru1_pdu = RRB("10.53.252.17", [8])
_du_pdu.pdu_ports[2].contactor = "NORMALLY_OPENED"
_ru1_pdu.pdu_ports[8].contactor = "NORMALLY_OPENED"

_pdus = [_du_pdu,_ru1_pdu]

_ru_1 = RU(
    pdu_port=_ru1_pdu.pdu_ports[8],
    radio_type="OFEGSA",
    ru_hw_group="ThirdParty",
    serial_number="00456",
)

fujitsu_ru = FujitsuRU(
    radio_type=FujitsuRadioTypes.OFEGSA,
    hw_version="0100",
    serial_number="00456",
    product_code="TA08029-B312/01",
    pdu_port=_ru1_pdu.pdu_ports[8],
)

assert isinstance(fujitsu_ru, RU)
assert fujitsu_ru.ru_hw_group == "ThirdParty"  # automatically added

_capacity_unit = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIO",
	hardware_version="103",
	product_code="475266A.103",
    serial_number="DH214550607",
    pdu_port=_du_pdu.pdu_ports[2],

)
_common_unit = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
    pdu_port=_du_pdu.pdu_ports[2],
    hardware_type="ASIL",
	serial_number="L1220402706",
    rus=[fujitsu_ru],
)
_airscale = Airscale([_common_unit])
_cu = CU(
    backhaul_site_oam_ip="10.63.48.5",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.63.48.5", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.63.48.5", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.1", vlan_id=3101),
    x2u=NetworkAddress(v4="10.0.1.2", vlan_id=3101),
    s1u=NetworkAddress(v4="10.0.1.2", vlan_id=3101),
)
_du = DU(_airscale)
_cbts = ClassicalBts(cu=_cu, dus=[_du])

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.41.209.152", username="ute", password="ute"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_cbts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        ),
    ],
)
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_ORAN_CLASSICAL_SA_1ASIL_1ABIO_1OFEGSA",
    pdus=_pdus,
)
__all__ = ["tl"]
