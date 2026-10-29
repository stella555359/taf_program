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

__maintainer__ = "Melinda Gao"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_08_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_08@internal.nsn.com>"
__email__ = "xu.3.liu@nokia-sbell.com"
# common
__all__ = ["tl"]
_cfg_dir = os.path.dirname(os.path.abspath(__file__))
_attenuator = AHBTE(
    ip_addr="10.101.40.165",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4],
    model="PA-16-16-6-127-0.5-B-S",
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.239", username="vrf3_sg8", password="vrf3@sg8", port="48999"
)
_iperf_1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.239",
    iperf_path="/usr/bin/iperf",
    port="48330",
)
_iperf_2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.239",
    iperf_path="/usr/bin/iperf",
    port="48331",
)
_appserver = AppServer(_iperf_1)
_appserver.iperf_details.port = 48332


# CI_Detail_UE_Type='Huawei Honor 30s'
_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.28", username="nokia5G", password="noki@123"
    ),
    serial_number="H4K0221303000123",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf_1,
    capabilities=["SG8_HONOR30s", "cell_Mapping: [1]", "huawei"],
)
_ue2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.43", username="nokia5G", password="noki@123"
    ),
    serial_number="PLG5T20C01007859",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf_2,
    capabilities=["SG8_HONOR30s", "cell_Mapping: [2]", "huawei"],
)

# for UE MTK_lte
MTK_appserver_ssh = SshServiceDetails(
    addr="10.57.191.239", username="vrf3_sg8", password="vrf3@sg8",
)

_iperf_MTK = IperfDataTransferDetails(
    ssh_connection_details=MTK_appserver_ssh,
    network_interface_address="10.57.191.239",
    iperf_path="iperf",
    port="48335",
)

_appserver = AppServer(_iperf_MTK)

_mtk_host_ssh = SshServiceDetails(
    addr="10.68.86.41", username="mn5gran", password="nokia123@"
)

_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="",
    iperf_path="/data/local/tmp/iperf",
    port=48336,
)

_mtk = MediaTek(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.41", username="mn5gran", password="nokia123@"
    ),
    serial_number="0123456789ABCDEF",
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    imei="678944553240235",
    imsi="262033100004093",
    apn_url="wap1.nokia.com",
    iperf_details=_iperf_details_on_mtk,
    capabilities=["REAL_MTK_UEPC_1", "NSA", "mkt_lte"],
)


_ru_pdu = HBTE(addr="10.101.45.194", port_numbers=[2])
_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.10.49",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    pdu_port=_ru_pdu.pdu_ports[2],
    radio_type=RadioTypes.AQQS,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.101.51.7", username="toor4nsn", password="oZPS0POrRieRtu"
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

_gnb_pdu = HBTE(addr="10.101.45.196", port_numbers=[6])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[6],
    hardware_type="ASIM",
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.101.51.7", cablinks=_ru_cablinks
)

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.101.51.7",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.51.1", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.51.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.51.7", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.101.51.7",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.51.1", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.101.51.7",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.51.1", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.101.51.7",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.51.1", ip_prefix_length=27),
    ),
)


# cloud_topology
#_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_ASIBL_ABIOB1_AQQS_ENB"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=5955, global_bts_id=955)

# host
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.61", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_classical_bts],
    #enbs=[_lte_real_enb],
    appserver=_appserver,
    ues=[_ue1, _ue2, _mtk],
    core=RealCore(mcc=262, mnc=3),
    attenuator=_attenuator,
   #tl_cloud_topology=_tl_cloud_topology,
)
