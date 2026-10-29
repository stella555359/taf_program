import re
import os
import yaml
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import RealCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import HBTE, TopYoung
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import Android
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
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
from taf.config.testline.attenuator import AttenuationPort
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import AppServer
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.pdn import PDNTafUeAndroidDetails
from taf.config.testline.ue import TafUeFastmile, TafUeAndroid
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.lmi import LMI, Local
from taf.config.testline.attenuator import HBTE as HBTEAttenuator


__maintainer__ = "Shi Zhihao"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_04_01_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_04_01@internal.nsn.com>"  # TL owner's team
__email__ = "zhihao.shi@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.62", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS
_ru_pdu = HBTE(addr="10.71.196.174", port_numbers=[1])
_ru_pdu1 = HBTE(addr="10.71.196.178", port_numbers=[5])
_ru_pdu2 = HBTE(addr="10.71.196.114", port_numbers=[4])
_ru_pdu3 = HBTE(addr="10.71.196.120", port_numbers=[4])

_ru_lmi_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.71.217.224", username="mn5gran", password="nokia123@"
    )
)
_ru_lmi_pc1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.0.176.157", username="mn5gran", password="nokia123@"
    )
)

_ru_lmi = LMI(product_code="",
              host=_ru_lmi_pc,
              uart_mapping=[Local(port="COM3"), Local(port="COM4")])

_ru_lmi1 = LMI(product_code="",
              host=_ru_lmi_pc1,
              uart_mapping=[Local(port="COM3"), Local(port="COM4")])

_ru = RU(
    ru_hw_group="AVQC",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.224", username="mn5gran", password="nokia123@"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AVQC,
    serial_number="1M240305775",
    lmi=_ru_lmi
)

_ru1 = RU(
    ru_hw_group="AVQA",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.1.2", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.0.176.157", username="mn5gran", password="nokia123@"
    ),
    pdu_port=_ru_pdu1.pdu_ports[5],
    radio_type=RadioTypes.AVQA,
    serial_number="L1245003794",
    lmi=_ru_lmi1
)

_ru2 = RU(
    ru_hw_group="AVQA",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.1.2", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    pdu_port=_ru_pdu2.pdu_ports[4],
    radio_type=RadioTypes.AVQA,
    serial_number="L1242003420"
)

_ru3 = RU(
    ru_hw_group="AVQA",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.1.2", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    pdu_port=_ru_pdu3.pdu_ports[4],
    radio_type=RadioTypes.AVQA,
    serial_number="L1245003793"
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20", hardware_type="ABIP")
_gnb_pdu = TopYoung(addr="10.71.196.172", port_numbers=[3])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru, _ru1, _ru2, _ru3], f1_m_ip_addr="10.71.213.140")

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.213.140",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.57.249.192/26"),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.213.140", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.213.140", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.213.140",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.57.249.192/26"),
    ),
    x2u=NetworkAddress(
        v4="10.71.213.140",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.57.249.192/26"),
    ),
    s1u=NetworkAddress(
        v4="10.71.213.140",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.57.249.192/26"),
    ),
)

# cloud_topology
_tl_cloud_topology = "I&V-HGZ-TL572"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=572, global_bts_id=572)

# test pc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.62", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


# CI_Detail_UE_Type='Nokia FastMile 5G 3.1'
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.71.207.151",
    user="vrf4_sg4",
    password="vrf4@sg4",
    bind_interface_ip="10.71.207.151",
    expected_prompt="[vrf4_sg4@appserver ~]$ ",
    binary_path="/home/vrf4_sg4/taf_debug/iperf",
    ports=[54572, 54573],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    ue_pc_address='10.57.167.62',
    root_password='oLmZD=G:QeY@K=f:',
    default_user_password='Jtc95SfdW5+a:fg6',
    ue_manage_ip='10.71.213.143',
    serial_number='LPL243600018',
    data_transfer=[_fastmile_data_transfer_1],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version='Receiver 5Gmm28-B',
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"]
)

