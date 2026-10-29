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

__maintainer__ = "Bi Jiajian"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG2"
__email__ = "jiajian.bi@nokia-sbell.com"

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.163", username="ute", password="iW_K#8.ute%A10h0m0ra"
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
_real_enb_pdu = FACOM(addr="10.57.246.207", port_numbers=[1])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.152.126", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

##5GRU for classical BTS
_ru_pdu = FACOM(addr="10.57.246.203", port_numbers=[1])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="user", password="pass"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
)


##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_pdu = FACOM(addr="10.57.246.207", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.57.131.106")

##CU
_cu = CU(
    backhaul_site_oam_ip="10.57.131.106",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.131.106", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.131.106", username="Nemuadmin", password="nemuuser"
    ),
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id="1", global_bts_id="24")

##HBTE_MCS
_hbte = HBTE(
    ip_addr="10.57.152.124",
    port="5000",
    mcs_port_numbers=[1],
    model="PPSAM-64X16-2.3-3.8-90-0.5-360-1-A",
)

# SIGSPARK
_ue_host1_ssh = SshServiceDetails(
    addr="10.57.248.244", username="spark", password="spark"
)

_ue_host2_ssh = SshServiceDetails(
    addr="10.57.248.242", username="spark", password="spark"
)

_spark_appserver_ssh = SshServiceDetails(
    addr="10.57.163.35", username="cmw_sg2", password="12345678"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.163.35",
    iperf_path="iperf",
    port=52228,
)

_sigspark1 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="5c253f7c",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.4/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032995949",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="79e33f87",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.4/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032995951",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark3 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="915f1dec",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.4/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032995946",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark4 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="924467fe",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.4/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032995952",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark5 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="ae5cbe0c",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.4/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032995947",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark6 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="5b269752",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.4/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032995953",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark7 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="c3831ed0",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.4/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032995950",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark8 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="c86177ef",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.4/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032995948",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark9 = Android(
    ssh_connection_details=_ue_host2_ssh,
    serial_number="52cb1c66",
    server_dir="C:/Program Files (x86)/Spark1.1.1996.15/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100004129",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark10 = Android(
    ssh_connection_details=_ue_host2_ssh,
    serial_number="248084ff",
    server_dir="C:/Program Files (x86)/Spark1.1.1996.15/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100004131",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark11 = Android(
    ssh_connection_details=_ue_host2_ssh,
    serial_number="b0d223cd",
    server_dir="C:/Program Files (x86)/Spark1.1.1996.15/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100004133",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark12 = Android(
    ssh_connection_details=_ue_host2_ssh,
    serial_number="5eb6afcc",
    server_dir="C:/Program Files (x86)/Spark1.1.1996.15/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100004134",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark13 = Android(
    ssh_connection_details=_ue_host2_ssh,
    serial_number="7cc1bde4",
    server_dir="C:/Program Files (x86)/Spark1.1.1996.15/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100004132",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark14 = Android(
    ssh_connection_details=_ue_host2_ssh,
    serial_number="8e822892",
    server_dir="C:/Program Files (x86)/Spark1.1.1996.15/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100004135",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark15 = Android(
    ssh_connection_details=_ue_host2_ssh,
    serial_number="30d888ba",
    server_dir="C:/Program Files (x86)/Spark1.1.1996.15/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100004130",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark16 = Android(
    ssh_connection_details=_ue_host2_ssh,
    serial_number="516eb97b",
    server_dir="C:/Program Files (x86)/Spark1.1.1996.15/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100004136",
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
        _sigspark3,
        _sigspark4,
        _sigspark5,
        _sigspark7,
        _sigspark8,
        _sigspark2,
        _sigspark6,
        _sigspark9,
        _sigspark10,
        _sigspark11,
        _sigspark12,
        _sigspark13,
        _sigspark14,
        _sigspark15,
        _sigspark16,
    ],
    tl_cloud_topology=_tl_cloud_topology,
)
