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
from taf.config.testline.attenuator import HBTE as ATTEN_HBTE
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import AppServer
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc


__maintainer__ = "Zhenzhen Ren"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_08_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_08@internal.nsn.com>"
__email__ = "zhenzhen.ren@nokia-sbell.com"
# common
__all__ = ["tl"]
_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_attenuator = ATTEN_HBTE(
    ip_addr="10.101.52.212",
    port=5000,
    model="PA-16-16-6-127-0.5-B-S",
    attenuation_port_numbers=[1, 2, 3, 4,],
)
# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.12", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS RU PB

_ru1_pdu = HBTE(addr="10.71.195.217", port_numbers=[1])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.101.46.35", username="root", password="root",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala",
    ),
    pdu_port=_ru1_pdu.pdu_ports[1],
    radio_type=RadioTypes.AHPF,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru2_pdu = HBTE(addr="10.71.195.217", port_numbers=[3])

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.18.36",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3",
        username="root",
        password="I9LzXPHVEqLorL/x0tAG5ztQ/Y8vVmhmlN9LSkVW4CQ=",
    ),
    pdu_port=_ru2_pdu.pdu_ports[3],
    radio_type=RadioTypes.UHIE,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)


# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.71.210.211", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.71.195.217", port_numbers=[8])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[8],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru1, _ru2], f1_m_ip_addr="10.71.210.211")
# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.210.211",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.210.193", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.210.211", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.210.211", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.210.211",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.210.193", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.71.210.211",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.210.193", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.71.210.211",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.210.193", ip_prefix_length=27),
    ),
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIBL_ABIOB1_3UHIE"
# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=51008, global_bts_id=1008)


_appserver_ssh = SshServiceDetails(
    addr="10.71.219.237", username="cmw_sg8", password="cm@8",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.237",
    iperf_path="iperf",
    port=58999,
)

_appserver = AppServer(_iperf_details_on_appserver)


# for MTK1
_mtk_host_ssh_193 = SshServiceDetails(
    addr="10.71.217.193", username="nokia5G", password="noki@123"
)

_iperf_details_on_mtk_193 = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh_193,
    network_interface_address="",
    iperf_path="/data/local/tmp/iperf",
    port=58165,
)

_mtk_193 = MediaTek(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.193", username="nokia5G", password="noki@123"
    ),
    serial_number="0123456789ABCDEF",
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    imei="547546823423548",
    imsi="262033100007794",
    apn_url="dxdata1",
    iperf_details=_iperf_details_on_mtk_193,
    capabilities=["REAL_MTK_UEPC_193", "SA"],
)


# for MTK2
_mtk_host_ssh_248 = SshServiceDetails(
    addr="10.71.218.248", username="nokia5G", password="noki@123"
)

_iperf_details_on_mtk_248 = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh_248,
    network_interface_address="",
    iperf_path="/data/local/tmp/iperf",
    port=58166,
)

_mtk_248 = MediaTek(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.248", username="nokia5G", password="noki@123"
    ),
    serial_number="0123456789ABCDEF",
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    imei="428639169092763",
    imsi="262033100010054",
    apn_url="dxdata1",
    iperf_details=_iperf_details_on_mtk_248,
    capabilities=["REAL_MTK_UEPC_248", "SA"],
)


tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    appserver=_appserver,
    ues=[_mtk_193, _mtk_248],
    core=RealCore(mcc=262, mnc=3),
    attenuator=_attenuator,
    tl_cloud_topology=_tl_cloud_topology,
)
