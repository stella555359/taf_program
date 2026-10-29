import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.core import RealCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import HBTE
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.gnb.du import Cablink, Endpoint
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
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import AppServer

from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc

__maintainer__ = "Zhihao Shi"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_04_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_04@internal.nsn.com>"  # TL owner's team
__email__ = "zhihao.shi@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.136", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS
_ru_pdu = HBTE(addr="10.68.87.116", port_numbers=[2])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[2],
    radio_type=RadioTypes.AEQY,
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.68.87.115", port_numbers=[1])

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

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale,
    rus=[_ru],
    f1_m_ip_addr="10.68.89.52",
    cablinks=_ru_cablinks,
)

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.68.89.52",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.68.89.33/27"),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.89.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.89.52", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.68.89.52",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.68.89.33/27"),
    ),
    x2u=NetworkAddress(
        v4="10.68.89.52",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.68.89.33/27"),
    ),
    s1u=NetworkAddress(
        v4="10.68.89.52",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.68.89.33/27"),
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.68.89.53", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = HBTE(addr="10.68.87.115", port_numbers=[1])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[1],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIKL_ABILB1_AEQY"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=316, global_bts_id=316)

# CI_Detail_UE_Type='Nokia FastMile 5G Gateway 3.1'
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.163.51",
    user="cmw_sg4",
    password="Zvmsg04_159357!",
    bind_interface_ip="10.57.163.51",
    expected_prompt="[cmw_sg4@smw_sg4 ~]$ ",
    binary_path="/home/cmw_sg4/taf_debug/iperf",
    ports=[53316, 54316],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    ue_pc_address="10.57.167.136",
    root_password="678a8ec23cfb",
    ue_manage_ip="10.101.40.3",
    serial_number="2a5a0822",
    data_transfer=[_fastmile_data_transfer_1],
    ue_pc_port=5555,
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

_fastmile_appserver_2 = TafUeAppServer(
   app_server_name='APP_SERVER_1',
   address='10.57.163.51',
   user='cmw_sg4',
   password='Zvmsg04_159357!',
   bind_interface_ip='10.57.163.51',
   expected_prompt='[cmw_sg4@smw_sg4 ~]$ ',
   binary_path='/home/cmw_sg4/taf_debug/iperf',
   ports=[53701, 54701])

_fastmile_data_transfer_2 = TafUeDataTransferProtocol(
   protocol_name='iperf',
   app_server=_fastmile_appserver_2,
   interval=1,
   binary_path='iperf',
   version=2)

_fastmile_2= TafUeFastmile(
   ue_pc_address='10.57.167.136',
   root_password='cf7a863279f3',
   ue_manage_ip='10.101.40.2',
   serial_number='57e3cbcd',
   data_transfer=[_fastmile_data_transfer_2],
   ue_pc_port=5555,
   capabilities=['REAL_FASTMILE_UE2', 'nokia_fastmile'])

# switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="0.0.0.0", port="1", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

# switch Mtor
_dell_s4048ton_ssh = SshServiceDetails(
    addr="0.0.0.0", port="1", username="5gran", password="nokia123"
)
_dell_s4048ton_switch = DellS4048TONSwitch(_dell_s4048ton_ssh)

_attenuator = TopYoung(ip_addr="x.x.x.x", port=23, attenuation_port_numbers=[7, 8])

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    core=RealCore(mcc=262, mnc=3),
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_fastmile_1, _fastmile_2],
    attenuator=_attenuator,
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
)
