import os
import yaml
import re
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.core import RealCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import HBTE, TopYoung
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import Android
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import RealEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.attenuator import AttenuationPort
from taf.config.testline.attenuator import TopYoung as TOPYOUNG
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import AppServer
from taf.config.testline import LicenseKeeper

__maintainer__ = "Jianhua Li"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_08_01_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_08_01@internal.nsn.com>"  # TL owner's team
__email__ = "qingqing.1.wang@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]
_licensekeeper = LicenseKeeper(username="HAZ4_SG8", password="HAZ4_SG8")

_cfg_dir = os.path.dirname(os.path.abspath(__file__))


_ue_host_ssh = SshServiceDetails(
    addr="10.71.217.81", username="nokia5G", password="noki@123"
)

_ue_host_ssh_1 = SshServiceDetails(
    addr="10.71.218.118", username="MN5GRAN", password="nokia123@"
)


_spark_appserver_ssh = SshServiceDetails(
    addr="10.57.191.239", username="vrf3_sg8", password="vrf3@sg8", port="48999"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.191.239",
    iperf_path="iperf",
    port=48039,
)

_iperf_details_on_appserver_1 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.191.239",
    iperf_path="iperf",
    port=48038,
)

_appserver = AppServer(_iperf_details_on_appserver)
_appserver.iperf_details.port = 48039

_sigspark = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="55bd4050",
    server_dir="C:/Program Files (x86)/Spark1.1.2001.112/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100010042",
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    licensekeeper=_licensekeeper,
)


_2_sigspark = Android(
    ssh_connection_details=_ue_host_ssh_1,
    serial_number="8f54fc0d",
    server_dir="C:/Program Files (x86)/Spark1.1.2001.112/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver_1,
    imsi="262033100007804",
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    licensekeeper=_licensekeeper,
)


# 5GRU for classicalBTS
_ru_pdu = TopYoung(addr="10.71.195.198", port_numbers=[3])


_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[3],
    radio_type=RadioTypes.UHIE,
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20", hardware_type="ABIO", rus=[_ru])
_gnb_pdu = HBTE(addr="10.71.195.209", port_numbers=[1])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
    hardware_type="ASIB",
)

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru, label="SFP", port_id=1),
    ),
]

_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.71.210.131", cablinks=_ru_cablinks)

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.210.131",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.52.129", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.210.131", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.210.131", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.210.131",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.210.129", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.71.210.131",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.210.129", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.71.210.131",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.210.129", ip_prefix_length=27),
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.71.210.130", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = TopYoung(addr="10.71.195.209", port_numbers=[1])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[1],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIBL_ABIOB1_AQQQ_ENB"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=1149, global_bts_id=51904)

# host
_gnb_testpc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.85", username="ute", password="ute"
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
    test_pcs=[_gnb_testpc],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    appserver=_appserver,
    ues=[_2_sigspark, _sigspark],
    core=RealCore(mcc=262, mnc=3),
    tl_cloud_topology=_tl_cloud_topology,
)
