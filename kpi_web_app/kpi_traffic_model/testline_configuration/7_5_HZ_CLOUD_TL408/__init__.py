######################################
#  TestLine Cloud HZ L1BYPASS
#
#  @TestLine: TL408
#  @Last Modify: 2019-12-10
######################################
__maintainer__ = "yonmiao"
__team__ = "NSB MN ECE RD 2 CN 06 SG"
__email__ = "yonggang.miao@nokia-sbell.com"


import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    OpenStackConnectionDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
)
from taf.config.testline.cloud_hosting import NCIR, ControlNode
from taf.config.testline.gnb import CloudBts, CU, DU
from taf.config.testline.core import LTEEmuCore
from taf.config.testline.ue import AirphoneCloud, Airphone
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FACOM


################    Common     ################
_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

################     Test PC    ################
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.209.186", username="ute", password="ute"
    )
)

################    NCIR    ################
_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.57.138.18", username="TL408", tenant="TL408", password="NCIR@l408"
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.138.18", username="TL242", password="NCIR@l408"
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_ncir = NCIR(compute_nodes=[], control_nodes=[_control_0], version="ncir_19")


################    DU1    ################

_gnb_1_airscale_cu_lmp = SshServiceDetails(
    addr="10.57.146.130", username="toor4nsn", password="oZPS0POrRieRtu"
)

_gnb_1_airscale_cu_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_1_pdu = FACOM(addr="10.57.247.202", port_numbers=[1])

_gnb_1_airscale_cu = CommonUnit(
    lmp_connection=_gnb_1_airscale_cu_lmp,
    capacity_units=[_gnb_1_airscale_cu_capacity_unit],
    pdu_port=_gnb_1_pdu.pdu_ports[1],
)

_gnb_1_airscale = Airscale(common_units=[_gnb_1_airscale_cu])

_du1 = DU(airscale=_gnb_1_airscale)


################      CloudBts1    ################
_cu1 = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.219.61", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.219.61", username="Nemuadmin", password="nemuuser"
    ),
)
# ABIL
_capacity_unit = CapacityUnit(addr="192.168.253.22")
# PDU
_gnb_1_pdu = FACOM(addr="10.57.247.202", port_numbers=[1])
# ASIK
_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.146.130", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_1_pdu.pdu_ports[1],
)

_airscale_1 = Airscale(common_units=[_common_unit_1])

_du_1 = DU(airscale=_airscale_1)

_cloud_gnb1 = CloudBts(cu=_cu1, dus=[_du_1], cloud_deployment=None, vnf_name="vnf_ncir")

################       LTEemuSim    ################
_lteemu = LTEEmuCore(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.209.240", username="ute", password="ute"
    ),
    dir_path="/home/ute/wts_4.0.12188",
    cfg_filename="basic_l1bypass_nsa_call_tdd_mmwv.cfg",
    mme_ip="",
    edaemon_port="22222",
    egate_port="20000",
)

################     Airphone    ################
_airphone_cloud = AirphoneCloud(
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.146.131", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(addr="10.57.146.131"),
)

_egate = SshServiceDetails(addr="0.0.0.0", username="user2", password="password2")

_l3 = SshServiceDetails(addr="3.3.3.3", username="user3", password="password3")

_l2 = SshServiceDetails(addr="10.57.209.16", username="_rcpadmin", password="RCP_owner")

_airphone_pdu = FACOM(addr="10.57.247.202", port_numbers=[2])

_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.146.131", username="toor4nsn", password="oZPS0POrRieRtu"
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

################      TestLine     ################

tl = TestLine(
    test_pc=_host,
    gnbs=[_cloud_gnb1],  # if there are two or more gnbs, use this pramater:
    cloud_hostings=[_ncir],
    core=_lteemu,  # if use EPC ,please use replace with this:
    ues=[_airphone],  # if ENV is only one ue, please delete others
    tl_cloud_topology="CLOUD_5G_INVENTORY",
)


Baseband = "ABIL"
airscaleNodeID = ["0x10", "0x12"]
TL_ID = "tl408"

cfg_filename_ipv4 = "basic_nsa_call_tdd_above6GHz.cfg"
cfg_filename_ipv6 = "basic_nsa_call_tdd_above6GHz_ipv6.cfg"

L1byPass_flag = "L1BYPASS"
__all__ = ["tl"]
