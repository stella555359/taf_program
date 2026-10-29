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
from taf.config.testline.gnb.du import Cablink, Endpoint
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

__maintainer__ = "Hongli Xu"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_08_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_08@internal.nsn.com>"
__email__ = "hongli.xu@nokia-sbell.com"
# common
__all__ = ["tl"]
_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# for UE huawei_NR
huawei_appserver_ssh = SshServiceDetails(
    addr="10.57.191.239", username="vrf3_sg8", password="vrf3@sg8", port="48320"
)

_iperf_0 = IperfDataTransferDetails(
    ssh_connection_details=huawei_appserver_ssh,
    network_interface_address="10.57.191.239",
    iperf_path="/usr/bin/iperf",
    port="58320",
)

_appserver = AppServer(_iperf_0)
_appserver.iperf_details.port = 58320

_ue0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.191", username="mn5gran", password="nokia123@"
    ),
    serial_number="7TD5T21402015221",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf_0,
    capabilities=["SG8_HONOR30s", "cell_Mapping: [1]", "huawei"],
)

# for UE MTK_lte

MTK_appserver_ssh = SshServiceDetails(
    addr="10.57.191.239", username="vrf3_sg8", password="vrf3@sg8",
)

_iperf_1 = IperfDataTransferDetails(
    ssh_connection_details=MTK_appserver_ssh,
    network_interface_address="10.57.191.239",
    iperf_path="iperf",
    port="48333",
)

_appserver = AppServer(_iperf_1)
# _appserver.iperf_details.port = 48333

_mtk_host_ssh_1 = SshServiceDetails(
    addr="10.71.217.96", username="nokia5G", password="noki@123"
)


_iperf_details_on_mtk_1 = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh_1,
    network_interface_address="",
    iperf_path="/data/local/tmp/iperf",
    port=48334,
)

_mtk_1 = MediaTek(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.96", username="nokia5G", password="noki@123"
    ),
    serial_number="0123456789ABCDEF",
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    imei="123456712345673",
    imsi="262033100009236",
    apn_url="wap1.nokia.com",
    iperf_details=_iperf_details_on_mtk_1,
    capabilities=["REAL_MTK_UEPC_1", "NSA", "mkt_lte"],
)


_ru_pdu = HBTE(addr="10.71.195.185", port_numbers=[3])
_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.10.49",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    pdu_port=_ru_pdu.pdu_ports[3],
    radio_type=RadioTypes.AQQS,
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.71.210.149", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20", hardware_type="ABIP",)

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=2),
        target=Endpoint(unit=_ru, label="SFP", port_id=2),
    ),
]

_gnb_pdu = HBTE(addr="10.71.195.209", port_numbers=[7])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[7],
    hardware_type="ASIM",
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.71.210.149", cablinks=_ru_cablinks
)

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.210.149",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.210.129", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.210.149", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.210.149", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.210.149",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.210.129", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.71.210.149",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.210.129", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.71.210.149",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.210.129", ip_prefix_length=27),
    ),
)


# cloud_topology
# _tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_ASIBL_ABIOB1_AQQS_ENB"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=11627, global_bts_id=1133)

# host
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.166", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_classical_bts],
    # enbs=[_lte_real_enb],
    appserver=_appserver,
    ues=[_ue0, _mtk_1],
    core=RealCore(mcc=262, mnc=3),
    # attenuator=_attenuator,
    # tl_cloud_topology=_tl_cloud_topology,
)
