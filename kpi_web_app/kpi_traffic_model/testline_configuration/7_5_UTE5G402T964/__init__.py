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

__maintainer__ = "Chen Xiaoqing"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_2_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "xiaoqing.chen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.201", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# epcsim
_epc_sim = EPCSim(
    mme_ip="3.3.3.3",
    mcc=262,
    mnc=3,
    tac=61,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.131.166", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    dir_path="/opt/iphy/latest/",
    cfg_filename="eNB_WMP_new.cfg",
)

# 5GRU for classicalBTS
_ru_pdu = FACOM(addr="10.57.240.198", port_numbers=[4])

_ru = RU(
    #'AEQP'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[4],
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.131.58", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.57.240.252", port_numbers=[5])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.57.131.58")

_cu = CU(
    backhaul_site_oam_ip="10.68.88.41",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.131.58", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.131.58", username="Nemuadmin", password="nemuuser"
    ),
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id="1", global_bts_id="964")

# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.57.240.213", username="spark", password="spark"
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.163.35", username="cmw_sg2", password="12345678"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.35",
    iperf_path="iperf",
    port=52228,
)

_appserver = AppServer(_iperf)

_sigspark_1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="1c105102",
    server_dir="C:/Program Files (x86)/Spark1.1.2003.9/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="450053100009271",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_2 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="742b40f1",
    server_dir="C:/Program Files (x86)/Spark1.1.2003.9/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="450053100009270",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_3 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="2ce573e0",
    server_dir="C:/Program Files (x86)/Spark1.1.2003.9/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="450053100009268",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_4 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="785e47db",
    server_dir="C:/Program Files (x86)/Spark1.1.2003.9/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="450053100009274",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_5 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="24ae85a0",
    server_dir="C:/Program Files (x86)/Spark1.1.2003.9/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="450053100009275",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_6 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="ecb50742",
    server_dir="C:/Program Files (x86)/Spark1.1.2003.9/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="450053100009273",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_7 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="9b3372c9",
    server_dir="C:/Program Files (x86)/Spark1.1.2003.9/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="450053100009272",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_8 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="e28e3201",
    server_dir="C:/Program Files (x86)/Spark1.1.2003.9/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="450053100009269",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

tl = TestLine(
    test_pc=_host,
    core=_epc_sim,
    gnbs=[_classical_bts],
    ues=[
        _sigspark_1,
        _sigspark_2,
        _sigspark_3,
        _sigspark_4,
        _sigspark_5,
        _sigspark_6,
        _sigspark_7,
        _sigspark_8,
    ],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
)
