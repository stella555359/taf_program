import os
import yaml
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.core import RealCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import HBTE, TopYoung
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.lmi import LMI, Local

__maintainer__ = "Zhihao Shi"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_04_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_04@internal.nsn.com>"  # TL owner's team
__email__ = "zhihao.shi@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# 5GRU for classicalBTS
_ru_pdu = TopYoung(addr="10.101.45.119", port_numbers=[1])

_ru_lmi_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.101.47.94", username="ute", password="3edc4rfv%TGB"
    )
)

_ru_lmi = LMI(product_code="",
              host=_ru_lmi_pc,
              uart_mapping=[Local(port='/dev/ttyUSB0')])

_ru = RU(
    ru_hw_group="AVQC",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.94", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AVQC,
    serial_number="1M235231331",
    lmi=_ru_lmi
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.101.45.112", port_numbers=[1])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru, label="SFP", port_id=1),
    )
]

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.101.50.66", cablinks=_ru_cablinks
)

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.101.50.66",
        vlan_id=1,
        routing_v4=RoutingInformation(gateway="10.101.50.65/27"),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.50.66", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.50.66", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.101.50.66",
        vlan_id=1,
        routing_v4=RoutingInformation(gateway="10.101.50.65/27"),
    ),
    x2u=NetworkAddress(
        v4="10.101.50.66",
        vlan_id=1,
        routing_v4=RoutingInformation(gateway="10.101.50.65/27"),
    ),
    s1u=NetworkAddress(
        v4="10.101.50.66",
        vlan_id=1,
        routing_v4=RoutingInformation(gateway="110.101.50.65/27"),
    ),
)

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=536870825, global_bts_id=536870825)

# test pc
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.41", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[_classical_bts],

)

# CI_Detail_UE_Type='Nokia FastMile 5G Gateway 3.1'
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.179.238",
    user="vrf4_sg4",
    password="vrf4@sg4",
    bind_interface_ip="10.57.179.238",
    expected_prompt="[vrf4_sg4@appserver ~]$ ",
    binary_path="/home/vrf4_sg4/taf_debug/iperf",
    ports=[53581, 54581],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    ue_pc_address="10.57.157.41",
    root_password='n5P@4N6+uL3CNWj9',
    default_user_password='SUDvo@MqV:ybkc!-',
    ue_manage_ip="10.101.40.6",
    data_transfer=[_fastmile_data_transfer_1],
    serial_number='KLT234301913',
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version='receiver 5g19a',
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

# CI_Detail_UE_Type='Nokia FastMile 5G Gateway 3.1'
_fastmile_appserver_2 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.179.238",
    user="vrf4_sg4",
    password="vrf4@sg4",
    bind_interface_ip="10.57.179.238",
    expected_prompt="[vrf4_sg4@appserver ~]$ ",
    binary_path="/home/vrf4_sg4/taf_debug/iperf",
    ports=[53717, 54717],
)

_fastmile_data_transfer_2 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_2,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_2 = TafUeFastmile(
    ue_pc_address="10.57.157.41",
    root_password="di3XS4nMMUX6+nck",
    default_user_password='#Q=CJjSX6DSD6n%K',
    ue_manage_ip='10.101.43.35',
    serial_number='KLT23080002F',
    data_transfer=[_fastmile_data_transfer_1],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version='receiver 5g19a',
    capabilities=["REAL_FASTMILE_UE2", "nokia_fastmile"],
)

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

tl = TestLine(
    test_pc=_host,
    test_pcs=[_host],
    gnbs=[_classical_bts],
    core=RealCore(mcc=262, mnc=3),
    ues=[_fastmile_1, _fastmile_2],
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
)
