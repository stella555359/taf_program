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
        addr="10.57.167.113", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS RU PB

_ru1_pdu = HBTE(addr="10.101.46.46", port_numbers=[2])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.101.46.35",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3",
        username="root",
        password="I9LzXPHVEqLorL/x0tAG5ztQ/Y8vVmhmlN9LSkVW4CQ=",
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.UHIE,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru2_pdu = HBTE(addr="10.101.46.46", port_numbers=[3])

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

_ru3_pdu = HBTE(addr="10.101.46.47", port_numbers=[2])

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.18.34",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3",
        username="root",
        password="I9LzXPHVEqLorL/x0tAG5ztQ/Y8vVmhmlN9LSkVW4CQ=",
    ),
    pdu_port=_ru3_pdu.pdu_ports[2],
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
    addr="10.101.52.210", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.101.46.48", port_numbers=[7])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[7],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru1, _ru2, _ru3], f1_m_ip_addr="10.101.52.210")
# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.101.52.210",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.52.193", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.52.210", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.52.210", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.101.52.210",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.52.193", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.101.52.210",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.52.193", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.101.52.210",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.52.193", ip_prefix_length=27),
    ),
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIBL_ABIOB1_3UHIE"
# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=10557, global_bts_id=1908)


_appserver_ssh = SshServiceDetails(
    addr="10.57.191.239", username="vrf3_sg8", password="vrf3@sg8",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.239",
    iperf_path="iperf",
    port=48999,
)

_appserver = AppServer(_iperf_details_on_appserver)


# for FastMile CPE
_fastmile_appserver_2 = TafUeAppServer(
    app_server_name="APP_SERVER_2",
    address="10.57.191.239",
    user="vrf3_sg8",
    password="vrf3@sg8",
    bind_interface_ip="10.57.191.239",
    expected_prompt="[vrf3_sg8@appserver ~]$",
    binary_path="/usr/bin/iperf",
    ports=[48005, 48163],
)

_fastmile_data_transfer_2 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_2,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_2 = TafUeFastmile(
    com_port="4",
    ue_pc_address="10.101.47.221",
    root_password="73aa4a42ab45",
    ue_manage_ip="192.168.1.1",
    serial_number="LPL221400464",
    data_transfer=[_fastmile_data_transfer_2],
    ue_pc_port=5555,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE2", "nokia_fastmile"],
)


# for MTK
_mtk_host_ssh_187 = SshServiceDetails(
    addr="10.68.86.187", username="mn5gran", password="nokia123@"
)

_iperf_details_on_mtk_187 = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh_187,
    network_interface_address="",
    iperf_path="/data/local/tmp/iperf",
    port=48162,
)

_mtk_187 = MediaTek(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.187", username="mn5gran", password="nokia123@"
    ),
    serial_number="0123456789ABCDEF",
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    imei="678944553240235",
    imsi="460023100008477",
    apn_url="wap2.nokia.com",
    iperf_details=_iperf_details_on_mtk_187,
    capabilities=["REAL_MTK_UEPC_187", "SA"],
)


tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    appserver=_appserver,
    ues=[_fastmile_2, _mtk_187],
    core=RealCore(mcc=262, mnc=3),
    attenuator=_attenuator,
    tl_cloud_topology=_tl_cloud_topology,
)
