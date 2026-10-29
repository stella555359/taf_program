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
        addr="10.58.238.125", username="ute", password="ute"
    ),
    connections=[NetworkAddress(v4="192.168.255.129")],
)

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))
_du_pdu = RRB("10.58.242.47", [7])
_ru1_pdu = RRB("10.58.242.49", [8])
_ru2_pdu = RRB("10.58.242.49", [4])
_ru3_pdu = RRB("10.58.242.77", [8])
_du_pdu.pdu_ports[7].contactor = "NORMALLY_OPENED"
_ru1_pdu.pdu_ports[8].contactor = "NORMALLY_OPENED"
_ru2_pdu.pdu_ports[4].contactor = "NORMALLY_OPENED"
_ru3_pdu.pdu_ports[8].contactor = "NORMALLY_OPENED"
_pdus = [_du_pdu, _ru1_pdu, _ru2_pdu, _ru3_pdu]

##ahhb radio 
_ru_2 = RU(
    radio_type=RadioTypes.AHHB,
    ru_hw_group="FRMr5.1_1_4T4R",
    serial_number="LR250211566",
    product_code="474252A.102",
    pdu_port=_ru2_pdu.pdu_ports[4], 
)

##ahpmdg radio 
_ru_3 = RU(
    radio_type=RadioTypes.AHPMDG,
    ru_hw_group="FRMr6.2_4T4R",
    serial_number="K9250314839",
    product_code="476122A.101",  
    pdu_port=_ru3_pdu.pdu_ports[8],    
)

##fujitsu ofegsa ru
_ru_1 = FujitsuRU(
    radio_type=FujitsuRadioTypes.OFEGSA,
    hw_version="0100",
#    ru_hw_group="ThirdParty",
    serial_number="00445",
    product_code="TA08029-B312/01",
#    netconf_ssh_configuration=SshServiceDetails(addr="172.22.0.2",username="fjncuser0", password="ncCl2fjRu+autH0")
    pdu_port=_ru1_pdu.pdu_ports[8],
)

_common_unit = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_du_pdu.pdu_ports[7],
    hardware_type="ASOG",
	serial_number="L1244502210",
    rus=[_ru_1, _ru_2, _ru_3],
)
_airscale = Airscale([_common_unit])
_cu = CU(
    backhaul_site_oam_ip="10.58.239.191",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.58.239.191", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.58.239.191", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.1", vlan_id=1101),
    x2u=NetworkAddress(v4="10.0.1.2", vlan_id=1101),
    s1u=NetworkAddress(v4="10.0.1.2", vlan_id=1101),
)
_du = DU(_airscale)
_cbts = ClassicalBts(cu=_cu, dus=[_du])

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.58.238.125", username="ute", password="ute"
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
    tl_cloud_topology="CLOUD_5G_ORAN_CLASSICAL_ASOG_OFEGSA_AHHB_AHPMDG",
    #ues=[_ue],
    pdus=_pdus,
)
__all__ = ["tl"]
