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
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import AppServer

__maintainer__ = "Jianhua Li"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_08_01_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_08_01@internal.nsn.com>"  # TL owner's team
__email__ = "jianhua.h.li@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]


_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.160", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_mtk_appserver_ssh = SshServiceDetails(
    addr="10.57.162.11",
    username="cmw_sg8",
    password="Bestcm@8",
)
 
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_mtk_appserver_ssh,
    network_interface_address="10.57.162.11",
    iperf_path="iperf",
    port=58077,
)

_appserver = AppServer(_iperf_details_on_appserver)
 
_mtk_host_ssh = SshServiceDetails(
    addr="10.71.217.56", username="nokia5G", password="noki@123"
)

_mtk_host_ssh_1 = SshServiceDetails(
    addr="10.71.218.68", username="nokia5G", password="noki@123"
)
 
_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="",
    iperf_path="/data/local/tmp/iperf",
    port=58078, 
)

_iperf_details_on_mtk_1 = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh_1,
    network_interface_address="",
    iperf_path="/data/local/tmp/iperf",
    port=58079,
)
 
# CI_Detail_UE_Type='MTK'
_mtk = MediaTek(
    ssh_connection_details=_mtk_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    imei="887228944947360",
    imsi="262033100009229",
    apn_url="stdata1",
    iperf_details=_iperf_details_on_mtk,
    capabilities=["REAL_MEDIATEK_UE"],
)

_mtk_1 = MediaTek(
    ssh_connection_details=_mtk_host_ssh_1,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    imei="234533456764339",
    imsi="262033100004091",
    apn_url="wap2.nokia.com",
    iperf_details=_iperf_details_on_mtk_1,
    capabilities=["REAL_MEDIATEK_UE"],
)

# 5GRU for classicalBTS
_ru_pdu = TopYoung(addr="10.71.195.196", port_numbers=[6])


_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[6],
    radio_type=RadioTypes.UHIE,
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.71.210.109", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.71.195.187", port_numbers=[5])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.71.210.109")

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.210.109",
        routing=RoutingInformation(gateway="10.71.210.97", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.210.109", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.210.109", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.210.109",
        routing=RoutingInformation(gateway="10.71.210.97", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.71.210.109",
        routing=RoutingInformation(gateway="10.71.210.97", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.71.210.109",
        routing=RoutingInformation(gateway="10.71.210.97", ip_prefix_length=27),
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
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIKL_ABILB1_UHIE"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=10553, global_bts_id=10553)


tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    appserver=_appserver,
    ues=[_mtk, _mtk_1],
    core=RealCore(mcc=262, mnc=3),
    tl_cloud_topology=_tl_cloud_topology,
)
