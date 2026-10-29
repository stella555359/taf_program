import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
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
from taf.config.testline.attenuator import AttenuationPort, TopYoung

__maintainer__ = "Caoli Hu"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_1_GMS <I_MN_5G_RAN_IV4_LINE_HZG_1@internal.nsn.com>"
)
__email__ = "caoli.hu@nokia-sbell.com"


## common
# __all__ = ["tl"]
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# Test PC
_host_primary_core = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.4", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_host_secondary_core = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.115", username="ute", password="iW_K#8.ute%A10h0m0ra"
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

# 4GRU for RealEnb
_ru_enb_pdu = PBHBTE(addr="1.1.1.1", port_numbers=[1])

_ru_enb = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="usr", password="psswd"
    ),
    pdu_port=_ru_enb_pdu.pdu_ports[1],
)

##RealEnb
_real_enb_pdu = PBHBTE(addr="1.1.1.1", port_numbers=[4])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[4],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)

##GNB1
##5GRU for TL1111 classicalBTS
_gnb_1_ru_1_pdu = PBHBTE(addr="10.71.197.46", port_numbers=[5])
_gnb_1_ru_2_pdu = PBHBTE(addr="10.71.197.42", port_numbers=[5])
_gnb_1_ru_3_pdu = PBHBTE(addr="10.71.197.48", port_numbers=[5])
_gnb_1_ru_4_pdu = PBHBTE(addr="10.71.197.42", port_numbers=[6])
_gnb_1_ru_5_pdu = PBHBTE(addr="10.71.197.42", port_numbers=[4])
_gnb_1_ru_6_pdu = PBHBTE(addr="10.71.197.42", port_numbers=[2])
_gnb_1_ru_7_pdu = PBHBTE(addr="10.71.197.46", port_numbers=[1])
##_gnb_1_ru_2_pdu = FACOM(addr="10.57.249.15", port_numbers=[2])
##_gnb_1_ru_3_pdu = FACOM(addr="10.57.249.29", port_numbers=[1])

_gnb_1_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_gnb_1_ru_1_pdu.pdu_ports[5],
    radio_type="AEHC",
    serial_number="L1211707926",
)

_gnb_1_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_gnb_1_ru_2_pdu.pdu_ports[5],
    radio_type="AEHC",
    serial_number="L1211707928",
)

_gnb_1_ru_3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_gnb_1_ru_3_pdu.pdu_ports[5],
    radio_type="AEHC",
    serial_number="L1211707936",
)

_gnb_1_ru_4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_gnb_1_ru_4_pdu.pdu_ports[6],
    radio_type="AHFIB",
    serial_number="BL2147V0RGT",
)

_gnb_1_ru_5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_gnb_1_ru_5_pdu.pdu_ports[4],
    radio_type="AHFIB",
    serial_number="BL2147V0RGZ",
)

_gnb_1_ru_6 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_gnb_1_ru_6_pdu.pdu_ports[2],
    radio_type="AHFIB",
    serial_number="BL2147V0RGS",
)

_gnb_1_ru_7 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_gnb_1_ru_7_pdu.pdu_ports[1],
    radio_type="FXEB",
    serial_number="1M174025050",
)

_attenuator = TopYoung(
    ip_addr="1.1.1.1", port=5000, attenuation_port_numbers=[1, 2, 9, 10]
)

##DU for TL1111 classicalBTS
_gnb_1_airscale_cu_lmp_left = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_gnb_1_airscale_cu_lmp_right = SshServiceDetails(
    addr="192.168.255.119", username="toor4nsn", password="oZPS0POrRieRtu"
)

# _gnb_1_airscale_cu_capacity_unit_left = CapacityUnit(addr="6.6.6.6", rus=[_gnb_1_ru_1])
#
# _gnb_1_airscale_cu_capacity_unit_right = CapacityUnit(addr="6.6.6.6", rus=[_gnb_1_ru_2])

