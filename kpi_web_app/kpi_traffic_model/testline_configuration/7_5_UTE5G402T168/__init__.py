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
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.appserver import AppServer

# added in taf.meta 5.4
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)
from taf.config.testline.attenuator import AttenuationPort, TopYoung, RadioRack
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
    RealCore4G,
    RealCore,
    RealCore5GDetails,
    AMF,
)
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline import TafUeDataTransferProtocol, TafUeAtDataTransferProtocol
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import SshServiceDetails
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.pdu import ATEN
from taf.config.testline.ue import TafUeAt, MediaTek, TafUeFastmile
from taf.config.testline import LicenseKeeper
from taf.config.testline.pdn import PDN, PDPTypes

__maintainer__ = "Xueqin Deng"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02@internal.nsn.com"
__email__ = "xueqin.deng@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.68", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# RealEnb
_real_enb_pdu = HBTE(addr="10.57.249.11", port_numbers=[1, 2])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.211.146",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[2],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# Attenuators
_attenuator = RadioRack(
    ip_addr="10.71.204.165", port=50000, attenuation_port_numbers=range(1, 16)
)

# #5GRU_0 for cloudBTS
_ru_pdu = HBTE(addr="10.57.249.26", port_numbers=[1])

_ru = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.128",
        username="root",
        password="root",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.33.128", username="root", password="root"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
    # radio_type="AHLOB",
    radio_type=RadioTypes.AHLOB.value,
)

# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.195", username="vrf3_sg2", password="vrf3@sg2", port="46168"
)

iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.195",
    iperf_path="iperf",
    port=46168,
)
_appserver = AppServer(iperf_details)

_mtk_host_ssh = SshServiceDetails(
    addr="10.0.176.23", username="mn5gran", password="nokia123@"
)

_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="",
    iperf_path="/usr/bin/iperf",
    port=43168,
)

# MTK
_mtk = MediaTek(
    ssh_connection_details=_mtk_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="C:/tools/MTK/Item.3_NR16.R2.MP.W22.18.p1_MT6298_DONGLE(NLWCG_SAP_R16)_bin/MDDB_MT6298_S00_NR16_R2_MP_W22_18_P1.EDB",
    log_filter="2.Gen98_Default_Standard",
    imei="38174081794214",
    imsi="262033100012814",
    apn_url="dxdata3",
    iperf_details=_iperf_details_on_mtk,
    capabilities=["REAL_MEDIATEK_UE"],
)

# SIGSPARK
_licensekeeper = LicenseKeeper(username="HAZ3_SG2", password="HAZ3_SG2")

_IMSI_0 = "262033100012816"
_IMSI_1 = "262033100012817"
_IMSI_2 = "262033100012815"
_IMSI_3 = "262033100016947"

# Multi UE X65 spark
_appserver_ip_addr1 = "10.71.207.155"

_spark_appserver_ssh1 = SshServiceDetails(
    addr=_appserver_ip_addr1, username="vrf3_sg2", password="vrf3@sg2"
)

_iperf_details_on_appserver1 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh1,
    network_interface_address=_appserver_ip_addr1,
    iperf_path="iperf",
    port=43168,
    ports=[43168, 43169, 43170, 43171, 43172, 43173],
)

_spark_host_ssh = SshServiceDetails(
    addr="10.71.217.5", username="mn5gran", password="nokia123@"
)

_spark_server_dir = "C:/Program Files (x86)/Spark1.1.2011.3/Bin/Spark.exe"

_sigspark_1 = Android(
    ssh_connection_details=_spark_host_ssh,
    serial_number="0420243B2442001",
    server_dir=_spark_server_dir,
    python_path="C:/Users/mn5gran/AppData/Local/Programs/Python/Python312",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_1,
    licensekeeper=_licensekeeper,
)

_sigspark_2 = Android(
    ssh_connection_details=_spark_host_ssh,
    serial_number="0420243B2442001",
    server_dir=_spark_server_dir,
    python_path="C:/Users/mn5gran/AppData/Local/Programs/Python/Python312",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_2,
    licensekeeper=_licensekeeper,
)

_mtp_host_ssh = SshServiceDetails(
    addr="10.71.218.100", username="mn5gran", password="nokia123@"
)

_mtp_spark_server_dir = "C:/Program Files (x86)/Spark1.1.2011.3/Bin/Spark.exe"

_mtpspark = Android(
    ssh_connection_details=_mtp_host_ssh,
    serial_number="8a9bbc9",
    server_dir=_mtp_spark_server_dir,
    python_path="C:/Python38",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_0,
    licensekeeper=_licensekeeper,
)

_m90 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.159", username="mn5gran", password="nokia123@"
    ),
    serial_number="MTK_716_003",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.1/Bin/Spark.exe",
    python_path="C:/Program Files/Python39",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_appserver1,
    imsi=_IMSI_3,
    capabilities=["REAL_ANDROID_UE", "samsung", "huawei_sigspark"],
    licensekeeper=_licensekeeper,
)


# #DU_0 for cloudlBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.71.212.72", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.22")

_du_pdu = HBTE(addr="10.57.241.165", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_du_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.71.212.72")


# #CU
_cu = CU(
    backhaul_site_oam_ip="10.71.212.72",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.212.72", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.212.72", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=168, global_bts_id=168)


_pdns = [
    PDN(pdp_type=PDPTypes.IP.value, apn="dxdata3"),
]
_core = RealCore(pdns=_pdns)


# #cloud_topology------------------------------------------------
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASOE_AHFIB"

tl = TestLine(
    test_pc=_host,
    ues=[_mtpspark, _sigspark_1, _sigspark_2, _m90],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
    core=_core,
    attenuator=_attenuator,
)
