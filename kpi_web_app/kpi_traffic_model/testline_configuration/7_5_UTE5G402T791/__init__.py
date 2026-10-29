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
        addr="10.101.60.97", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# epcsim
_epc_sim = EPCSim(
    mme_ip="3.3.3.3",
    mcc=262,
    mnc=3,
    tac=61,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.101.60.97", username="ute", password="iW_K#8.ute%A10h0m0ra"
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
_ru_pdu = FACOM(addr="10.57.242.50", port_numbers=[6])
_ru1_pdu = FACOM(addr="10.57.242.50", port_numbers=[2])
_ru2_pdu = FACOM(addr="10.57.242.50", port_numbers=[5])
_ru = RU(
    #'AEQE'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[6],
)
_ru1 = RU(
    #'AEQE'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
)
_ru2 = RU(
    #'AEQE'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[5],
)
# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.223.243", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.57.242.45", port_numbers=[7])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[7],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru, _ru1, _ru2], f1_m_ip_addr="10.71.215.197")

_cu = CU(
    backhaul_site_oam_ip="10.57.223.243",  
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.223.243", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.223.243", username="Nemuadmin", password="nemuuser"
    ),
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id="3", global_bts_id="10893")

_appserver_ssh = SshServiceDetails( 
    addr="10.57.163.35", username="cmw_sg2", password="12345678"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.35",
    iperf_path="/usr/bin/iperf",
    port=52970,
)
# mcs
_hbte = HBTE(
    ip_addr="10.57.231.153",
    port="5000",
    attenuation_port_numbers=[1],
    model="PPSAM-64X16-2.3-3.8-90-0.5-360-1-A",
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
        addr="10.57.156.146	", username="spark", password="spark"
    ),
    serial_number="8800df0f",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.12\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100013185", 
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_2 = Android( 
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.146	", username="spark", password="spark"
    ),
    serial_number="8800df0f",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.12\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100011499", 
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_3 = Android(  
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.146	", username="spark", password="spark"
    ),
    serial_number="8800df0f",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.12\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100013182", 
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_4 = Android(  
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.146	", username="spark", password="spark"
    ),
    serial_number="8800df0f",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.12\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100013181", 
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_5 = Android(  
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.146	", username="spark", password="spark"
    ),
    serial_number="8800df0f",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.12\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100013183",  
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_6 = Android( 
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.146	", username="spark", password="spark"
    ),
    serial_number="8800df0f",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.12\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100013184",  
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_7 = Android(  
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.146	", username="spark", password="spark"
    ),
    serial_number="8800df0f",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.12\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262038001006421", 
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_8 = Android(  
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.146	", username="spark", password="spark"
    ),
    serial_number="8800df0f",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.12\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033032996938",  
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)


_sigspark_9 = Android(  
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.131", username="root", password="Dinglicom"
    ),
    serial_number="223db2c",
    server_dir="F:\DingliApp\Pilot PioneerX11.0.9.0\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100013198",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_11 = Android(  
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.131", username="root", password="Dinglicom"
    ),
    serial_number="223db2c",
    server_dir="F:\DingliApp\Pilot PioneerX11.0.9.0\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100013201",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_12 = Android( 
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.131", username="root", password="Dinglicom"
    ),
    serial_number="223db2c",
    server_dir="F:\DingliApp\Pilot PioneerX11.0.9.0\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100013202",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_13 = Android(  
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.131", username="root", password="Dinglicom"
    ),
    serial_number="223db2c",
    server_dir="F:\DingliApp\Pilot PioneerX11.0.9.0\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100013203",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_14 = Android(  
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.131", username="root", password="Dinglicom"
    ),
    serial_number="223db2c",
    server_dir="F:\DingliApp\Pilot PioneerX11.0.9.0\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100013204",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)




_sigspark_18 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.149", username="spark", password="spark"
    ),
    serial_number="d497cecc",
    server_dir="C:\Program Files (x86)\Spark1.1.2007.12\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100004095",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_19 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.149", username="spark", password="spark"
    ),
    serial_number="d497cecc",
    server_dir="C:\Program Files (x86)\Spark1.1.2007.12\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100004096",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_20 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.149", username="spark", password="spark"
    ),
    serial_number="d497cecc",
    server_dir="C:\Program Files (x86)\Spark1.1.2007.12\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100004097",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_21 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.149", username="spark", password="spark"
    ),
    serial_number="d497cecc",
    server_dir="C:\Program Files (x86)\Spark1.1.2007.12\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100004098",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_22 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.149", username="spark", password="spark"
    ),
    serial_number="d497cecc",
    server_dir="C:\Program Files (x86)\Spark1.1.2007.12\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100004099",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_23 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.149", username="spark", password="spark"
    ),
    serial_number="d497cecc",
    server_dir="C:\Program Files (x86)\Spark1.1.2007.12\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100004100",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_24 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.149", username="spark", password="spark"
    ),
    serial_number="d497cecc",
    server_dir="C:\Program Files (x86)\Spark1.1.2007.12\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100004101",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_25 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.149", username="spark", password="spark"
    ),
    serial_number="d497cecc",
    server_dir="C:\Program Files (x86)\Spark1.1.2007.12\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100004102",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)



_sigspark_27 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.132", username="root", password="123456"
    ),
    serial_number="d711e9e0",
    server_dir="D:\PioneerFDD\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100013190",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_28 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.132", username="root", password="123456"
    ),
    serial_number="d711e9e0",
    server_dir="D:\PioneerFDD\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100013175",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_29 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.132", username="root", password="123456"
    ),
    serial_number="d711e9e0",
    server_dir="D:\PioneerFDD\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100013193",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_30 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.132", username="root", password="123456"
    ),
    serial_number="d711e9e0",
    server_dir="D:\PioneerFDD\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100013178",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_32 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.132", username="root", password="123456"
    ),
    serial_number="d711e9e0",
    server_dir="D:\PioneerFDD\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100013177",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_33 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.132", username="root", password="123456"
    ),
    serial_number="d711e9e0",
    server_dir="D:\PioneerFDD\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100013173",
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
        _sigspark_9,
        _sigspark_11,
        _sigspark_12,
        _sigspark_13,
        _sigspark_14,
        _sigspark_18,
        _sigspark_19,
        _sigspark_20,
        _sigspark_21,
        _sigspark_22,
        _sigspark_23,
        _sigspark_24,
        _sigspark_25,
        _sigspark_27,
        _sigspark_28,
        _sigspark_29,
        _sigspark_30,
        _sigspark_32,
        _sigspark_33,
    ],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
    mcses=_hbte,  
    attenuator=_attenuator,
)
# compatibility workaround
