import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, RealCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import HBTE
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

__maintainer__ = "Melinda Gao"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_8_GMS <I_MN_5G_RAN_IV8_LINE_HZG_5@internal.nsn.com>"
)
__email__ = "melinda.gao@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_licensekeeper = LicenseKeeper(username="HAZ4_SG8", password="HAZ4_SG8")
# AEQZ1
_attenuator1 = AHBTE(
    ip_addr="10.71.204.118",
    port=5000,
    attenuation_port_numbers=[13, 14],
    model="PA-16-16-6-127-0.5-B-S",
)

# AEQZ2
_attenuator2 = AHBTE(
    ip_addr="10.71.204.118",
    port=5000,
    attenuation_port_numbers=[1, 2],
    model="PA-16-16-6-127-0.5-B-S",
)

# AEQZ3
_attenuator3 = AHBTE(
    ip_addr="10.71.210.236",
    port=5000,
    attenuation_port_numbers=[17, 18, 19, 20],
    model="PA-16-16-6-127-0.5-B-S",
)

# AHPB1
_attenuator4 = AHBTE(
    ip_addr="10.71.204.118",
    port=5000,
    attenuation_port_numbers=[1, 3],
    model="PA-16-16-6-127-0.5-B-S",
)

# AHPB2
_attenuator5 = AHBTE(
    ip_addr="10.71.204.118",
    port=5000,
    attenuation_port_numbers=[11, 12],
    model="PA-16-16-6-127-0.5-B-S",
)


# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.20", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# epcsim
_epc_sim = EPCSim(
    mme_ip="10.107.180.5",
    mcc="262",
    mnc="3",
    tac="20200",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.107.178.71", username="test", password="NOKIA123"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)

_mtk_appserver_ssh = SshServiceDetails(
    addr="10.57.162.11",
    username="cmw_sg8",
    password="Bestcm@8",
)

_spark_appserver_ssh = SshServiceDetails(
    addr="10.57.162.11", username="cmw_sg8", password="Bestcm@8", port="58999"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_mtk_appserver_ssh,
    network_interface_address="10.57.162.11",
    iperf_path="iperf",
    port=58099,
)

_iperf_details_on_appserver_spark = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.162.11",
    iperf_path="iperf",
    port=58098,
)

_ue_host_ssh = SshServiceDetails(
    addr="10.71.204.119", username="spark", password="spark"
)

_appserver = AppServer(_iperf_details_on_appserver)
_mtk_host_ssh = SshServiceDetails(
    addr="10.71.218.121", username="MN5GRAN", password="nokia123@"
)

# _mtk_host_ssh_1 = SshServiceDetails(
#     addr="10.71.217.70", username="nokia5G", password="noki@123"
# )
#
# _mtk_host_ssh_2 = SshServiceDetails(
#     addr="10.71.217.96", username="nokia5G", password="noki@123"
# )

_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="",
    iperf_path="/data/local/tmp/iperf",
    port=58098,
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.162.11", username="cmw_sg8", password="Bestcm@8", port="58999"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.11",
    #   iperf_path="/cygdrive/c/iperf",
    iperf_path="/system/bin",
    port="58087",
)

_iperf1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.11",
    #   iperf_path="/cygdrive/c/iperf",
    iperf_path="/system/bin",
    port="58086",
)

# CI_Detail_UE_Type='MTK'
_mtk = MediaTek(
    ssh_connection_details=_mtk_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    imei="887465123457692",
    imsi="262033100001120",
    apn_url="dxdata1",
    iperf_details=_iperf_details_on_mtk,
    capabilities=["REAL_MEDIATEK_UE_907", 'SA'],
    log_filter="2.Gen98_Default_Standard",
    serial_number="0123456789ABCDEF"
)

# UE info need to modify
# CI_Detail_UE_Type='Huawei Mate40'
_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.72", username="nokia5G", password="noki@123"
    ),
    serial_number="H4K0221303000123",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["SG8_HUAWEI", "huawei"],
)

_ue2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.121", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCT10J1KWF",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf1,
    capabilities=["SG8_samsung", "samsung"],
)

_sigspark = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="021010002147007",
    server_dir="C:/Program Files (x86)/Spark1.1.2007.17/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver_spark,
    imsi="262033100010042",
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    licensekeeper=_licensekeeper,
)

