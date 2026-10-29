__maintainer__ = "Bhakti Patel"
__team__ = "MN_RAN_BLR_VRF_T12"
__email__ = "bhakti.ka_patel@nokia.com"
__Owner_email__ = "bhargav.chemuturi@nokia.com"

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
from taf.config.testline.connection_details import (
    SshServiceDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.connection_details import (
    SshServiceDetails,
    TelnetConnectionDetails,
    HttpConnectionDetails,
)

_test_pc_master = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.53.164.17", username="ute", password="ute"
    ),
    connections=[NetworkAddress(v4="192.168.255.129")],
)

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))
_du_pdu = RRB("10.41.155.182", [3])
_ru1_pdu = RRB("10.41.155.183", [6])
_ru2_pdu = RRB("10.41.155.183", [1])
_ru3_pdu = RRB("10.41.155.167", [3])
_ru4_pdu = RRB("10.41.155.183", [7])
_ru5_pdu = RRB("10.41.155.183", [3])
_du_pdu.pdu_ports[3].contactor = "NORMALLY_OPENED"
_ru1_pdu.pdu_ports[6].contactor = "NORMALLY_OPENED"
_ru2_pdu.pdu_ports[1].contactor = "NORMALLY_OPENED"
_ru3_pdu.pdu_ports[3].contactor = "NORMALLY_OPENED"
_ru4_pdu.pdu_ports[7].contactor = "NORMALLY_OPENED"
_ru5_pdu.pdu_ports[3].contactor = "NORMALLY_OPENED"
_pdus = [_du_pdu, _ru1_pdu, _ru2_pdu, _ru3_pdu, _ru4_pdu, _ru5_pdu]


_rmod_1 = RU(
    ru_hw_group="cMAAr6.2_32T32R",
    radio_type=RadioTypes.AQQJ,
    serial_number="NQ233890018",
    pdu_port=_ru1_pdu.pdu_ports[6],
)
_rmod_2 = RU(
    ru_hw_group="cMAAr6.2_32T32R",
    radio_type=RadioTypes.AQQJ,
    serial_number="NQ233691236",
    pdu_port=_ru2_pdu.pdu_ports[1],
)
_rmod_3 = RU(
    ru_hw_group="cMAAr6.2_32T32R",
    radio_type=RadioTypes.AVQA,
    serial_number="L1251304484",
    pdu_port=_ru3_pdu.pdu_ports[3],
)
_rmod_4 = RU(
    ru_hw_group="FRMr5.1_1_2T4R",
    radio_type=RadioTypes.AHPB,
    serial_number="DH242419222",
    pdu_port=_ru4_pdu.pdu_ports[7],
)
_rmod_5 = RU(
    ru_hw_group="FRMr5.1_1_2T4R",
    radio_type=RadioTypes.AHPJ,
    serial_number="K9232924276",
    pdu_port=_ru5_pdu.pdu_ports[3],
)

_common_unit = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_du_pdu.pdu_ports[3],
    hardware_type="ASOE",
    capacity_units=[],
    serial_number="DH242504643",
    rus=[_rmod_1, _rmod_2, _rmod_3, _rmod_4, _rmod_5],
)
_airscale = Airscale([_common_unit])
_cu = CU(
    backhaul_site_oam_ip="10.53.203.120",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
)
_du = DU(_airscale)
_cbts = ClassicalBts(cu=_cu, dus=[_du])

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.53.164.17", username="ute", password="ute"
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
    tl_cloud_topology="CLOUD_5G_ASOE_2AQQJ_AVQA_AHPB_AHPJ",
    # ues=[_ue],
    pdus=_pdus,
)
__all__ = ["tl"]