_fastmile_appserver_2 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.71.207.151",
    user="vrf4_sg4",
    password="vrf4@sg4",
    bind_interface_ip="10.71.207.151",
    expected_prompt="[vrf4_sg4@appserver ~]$ ",
    binary_path="/home/vrf4_sg4/taf_debug/iperf",
    ports=[54703, 54705],
)

_fastmile_data_transfer_2 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_2,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_2 = TafUeFastmile(
    ue_pc_address='10.57.167.62',
    root_password='Ske,DVYQCQSq9TMA',
    default_user_password='kvDLF@jv_b+@siUC',
    ue_manage_ip='10.71.213.142',
    serial_number='LPL243600005',
    data_transfer=[_fastmile_data_transfer_2],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version='Receiver 5Gmm28-B',
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
    ports=[54706, 54707],
)

_fastmile_data_transfer_3 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_3,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_3 = TafUeFastmile(
    ue_pc_address='10.57.167.62',
    root_password='d!.qftKgrUDy3CxT',
    default_user_password='P.P@6c_.hvtCePtY',
    ue_manage_ip='10.71.205.213',
    serial_number='LPL243600019',
    data_transfer=[_fastmile_data_transfer_3],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version='Receiver 5Gmm28-B',
    capabilities=["REAL_FASTMILE_UE3", "nokia_fastmile"]
)

_fastmile_appserver_4 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.71.207.151",
    user="vrf4_sg4",
    password="vrf4@sg4",
    bind_interface_ip="10.71.207.151",
    expected_prompt="[vrf4_sg4@appserver ~]$ ",
    binary_path="/home/vrf4_sg4/taf_debug/iperf",
    ports=[54708, 5479],
)

_fastmile_data_transfer_4 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_4,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_4 = TafUeFastmile(
    ue_pc_address='10.57.167.62',
    root_password='UQCytMiTG:-jA.js',
    default_user_password='4hfj,m.CZTg=2+Ez',
    ue_manage_ip='10.71.205.214',
    serial_number='LPL244300218',
    data_transfer=[_fastmile_data_transfer_4],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version='Receiver 5Gmm28-B',
    capabilities=["REAL_FASTMILE_UE4", "nokia_fastmile"]
)

# Shared PDN configuration
_android_pdn_1 = PDNTafUeAndroidDetails(
    entryName="dxstatic8", apnName="dxstatic8", apnType=["DEFAULT"]
)

def create_android_ue(ue_number, serial_number, capabilities, bind_ue_ip, imei=None, imsi=None,
                     interface_name=None, qualcomm_prototype=False, port_offset=0):
    """Create Android UE configuration with app server and data transfer"""
    base_port = 54610 + ue_number
    
    appserver = TafUeAppServer(
        app_server_name="APP_SERVER_2",
        address="10.57.191.246",
        user="vrf4_sg4",
        password="vrf4@sg4",
        bind_interface_ip="10.57.191.246",
        binary_path='/home/vrf4_sg4/taf_debug/iperf',
        ports=[base_port + port_offset, base_port + port_offset - 500],
    )
    
    data_transfer_kwargs = {
        "protocol_name": "iperf",
        "app_server": appserver,
        "interval": 1,
        "bind_ue_ip": bind_ue_ip,
        "server_close_delay": 50,
        "binary_path": '/data/local/tmp/iperf',
    }
    if interface_name:
        data_transfer_kwargs["interface_name"] = interface_name
    
    data_transfer = TafUeDataTransferProtocol(**data_transfer_kwargs)
    
    ue_kwargs = {
        "serial_number": serial_number,
        "capabilities": capabilities,
        "ue_pc_address": "10.0.176.238",
        #"proxy_mngr_port": 9955,
        "ue_pc_port": 22222,
        "ueproxy_force_release": True,
        "data_transfer": [data_transfer],
        "ssh_connection_details": SshServiceDetails(
            addr="10.0.176.238", username="mn5gran", password="nokia123@"
        ),
        "imei": imei,
        "imsi": imsi,
        "pdns": [_android_pdn_1],
        "allow_kw_logs": False,
    }
    if qualcomm_prototype:
        ue_kwargs["qualcomm_prototype"] = True
    
    return TafUeAndroid(**ue_kwargs)

