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
from taf.config.testline.ue import TafUeAt
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
        addr="10.57.159.21", username="ute", password="iW_K#8.ute%A10h0m0ra"
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
        addr="172.16.37.128",
        username="root",
        password="root",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.37.128", username="root", password="root"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
    # radio_type="AHLOB",
    radio_type=RadioTypes.AHLOB.value,
)

# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.195", username="vrf3_sg2", password="vrf3@sg2", port="46129"
)

iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.195",
    iperf_path="iperf",
    port=46129,
)
_appserver = AppServer(iperf_details)

# Multi UE X65

# SIGSPARK
_appserver_ip_addr1 = "10.57.191.195"

_spark_appserver_ssh1 = SshServiceDetails(
    addr=_appserver_ip_addr1, username="vrf3_sg2", password="vrf3@sg2"
)

_iperf_details_on_appserver1 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh1,
    network_interface_address=_appserver_ip_addr1,
    iperf_path="iperf",
    port=43129,
)

_ue_host_ssh = SshServiceDetails(
    addr="10.71.204.166", username="spark", password="spark"
)

_licensekeeper = LicenseKeeper(username="HAZ3_SG2", password="HAZ3_SG2")

_IMSI_1 = "001013100008831"
_IMSI_2 = "001013001006024"
_IMSI_3 = "001013100008834"
_IMSI_4 = "001013100008832"
_IMSI_5 = "001013100008835"
_IMSI_6 = "001013001006204"
_IMSI_7 = "001013032995982"
_IMSI_8 = "001013100008833"

_spark_server_dir = "C:/Program Files (x86)/Spark1.1.2009.45/Bin/Spark.exe"

_sigspark_1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="021010322239003",
    server_dir=_spark_server_dir,
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_1,
    licensekeeper=_licensekeeper,
)

_sigspark_2 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="021010322239003",
    server_dir=_spark_server_dir,
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_2,
    licensekeeper=_licensekeeper,
)

_sigspark_3 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="021010322239003",
    server_dir=_spark_server_dir,
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_3,
    licensekeeper=_licensekeeper,
)

_sigspark_4 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="021010322239003",
    server_dir=_spark_server_dir,
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_4,
    licensekeeper=_licensekeeper,
)

_sigspark_5 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="021010322239003",
    server_dir=_spark_server_dir,
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_5,
    licensekeeper=_licensekeeper,
)

_sigspark_6 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="021010322239003",
    server_dir=_spark_server_dir,
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_6,
    licensekeeper=_licensekeeper,
)

_sigspark_7 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="021010322239003",
    server_dir=_spark_server_dir,
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_7,
    licensekeeper=_licensekeeper,
)

_sigspark_8 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="021010322239003",
    server_dir=_spark_server_dir,
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_8,
    licensekeeper=_licensekeeper,
)
# #DU_0 for cloudlBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.71.211.147", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.22")

_du_pdu = HBTE(addr="10.57.241.165", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_du_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.71.211.147")


# #CU
_cu = CU(
    backhaul_site_oam_ip="10.71.211.147",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.211.147", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.211.147", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=129, global_bts_id=129)


_pdns = [
    PDN(pdp_type=PDPTypes.IP.value, apn="dxdata1"),
    PDN(pdp_type=PDPTypes.IP.value, apn="mdrbnokiacom"),
]
_core = RealCore(pdns=_pdns)


# #cloud_topology------------------------------------------------
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIB_ABIO_AHLOB"

tl = TestLine(
    test_pc=_host,
    ues=[
        _sigspark_1,
        _sigspark_2,
        _sigspark_3,
        _sigspark_4,
        _sigspark_5,
        _sigspark_6,
        _sigspark_7,
        _sigspark_8,
    ],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
    core=_core,
    attenuator=_attenuator,
)
