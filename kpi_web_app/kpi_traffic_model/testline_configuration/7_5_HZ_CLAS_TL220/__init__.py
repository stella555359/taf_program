######################################
#  TestLine Classical HZ
#  @Last Modify: 2019-12-23
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

################    Common     ################
__all__ = ["tl"]
_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

"""
_PARAMS_TO_MODIFY_SCF = [
    dict(value='CI-TLDX0205', dist_name='MRBTS-1900', p_name='btsName'),
    dict(value='172.18.10.20', dist_name='LTE_x2', p_name='amfIPAddress'),
    dict(value='172.18.10.11', dist_name='CU_x2Cplane', p_name='localIpAddr'),
    dict(value='172.18.10.12', dist_name='CU_s1Uplane', p_name='localIpAddr'),
    dict(value='172.18.10.12', dist_name='CU_x2Uplane', p_name='localIpAddr')
]
"""

#########    Testpc    ##########
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.209.186", username="ute", password="ute"
    )
)


################    DU1    ################
_gnb_1_airscale_cu_lmp = SshServiceDetails(
    addr="10.57.147.132", username="toor4nsn", password="oZPS0POrRieRtu"
)

_gnb_1_airscale_cu_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_1_pdu = FACOM(addr="10.57.247.218", port_numbers=[3])

_gnb_1_airscale_cu = CommonUnit(
    lmp_connection=_gnb_1_airscale_cu_lmp,
    capacity_units=[_gnb_1_airscale_cu_capacity_unit],
    pdu_port=_gnb_1_pdu.pdu_ports[3],
)

_gnb_1_airscale = Airscale(common_units=[_gnb_1_airscale_cu])

_du1 = DU(airscale=_gnb_1_airscale)

################    DU2    ################
_gnb_1_airscale_cu_lmp = SshServiceDetails(
    addr="10.57.147.136", username="toor4nsn", password="oZPS0POrRieRtu"
)

_gnb_1_airscale_cu_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_1_pdu = FACOM(addr="10.57.247.218", port_numbers=[2])

_gnb_1_airscale_cu = CommonUnit(
    lmp_connection=_gnb_1_airscale_cu_lmp,
    capacity_units=[_gnb_1_airscale_cu_capacity_unit],
    pdu_port=_gnb_1_pdu.pdu_ports[2],
)

_gnb_1_airscale = Airscale(common_units=[_gnb_1_airscale_cu])

_du2 = DU(airscale=_gnb_1_airscale)

################      ClassicalBts1    ################
_cu1 = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.149.162", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.149.162", username="Nemuadmin", password="nemuuser"
    ),
)

_cloud_gnb1 = ClassicalBts(dus=[_du1], cu=_cu1)
# _cloud_gnb1.instance_id = 2003

################      ClassicalBts2    ################
_cu2 = CU(
    backhaul_site_oam_ip="10.57.149.164",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.149.164", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.149.164", username="Nemuadmin", password="nemuuser"
    ),
)

_cloud_gnb2 = ClassicalBts(dus=[_du2], cu=_cu2)
# _cloud_gnb2.instance_id = 2007

#########    LteEmu   ##########
_lteemu = LTEEmuCore(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.201.24", username="nokia", password="nokia123"
    ),
    dir_path="/home/nokia/LTEemu_core2_64_3252",
    cfg_filename="basic_wts_step1.cfg",
    mme_ip="",
    edaemon_port="22222",
    egate_port="9880",
)

# _scf = SCF(project='5G19', name='SBTS5G19_5g_pid12_classical.xml', scf_params=_PARAMS_TO_MODIFY_SCF)

#########   Airphone   ##########
_airphone_cloud = AirphoneCloud(
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.201.83", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(addr="10.57.201.83"),
)

_egate = SshServiceDetails(addr="0.0.0.0", username="user2", password="password2")

_l3 = SshServiceDetails(addr="3.3.3.3", username="user3", password="password3")

_l2 = SshServiceDetails(addr="10.57.209.16", username="_rcpadmin", password="RCP_owner")

_airphone_pdu = FACOM(addr="10.57.242.30", port_numbers=[5])

_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.232.213", username="toor4nsn", password="oZPS0POrRieRtu"
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

#########    Testline     ##########
tl = TestLine(
    test_pc=_host,
    gnbs=[
        _cloud_gnb1,
        _cloud_gnb2,
    ],  # if there are two or more gnbs, use this pramater:  gnbs=[_cloud_gnb1, _cloud_gnb2]
    core=_lteemu,  # if use EPC ,please use replace with this:   core=_epc_sim,
    ues=[_airphone],  # if ENV is only one ue, please delete others
    tl_cloud_topology="CLOUD_5G_INVENTORY",
)

# tl.scf=_scf             # still a WA

# customer parameter
# PACKAGE_SERVER_IP = '10.57.212.88'
# PACKAGE_SERVER_USER = 'root'
# PACKAGE_SERVER_PWD = 'uteadmin'
# gNB_Package_path = '/home/package'
# YAFT_path = '/home/yaft'
# package_url = 'https://artifactory-espoo1.ext.net.nokia.com/artifactory/mnp5g-central-public-local/System_Release/'
# Baseband = 'ABIL'
