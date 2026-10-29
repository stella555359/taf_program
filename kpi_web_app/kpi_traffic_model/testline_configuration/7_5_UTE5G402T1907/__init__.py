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
from taf.config.testline.pdu import HBTE, TopYoung
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
from taf.config.testline.attenuator import AttenuationPort
from taf.config.testline.attenuator import TopYoung as TOPYOUNG
from taf.config.testline.attenuator import HBTE as ATTEN_HBTE
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import AppServer

__maintainer__ = "zhenzhen ren"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_08_01_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_08_01@internal.nsn.com>"  # TL owner's team
__email__ = "zhenzhen.ren@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]


_cfg_dir = os.path.dirname(os.path.abspath(__file__))
_attenuator = ATTEN_HBTE(
    ip_addr="10.101.52.202",
    port=5000,
    model="PA-16-16-6-127-0.5-B-S",
    attenuation_port_numbers=[1, 2, 3, 4],
)

_mtk_appserver_ssh = SshServiceDetails(
    addr="10.57.173.234", username="vrf3_sg8", password="vrf3@sg8",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_mtk_appserver_ssh,
    network_interface_address="10.57.173.234",
    iperf_path="iperf",
    port=48077,
)

_appserver = AppServer(_iperf_details_on_appserver)

_mtk_host_ssh = SshServiceDetails(
    addr="10.68.86.187", username="mn5gran", password="nokia123@"
)

_mtk_host_ssh_1 = SshServiceDetails(
    addr="10.101.47.127", username="mn5gran", password="nokia123@"
)

_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="",
    iperf_path="/data/local/tmp/iperf",
    port=48078,
)

_iperf_details_on_mtk_1 = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh_1,
    network_interface_address="",
    iperf_path="/data/local/tmp/iperf",
    port=48079,
)

# CI_Detail_UE_Type='MTK'
_mtk = MediaTek(
    ssh_connection_details=_mtk_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    imei="456576823424567",
    imsi="262033100001064",
    apn_url="dxdata1",
    iperf_details=_iperf_details_on_mtk,
    capabilities=["REAL_MEDIATEK_UE0", "SA"],
)

_mtk_1 = MediaTek(
    ssh_connection_details=_mtk_host_ssh_1,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    imei="234533456764339",
    imsi="262033100004091",
    apn_url="dxdata1",
    iperf_details=_iperf_details_on_mtk_1,
    capabilities=["REAL_MEDIATEK_UE1", "SA"],
)

# 5GRU for classicalBTS
_ru1_pdu = HBTE(addr="10.101.46.46", port_numbers=[4])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.101.46.35",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    pdu_port=_ru1_pdu.pdu_ports[4],
    radio_type=RadioTypes.UHIE,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru2_pdu = HBTE(addr="10.101.46.50", port_numbers=[2])

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.18.36",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    pdu_port=_ru2_pdu.pdu_ports[2],
    radio_type=RadioTypes.UHIE,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru3_pdu = HBTE(addr="10.101.46.46", port_numbers=[5])

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.18.34",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    pdu_port=_ru3_pdu.pdu_ports[5],
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
    addr="10.101.52.194", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.101.46.48", port_numbers=[6])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[6],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru1, _ru2, _ru3], f1_m_ip_addr="10.101.52.194")


# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.101.52.194",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.52.193", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.52.194", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.52.194", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.101.52.194",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.52.193", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.101.52.194",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.52.193", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.101.52.194",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.52.193", ip_prefix_length=27),
    ),
)


# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIBL_ABIOB1_3UHIE"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=11632, global_bts_id=1907)


# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.99", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    appserver=_appserver,
    ues=[_mtk_1, _mtk],
    core=RealCore(mcc=262, mnc=3),
    attenuator=_attenuator,
    tl_cloud_topology=_tl_cloud_topology,
)
