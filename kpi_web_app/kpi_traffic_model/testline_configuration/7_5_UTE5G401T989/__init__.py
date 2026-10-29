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
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.appserver import AppServer
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact

__maintainer__ = "Rao Shengrong"  # TL owner name
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04@internal.nsn.com"  # TL owner's team
__email__ = "shengrong.rao@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.57", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS
_ru_pdu1 = FACOM(addr="10.64.166.130", port_numbers=[1])
_ru1 = RU(
    ru_hw_group="AWGUD",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="ckBW1r1CX7VUPHcoHd69to3UwvEVm+cGW1aXDlfr51Y=",
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_pdu1.pdu_ports[1],
)

_ru_pdu2 = FACOM(addr="10.64.166.130", port_numbers=[2])
_ru2 = RU(
    ru_hw_group="AWGUD",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="asmr"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_pdu2.pdu_ports[2],
)

_ru_pdu3 = FACOM(addr="10.64.166.130", port_numbers=[3])
_ru3 = RU(
    ru_hw_group="AWEUA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="asmr"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_pdu3.pdu_ports[3],
)


##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = FACOM(addr="10.64.166.130", port_numbers=[4])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[4],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru1, _ru2, _ru3], f1_m_ip_addr="10.71.209.239")


##CU
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.64.166.130",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.64.166.130",
        username="Nemuadmin",
        password="nemuuser",
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.64.166.130", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = FACOM(addr="10.64.166.130", port_numbers=[3])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[3],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

## switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.101.63.81", port="1/22", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

##cloud_topology
# _tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=747)
_netact = Netact("10.107.178.214")

# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.57.178.18", username="mmw_sg4", password="mm@4", port="44341"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.18",
    iperf_path="/usr/bin/iperf",
    port="44341",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.18",
    iperf_path="/usr/bin/iperf",
    port="44341",
)

_appserver = AppServer(_iperf_details_on_appserver)

# Qualcomm
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.11", username="nokia5G", password="noki@123"
    ),
    serial_number="8cda1e05",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.4/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    # qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    # diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "askey_sigspark"],
    imsi="310260310000782",
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
    nms=_netact,
    switches=[_dell_s4048on_switch],
    appserver=_appserver,
    ues=[ue_config],
)
