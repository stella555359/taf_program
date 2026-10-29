import os
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.mcs import HBTE
from taf.config.testline.mcs import TopYoung
from taf.config.testline.attenuator import HBTE

# from taf.config.testline.attenuator import AttenuationPort, TopYoung
# from taf.config.testline import HBTE
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
    MediaTek,
    LicenseKeeper,
)
from taf.config.testline import (
    Enb,
    SimEnb,
    RealEnb,
    RadioModule,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.appserver import AppServer

__maintainer__ = "Wang Ming"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_2_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "ming.5.wang@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.131.180", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# epcsim
_epc_sim = EPCSim(
    mme_ip="3.3.3.3",
    mcc=262,
    mnc=3,
    tac=61,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.131.180", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    dir_path="/opt/iphy/latest/",
    cfg_filename="eNB_WMP_new.cfg",
)

# PA
_attenuator = HBTE(
    ip_addr="10.71.215.209",
    port=5000,
    attenuation_port_numbers=[13, 14, 15, 16],
    model="PA-32-32-6-127-0.5",
)

# 5GRU for classicalBTS
_ru_pdu = FACOM(addr="10.71.197.82", port_numbers=[2])

_ru = RU(
    #'AEQE'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[2],
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.71.215.197", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.71.215.197")

_cu = CU(
    backhaul_site_oam_ip="10.71.215.197",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.215.197", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.215.197", username="Nemuadmin", password="nemuuser"
    ),
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id="3", global_bts_id="10893")

_appserver_ssh = SshServiceDetails(
    addr="10.71.219.230", username="iperf", password="39nBTScHWRf3weyBMK0="
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.230",
    iperf_path="/usr/bin/iperf",
    port=52970,
)

_topyoung = TopYoung(
    ip_addr="10.71.215.204",
    port=28888,
    mcs_port_numbers=[1],
    model="MCS2350A2-128B16-E6",
)

_appserver = AppServer(_iperf)

# _tm500 = TM500(
#    tma_host=SshServiceDetails(
#        addr="10.57.130.166",
#        username="nokia5G",
#        password="noki@123",
#    ),
#    tma_command_port=5030,
#    pdu_port=None,
#    iperf_details=_iperf,
#    tma_path="/cygdrive/c/Program Files (x86)/Aeroflex/TM500/5G NR - NLA_4_31_0/Test Mobile Application/TmaApplication.exe",
# )

_sigspark_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.128", username="nokia5G", password="noki@123"
    ),
    serial_number="8800df0f",
    server_dir="C:\Program Files (x86)\Spark1.1.2005.6\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262038001006105",
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.215.162", username="spark", password="spark"
    ),
    serial_number="223db2c",
    server_dir="C:\Program Files (x86)\Spark1.1.1998.10\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100004131",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.215.162", username="spark", password="spark"
    ),
    serial_number="d497cecc",
    server_dir="C:\Program Files (x86)\Spark1.1.1998.10\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100004133",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_4 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.215.162", username="spark", password="spark"
    ),
    serial_number="a955f092",
    server_dir="C:\Program Files (x86)\Spark1.1.1998.10\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100004134",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_5 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.215.162", username="spark", password="spark"
    ),
    serial_number="95b5ed2a",
    server_dir="C:\Program Files (x86)\Spark1.1.1998.10\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100004132",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_6 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.215.162", username="spark", password="spark"
    ),
    serial_number="d77a0eda",
    server_dir="C:\Program Files (x86)\Spark1.1.1998.10\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100004135",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_7 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.215.162", username="spark", password="spark"
    ),
    serial_number="d711e9e0",
    server_dir="C:\Program Files (x86)\Spark1.1.1998.10\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100004130",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_8 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.215.162", username="spark", password="spark"
    ),
    serial_number="e1c97de5",
    server_dir="C:\Program Files (x86)\Spark1.1.1998.10\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100004136",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

tl = TestLine(
    test_pc=_host,
    core=_epc_sim,
    gnbs=[_classical_bts],
    ues=[_sigspark_1],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
    mcses=_topyoung,
    attenuator=_attenuator,
)
# compatibility workaround
