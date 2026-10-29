import os
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
from taf.config.testline.lmi import LMI, Local
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc

__maintainer__ = "Shi Zhihao"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_04_01_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_04_01@internal.nsn.com>"  # TL owner's team
__email__ = "zhihao.shi@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.39", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS
_ru_pdu = TopYoung(addr="10.71.196.122", port_numbers=[2])

_ru_lmi_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.71.218.38", username="ute", password="3edc4rfv%TGB"
    )
)

_ru_lmi = LMI(product_code="",
              host=_ru_lmi_pc,
              uart_mapping=[Local(port='/dev/ttyUSB0')])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.218.38", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu.pdu_ports[2],
    radio_type=RadioTypes.AVQC,
    lmi=_ru_lmi
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.71.196.116", port_numbers=[5])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.71.212.205")

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.212.205",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.68.89.65/27"),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.212.205", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.212.205", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.212.205",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.68.89.65/27"),
    ),
    x2u=NetworkAddress(
        v4="10.71.212.205",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.68.89.65/27"),
    ),
    s1u=NetworkAddress(
        v4="10.71.212.205",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.68.89.65/27"),
    ),
)

# RealEnb
#_lmp_connection_enb = SshServiceDetails(
#    addr="10.71.212.206", username="toor4nsn", password="oZPS0POrRieRtu"
#)
#_enb_pdu = HBTE(addr="10.71.196.116", port_numbers=[5])
#_common_unit_1 = CommonUnit(
#    lmp_connection=_lmp_connection_enb,
#    capacity_units=[],
#    pdu_port=_enb_pdu.pdu_ports[5],
#)
#_real_enb = Airscale(common_units=[_common_unit_1])
#_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# cloud_topology
_tl_cloud_topology = "I&V-HGZ-TL567"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=536870819, global_bts_id=536870819)

# CI_Detail_UE_Type='Nokia FastMile 5G Gateway/Receiver'
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.71.207.151",
    user="vrf4_sg4",
    password="vrf4@sg4",
    bind_interface_ip="10.71.207.151",
    expected_prompt="[vrf4_sg4@appserver ~]$ ",
    binary_path="/home/vrf4_sg4/taf_debug/iperf",
    ports=[54067,54567],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    ue_pc_address='10.57.167.39',
    root_password='a74a48c2e639',
    ue_manage_ip='10.71.205.102',
    serial_number='LPL2214005AD',
    version='3.2',
    data_transfer=[_fastmile_data_transfer_1],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"]
)

_fastmile_appserver_2 = TafUeAppServer(
    app_server_name="APP_SERVER_2",
    address="10.71.207.151",
    user="vrf4_sg4",
    password="vrf4@sg4",
    bind_interface_ip="10.71.207.151",
    expected_prompt="[vrf4_sg4@appserver ~]$ ",
    binary_path="/home/vrf4_sg4/taf_debug/iperf",
    ports=[54766, 54716],
)

_fastmile_data_transfer_2 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_2,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_2 = TafUeFastmile(
    ue_pc_address='10.57.167.39',
    root_password='62ea6d2275af',
    ue_manage_ip='10.71.205.98',
    serial_number='LPL22140056E',
    version='3.2',
    data_transfer=[_fastmile_data_transfer_2],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    capabilities=["REAL_FASTMILE_UE2", "nokia_fastmile"]
)

_fastmile_appserver_3 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.71.207.151",
    user="vrf4_sg4",
    password="vrf4@sg4",
    bind_interface_ip="10.71.207.151",
    expected_prompt="[vrf4_sg4@appserver ~]$ ",
    binary_path="/home/vrf4_sg4/taf_debug/iperf",
    ports=[54167,54667],
)

_fastmile_data_transfer_3 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_3,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_3 = TafUeFastmile(
    ue_pc_address='10.57.167.39',
    root_password='696a3262399d',
    ue_manage_ip='10.71.212.226',
    serial_number='FSH204000072',
    version='3.1',
    data_transfer=[_fastmile_data_transfer_3],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    capabilities=["REAL_FASTMILE_UE3", "nokia_fastmile"]
)

_fastmile_appserver_4 = TafUeAppServer(
    app_server_name="APP_SERVER_2",
    address="10.71.207.151",
    user="vrf4_sg4",
    password="vrf4@sg4",
    bind_interface_ip="10.71.207.151",
    expected_prompt="[vrf4_sg4@appserver ~]$ ",
    binary_path="/home/vrf4_sg4/taf_debug/iperf",
    ports=[54866, 54816],
)

_fastmile_data_transfer_4 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_4,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_4 = TafUeFastmile(
    ue_pc_address='10.57.167.39',
    root_password='3.ArKmHKz=Yy:5Xx',
    default_user_password='XF_3g-2NGp+@!_!f',
    ue_manage_ip='10.71.212.227',
    serial_number='LPL244900018',
    version='Receiver 5Gmm28-A',
    data_transfer=[_fastmile_data_transfer_4],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    capabilities=["REAL_FASTMILE_UE4", "nokia_fastmile"]
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

# test pc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.39", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.134", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
)

tl = TestLine(
    # test_pc=_host,
    test_pc=_test_pc,
    test_pcs=[_test_pc, _test_pc_enb],
    gnbs=[_classical_bts],
    core=RealCore(mcc=262, mnc=3),
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_fastmile_1, _fastmile_2, _fastmile_3, _fastmile_4],
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
)
