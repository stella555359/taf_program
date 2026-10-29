import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.pdu import TopYoung
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import FACOM
from taf.config.testline.pdu import HBTE as PBHBTE
from taf.config.testline.ue import Prisma, MediaTek
from taf.config.testline.core import EPCSim, RealCore4G
from taf.config.testline.ue import Android
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline.connection_details import (
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer
from taf.config.testline import LicenseKeeper
from taf.config.testline.attenuator import AttenuationPort

__maintainer__ = "Ge Gao"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_1_GMS <I_MN_5G_RAN_IV4_LINE_HZG_1@internal.nsn.com>"
)
__email__ = "ge.gao@nokia-sbell.com"


## common
# __all__ = ["tl"]
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# Test PC
_host_primary_core = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.122", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_host_secondary_core = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.121", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##Real EPC is used. epcsim is here only as a backup solution.
_epc_sim = EPCSim(
    mme_ip="10.108.221.70",
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

##GNB1
##5GRU for TL1129 classicalBTS
_gnb_1_ru_1_pdu = TopYoung(addr="10.71.197.52", port_numbers=[4])
_gnb_1_ru_2_pdu = PBHBTE(addr="10.71.197.38", port_numbers=[6])
_gnb_1_ru_3_pdu = TopYoung(addr="10.71.197.52", port_numbers=[3])
_gnb_1_ru_4_pdu = PBHBTE(addr="10.71.197.45", port_numbers=[4])
_gnb_1_ru_5_pdu = PBHBTE(addr="10.71.197.45", port_numbers=[5])
_gnb_1_ru_6_pdu = PBHBTE(addr="10.71.197.39", port_numbers=[2])

_gnb_1_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_gnb_1_ru_1_pdu.pdu_ports[4],
    radio_type="AENB",
    serial_number="1M210806749",
)

_gnb_1_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_gnb_1_ru_2_pdu.pdu_ports[6],
    radio_type="AENB",
    serial_number="1M212300138",
)

_gnb_1_ru_3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_gnb_1_ru_3_pdu.pdu_ports[3],
    radio_type="AENB",
    serial_number="1M214106731",
)

_gnb_1_ru_4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_gnb_1_ru_4_pdu.pdu_ports[4],
    radio_type="AHIB",
    serial_number="AH193502891",
)

_gnb_1_ru_5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_gnb_1_ru_5_pdu.pdu_ports[5],
    radio_type="AHIB",
    serial_number="EA174610761",
)

_gnb_1_ru_6 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_gnb_1_ru_6_pdu.pdu_ports[2],
    radio_type="AHIB",
    serial_number="EA174610754",
)


##DU for TL1129 classicalBTS
_gnb_1_airscale_cu_lmp_left = SshServiceDetails(
    addr="192.168.255.119", username="toor4nsn", password="oZPS0POrRieRtu"
)

_gnb_1_airscale_cu_lmp_right = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

# _gnb_1_airscale_cu_capacity_unit_left = CapacityUnit(addr="6.6.6.6", rus=[_gnb_1_ru_1])
#
# _gnb_1_airscale_cu_capacity_unit_right = CapacityUnit(addr="6.6.6.6", rus=[_gnb_1_ru_2])

_gnb_1_airscale_BBMOD_right_1 = CapacityUnit(addr="1.1.1.1", rus=[_gnb_1_ru_1])
_gnb_1_airscale_BBMOD_right_2 = CapacityUnit(addr="1.1.1.1", rus=[_gnb_1_ru_2])
_gnb_1_airscale_BBMOD_right_3 = CapacityUnit(addr="1.1.1.1", rus=[_gnb_1_ru_3])
_gnb_1_airscale_BBMOD_right_4 = CapacityUnit(addr="1.1.1.1", rus=[_gnb_1_ru_4])
_gnb_1_airscale_BBMOD_right_5 = CapacityUnit(addr="1.1.1.1", rus=[_gnb_1_ru_5])
_gnb_1_airscale_BBMOD_right_6 = CapacityUnit(addr="1.1.1.1", rus=[_gnb_1_ru_6])
_gnb_1_airscale_BBMOD_left_1 = CapacityUnit(addr="1.1.1.1", rus=[])


