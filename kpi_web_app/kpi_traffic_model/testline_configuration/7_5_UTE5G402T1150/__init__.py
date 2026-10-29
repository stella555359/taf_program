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
from taf.config.testline.attenuator import AttenuationPort
from taf.config.testline.attenuator import HBTE as ATTEN_HBTE
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import AppServer

from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
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
    ip_addr="10.101.49.151",
    port=5000,
    model="PA-16-16-6-127-0.5-B-S",
    attenuation_port_numbers=[
        1,
        34,
        67,
        100,
        5,
        38,
        71,
        104,
        9,
        42,
        75,
        108,
        13,
        46,
        79,
        112,
        17,
        50,
        83,
        116,
        21,
        54,
        87,
        120,
    ],
)

# 5GRU for classicalBTS RU PB
_ru1_pdu = HBTE(addr="10.101.45.204", port_numbers=[4])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[4],
    radio_type=RadioTypes.AZQF,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[34],
        _attenuator.attenuator_ports[67],
        _attenuator.attenuator_ports[100],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[38],
        _attenuator.attenuator_ports[71],
        _attenuator.attenuator_ports[104],
    ],
)

_ru2_pdu = HBTE(addr="10.101.45.204", port_numbers=[3])

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[3],
    radio_type=RadioTypes.AZQF,
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[42],
        _attenuator.attenuator_ports[75],
        _attenuator.attenuator_ports[108],
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[46],
        _attenuator.attenuator_ports[79],
        _attenuator.attenuator_ports[112],
    ],
)

_ru3_pdu = TopYoung(addr="10.101.45.203", port_numbers=[8])

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru3_pdu.pdu_ports[8],
    radio_type=RadioTypes.AZQF,
    attenuation_ports=[
        _attenuator.attenuator_ports[17],
        _attenuator.attenuator_ports[50],
        _attenuator.attenuator_ports[83],
        _attenuator.attenuator_ports[116],
        _attenuator.attenuator_ports[21],
        _attenuator.attenuator_ports[54],
        _attenuator.attenuator_ports[87],
        _attenuator.attenuator_ports[120],
    ],
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIO",
)

_ru_cablinks = [Cablink(source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
    target=Endpoint(unit=_ru1, label="SFP", port_id=1)),
    Cablink(source=Endpoint(unit=_capacity_unit, label="SFP", port_id=7),
    target=Endpoint(unit=_ru1, label="SFP", port_id=2)),
    Cablink(source=Endpoint(unit=_capacity_unit, label="SFP", port_id=2),
    target=Endpoint(unit=_ru2, label="SFP", port_id=1)),
    Cablink(source=Endpoint(unit=_capacity_unit, label="SFP", port_id=8),
    target=Endpoint(unit=_ru2, label="SFP", port_id=2)),
    Cablink(source=Endpoint(unit=_capacity_unit, label="SFP", port_id=3),
    target=Endpoint(unit=_ru3, label="SFP", port_id=1)),
    Cablink(source=Endpoint(unit=_capacity_unit, label="SFP", port_id=9),
    target=Endpoint(unit=_ru3, label="SFP", port_id=2))]

_gnb_pdu = TopYoung(addr="10.101.45.203", port_numbers=[5])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
    hardware_type="ASIL",
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale, rus=[_ru1, _ru2, _ru3], f1_m_ip_addr="10.101.51.58", cablinks=_ru_cablinks
)

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.101.51.58",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.51.33", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.51.58", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.51.58", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.101.51.58",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.51.33", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.101.51.58",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.51.33", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.101.51.58",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.51.33", ip_prefix_length=27),
    ),
)


# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_SA_ASILL_ABIOB1_2XAZQF"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=1150, global_bts_id=1150)

_appserver_ssh = SshServiceDetails(
    addr="10.57.162.11",
    username="cmw_sg8",
    password="Bestcm@8",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.11",
    iperf_path="iperf",
    port=58999,
)

_appserver = AppServer(_iperf_details_on_appserver)

_mtk_host_ssh_32 = SshServiceDetails(
    addr="10.68.86.82", username="MN5GRAN", password="nokia123@"
)

_iperf_details_on_mtk_32 = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh_32,
    network_interface_address="",
    iperf_path="/data/local/tmp/iperf",
    port=58300,
)

_mtk_32 = MediaTek(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.82", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="0123456789ABCDEF",
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    imei="887239942934318",
    imsi="262033100010044",
    apn_url="wap2.nokia.com",
    iperf_details=_iperf_details_on_mtk_32,
    capabilities=["REAL_MTK_UEPC_32", "SA"],
)


# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.70.230.156", username="ute", password="uteUTE!"
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
    gnbs=[_classical_bts],
    appserver=_appserver,
    ues=[_mtk_32],
    core=RealCore(mcc=262, mnc=3),
    attenuator=_attenuator,
    tl_cloud_topology=_tl_cloud_topology,
)
