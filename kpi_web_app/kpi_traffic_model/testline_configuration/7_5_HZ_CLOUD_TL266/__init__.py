######################################
#  TestLine Cloud HZ
#
#  @TestLine: TL266
#  @Last Modify: 2019-12-25
######################################
__maintainer__ = "Xu Zhuoyan"
__team__ = "NSB MN ECE RD 2 CN 06 SG"
__email__ = "zhuoyan.xu@nokia-sbell.com"


import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb import CU, ClassicalBts, CloudBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import FACOM

# from taf.config.testline.ue import Qualcomm, Prisma, QualcommUeType, Android
from taf.config.testline.ue import *
from taf.config.testline.core import EPCSim, LTEEmuCore
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer


################    Common     ################
_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


################     Test PC    ################
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.209.186", username="ute", password="ute"
    )
)

################    DU1    ################

_gnb_1_airscale_cu_lmp = SshServiceDetails(
    addr="10.57.146.170", username="toor4nsn", password="oZPS0POrRieRtu"
)

_gnb_1_airscale_cu_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_1_pdu = FACOM(addr="10.57.247.205", port_numbers=[3])

_gnb_1_airscale_cu = CommonUnit(
    lmp_connection=_gnb_1_airscale_cu_lmp,
    capacity_units=[_gnb_1_airscale_cu_capacity_unit],
    pdu_port=_gnb_1_pdu.pdu_ports[3],
)

_gnb_1_airscale = Airscale(common_units=[_gnb_1_airscale_cu])

_du1 = DU(airscale=_gnb_1_airscale)


################      CloudBts1    ################
_cu1 = CU(
    backhaul_site_oam_ip="10.57.201.37",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.201.37", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.201.37", username="Nemuadmin", password="nemuuser"
    ),
)

_cloud_gnb1 = CloudBts(dus=[_du1], cu=_cu1, cloud_deployment="")


################       LTEemuSim    ################
_lteemu = LTEEmuCore(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.209.195", username="ute", password="ute"
    ),
    dir_path="/home/ute/WTS_1654065",
    cfg_filename="basic_wts_step1.cfg",
    mme_ip="",
    edaemon_port="22222",
    egate_port="20000",
)

################      TestLine     ################

tl = TestLine(
    test_pc=_host,
    gnbs=[_cloud_gnb1],  # if there are two or more gnbs, use this pramater:
    core=_lteemu,  # if use EPC ,please use replace with this:
    ues=[],  # if ENV is only one ue, please delete others
    tl_cloud_topology="CLOUD_5G_INVENTORY",
)

__all__ = ["tl"]