# CI_Detail_UE_Type='Samsung s24'
_android_1 = create_android_ue(
    ue_number=1,
    serial_number="RFCX720ESLY",
    capabilities=["REAL_ANDROID_UE1", "samsung"],
    bind_ue_ip="10.64.21.203",
    interface_name="rmnet_data0",
    port_offset=1
)

# CI_Detail_UE_Type='MTK MT6986D k6991'
_android_2 = create_android_ue(
    ue_number=2,
    serial_number="ea616eb1",
    capabilities=["REAL_ANDROID_UE2", "xiaomi"],
    bind_ue_ip="10.64.21.200",
    interface_name="rmnet_data1",
    port_offset=2
)

_android_3 = create_android_ue(
    ue_number=3,
    serial_number="134dc3b3",
    capabilities=["REAL_ANDROID_UE3", "xiaomi"],
    bind_ue_ip="10.64.21.204",
    interface_name="rmnet_data1",
    port_offset=3
)

# CI_Detail_UE_Type='MTP DX85'
_android_4 = create_android_ue(
    ue_number=4,
    serial_number="c650af92",
    capabilities=["REAL_ANDROID_UE4", "xiaomi"],
    bind_ue_ip="10.64.21.195",
    interface_name="rmnet_data1",
    port_offset=4
)

_android_5 = create_android_ue(
    ue_number=5,
    serial_number="cb43977a",
    capabilities=["REAL_ANDROID_UE5", "xiaomi"],
    bind_ue_ip="10.64.21.207",
    interface_name="rmnet_data1",
    port_offset=5
)

_android_6 = create_android_ue(
    ue_number=6,
    serial_number="fdd148ea",
    capabilities=["REAL_ANDROID_UE6", "xiaomi"],
    bind_ue_ip="10.64.21.208",
    interface_name="rmnet_data1",
    port_offset=6
)

_android_7 = create_android_ue(
    ue_number=7,
    serial_number="984c370f",
    capabilities=["REAL_ANDROID_UE7", "xiaomi"],
    bind_ue_ip="10.64.21.242",
    interface_name="rmnet_data1",
    port_offset=7
)

_android_8 = create_android_ue(
    ue_number=8,
    serial_number="8351ab76",
    capabilities=["REAL_ANDROID_UE8", "xiaomi"],
    bind_ue_ip="10.64.21.244",
    interface_name="rmnet_data1",
    port_offset=8
)

_android_9 = create_android_ue(
    ue_number=9,
    serial_number="8e698851",
    capabilities=["REAL_ANDROID_UE9", "xiaomi"],
    bind_ue_ip="10.64.21.245",
    interface_name="rmnet_data1",
    port_offset=9
)

_android_10 = create_android_ue(
    ue_number=10,
    serial_number="554acfa2",
    capabilities=["REAL_ANDROID_UE10", "xiaomi"],
    bind_ue_ip="10.64.21.243",
    interface_name="rmnet_data1",
    port_offset=10
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

_hbte_attenuator = HBTEAttenuator(ip_addr="10.71.205.183",
                                  port=5000,
                                  attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                  model='PA-16-16-6-127-0.5-B-S')

tl = TestLine(
    test_pc=_host,
    test_pcs=[_test_pc],
    gnbs=[_classical_bts],
    core=RealCore(mcc=262, mnc=3),
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_fastmile_1, _fastmile_2, _fastmile_3, _fastmile_4, _android_1, _android_2, _android_3, _android_4, _android_5, _android_6, _android_7, _android_8, _android_9, _android_10],
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
    attenuators=[_hbte_attenuator]
)