_gnb_1_airscale_BBMOD_left_1 = CapacityUnit(
    addr="1.1.1.1",
    rus=[_gnb_1_ru_1, _gnb_1_ru_2, _gnb_1_ru_3, _gnb_1_ru_4, _gnb_1_ru_5, _gnb_1_ru_6],
)
_gnb_1_airscale_BBMOD_left_2 = CapacityUnit(addr="1.1.1.1", rus=[_gnb_1_ru_7])
_gnb_1_airscale_BBMOD_right_1 = CapacityUnit(addr="1.1.1.1", rus=[])


_gnb_1_pdu_left = PBHBTE(addr="10.71.197.45", port_numbers=[1])
_gnb_1_pdu_right = PBHBTE(addr="10.71.197.45", port_numbers=[2])

_gnb_1_airscale_cu_left = CommonUnit(
    lmp_connection=_gnb_1_airscale_cu_lmp_left,
    capacity_units=[
        _gnb_1_airscale_BBMOD_left_1,
        _gnb_1_airscale_BBMOD_left_2,
    ],
    pdu_port=_gnb_1_pdu_left.pdu_ports[1],
)

_gnb_1_airscale_cu_right = CommonUnit(
    lmp_connection=_gnb_1_airscale_cu_lmp_right,
    capacity_units=[_gnb_1_airscale_BBMOD_right_1],
    pdu_port=_gnb_1_pdu_right.pdu_ports[2],
)

_gnb_1_airscale = Airscale(
    common_units=[_gnb_1_airscale_cu_left, _gnb_1_airscale_cu_right]
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
        _gnb_1_ru_7,
    ],
    f1_m_ip_addr="10.71.215.43",
)


##CU for TL1111 classicalBTS
_gnb_1_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.215.43", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.215.43", username="Nemuadmin", password="nemuuser"
    ),
)

## TL1111 classicalBTS
_classical_gnb_1 = ClassicalBts(
    dus=[_gnb_1_du], cu=_gnb_1_cu, instance_id="11094", global_bts_id="11094"
)

# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.71.218.70", username="nokia5G", password="noki@123"
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
    port=51013,
)

_spark_appserver_ssh2 = SshServiceDetails(
    addr="10.71.207.142", username="vrf4_sg1", password="vrf4@sg1", port=51126
)
_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh2,
    network_interface_address="10.71.207.142",
    iperf_path=None,
    port=51011,
)

# CI_Detail_UE_Type='Huawei Honor 30s'
# _sigspark1 = Android(
#     ssh_connection_details=_ue_host_ssh,
#     serial_number="9YS0220103031558",
#     server_dir="C:/Program Files (x86)/Spark1.1.2003.15/Bin/Spark.exe",
#     python_path="C:/Python27",
#     iperf_details=_iperf_details_on_appserver1,
#     capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
#     imsi="460028001006398",
# )

_sigspark1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="9EQUT20903003186",  # '9YS0220103005528',##'L8K5T19919002146',
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python38/python.exe",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["SG4_HONOR30s", "huawei"],
    imsi="460028001006161",
)

_samsung = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="RFCRA1GWA9N",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python38/python.exe",
    service_call_attach="14",
    service_call_detach="14",
    iperf_details=_iperf_details_on_appserver2,
    capabilities=["samsung", "samsung_lte"],
    imsi="310260100010809",
)

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.142",
    username="vrf4_sg1",
    password="vrf4@sg1",
    port=51040,
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.142",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port=51040,
)
_appserver = AppServer(_iperf)
_appserver.iperf_details.port = 51040

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_INVENTORY"


tl = TestLine(
    test_pc=None,
    test_pcs=[_host_primary_core, _host_secondary_core],
    gnbs=[_classical_gnb_1],
    enbs=[_lte_real_enb],
    core=_epc_sim,
    ues=[_sigspark1, _samsung],
    appserver=_appserver,
    attenuator=_attenuator,
    tl_cloud_topology=_tl_cloud_topology,
)
