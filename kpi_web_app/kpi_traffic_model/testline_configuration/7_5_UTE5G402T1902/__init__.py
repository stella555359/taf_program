import os
import yaml
import re
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.core import RealCore
from taf.config.testline import RU, DU
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

# from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.attenuator import HBTE as ATTEN_HBTE
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import AppServer

from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc

__maintainer__ = "zhenzhen ren"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_08_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_08@internal.nsn.com>"
__email__ = "zhenzhen.ren@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_attenuator = ATTEN_HBTE(
    ip_addr="10.71.204.73",
    port=5000,
    model="PA-16-16-6-127-0.5-B-S",
    attenuation_port_numbers=[
        9,
        13,
        26,
        30,
        43,
        47,
        60,
        64,
    ],
)

# 5GRU for classicalBTS RU PB
_ru_pdu_aggressor_1 = TopYoung(addr="10.71.195.196", port_numbers=[4])
_ru1_pdu = TopYoung(addr="10.71.195.200", port_numbers=[2])

_ru_aggressor_1 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_aggressor_1.pdu_ports[4],
    radio_type=RadioTypes.AWHQE,
    serial_number="EB2125R0103",
    attenuation_ports=None,
)

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.132", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AZQF,
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[26],
        _attenuator.attenuator_ports[30],
        _attenuator.attenuator_ports[43],
        _attenuator.attenuator_ports[47],
        _attenuator.attenuator_ports[60],
        _attenuator.attenuator_ports[64],
    ],
)

_ru_pdu_aggressor_2 = TopYoung(addr="10.71.195.202", port_numbers=[5])
_ru2_pdu = TopYoung(addr="10.71.195.202", port_numbers=[2])

_ru_aggressor_2 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_aggressor_2.pdu_ports[5],
    radio_type=RadioTypes.AZNA,
    serial_number="EA224651707",
    attenuation_ports=None,
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.133", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[2],
    radio_type=RadioTypes.AZQF,
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[26],
        _attenuator.attenuator_ports[30],
        _attenuator.attenuator_ports[43],
        _attenuator.attenuator_ports[47],
        _attenuator.attenuator_ports[60],
        _attenuator.attenuator_ports[64],
    ],
)

_ru3_pdu = TopYoung(addr="10.71.195.200", port_numbers=[6])

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.131", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru3_pdu.pdu_ports[6],
    radio_type=RadioTypes.AZNA,
)

_ru4_pdu = TopYoung(addr="10.71.195.198", port_numbers=[6])

_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.130", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru4_pdu.pdu_ports[6],
    radio_type=RadioTypes.AZNA,
)

_ru5_pdu = TopYoung(addr="10.71.195.198", port_numbers=[4])

_ru5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.129", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru5_pdu.pdu_ports[4],
    radio_type=RadioTypes.AZNA,
)

_ru6_pdu = TopYoung(addr="10.71.195.200", port_numbers=[5])

_ru6 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.128", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru6_pdu.pdu_ports[5],
    radio_type=RadioTypes.AZNA,
)

_ru7_pdu = TopYoung(addr="10.71.195.210", port_numbers=[5])

_ru7 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.134",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru7_pdu.pdu_ports[5],
    radio_type=RadioTypes.AHFII,
)

_ru8_pdu = TopYoung(addr="10.71.195.216", port_numbers=[2])

_ru8 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.135", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru8_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHFB,
)
_ru9_pdu = TopYoung(addr="10.71.195.196", port_numbers=[5])

_ru9 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.64.2",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    pdu_port=_ru9_pdu.pdu_ports[5],
    radio_type=RadioTypes.AZNA,
)

_ru10_pdu = TopYoung(addr="10.71.195.196", port_numbers=[6])

_ru10 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.64.2",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    pdu_port=_ru10_pdu.pdu_ports[6],
    radio_type=RadioTypes.AZNA,
)

_ru11_pdu = TopYoung(addr="10.71.195.200", port_numbers=[3])

