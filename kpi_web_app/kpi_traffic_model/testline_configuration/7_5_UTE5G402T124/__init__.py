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
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)  # added in taf.meta.5.4
from taf.config.testline.core import (
    EPCSim,
    RealCore4G,
    RealCore,
    RealCore5GDetails,
    AMF,
)
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.pdu import TopYoung, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import TafUeAt, MediaTek, TafUeFastmile
from taf.config.testline import LicenseKeeper
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline.connection_details import (
    SshServiceDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer, TafUeAppServer
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol

# added in taf.meta 5.4
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.hardware_controller import (
    AmiaFanHardwareController,
    GPSPowerHardwareController,
)
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)

__maintainer__ = "Xueqin Deng"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02@internal.nsn.com"
__email__ = "xueqin.deng@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.195", username="vrf3_sg2", password="vrf3@sg2", port="46124"
)

iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.195",
    iperf_path="iperf",
    port=46124,
)
_appserver = AppServer(iperf_details)

# Qualcomm MTP8750 X80
_app_server_1 = TafUeAppServer(
    app_server_name="APP_SERVER",
    address="10.57.191.234",
    user="vrf3_sg2",
    password="vrf3@sg2",
    bind_interface_ip="10.57.191.234",
    expected_prompt="[vrf3_sg2@appserver ~]$",
    ports=[42124, 43124],
)

_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_app_server_1,
    interval=1,
    binary_path="/system/bin/",
    version=2,
)

_data_transfer_ping = TafUeDataTransferProtocol(
    protocol_name="ping", app_server=_app_server_1, interval=1
)

_data_transfer_ftp = TafUeDataTransferProtocol(
    protocol_name="ftp", app_server=_app_server_1, interval=1
)

_mtp = TafUeAt(
    com_port="5",
    serial_number="b3571a7f",
    capabilities=["qualcomm"],
    ue_pc_address="10.57.130.61",
    ue_pc_login="mn5gran",
    ue_pc_password="nokia123@",
    ue_pc_expected_prompt="MN5GRAN@CNHZ5GRAN2740.*$",
    #    ue_expected_prompt='\/ #',
    data_transfer=[_data_transfer_iperf, _data_transfer_ping, _data_transfer_ftp],
    phone_number="+8613100012811",
    ue_pc_port="80",
    imei="004403162098687",
    imsi="262033100012811",
)

# Multi UE X65

# SIGSPARK
_appserver_ip_addr1 = "10.71.207.155"

_spark_appserver_ssh1 = SshServiceDetails(
    addr=_appserver_ip_addr1, username="vrf3_sg2", password="vrf3@sg2"
)

_iperf_details_on_appserver1 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh1,
    network_interface_address=_appserver_ip_addr1,
    iperf_path="iperf",
    port=43124,
)

_spark_host_ssh = SshServiceDetails(
    addr="10.57.147.195", username="spark", password="spark"
)

_licensekeeper = LicenseKeeper(username="HAZ3_SG2", password="HAZ3_SG2")

_IMSI_1 = "262033100001075"
_IMSI_2 = "262033100010731"
_IMSI_3 = "262033100001073"
_IMSI_4 = "262033032995953"
_IMSI_5 = "262033100012811"

_spark_server_dir = "C:/Program Files (x86)/Spark1.1.2011.3/Bin/Spark.exe"

_sigspark_1 = Android(
    ssh_connection_details=_spark_host_ssh,
    serial_number="045091002144002",
    server_dir=_spark_server_dir,
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_1,
    licensekeeper=_licensekeeper,
)

_sigspark_2 = Android(
    ssh_connection_details=_spark_host_ssh,
    serial_number="045091002144002",
    server_dir=_spark_server_dir,
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_2,
    licensekeeper=_licensekeeper,
)

_sigspark_3 = Android(
    ssh_connection_details=_spark_host_ssh,
    serial_number="045091002144002",
    server_dir=_spark_server_dir,
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_3,
    licensekeeper=_licensekeeper,
)

_sigspark_4 = Android(
    ssh_connection_details=_spark_host_ssh,
    serial_number="045091002144002",
    server_dir=_spark_server_dir,
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_4,
    licensekeeper=_licensekeeper,
)

# #5GRU_0 for cloudBTS
_gnb_pdu = TopYoung(addr="10.57.251.234", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.128",
        username="root",
        password="root",
    ),
    pdu_port=_gnb_pdu.pdu_ports[3],
    radio_type="AHLOA",
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129",
        username="root",
        password="root",
    ),
    pdu_port=_gnb_pdu.pdu_ports[4],
    radio_type="AHLOA",
)

# #DU_0 for cloudlBTS
_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(
    addr="192.168.253.20", hardware_type="ABIL", rus=[_ru1, _ru2]
)

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
    hardware_type="ASIK",
)

_airscale = Airscale(common_units=[_common_unit_0])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru1, label="SFP", port_id=2),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=2),
        target=Endpoint(unit=_ru2, label="SFP", port_id=2),
    ),
]

_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2],
    f1_m_ip_addr="10.57.149.130",
    cablinks=_ru_cablinks,
)

# #CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.57.149.130",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.149.129", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.149.130", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.149.130", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.57.149.130",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.149.129", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.57.149.130",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.149.129", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.57.149.130",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.149.129", ip_prefix_length=27),
    ),
)


# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=37574, global_bts_id=37574)

_pdns = [
    PDN(pdp_type=PDPTypes.IP.value, apn="wap1nokiacom"),
    PDN(pdp_type=PDPTypes.IP.value, apn="dxdata3"),
]
_core = RealCore(pdns=_pdns)

# #host
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.90", username="ute", password="ute"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_QC_SA_ASIKL_ABILB1_2xAHLOA"

tl = TestLine(
    test_pc=_test_pc,
    ues=[_sigspark_1, _sigspark_2, _sigspark_3, _sigspark_4, _mtp],
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
    core=_core,
)
