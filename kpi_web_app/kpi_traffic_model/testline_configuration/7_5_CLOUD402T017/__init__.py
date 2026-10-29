import os
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.ue import Android
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline.attenuator import HBTE
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Enb, SimEnb, RealEnb, RadioModule, LTEEmuEnb
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.mcs import HBTE

__maintainer__ = "BIJIAJIAN"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG2"
__email__ = "jiajian.bi@nokia-sbell.com"

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.112", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# Real 5G Core is used in real world.  here use EPCsim as the 5GC class is not implemented in tl config lib yet.
_epc_sim = EPCSim(
    mme_ip="10.110.227.5",
    mcc="460",
    mnc="2",
    tac="0",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.227.70", username="haijtest", password="Nokia_1234"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)

# RealEnb
_real_enb_pdu = FACOM(addr="10.57.242.142", port_numbers=[5])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.231.123", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[5],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

##5GRU for classical BTS
_ru1_pdu = FACOM(addr="10.57.131.130", port_numbers=[4])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="user", password="pass"
    ),
    pdu_port=_ru1_pdu.pdu_ports[4],
)

_ru2_pdu = FACOM(addr="10.57.243.153", port_numbers=[2])

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="user", password="pass"
    ),
    pdu_port=_ru2_pdu.pdu_ports[2],
)

_ru3_pdu = FACOM(addr="10.57.243.153", port_numbers=[3])

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="user", password="pass"
    ),
    pdu_port=_ru3_pdu.pdu_ports[3],
)

_ru4_pdu = FACOM(addr="10.57.131.130", port_numbers=[4])

_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="user", password="pass"
    ),
    pdu_port=_ru4_pdu.pdu_ports[4],
)

_ru5_pdu = FACOM(addr="10.57.243.153", port_numbers=[2])

_ru5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="user", password="pass"
    ),
    pdu_port=_ru5_pdu.pdu_ports[2],
)

_ru6_pdu = FACOM(addr="10.57.243.153", port_numbers=[3])

_ru6 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="user", password="pass"
    ),
    pdu_port=_ru6_pdu.pdu_ports[3],
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_pdu = FACOM(addr="10.57.242.46", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6], f1_m_ip_addr="10.57.223.233")

##CU
_cu = CU(
    backhaul_site_oam_ip="10.57.223.233",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.223.233", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.223.233", username="Nemuadmin", password="nemuuser"
    ),
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id="17", global_bts_id="17")

##HBTE_MCS
_hbte = HBTE(
    ip_addr="10.57.156.181",
    port="5000",
    mcs_port_numbers=[1],
    model="PPSAM-64X16-2.3-3.8-90-0.5-360-1-A",
)

# SIGSPARK
_ue_host1_ssh = SshServiceDetails(
    addr="10.57.156.182", username="spark", password="spark"
)

_ue_host2_ssh = SshServiceDetails(
    addr="10.57.156.183", username="spark", password="spark"
)

_ue_host3_ssh = SshServiceDetails(
    addr="10.70.222.178", username="spark", password="spark"
)

_ue_host4_ssh = SshServiceDetails(
    addr="10.70.222.179", username="spark", password="spark"
)

_spark_appserver_ssh = SshServiceDetails(
    # addr="10.57.163.35",username="cmw_sg2",password="12345678"
    addr="10.57.162.12", 
    username="cmw_sg2", 
    password="cm@2",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.162.12",
    iperf_path="/usr/bin/iperf",
    port=52228,
)

_sigspark1 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="3a843cfe",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032993568",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="3ae9afec",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032996935",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark3 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="70507bd7",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032996937",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark4 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="70814971",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032996936",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark5 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="87762734",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032996901",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark6 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="e19a20bd",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032996902",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark7 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="f0872d22",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032996903",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark8 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="3a843cfe",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032996934",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark9 = Android(
    ssh_connection_details=_ue_host3_ssh,
    serial_number="8dbb8e3b",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100008437",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark10 = Android(
    ssh_connection_details=_ue_host3_ssh,
    serial_number="3c84598e",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100008431",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark11 = Android(
    ssh_connection_details=_ue_host3_ssh,
    serial_number="9984304",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100008428",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark12 = Android(
    ssh_connection_details=_ue_host3_ssh,
    serial_number="7b38be73",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100008441",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark13 = Android(
    ssh_connection_details=_ue_host3_ssh,
    serial_number="f552a44c",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100008430",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark14 = Android(
    ssh_connection_details=_ue_host3_ssh,
    serial_number="21179052",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100008438",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark15 = Android(
    ssh_connection_details=_ue_host3_ssh,
    serial_number="4e514a93",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100008429",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark16 = Android(
    ssh_connection_details=_ue_host3_ssh,
    serial_number="84cec6d",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100008436",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark17 = Android(
    ssh_connection_details=_ue_host4_ssh,
    serial_number="e31f63ff",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032993563",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark18 = Android(
    ssh_connection_details=_ue_host4_ssh,
    serial_number="a02d00cf",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100008433",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark19 = Android(
    ssh_connection_details=_ue_host4_ssh,
    serial_number="f97a9bc1",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262038001006325",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark20 = Android(
    ssh_connection_details=_ue_host4_ssh,
    serial_number="e38279b1",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100008432",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark21 = Android(
    ssh_connection_details=_ue_host4_ssh,
    serial_number="20f53347",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032993566",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark22 = Android(
    ssh_connection_details=_ue_host4_ssh,
    serial_number="5a0d84af",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100008434",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark23 = Android(
    ssh_connection_details=_ue_host4_ssh,
    serial_number="a2d367ca",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032993562",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark24 = Android(
    ssh_connection_details=_ue_host4_ssh,
    serial_number="5056a1c0",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100008435",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark25 = Android(
    ssh_connection_details=_ue_host2_ssh,
    serial_number="5056a1c0",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="460023100010675",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark26 = Android(
    ssh_connection_details=_ue_host2_ssh,
    serial_number="5056a1c0",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100011520",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark27 = Android(
    ssh_connection_details=_ue_host2_ssh,
    serial_number="5056a1c0",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100011521",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark28 = Android(
    ssh_connection_details=_ue_host2_ssh,
    serial_number="5056a1c0",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100004104",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark29 = Android(
    ssh_connection_details=_ue_host2_ssh,
    serial_number="5056a1c0",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="460023100010676",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark30 = Android(
    ssh_connection_details=_ue_host2_ssh,
    serial_number="5056a1c0",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="460023100010678",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark31 = Android(
    ssh_connection_details=_ue_host2_ssh,
    serial_number="5056a1c0",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100011518",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark32 = Android(
    ssh_connection_details=_ue_host2_ssh,
    serial_number="5056a1c0",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.35\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="460023100010677",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    core=_epc_sim,
    mcses=_hbte,
    ues=[
        _sigspark1,
        _sigspark2,
        _sigspark3,
        _sigspark4,
        _sigspark5,
        _sigspark6,
        _sigspark7,
        _sigspark8,
        _sigspark9,
        _sigspark10,
        _sigspark11,
        _sigspark12,
        _sigspark13,
        _sigspark14,
        _sigspark15,
        _sigspark16,
        _sigspark17,
        _sigspark18,
        _sigspark19,
        _sigspark20,
        _sigspark21,
        _sigspark22,
        _sigspark23,
        _sigspark24,
        _sigspark25,
        _sigspark26,
        _sigspark27,
        _sigspark28,
        _sigspark29,
        _sigspark30,
        _sigspark31,
        _sigspark32,
    ],
    tl_cloud_topology=_tl_cloud_topology,
)
