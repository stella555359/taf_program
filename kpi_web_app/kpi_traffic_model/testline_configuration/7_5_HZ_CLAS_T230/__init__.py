######################################
#  TestLine Classical HZ
#
#  @TestLine: TL230
#  @Last Modify: 2019-12-10
######################################
__maintainer__ = "yonmiao"
__team__ = "NSB MN ECE RD 2 CN 06 SG"
__email__ = "yonggang.miao@nokia-sbell.com"

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
        addr="10.57.212.88", username="ute", password="ute"
    )
)

################    DU1    ################


_gnb_1_airscale_cu_lmp = SshServiceDetails(
    addr="", username="toor4nsn", password="oZPS0POrRieRtu"
)

_gnb_1_airscale_cu_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_1_pdu = FACOM(addr="", port_numbers=[2])

_gnb_1_airscale_cu = CommonUnit(
    lmp_connection=_gnb_1_airscale_cu_lmp,
    capacity_units=[_gnb_1_airscale_cu_capacity_unit],
    pdu_port=_gnb_1_pdu.pdu_ports[2],
)

_gnb_1_airscale = Airscale(common_units=[_gnb_1_airscale_cu])

_du1 = DU(airscale=_gnb_1_airscale)


################      ClassicalBts1    ################
_cu1 = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.146.145", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.146.145", username="Nemuadmin", password="nemuuser"
    ),
)

_cloud_gnb1 = ClassicalBts(dus=[_du1], cu=_cu1)


################       LTEemuSim    ################
_lteemu = LTEEmuCore(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.16", username="ute", password="ute"
    ),
    dir_path="/home/ute/wts/",
    cfg_filename="basic_wts_step2.cfg",
    mme_ip="",
    edaemon_port="22222",
    egate_port="20000",
)


################     Airphone    ################
_airphone_cloud = AirphoneCloud(
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.146.131", username="toor4nsn", password="ute"
    ),
    oam_http_connection_details=HttpConnectionDetails(addr="10.57.201.83"),
)

_egate = SshServiceDetails(addr="0.0.0.0", username="user2", password="password2")

_l3 = SshServiceDetails(addr="3.3.3.3", username="user3", password="password3")

_l2 = SshServiceDetails(addr="10.57.209.16", username="_rcpadmin", password="RCP_owner")

_airphone_pdu = FACOM(addr="", port_numbers=[5])

_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.146.146", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_airphone_pdu.pdu_ports[5],
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

################      TestLine     ################

tl = TestLine(
    test_pc=_host,
    gnbs=[
        _cloud_gnb1
    ],  # if there are two or more gnbs, use this pramater:  gnbs=[_cloud_gnb1, _cloud_gnb2]
    core=_lteemu,  # if use EPC ,please use replace with this:   core=_epc_sim,
    ues=[_airphone],  # if ENV is only one ue, please delete others
    tl_cloud_topology="CLOUD_5G_INVENTORY",
)

__all__ = ["tl"]
