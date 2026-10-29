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

__maintainer__ = "bijiajian"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG2"
__email__ = "jiajian.bi@nokia-sbell.com"

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.234.180", username="ute", password="iW_K#8.ute%A10h0m0ra"
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
        addr="10.57.240.179", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[5],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

##5GRU for classical BTS
_ru1_pdu = FACOM(addr="10.57.243.21", port_numbers=[3])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="user", password="pass"
    ),
    pdu_port=_ru1_pdu.pdu_ports[3],
)

_ru2_pdu = FACOM(addr="10.57.243.21", port_numbers=[5])

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="user", password="pass"
    ),
    pdu_port=_ru2_pdu.pdu_ports[5],
)

_ru3_pdu = FACOM(addr="10.57.243.21", port_numbers=[4])

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="user", password="pass"
    ),
    pdu_port=_ru3_pdu.pdu_ports[4],
)

_ru4_pdu = FACOM(addr="10.57.234.189", port_numbers=[5])

_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="user", password="pass"
    ),
    pdu_port=_ru4_pdu.pdu_ports[5],
)

_ru5_pdu = FACOM(addr="10.57.234.189", port_numbers=[4])

_ru5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="user", password="pass"
    ),
    pdu_port=_ru5_pdu.pdu_ports[4],
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_pdu = FACOM(addr="10.57.240.253", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1, _ru2, _ru3, _ru4, _ru5], f1_m_ip_addr="10.57.131.55")

##CU
_cu = CU(
    backhaul_site_oam_ip="10.57.131.55",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.131.55", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.131.55", username="Nemuadmin", password="nemuuser"
    ),
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id="20222", global_bts_id="20222")

# SIGSPARK
_ue_host1_ssh = SshServiceDetails(
    addr="10.57.234.180", username="spark", password="spark"
)

_spark_appserver_ssh = SshServiceDetails(
    addr="10.57.162.12", username="cmw_sg2", password="cm@2"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.162.12",
    iperf_path="iperf",
    port=50222,
)

_sigspark1 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="3df8a4f4",
    server_dir="C:\Program Files (x86)\Spark1.1.2006.1\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="460023100010676",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="323a76d0",
    server_dir="C:\Program Files (x86)\Spark1.1.2006.1\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100011521",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark3 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="d83a8a5b",
    server_dir="C:\Program Files (x86)\Spark1.1.2006.1\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100004104",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark4 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="1732daa3",
    server_dir="C:\Program Files (x86)\Spark1.1.2006.1\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100011520",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark5 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="a11f4c24",
    server_dir="C:\Program Files (x86)\Spark1.1.2006.1\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="460023100010678",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark6 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="851597fa",
    server_dir="C:\Program Files (x86)\Spark1.1.2006.1\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100011518",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark7 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="bd67e9df",
    server_dir="C:\Program Files (x86)\Spark1.1.2006.1\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="460023100010677",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark8 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="ffea8d6b",
    server_dir="C:\Program Files (x86)\Spark1.1.2006.1\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100011519",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    core=_epc_sim,
    ues=[
        _sigspark1,
        _sigspark2,
        _sigspark3,
        _sigspark4,
        _sigspark5,
        _sigspark6,
        _sigspark7,
        _sigspark8,
    ],
    tl_cloud_topology=_tl_cloud_topology,
)
