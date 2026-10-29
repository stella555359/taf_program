import os
import yaml
import re
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500, Android
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.nms import Netact

__maintainer__ = "ChenCheng"  # TL owner name
__team__ = "I_MN_5G_RAN_IV4_LINE_HZG_8_IV@internal.nsn.com"  # TL owner's team
__email__ = "cheng.2.chen@nokia-sbell.com"  # TL owner's email
# common
__all__ = ["tl"]
_cfg_dir = os.path.dirname(os.path.abspath(__file__))
##testPc(taf)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.141", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
# 5GRU for classicalBTS
# PB for RU
# the sequence accord to webui read out.
_ru_pdu = FACOM(addr="10.68.87.111", port_numbers=[1])
_ru = RU(
    ru_hw_group="AEQV",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.127", username="nokia5G", password="noki@123"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
)
_ru_pdu2 = FACOM(addr="10.68.87.111", port_numbers=[2])
_ru2 = RU(
    ru_hw_group="AEQV",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.120", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu2.pdu_ports[2],
)
_ru_pdu3 = FACOM(addr="10.68.87.109", port_numbers=[2])
_ru3 = RU(
    ru_hw_group="AEQV",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.118", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu3.pdu_ports[2],
)
##classical gNB parameter
# gNB lmp ip
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
# abil internal ip
_capacity_unit = CapacityUnit(addr="192.168.253.20")
# gNB PB
_gnb_pdu = FACOM(addr="10.68.87.107", port_numbers=[3])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru, _ru2, _ru3])
# _du = DU(airscale=_airscale, rus=[_ru])
# gNB oam mplane ip
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.89.20", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.89.20", username="Nemuadmin", password="nemuuser"
    ),
)
# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.68.89.13", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = FACOM(addr="10.57.241.160", port_numbers=[2])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[2],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)
## switch Dtor
# switch prot to ASIK EIF
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.68.85.9", port="1/21", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)
##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"
# instance_id = MRBTS_ID
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=810)
# netact ip
_netact = Netact("10.106.161.25")
##L3 call added
# QualComm UE
_appserver_ssh = SshServiceDetails(
    addr="10.57.162.10", username="cmw_sg7", password="Nokia07!", port="57892"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.10",
    iperf_path="/usr/bin/iperf",
    port=57892,
)
# CI_Detail_UE_Type='Huawei Honor 30s'
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.127", username="nokia5G", password="noki@123"
    ),
    serial_number="174e8f62",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "HONOR"],
)
# Askey
ue_config_path = os.path.join(_cfg_dir, "TestData/askey.yml")
if os.path.isfile(ue_config_path):
    with open(ue_config_path) as f:
        ue_config = yaml.load(f, Loader=yaml.FullLoader)
else:
    ue_config = ""
tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    switches=[_dell_s4048on_switch],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
    ues=[ue_config],
)