_ru11 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.64.2",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    pdu_port=_ru11_pdu.pdu_ports[3],
    radio_type=RadioTypes.AZNA,
)

# DU for classicalBTS
_lmp_connection_aggressor = SshServiceDetails(
    addr="10.71.210.146", username="toor4nsn", password="oZPS0POrRieRtu"
)

_lmp_connection = SshServiceDetails(
    addr="10.71.210.199", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_aggressor = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIO",
)

_capacity_unit = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIO",
)

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru1, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=7),
        target=Endpoint(unit=_ru1, label="SFP", port_id=2),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=2),
        target=Endpoint(unit=_ru2, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=8),
        target=Endpoint(unit=_ru2, label="SFP", port_id=2),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=3),
        target=Endpoint(unit=_ru3, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=9),
        target=Endpoint(unit=_ru3, label="SFP", port_id=2),
    ),
]

_gnb_pdu_aggressor = HBTE(addr="10.71.195.209", port_numbers=[6])
_common_unit_aggressor = CommonUnit(
    lmp_connection=_lmp_connection_aggressor,
    capacity_units=[_capacity_unit_aggressor],
    pdu_port=_gnb_pdu_aggressor.pdu_ports[6],
)

_gnb_pdu = HBTE(addr="10.71.195.213", port_numbers=[4])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[4],
    hardware_type="ASIL",
)
_airscale_aggressor = Airscale(common_units=[_common_unit_aggressor])
_airscale = Airscale(common_units=[_common_unit_0])
_du_aggressor = DU(
    airscale=_airscale,
    rus=[_ru_aggressor_1, _ru_aggressor_2],
    f1_m_ip_addr="10.71.210.146",
)
_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6, _ru7, _ru8, _ru9, _ru10, _ru11],
    f1_m_ip_addr="10.71.210.199",
    cablinks=_ru_cablinks,
)

# CU
_cu_agressor = CU(
    backhaul_site_oam_ip="10.71.210.146",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.210.146", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.210.146", username="Nemuadmin", password="nemuuser"
    ),
)

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.210.199",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.210.193", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.210.199", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.210.199", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.210.199",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.210.193", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.71.210.199",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.210.193", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.71.210.199",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.210.193", ip_prefix_length=27),
    ),
)


# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_SA_ASILL_ABIOB1_2XAZQF"

# classicalbts
_classical_bts_aggressor = ClassicalBts(
    dus=[_du_aggressor], cu=_cu_agressor, instance_id=1146, global_bts_id=11633
)
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=1902, global_bts_id=10744)

_appserver_ssh = SshServiceDetails(
    addr="10.57.173.234",
    username="vrf3_sg8",
    password="vrf3@sg8",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.173.234",
    iperf_path="iperf",
    port=48999,
)

_appserver = AppServer(_iperf_details_on_appserver)

# for FastMile CPE
_fastmile_appserver_2 = TafUeAppServer(
    app_server_name="APP_SERVER_2",
    address="10.57.173.234",
    user="vrf3_sg8",
    password="vrf3@sg8",
    bind_interface_ip="10.57.173.234",
    expected_prompt="[vrf3_sg8@APPServer-3 ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=[48017, 48427],
)
_fastmile_data_transfer_2 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_2,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_2 = TafUeFastmile(
    com_port="11",
    ue_pc_address="10.0.176.197",
    root_password="f47aad72ce35",
    ue_manage_ip="192.168.1.1",
    serial_number="",
    data_transfer=[_fastmile_data_transfer_2],
    ue_pc_port=5555,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE2", "nokia_fastmile"],
)

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.62", username="ute", password="iW_K#8.ute%A10h0m0ra"
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
    test_pc=_host,
    gnbs=[_classical_bts, _classical_bts_aggressor],
    appserver=_appserver,
    ues=[_fastmile_2],
    core=RealCore(mcc=262, mnc=3),
    attenuator=_attenuator,
    tl_cloud_topology=_tl_cloud_topology,
)
