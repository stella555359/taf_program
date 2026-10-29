__maintainer__ = "Sreekumar"
__team__ = "I_MN_RAN_RD_VRF_BLR1_T08_GMS"
__email__ = "sreekumar.narimuri_kumaran@nokia.com"
__owner_email__ = "sreekumar.narimuri_kumaran@nokia.com"

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
        addr="10.58.238.126", username="ute", password="ute"
    ),
    connections=[NetworkAddress(v4="192.168.255.129")],
)


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))
_du_pdu = RRB("10.58.242.47", [3])
_ru1_pdu = RRB("10.58.242.49", [8])
_du_pdu.pdu_ports[3].contactor = "NORMALLY_OPENED"
_ru1_pdu.pdu_ports[8].contactor = "NORMALLY_OPENED"

_pdus = [_du_pdu,_ru1_pdu]

_ru_1 = RU(
    pdu_port=_ru1_pdu.pdu_ports[8],
    radio_type="OFEGSA",
    ru_hw_group="ThirdParty",
    serial_number="00029",
)

fujitsu_ru = FujitsuRU(
    radio_type=FujitsuRadioTypes.OFEGSA,
    hw_version="0100",
    serial_number="00029",
    product_code="FJRU-N75N3N1-G",
    #netconf_ssh_configuration=SshServiceDetails(addr="172.22.0.2",username="fjncuser0", password="ncCl2fjRu+autH0"),
    netconf_ssh_configuration=SshServiceDetails(addr="172.22.0.2",username="oranuser", password="o-ran-password"),
    pdu_port=_ru1_pdu.pdu_ports[8],
)

assert isinstance(fujitsu_ru, RU)
assert fujitsu_ru.ru_hw_group == "ThirdParty"  # automatically added

_capacity_unit = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIO",
	hardware_version="103",
	product_code="475266A.103",
    serial_number="DH214840647",
    pdu_port=_du_pdu.pdu_ports[3],

)
_common_unit = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
    pdu_port=_du_pdu.pdu_ports[3],
    hardware_type="ASIM",
	serial_number="L1233404787",
    #rus=[_ru_1],
    rus=[fujitsu_ru],
)
_airscale = Airscale([_common_unit])
_cu = CU(
    backhaul_site_oam_ip="10.58.239.63",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.58.239.63", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.58.239.63", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.1", vlan_id=203),
    x2u=NetworkAddress(v4="10.0.1.2", vlan_id=203),
    s1u=NetworkAddress(v4="10.0.1.2", vlan_id=203),
)
_du = DU(_airscale)
_cbts = ClassicalBts(cu=_cu, dus=[_du])

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.58.238.126", username="ute", password="ute"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_cbts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        ),
       # _ue,
    ],
)
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_ORAN_CLASSICAL_SA_1ASIM_1ABIO_1OFEGSA",
    #ues=[_ue],
    pdus=_pdus,
)
__all__ = ["tl"]
