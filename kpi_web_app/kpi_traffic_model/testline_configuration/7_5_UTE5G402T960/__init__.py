import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.core import EPCSim, RealCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import HBTE, FPFH, TopYoung
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
#from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
#from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import AppServer
from taf.config.testline import LicenseKeeper
from taf.config.testline.nms import NetAct

__maintainer__ = "Jessy"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_8_GMS <I_MN_5G_RAN_IV8_LINE_HZG_5@internal.nsn.com>"
)
__email__ = "jiangjing.lin@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_licensekeeper = LicenseKeeper(username="HAZ4_SG8", password="HAZ4_SG8")
# _licensekeeper = LicenseKeeper(username="jie-jessy.li@nokia-sbell.com", password="nokia123")
# AQQA
_attenuator1 = AHBTE(
    ip_addr="10.71.204.5",
    port=5000,
    attenuation_port_numbers=[9,10,11,12,13,14,15,16],
    model="PA-16-16-6-127-0.5-B-S",
)


_appserver_ssh = SshServiceDetails(
    addr="10.71.219.237", username="cmw_sg8", password="cm@8", port="58999"
)


_iperf1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.237",
    #   iperf_path="/cygdrive/c/iperf",
    iperf_path="/usr/bin",
    port="58091",
)


_iperf2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.237",
    #   iperf_path="/cygdrive/c/iperf",
    iperf_path="/usr/bin",
    port="58092",
)


_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.237",
    iperf_path="iperf",
    port=58099,
)

_appserver = AppServer(_iperf_details_on_appserver)




# module UE spark
_ue_host_ssh = SshServiceDetails(
    addr="10.71.204.36", username="spark", password="spark"
)

_spark_appserver_ssh = SshServiceDetails(
    addr="10.71.219.237", username="cmw_sg8", password="cm@8", port="58999"
)

_iperf_details_on_appserver_1 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.71.219.237",
    iperf_path="iperf",
    port=58093,
)

_iperf_details_on_appserver_2 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.71.219.237",
    iperf_path="iperf",
    port=58094,
)

_iperf_details_on_appserver_3 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.71.219.237",
    iperf_path="iperf",
    port=58095,
)

_iperf_details_on_appserver_4 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.71.219.237",
    iperf_path="iperf",
    port=58096,
)

_sigspark1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="021010312243001",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver_1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033100012786",
    licensekeeper=_licensekeeper,
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="021010312243001",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver_2,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033100007822",
    licensekeeper=_licensekeeper,
)

_sigspark3 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="021010312243001",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver_3,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033100007789",
    licensekeeper=_licensekeeper,
)

_sigspark4 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="021010312243001",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver_4,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033100012787",
    licensekeeper=_licensekeeper,
)

# 5GRU for classicalBTS RU PB
_ru_pdu1 = FPFH(addr="10.71.195.181", port_numbers=[4])


# AHFII
_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    # lmp_connection=SshServiceDetails(addr='192.168.100.3', username='root', password='umniedziala'),
    pdu_port=_ru_pdu1.pdu_ports[4],
    radio_type=RadioTypes.AQQA,
    attenuation_ports=[
        _attenuator1.attenuator_ports[9],
        _attenuator1.attenuator_ports[10],        
        _attenuator1.attenuator_ports[11],
        _attenuator1.attenuator_ports[12],        
        _attenuator1.attenuator_ports[13],
        _attenuator1.attenuator_ports[14],        
        _attenuator1.attenuator_ports[15],
        _attenuator1.attenuator_ports[16],        
    ],
)

_ru_pdu2 = FPFH(addr="10.71.195.182", port_numbers=[4])


# AHFII
_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    # lmp_connection=SshServiceDetails(addr='192.168.100.3', username='root', password='umniedziala'),
    pdu_port=_ru_pdu2.pdu_ports[4],
    radio_type=RadioTypes.AEQZ,
    attenuation_ports=[
        _attenuator1.attenuator_ports[9],
        _attenuator1.attenuator_ports[10],        
        _attenuator1.attenuator_ports[11],
        _attenuator1.attenuator_ports[12],        
        _attenuator1.attenuator_ports[13],
        _attenuator1.attenuator_ports[14],        
        _attenuator1.attenuator_ports[15],
        _attenuator1.attenuator_ports[16],        
    ],
)

_ru3_pdu = HBTE(addr="10.71.195.181", port_numbers=[2])

# AHFII
_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.129", username="serviceuser", password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru3_pdu.pdu_ports[2],
    radio_type=RadioTypes.AZQF,
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIO",
)
_gnb_pdu = HBTE(addr="10.71.195.187", port_numbers=[8])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[8],
    hardware_type="ASIL",
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale, rus=[_ru1, _ru2, _ru3,], f1_m_ip_addr="10.71.210.113"
)

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.210.113",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.210.97", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.210.113", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.210.113", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.210.113",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.210.97", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.71.210.113",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.210.97", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.71.210.113",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.210.97", ip_prefix_length=27),
    ),
)

# RealEnb
# _lmp_connection_enb = SshServiceDetails(
#     addr="10.101.48.99", username="toor4nsn", password="oZPS0POrRieRtu"
# )
# _enb_pdu = HBTE(addr="10.68.87.125", port_numbers=[5])
# _common_unit_1 = CommonUnit(
#     lmp_connection=_lmp_connection_enb,
#     capacity_units=[],
#     pdu_port=_enb_pdu.pdu_ports[5],
# )
# _real_enb = Airscale(common_units=[_common_unit_1])
# _lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_SA_ASILL_ABIOB1_3xAHFII"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=960, global_bts_id=5960)

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

# host
_gnb_testpc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.217.63", username="ute", password="ute"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

tl = TestLine(
    test_pc=_gnb_testpc,
    gnbs=[_classical_bts],
    # enbs=[_lte_real_enb],
    appserver=_appserver,
    ues=[_sigspark1, _sigspark2, _sigspark3, _sigspark4],
    # core=_epc_sim,
    core=RealCore(mcc=262, mnc=3),
    attenuator=[_attenuator1],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_NetAct,
)