# 5GRU for classicalBTS RU PB
# AEQZ1
_ru_pdu1 = HBTE(addr="10.71.195.238", port_numbers=[1])
# AEQZ2
_ru_pdu2 = HBTE(addr="10.71.195.238", port_numbers=[5])
# AEQZ3
_ru_pdu3 = HBTE(addr="10.71.195.238", port_numbers=[4])
# AHPB1
_ru_pdu4 = HBTE(addr="10.71.195.238", port_numbers=[3])
# AHPB2
_ru_pdu5 = HBTE(addr="10.71.195.238", port_numbers=[2])

# AEQZ1
_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    # lmp_connection=SshServiceDetails(addr='192.168.100.3', username='root', password='umniedziala'),
    pdu_port=_ru_pdu1.pdu_ports[1],
    radio_type=RadioTypes.AEQZ,
    attenuation_ports=[
        _attenuator1.attenuator_ports[13],
        _attenuator1.attenuator_ports[14],
    ],
)

# AEQZ2
_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.6",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    # lmp_connection=SshServiceDetails(addr='192.168.100.3', username='root', password='umniedziala'),
    pdu_port=_ru_pdu2.pdu_ports[5],
    radio_type=RadioTypes.AEQZ,
    attenuation_ports=[
        _attenuator2.attenuator_ports[1],
        _attenuator2.attenuator_ports[2],
    ],
)

# AEQZ3
_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.10",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    # lmp_connection=SshServiceDetails(addr='192.168.100.3', username='root', password='umniedziala'),
    pdu_port=_ru_pdu3.pdu_ports[4],
    radio_type=RadioTypes.AEQZ,
    attenuation_ports=[
        _attenuator3.attenuator_ports[17],
        _attenuator3.attenuator_ports[18],
        _attenuator3.attenuator_ports[19],
        _attenuator3.attenuator_ports[20],
    ],
)

# AHPB1
_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.129", username="root", password="root"
    ),
    # lmp_connection=SshServiceDetails(addr='192.168.100.3', username='root', password='umniedziala'),
    pdu_port=_ru_pdu4.pdu_ports[3],
    radio_type=RadioTypes.AHPB,
    attenuation_ports=[
        _attenuator4.attenuator_ports[1],
        _attenuator4.attenuator_ports[3],
    ],
)

# AHPB2
_ru5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.128", username="root", password="root"
    ),
    # lmp_connection=SshServiceDetails(addr='192.168.100.3', username='root', password='umniedziala'),
    pdu_port=_ru_pdu5.pdu_ports[2],
    radio_type=RadioTypes.AHPB,
    attenuation_ports=[
        _attenuator5.attenuator_ports[11],
        _attenuator5.attenuator_ports[12],
    ],
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.71.211.2", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.71.195.238", port_numbers=[1])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale, rus=[_ru1, _ru2, _ru3, _ru4, _ru5], f1_m_ip_addr="10.71.211.2"
)

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.211.2",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.211.1", ip_prefix_length=29),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.211.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.211.2", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.211.2",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.211.1", ip_prefix_length=29),
    ),
    x2u=NetworkAddress(
        v4="10.71.211.2",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.211.1", ip_prefix_length=29),
    ),
    s1u=NetworkAddress(
        v4="10.71.211.2",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.211.1", ip_prefix_length=29),
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.71.211.4", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = HBTE(addr="10.68.87.125", port_numbers=[5])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[5],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb, oam_ip="10.71.204.130", rms=None)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASOE_3XAEQZ_2XAHPB"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=1139, global_bts_id=1123)

# NetAct Gansu ssh_connection info
_NetAct_ssh_connection = SshServiceDetails(
    addr="10.108.248.82",
    username="omc",
    password="Nokia126_",
)

# NetAct Gansu http_connection info
_NetAct_http_connection = HttpConnectionDetails(
    addr="https://gansulbwas.gansu.srnhz.nsn-rdnet.net/",
    username="omc",
    password="Nokia126_",
)

# NetAct
_NetAct = NetAct(
    ssh_connections_info=[_NetAct_ssh_connection],
    https_main_info=_NetAct_http_connection,
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    appserver=_appserver,
    # ues=[_mtk],
    ues=[_ue1, _ue2, _mtk, _sigspark],
    # core=_epc_sim,
    core=RealCore(mcc=262, mnc=3),
    attenuator=[_attenuator1, _attenuator2, _attenuator3, _attenuator4, _attenuator5],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_NetAct,
)
