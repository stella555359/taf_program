import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, RealCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import HBTE, FPFH
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import Android
from taf.config.testline.gnb import CU, ClassicalBts
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
)  # added in taf.meta.5.4
from taf.config.testline import RealEnb
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import AppServer
from taf.config.testline import LicenseKeeper
from taf.config.testline.nms import NetAct
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer


__maintainer__ = "Jun xia Zhou"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_8_GMS <I_MN_5G_RAN_IV8_LINE_HZG_5@internal.nsn.com>"
)
__email__ = "junxia.zhou@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_licensekeeper = LicenseKeeper(username="HAZ3_SG8", password="HAZ3_SG8")

_attenuator = AHBTE(
    ip_addr="10.57.239.114",
    port=5000,
    attenuation_port_numbers=[13, 14],
    model="PA-16-16-6-127-0.5-B-S",
)

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.223", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


_appserver_ssh = SshServiceDetails(
    addr="10.57.191.239", username="vrf3_sg8", password="vrf3@sg8", port="58999"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.239",
    iperf_path="iperf",
    port=58099,
)

_appserver = AppServer(_iperf_details_on_appserver)


# module UE spark
_ue_host_ssh = SshServiceDetails(
    addr="10.68.86.14", username="MN5GRAN", password="nokia123@"
)

_spark_appserver_ssh = SshServiceDetails(
    addr="10.57.191.239", username="vrf3_sg8", password="vrf3@sg8", port="58999"
)

_iperf_details_on_appserver_1 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.191.239",
    iperf_path="iperf",
    port=58187,
)

_iperf_details_on_appserver_2 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.191.239",
    iperf_path="iperf",
    port=58188,
)

_iperf_details_on_appserver_3 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.191.239",
    iperf_path="iperf",
    port=58189,
)

_iperf_details_on_appserver_4 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.191.239",
    iperf_path="iperf",
    port=58190,
)

_sigspark1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="021010312243002",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.15/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver_1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="450053100010777",
    licensekeeper=_licensekeeper,
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="021010312243002",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.15/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver_2,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="450053100010779",
    licensekeeper=_licensekeeper,
)

_sigspark3 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="021010312243002",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.15/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver_3,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="450053100010784",
    licensekeeper=_licensekeeper,
)

_sigspark4 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="5ec72a4b",
    server_dir="C:/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_appserver_4,
    capabilities=["qct_dx50"],
    imsi="",
)

# for FastMile CPE 1
_fastmile_appserver_2 = TafUeAppServer(
    app_server_name="APP_SERVER_2",
    address="10.57.173.234",
    user="vrf3_sg8",
    password="vrf3@sg8",
    bind_interface_ip="10.57.173.234",
    expected_prompt="[vrf3_sg8@APPServer-3 ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=[48017, 48427],
)
_fastmile_data_transfer_2 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_2,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1= TafUeFastmile(
    com_port='5',
    ue_pc_address='10.101.47.176',
    root_password='7aba54d2c5cc',
    ue_manage_ip='192.168.1.1',
    serial_number='0123456789ABCDEF',
    data_transfer=[_fastmile_data_transfer_2],
    ue_pc_port=5555,
    version='3.2',
    capabilities=['REAL_FASTMILE_UE2', 'nokia_fastmile'])


# AQVC
_ru_pdu = HBTE(addr="10.101.45.200", port_numbers=[2])

# AQVC
_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0=",
    ),
    # lmp_connection=SshServiceDetails(addr='192.168.100.3', username='root', password='umniedziala'),
    pdu_port=_ru_pdu.pdu_ports[2],
    radio_type=RadioTypes.AEQN,
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
    ],
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.101.51.8", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = FPFH(addr="10.57.176.234", port_numbers=[1])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.101.51.8"
)

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.101.51.8",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.51.1", ip_prefix_length=29),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.51.8", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.51.8", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.101.51.8",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.51.1", ip_prefix_length=29),
    ),
    x2u=NetworkAddress(
        v4="10.101.51.8",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.51.1", ip_prefix_length=29),
    ),
    s1u=NetworkAddress(
        v4="10.101.51.8",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.51.1", ip_prefix_length=29),
    ),
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASOE_3XAQQJ_2XAHPE"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=957, global_bts_id=5957)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    appserver=_appserver,
    ues=[_fastmile_1],
    core=RealCore(mcc=262, mnc=3),
    attenuator=_attenuator,
    tl_cloud_topology=_tl_cloud_topology,
)
