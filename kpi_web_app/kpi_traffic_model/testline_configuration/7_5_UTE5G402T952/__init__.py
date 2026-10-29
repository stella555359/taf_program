import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore, RealCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import HBTE
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
)  # added in taf.meta.5.4
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
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.pdn import PDN, PDPTypes

__maintainer__ = "cailanwen"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_08_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_08@internal.nsn.com>"
__email__ = "lanwen.cai@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_pdns = [
    PDN(pdp_type=PDPTypes.IP.value, apn="wap1.nokia.com"),
    PDN(pdp_type=PDPTypes.IP.value, apn="wap2.nokia.com"),
]


# test pc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="***", username="ute", password="ute"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.71.219.237",
    username="cmw_sg8",
    password="cm@8",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.237",
    iperf_path="iperf",
    port=58050,
)

_appserver = AppServer(_iperf_details_on_appserver)

_mtk_host_ssh_231 = SshServiceDetails(
    addr="10.68.86.231", username="nokia5G", password="noki@123"
)

_mtk_host_ssh_204 = SshServiceDetails(
    addr="10.68.86.204", username="nokia5G", password="noki@123"
)

_iperf_details_on_mtk_231 = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh_231,
    network_interface_address="",
    iperf_path="/data/local/tmp/iperf",
    port=58141,
)

_iperf_details_on_mtk_204 = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh_204,
    network_interface_address="",
    iperf_path="/data/local/tmp/iperf",
    port=58142,
)

# CI_Detail_UE_Type='MTK'
_mtk_231 = MediaTek(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.231", username="nokia5G", password="noki@123"
    ),
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    imei="234566345487753",
    imsi="262033100009235",
    apn_url="wap1.nokia.com",
    iperf_details=_iperf_details_on_mtk_231,
    capabilities=["REAL_MTK_UEPC_231", 'SA'],
)

_mtk_204 = MediaTek(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.204", username="nokia5G", password="noki@123"
    ),
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    imei="234567874453349",
    imsi="262038001006239",
    apn_url="wap2.nokia.com",
    iperf_details=_iperf_details_on_mtk_204,
    capabilities=["REAL_MTK_UEPC_204", 'SA'],
)

# 5GRU for classicalBTS RU PB
_ru1_pdu = HBTE(addr="10.68.87.120", port_numbers=[2])

_attenuator = AHBTE(
    ip_addr="10.101.48.124",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
    model="PA-16-16-6-127-0.5-B-S",
)

_attenuator2 = AHBTE(
    ip_addr="10.101.48.126",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    model="PA-16-16-6-127-0.5-B-S",
)

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.129", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AZQF,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator2.attenuator_ports[1],
        _attenuator2.attenuator_ports[2],
        _attenuator2.attenuator_ports[3],
        _attenuator2.attenuator_ports[4],
        _attenuator2.attenuator_ports[5],
        _attenuator2.attenuator_ports[6],
        _attenuator2.attenuator_ports[7],
        _attenuator2.attenuator_ports[8],
    ],
)

_ru2_pdu = HBTE(addr="10.68.87.125", port_numbers=[3])

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.128", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[3],
    radio_type=RadioTypes.AZQD,
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
        _attenuator2.attenuator_ports[9],
        _attenuator2.attenuator_ports[10],
        _attenuator2.attenuator_ports[11],
        _attenuator2.attenuator_ports[12],
    ],
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.68.87.125", port_numbers=[5])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru1, _ru2], f1_m_ip_addr="10.101.48.108")

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.101.48.108",
        routing=RoutingInformation(gateway="10.101.48.97", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.48.108", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.48.108", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.101.48.108",
        routing=RoutingInformation(gateway="10.101.48.97", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.101.48.108",
        routing=RoutingInformation(gateway="10.101.48.97", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.101.48.108",
        routing=RoutingInformation(gateway="10.101.48.97", ip_prefix_length=27),
    ),
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_SA_ASILL_ABIOB1_AZQD_AZQF"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=952, global_bts_id=5952)


tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_classical_bts],
    appserver=_appserver,
    ues=[_mtk_204, _mtk_231],
    core=RealCore(mcc=262, mnc=3),
    attenuators=[_attenuator, _attenuator2],
    tl_cloud_topology=_tl_cloud_topology,
)
