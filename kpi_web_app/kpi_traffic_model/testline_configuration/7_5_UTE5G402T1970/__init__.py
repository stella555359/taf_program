__maintainer__ = "Chen Jian"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05@internal.nsn.com>"
)
__email__ = "jian.1.chen@nokia.com"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import TopYoung, FACOM, HBTE
from taf.config.testline.ue import (
    Qualcomm,
    QualcommUeType,
    Android,
    MediaTek,
    TafUeAndroid,
)
from taf.config.testline.core import EPCSim
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline import LicenseKeeper
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)

from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline.attenuator import AttenuationPort
from taf.config.testline.appserver import AppServer
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.pdn import PDNTafUeAndroidDetails

## common
__all__ = ["tl"]
_CFG_DIR = os.path.dirname(os.path.abspath(__file__))
# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.179", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
# HETE renamed as AHBTE, TopYoung renamed as ATopYoung
_attenuator = AHBTE(
    ip_addr="10.71.208.204",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
)
##epcsim
_epc_sim = EPCSim(
    mme_ip="10.110.227.5",
    mcc="460",
    mnc="2",
    tac="0",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.221.135", username="haijtest", password="Nokia@12345"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)
# 4GRU for RealEnb_1
_ru_enb_1_pdu = HBTE(addr="10.68.87.10", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru_enb_1 = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="usr", password="psswd"
    ),
    pdu_port=_ru_enb_1_pdu.pdu_ports[3],
)

# 4GRU for RealEnb_2
_ru_enb_2_pdu = HBTE(addr="10.68.87.29", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru_enb_2 = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="usr", password="psswd"
    ),
    pdu_port=_ru_enb_2_pdu.pdu_ports[5],
)

# #RealEnb_1
_real_enb_1_pdu = HBTE(addr="10.68.87.13", port_numbers=[3])
_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.208.203", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_1_pdu.pdu_ports[3],
)
_real_enb_1 = Airscale(common_units=[_common_unit_2])
_lte_real_enb_1 = RealEnb(airscale=_real_enb_1, rms=_ru_enb_1)

##5GRU for classicalBTS
_ru_1_pdu = HBTE(addr="10.68.87.8", port_numbers=[1])
_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_1_pdu.pdu_ports[1],
    radio_type="AEQZ",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)
_ru_2_pdu = HBTE(addr="10.68.87.10", port_numbers=[5])
_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_2_pdu.pdu_ports[5],
    radio_type="AHLOA",
)


##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="1.1.1.1")
_gnb_pdu = HBTE(addr="10.68.87.29", port_numbers=[3])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru_1, _ru_2], f1_m_ip_addr="10.71.202.138")

##CU
_cu = CU(
    backhaul_site_oam_ip="10.71.202.138",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.202.138", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.202.138", username="Nemuadmin", password="nemuuser"
    ),
)
##cloud_topology
_tl_cloud_topology = "CLOUD_5G_INVENTORY"

_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="1970", global_bts_id="10295"
)

# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.71.203.100", username="spark", password="spark"
)
_ue_host_ssh_dingli = SshServiceDetails(
    addr="10.71.203.120", username="root", password="123456"
)

_spark_appserver_ssh = SshServiceDetails(
    addr="10.71.207.139", username="vrf3_sg5", password="vrf3@sg5"
)

_iperf_details_on_appserver1 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.71.207.139",
    iperf_path="iperf",
    port=45360,
)

# spark license
_licensekeeper = LicenseKeeper(username="HAZ3_SG5", password="HAZ3_SG5")

_sigspark1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="20c6082f",
    server_dir="C:/Program Files (x86)/Spark1.1.2006.7/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "dingli_pioneer"],
    imsi="262033100013215",
    licensekeeper=_licensekeeper,
)


_sigspark2 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="32960423",
    server_dir="C:/Program Files (x86)/Spark1.1.2006.7/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "dingli_pioneer"],
    imsi="262033031393346",
    licensekeeper=_licensekeeper,
)

_sigspark3 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="3a05bceb",
    server_dir="C:/Program Files (x86)/Spark1.1.2006.7/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "dingli_pioneer"],
    imsi="262033100013214",
    licensekeeper=_licensekeeper,
)

_sigspark4 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="5bad1282",
    server_dir="C:/Program Files (x86)/Spark1.1.2006.7/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "dingli_pioneer"],
    imsi="262033032990226",
    licensekeeper=_licensekeeper,
)

_sigspark5 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="c3bc2c53",
    server_dir="C:/Program Files (x86)/Spark1.1.2006.7/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "dingli_pioneer"],
    imsi="262038001006104",
    licensekeeper=_licensekeeper,
)


_sigspark6 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="f5664561",
    server_dir="C:/Program Files (x86)/Spark1.1.2006.7/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "dingli_pioneer"],
    imsi="262033032996911",
    licensekeeper=_licensekeeper,
)

_sigspark7 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="952c2fd8",
    server_dir="C:/Program Files (x86)/Spark1.1.2006.7/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "dingli_pioneer"],
    imsi="262038001008010",
    licensekeeper=_licensekeeper,
)

_sigspark8 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="10e3b830",
    server_dir="C:/Program Files (x86)/Spark1.1.2006.7/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "dingli_pioneer"],
    imsi="262033100011509",
    licensekeeper=_licensekeeper,
)

_app_server_1 = TafUeAppServer(
    app_server_name="APP_SG5_DXB",
    address="10.71.207.139",
    user="vrf3_sg5",
    password="vrf3@sg5",
    ports=[45083],
)

_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_app_server_1,
    interval=1,
    server_close_delay=50,
)

_pdn1 = PDNTafUeAndroidDetails(
    entryName="mdrb1.nokia.com", apnName="mdrb1.nokia.com", apnType=["DEFAULT"]
)

_android0 = TafUeAndroid(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.23", username="nokia5G", password="noki@123"
    ),
    serial_number="10e66f26",
    capabilities=["REAL_UE", "qualcomm"],
    ue_pc_address="10.71.217.23",
    proxy_mngr_port="9955",
    data_transfer=[_data_transfer_iperf],
    pdns=[_pdn1],
)

_android1 = TafUeAndroid(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.23", username="nokia5G", password="noki@123"
    ),
    serial_number="a41ab9b",
    capabilities=["REAL_UE", "qualcomm"],
    ue_pc_address="10.71.217.23",
    proxy_mngr_port="9955",
    data_transfer=[_data_transfer_iperf],
    pdns=[_pdn1],
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_epc_sim,
    enbs=[_lte_real_enb_1],
    ues=[
        _sigspark1,
        _sigspark2,
        _sigspark3,
        _sigspark4,
        _sigspark5,
        _sigspark6,
        _sigspark7,
        _sigspark8,
        _android0,
        _android1,
    ],
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
)