_gnb_1_pdu_left = PBHBTE(addr="10.71.197.45", port_numbers=[1])
_gnb_1_pdu_right = PBHBTE(addr="10.71.197.45", port_numbers=[2])

_gnb_1_airscale_cu_left = CommonUnit(
    lmp_connection=_gnb_1_airscale_cu_lmp_left,
    capacity_units=[_gnb_1_airscale_BBMOD_left_1],
    pdu_port=_gnb_1_pdu_left.pdu_ports[1],
)

_gnb_1_airscale_cu_right = CommonUnit(
    lmp_connection=_gnb_1_airscale_cu_lmp_right,
    capacity_units=[
        _gnb_1_airscale_BBMOD_right_1,
        _gnb_1_airscale_BBMOD_right_2,
        _gnb_1_airscale_BBMOD_right_3,
        _gnb_1_airscale_BBMOD_right_4,
        _gnb_1_airscale_BBMOD_right_5,
        _gnb_1_airscale_BBMOD_right_6,
    ],
    pdu_port=_gnb_1_pdu_right.pdu_ports[2],
)

_gnb_1_airscale = Airscale(
    common_units=[_gnb_1_airscale_cu_right, _gnb_1_airscale_cu_left]
)

_gnb_1_du = DU(
    airscale=_gnb_1_airscale,
    rus=[
        _gnb_1_ru_1,
        _gnb_1_ru_2,
        _gnb_1_ru_3,
        _gnb_1_ru_4,
        _gnb_1_ru_5,
        _gnb_1_ru_6,
    ],
    f1_m_ip_addr="10.71.215.46",
)


##CU for TL1129 classicalBTS
_gnb_1_cu = CU(
    backhaul_site_oam_ip="10.71.215.46",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.215.46", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.215.46", username="Nemuadmin", password="nemuuser"
    ),
)

## TL1129 classicalBTS
_classical_gnb_1 = ClassicalBts(
    dus=[_gnb_1_du], cu=_gnb_1_cu, instance_id="11096", global_bts_id="11096"
)

# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.71.217.133", username="nokia5G", password="noki@123"
)

_spark_appserver_ssh1 = SshServiceDetails(
    # addr="10.57.163.50", username="nokia", password="nokia123"
    addr="10.71.207.142",
    username="vrf4_sg1",
    password="vrf4@sg1",
)
_iperf_details_on_appserver1 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh1,
    network_interface_address="10.71.207.142",
    iperf_path="iperf",
    port=51014,
)

_appserver_ssh = SshServiceDetails(
    addr="10.71.217.133", username="nokia5G", password="noki@123"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.142",
    iperf_path="/data/local/tmp/iperf",
    port=51126,
)

_appserver = AppServer(_iperf_details_on_appserver)

_spark_appserver_ssh2 = SshServiceDetails(
    addr="10.71.207.142", username="vrf4_sg1", password="vrf4@sg1", port=51126
)
_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh2,
    network_interface_address="10.71.207.142",
    iperf_path=None,
    port=51015,
)

# XiaoMi 12
_licensekeeper = LicenseKeeper(username="HAZ4_SG1", password="HAZ4_SG1")
_sigspark1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="e5ab5da0",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python38",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "GuangHeTong", "huawei_sigspark"],
    imsi="460023100010696",
    licensekeeper=_licensekeeper,
)

# Samsung S21
_samsung = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="RFCR40P2NVX",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python38/python.exe",
    service_call_attach="14",
    service_call_detach="14",
    iperf_details=_iperf_details_on_appserver2,
    capabilities=["samsung", "samsung_lte"],
    imsi="310260100010215",
)
# _sigspark2 = Android(
#     ssh_connection_details=_ue_host_ssh,
#     serial_number="R3CNC0DF2SN",
#     server_dir="/cygdrive/c/pyro_server",
#     python_path="C:/Python27",
#     iperf_details=_iperf_details_on_appserver1,
#     capabilities=["REAL_ANDROID_UE", "samsung"],
#     imsi="460028001006398",
# )

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_INVENTORY"


tl = TestLine(
    test_pc=None,
    test_pcs=[_host_primary_core, _host_secondary_core],
    gnbs=[_classical_gnb_1],
    # enbs=[_lte_real_enb],
    core=_epc_sim,
    ues=[_sigspark1, _samsung],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
)
