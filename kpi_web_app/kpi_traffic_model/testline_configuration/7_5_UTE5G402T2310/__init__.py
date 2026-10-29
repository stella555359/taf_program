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
#from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.attenuator import HBTE as ATTEN_HBTE
#from taf.config.testline.attenuator import TopYoung as TOPYOUNG
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import AppServer

from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc

__maintainer__ = "eleven wu"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_08_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_08@internal.nsn.com>"
__email__ = "eleven.1.wu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_attenuator = ATTEN_HBTE(
    ip_addr="10.71.204.99",
    port=5000,
    model="PA-16-16-6-127-0.5-B-S",
    attenuation_port_numbers=[
        9,
        10,
        11,
        12,
    ],
)

# 5GRU for classicalBTS RU PB
_ru_pdu_1 = TopYoung(addr="10.71.195.215", port_numbers=[5])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.135", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_1.pdu_ports[5],
    radio_type=RadioTypes.AZQF,
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
)

_ru_pdu_2 = TopYoung(addr="10.71.195.216", port_numbers=[4])

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.135", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_2.pdu_ports[4],
    radio_type=RadioTypes.AZQF,
)

_ru_pdu_3 = HBTE(addr="10.71.195.204", port_numbers=[1])

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.135", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_3.pdu_ports[1],
    radio_type=RadioTypes.AZQC,
)

_ru_pdu_4 = HBTE(addr="10.71.195.204", port_numbers=[2])

_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.135", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_4.pdu_ports[2],
    radio_type=RadioTypes.AZQF,
)

_ru_pdu_5 = TopYoung(addr="10.71.195.202", port_numbers=[1])

_ru5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.135", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_5.pdu_ports[1],
    radio_type=RadioTypes.AZHA,
)


# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.210.219",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.49.129", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.210.219", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.210.219", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.210.219",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.49.129", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.71.210.219",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.49.129", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.71.210.219",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.49.129", ip_prefix_length=27),
    ),
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20", hardware_type="ASOH", rus=[_ru1, _ru2, _ru3, _ru4, _ru5])
_gnb_pdu = HBTE(addr="10.71.195.213", port_numbers=[2])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
    hardware_type="ASOH",
)
_airscale = Airscale(common_units=[_common_unit_0])
# Cablinks should be defined in the bottom of DU section
_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru1, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=2),
        target=Endpoint(unit=_ru1, label="SFP", port_id=2),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=3),
        target=Endpoint(unit=_ru2, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=8),
        target=Endpoint(unit=_ru2, label="SFP", port_id=2),
    ),
]
_du = DU(airscale=_airscale, rus=[_ru1, _ru2,_ru3, _ru4, _ru5], f1_m_ip_addr="10.71.210.219", cablinks=_ru_cablinks)


# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=2310, global_bts_id=36983)

# host
_gnb_testpc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.217.67", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_SA_ASOH_3xAZQF_AZQC_AZHA_AHFII_HAZ"

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.239", username="vrf3_sg8", password="vrf3@sg8"
)

_iperf_1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.239",
    iperf_path="/usr/bin/iperf",
    port="48999",
)


_appserver = AppServer(_iperf_1)
# cloud_topology

# for FastMile CPE
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_2",
    address="10.57.191.239",
    user="vrf3_sg8",
    password="vrf3@sg8",
    bind_interface_ip="10.57.191.239",
    expected_prompt="[cmw_sg8@APPServer-3 ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=[48490, 48491],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    com_port="3",
    ue_pc_address="10.71.217.17",
    root_password="abeaab629bc5",
    ue_manage_ip="192.168.1.1",
    serial_number="LPL2214005D7",
    data_transfer=[_fastmile_data_transfer_1],
    ue_pc_port=5555,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)




tl = TestLine(
    test_pc=_gnb_testpc,
    gnbs=[_classical_bts],
    appserver=_appserver,
    ues=[_fastmile_1],
    core=RealCore(mcc=262, mnc=3),
    attenuator=_attenuator,
    tl_cloud_topology=_tl_cloud_topology,
)
