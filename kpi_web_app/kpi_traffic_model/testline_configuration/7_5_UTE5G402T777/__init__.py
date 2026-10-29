import os
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE, FPFH
from taf.config.testline import TopYoung_PDU
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
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.core import (
    EPCSim,
    LTEEmuCore,
    PrismaCore,
    RealCore,
    RealCore4GDetails,
    RealCore5GDetails,
    AMF,
    MME,
)
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.appserver import AppServer
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4

__maintainer__ = "Chen Tong"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_2_GMS <I_MN_5G_RAN_IV4_LINE_HZG_2@internal.nsn.com>"
)
__email__ = "tong.chen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))


# Huawei
_appserver_ssh = SshServiceDetails(
    addr="10.71.219.230", username="iperf", password="39nBTScHWRf3weyBMK0=", port="52777"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.230",
    iperf_path="/usr/bin/iperf",
    port=52777,
)

_Xiaomi_host_ssh = SshServiceDetails(
    addr="10.71.217.186", username="MN5GRAN", password="nokia123@"
)

_Huawei_host_ssh = SshServiceDetails(
    addr="10.71.217.241", username="nokia5G", password="noki@123"
)

_appserver = AppServer(_iperf)

_Huawei = Android(
    ssh_connection_details=_Huawei_host_ssh,
    serial_number="L8K5T19919001465",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei"],
)

_Huawei_1_host_ssh = SshServiceDetails(
    addr="10.71.217.240", username="nokia5G", password="noki@123"
)

_Huawei_1 = Android(
    ssh_connection_details=_Huawei_1_host_ssh,
    serial_number="L8K5T19919001465",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei"],
)

_Spark_host_ssh = SshServiceDetails(
    addr="10.71.217.186", username="nokia5G", password="noki@123"
)

# CI_Detail_UE_Type='Huawei Mate 30 Pro 5G'
_sigspark = Android(
    ssh_connection_details=_Spark_host_ssh,
    serial_number="7TD5T21610004690",
    server_dir="C:/Program Files (x86)/Spark1.1.2006.7/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033100010765",
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_huawei_nr = Android(
    ssh_connection_details=_Spark_host_ssh,
    serial_number="7TD5T21610004690",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python37/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["cell_Mapping: [1]", "REAL_ANDROID_UE", "huawei"],
)


_xiaomi = Android(
    ssh_connection_details=_Xiaomi_host_ssh,
    serial_number="70f5029b",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "XIAOMI"],
)

# #pdn
_pdns = [
    PDN(PDPTypes.IPV4V6.value, "dxdata2"),
]

# #realcore5g  # updated 2020/02/10
_amf_oam_ssh_connection_details = SshServiceDetails(
    addr="10.110.66.198", username="test", password="Nokia456"
)
_n2_address = NetworkAddress(v4="10.0.0.0", v6="100:00::000", vlan_id=1)
_amf = AMF(oam_ssh_connection_details=_amf_oam_ssh_connection_details, n2=_n2_address)
_real_5g_core_details = RealCore5GDetails(amf=_amf)

# #realcore5g
_realcore = RealCore(five_g=_real_5g_core_details, mcc="262", mnc="03", pdns=_pdns)

# Dingli mozu
_ue_host_ssh = SshServiceDetails(
    addr="10.71.206.194", username="root", password="Dinglicom"
)

# CI_Detail_UE_Type='Dingli'
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.230",
    iperf_path="iperf",
    port=52777,
)

_sigspark_1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="ecbb80b4",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100001097",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_2 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="e4881a71",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100001098",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_3 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="41ec00a7",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100001099",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_4 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="330194af",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100001100",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_5 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="4ca1a83c",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100001101",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_6 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="710da4c7",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100001102",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_7 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="e83e187b",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100001103",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_8 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="1247a3af",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100001104",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_9 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="0123456789ABCDEF",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100001105",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark_10 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="293adb1b",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100001107",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

# CI_Detail_UE_Type='MTK'
_mtk_host_ssh = SshServiceDetails(
    addr="10.71.217.186", username="nokia5G", password="noki@123"
)

_mtk = MediaTek(
    ssh_connection_details=_mtk_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    imei="887239942947526",
    imsi="262033100010765",
    apn_url="wap1.nokia.com",
    iperf_details=_iperf,
    capabilities=["REAL_MEDIATEK_UE"],
)


# 5GRU for classicalBTS
_ru_0_pdu = FPFH(addr="10.56.122.101", port_numbers=[6])

_ru_0 = RU(
    #'AZHM'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        port=5,
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.211",
        username="nokia5G",
        password="noki@123",
    ),
    pdu_port=_ru_0_pdu.pdu_ports[6],
    radio_type=RadioTypes.AZHM,
    serial_number="1M213808305",
)

_ru_1_pdu = FPFH(addr="10.56.122.101", port_numbers=[5])

_ru_1 = RU(
    #'AZHM'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.6",
        port=2,
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.213",
        username="nokia5G",
        password="noki@123",
    ),
    pdu_port=_ru_1_pdu.pdu_ports[5],
    radio_type=RadioTypes.AZHM,
    serial_number="1M213808409",
)

_ru_2_pdu = FPFH(addr="10.56.122.101", port_numbers=[4])

_ru_2 = RU(
    #'AZHM'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.10",
        port=5,
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="1.0.0.0",
        username="nokia5G",
        password="noki@123",
    ),
    pdu_port=_ru_2_pdu.pdu_ports[4],
    radio_type=RadioTypes.AZHM,
    serial_number="1M222529293",
)

_ru_3_pdu = FPFH(addr="10.56.122.101", port_numbers=[3])

_ru_3 = RU(
    #'AZHM'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.154",
        port=2,
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.212",
        username="nokia5G",
        password="noki@123",
    ),
    pdu_port=_ru_3_pdu.pdu_ports[3],
    radio_type=RadioTypes.AZHM,
    serial_number="1M213808406",
)

_ru_4_pdu = FPFH(addr="10.56.122.101", port_numbers=[2])

_ru_4 = RU(
    #'AZHM'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.158",
        port=2,
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="1.0.0.0",
        username="nokia5G",
        password="noki@123",
    ),
    pdu_port=_ru_4_pdu.pdu_ports[2],
    radio_type=RadioTypes.AZHM,
    serial_number="1M222529217",
)

_ru_5_pdu = FPFH(addr="10.56.122.101", port_numbers=[1])

_ru_5 = RU(
    #'AZHM'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.162",
        port=2,
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="1.0.0.0",
        username="nokia5G",
        password="noki@123",
    ),
    pdu_port=_ru_5_pdu.pdu_ports[1],
    radio_type=RadioTypes.AZHM,
    serial_number="1M222529100",
)
# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.56.122.102", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru_0, _ru_1, _ru_2, _ru_3, _ru_4, _ru_5],
    f1_m_ip_addr="10.57.225.88",
)

_cu = CU(
    backhaul_site_oam_ip="10.57.225.88",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.225.88", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.225.88", username="Nemuadmin", password="nemuuser"
    ),
)


# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="2000777", global_bts_id="2000777"
)

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.77", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[_classical_bts],
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_realcore,
    ues=[
        _huawei_nr,
    ],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
    test_pcs=[_host],
)
