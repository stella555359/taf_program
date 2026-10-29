######################################
#  TestLine Classical HZ TL267
#  @Last Modify: 2020-01-06
######################################
__maintainer__ = "zhuoxu"
__team__ = "NSB MN ECE RD 2 CN 06 SG"
__email__ = "zhuoyan.xu@nokia-sbell.com"


import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.core import LTEEmuCore
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline import RU, DU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit

from taf.config.testline.legacy import SCF
from taf.config.testline.ue import *
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500

################    Common     ################
__all__ = ["tl"]
_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


#########    Testpc    ##########
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.209.186", username="ute", password="ute"
    )
)


################    DU1    ################
_gnb_1_airscale_cu_lmp = SshServiceDetails(
    addr="10.57.146.48", username="toor4nsn", password="oZPS0POrRieRtu"
)

_gnb_1_airscale_cu_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_1_pdu = FACOM(addr="10.57.247.196", port_numbers=[1])

_gnb_1_airscale_cu = CommonUnit(
    lmp_connection=_gnb_1_airscale_cu_lmp,
    capacity_units=[_gnb_1_airscale_cu_capacity_unit],
    pdu_port=_gnb_1_pdu.pdu_ports[1],
)

_gnb_1_airscale = Airscale(common_units=[_gnb_1_airscale_cu])

_du1 = DU(airscale=_gnb_1_airscale)


################      ClassicalBts1    ################
_cu1 = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.146.48", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.146.48", username="Nemuadmin", password="nemuuser"
    ),
)

_cloud_gnb1 = ClassicalBts(dus=[_du1], cu=_cu1)

#########    LteEmu   ##########
_lteemu = LTEEmuCore(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.209.197", username="ute", password="ute"
    ),
    dir_path="/home/ute/wts",
    cfg_filename="5gcn_opc.cfg",
    mme_ip="",
    edaemon_port="60001",
    egate_port="20000",
)

################     Airphone    ################
_airphone_cloud = AirphoneCloud(
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.146.93", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(addr="10.57.146.93"),
)

_egate = SshServiceDetails(addr="0.0.0.0", username="user2", password="password2")

_l3 = SshServiceDetails(addr="3.3.3.3", username="user3", password="password3")

_l2 = SshServiceDetails(addr="10.57.209.21", username="_rcpadmin", password="RCP_owner")

_airphone_pdu = FACOM(addr="10.57.247.199", port_numbers=[2])

_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.146.93", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_airphone_pdu.pdu_ports[2],
)

_l1 = Airscale(common_units=[_common_unit_1])

_airphone = Airphone(
    egate=_egate,
    l3_ssh_connection_details=_l3,
    l2_ssh_connection_details=_l2,
    l1=_l1,
    l3_port=1234,
    edaemon_port=33333,
    egate_port=22222,
    airphone_cloud=_airphone_cloud,
)

#########    Testline     ##########
tl = TestLine(
    test_pc=_host,
    gnbs=[
        _cloud_gnb1
    ],  # if there are two or more gnbs, use this pramater:  gnbs=[_cloud_gnb1, _cloud_gnb2]
    core=_lteemu,  # if use EPC ,please use replace with this:   core=_epc_sim,
    tl_cloud_topology="CLOUD_5G_INVENTORY",
)
