__maintainer__ = "Du Ning"
__team__ = "I_MN_5GSC_SW_ENG_1_CN_14_SG_GMS"
__email__ = "ning.du@nokia-sbell.com"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.core import LTEEmuCore
from taf.config.testline.core import EPCSim
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FACOM
from taf.config.testline import DU
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.testline import TestLine


_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.205.13", username="ute", password="ute"
    )
)

_lteemu = LTEEmuCore(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.147.167", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    dir_path="/home/ute/wts/",
    cfg_filename="basic_wts_step1.cfg",
    mme_ip="",
    edaemon_port="22222",
    egate_port="20000",
)

_epc_sim = EPCSim(
    mme_ip="3.3.3.3",
    mcc=262,
    mnc=3,
    tac=61,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.152.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    dir_path="/opt/iphy/latest/",
    cfg_filename="",
)

_lmp_connection = SshServiceDetails(
    addr="10.57.149.194", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_pdu = FACOM(addr="10.57.251.231", port_numbers=[3])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale)

_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.149.194", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.149.194", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts = ClassicalBts(dus=[_du], cu=_cu)

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIKA101_ABILA102_19A"

tl = TestLine(
    test_pc=_host,
    core=_lteemu,
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
)

CONTROLPC_HOST = "10.57.152.3"
CONTROLPC_USER = "tester"
CONTROLPC_PASSWD = "tester123"
APPserver_HOST = "10.57.205.26"
APPserver_USER = "ute"
APPserver_PASSWD = "ute"

__all__ = ["tl"]
