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
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.ue import (
    TafUeFastmile,
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
from taf.config.testline.appserver import AppServer, TafUeAppServer

__maintainer__ = "Wang Ming"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_2_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "lu.1.yu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.45", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# epcsim
_epc_sim = EPCSim(
    mme_ip="3.3.3.3",
    mcc=262,
    mnc=3,
    tac=61,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.45", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    dir_path="/opt/iphy/latest/",
    cfg_filename="eNB_WMP_new.cfg",
)

# PA

# 5GRU for classicalBTS
_ru_pdu = FACOM(addr="10.57.172.159", port_numbers=[2])
_ru1_pdu = FACOM(addr="10.57.172.156", port_numbers=[6])
_ru2_pdu = FACOM(addr="10.57.172.156", port_numbers=[5])
_ru = RU(
    #'AVQC'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[2],
)
_ru1 = RU(
    #'AVQC'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[6],
)
_ru2 = RU(
    #'AVQC'
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
    addr="10.57.224.131", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.57.172.158", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru, _ru1, _ru2], f1_m_ip_addr="10.57.224.131")

_cu = CU(
    backhaul_site_oam_ip="10.57.224.131",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.224.131", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.224.131", username="Nemuadmin", password="nemuuser"
    ),
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id="792", global_bts_id="792")

_ue_host_ssh = SshServiceDetails(
    addr="10.57.156.215", username="spark", password="spark"
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.244", username="vrf4_sg2", password="Vrf4@sg2_123456"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.244",
    iperf_path="/usr/bin/iperf",
    port=52792,
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
    ssh_connection_details=_ue_host_ssh,
    serial_number="8800df0f",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.45\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100017612",
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_2 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="8800df0f",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.45\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100017613",
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_3 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="8800df0f",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.45\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100017614",
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_4 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="8800df0f",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.45\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100017615",
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_5 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="8800df0f",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.45\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100017616",
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_6 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="8800df0f",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.45\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100017617",
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_7 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="8800df0f",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.45\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100017618",
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)
_sigspark_8 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="8800df0f",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.45\Bin\Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    imsi="262033100017619",
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.244",
    user="vrf4_sg2",
    password="Vrf4@sg2_123456",
    bind_interface_ip="10.57.191.244",
    expected_prompt="[vrf4_sg2@appserver ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=[52792, 52793],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="/usr/bin/iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    ue_pc_address="10.57.195.45",
    root_password="29fab2622c3b",
    ue_manage_ip="10.57.156.216",
    serial_number="LPL221400546",
    data_transfer=[_fastmile_data_transfer_1],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
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
        _fastmile_1,
    ],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
    mcses=_hbte,
)
# compatibility workaround
