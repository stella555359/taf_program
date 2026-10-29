import os
import yaml
import re
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import RealCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import HBTE, TopYoung
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import Android
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
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
from taf.config.testline.attenuator import AttenuationPort
from taf.config.testline.attenuator import TopYoung as TOPYOUNG
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import AppServer
from taf.config.testline import LicenseKeeper

__maintainer__ = "Jianhua Li"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_08_01_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_08_01@internal.nsn.com>"  # TL owner's team
__email__ = "jianhua.h.li@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]
_licensekeeper = LicenseKeeper(username="HAZ4_SG8", password="HAZ4_SG8")
_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.87", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.162.11", username="cmw_sg8", password="Bestcm@8", port="58999"
)

_ue_host_ssh = SshServiceDetails(
    addr="10.71.217.59", username="nokia5G", password="noki@123"
)

_ue_host_ssh_1 = SshServiceDetails(
    addr="10.71.217.59", username="nokia5G", password="noki@123"
)


_spark_appserver_ssh = SshServiceDetails(
    addr="10.57.162.11", username="cmw_sg8", password="Bestcm@8", port="58999"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.162.11",
    iperf_path="iperf",
    port=58045,
)

_iperf_details_on_appserver_1 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.162.11",
    iperf_path="iperf",
    port=58046,
)

_appserver = AppServer(_iperf_details_on_appserver)
_appserver.iperf_details.port = 58045

_sigspark = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="52b03d33",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.3/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100010042",
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    licensekeeper=_licensekeeper,
)


_2_sigspark = Android(
    ssh_connection_details=_ue_host_ssh_1,
    serial_number="46cd4453",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.3/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver_1,
    imsi="262033100007804",
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    licensekeeper=_licensekeeper,
)




# 5GRU for classicalBTS
_ru_pdu1 = TopYoung(addr="10.71.195.202", port_numbers=[5])

_ru_pdu2 = TopYoung(addr="10.71.195.202", port_numbers=[4])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.1.2",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu1.pdu_ports[5],
    radio_type=RadioTypes.UHIE,
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu2.pdu_ports[4],
    radio_type=RadioTypes.UHIE,
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.101.52.136", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = TopYoung(addr="10.71.195.206", port_numbers=[1])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru1, _ru2], f1_m_ip_addr="10.71.210.177")

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.210.177",
        routing=RoutingInformation(gateway="10.101.52.129", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.210.177", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.210.177", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.210.177",
        routing=RoutingInformation(gateway="10.101.52.129", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.71.210.177",
        routing=RoutingInformation(gateway="10.101.52.129", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.71.210.177",
        routing=RoutingInformation(gateway="10.101.52.129", ip_prefix_length=27),
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.101.52.137", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = HBTE(addr="10.68.87.36", port_numbers=[4])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[4],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIKL_ABILB1_UHIE"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=1135, global_bts_id=1135)


tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    appserver=_appserver,
    core=RealCore(mcc=262, mnc=3),
    ues=[_sigspark, _2_sigspark],
    tl_cloud_topology=_tl_cloud_topology,
)
