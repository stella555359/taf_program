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
_ru_pdu = HBTE(addr="10.68.87.116", port_numbers=[1])

_ru_lmi_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.86.229", username="ute", password="!Q2w3e4r5t6y7u"
    )
)

_ru_lmi = LMI(product_code="",
              host=_ru_lmi_pc,
              uart_mapping=[Local(port='/dev/ttyUSB0')])

_ru = RU(
    ru_hw_group="AQQY",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.229", username="ute", password="!Q2w3e4r5t6y7u"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AQQY,
    lmi=_ru_lmi
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.68.87.115", port_numbers=[5])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru, label="SFP", port_id=1),
    )
]

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.68.89.46", cablinks=_ru_cablinks
)

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.68.89.46",
        vlan_id=1,
        routing_v4=RoutingInformation(gateway="10.68.89.33/27"),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.89.46", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.89.46", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.68.89.46",
        vlan_id=1,
        routing_v4=RoutingInformation(gateway="10.68.89.33/27"),
    ),
    x2u=NetworkAddress(
        v4="10.68.89.46",
        vlan_id=1,
        routing_v4=RoutingInformation(gateway="10.68.89.33/27"),
    ),
    s1u=NetworkAddress(
        v4="10.68.89.46",
        vlan_id=1,
        routing_v4=RoutingInformation(gateway="10.68.89.33/27"),
    ),
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIL_ABIO_AQQY"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=536870817, global_bts_id=536870817)

# test pc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.83", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.133", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
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

# CI_Detail_UE_Type='Nokia FastMile 5G Gateway 3.1'
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name='APP_SERVER_1',
    address="10.57.191.246",
    user="vrf4_sg4",
    password="vrf4@sg4",
    bind_interface_ip="10.57.191.246",
    expected_prompt="[vrf4_sg4@appserver ~]$ ",
    binary_path="/home/vrf4_sg4/taf_debug/iperf",
    ports=[53710, 54710])

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name='iperf',
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path='iperf',
    version=2)

_fastmile_1= TafUeFastmile(
    ue_pc_address='10.57.155.83',
    root_password='NLw3oePyeR+=F.nX',
    default_user_password='G27_KQFaShcnJ:go',
    ue_manage_ip='10.68.89.38',
    data_transfer=[_fastmile_data_transfer_1],
    serial_number='LPL25100006D',
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version='Receiver 5Gmm28-A',
    capabilities=['REAL_FASTMILE_UE1', 'nokia_fastmile'])
    
_fastmile_appserver_2 = TafUeAppServer(
    app_server_name='APP_SERVER_1',
    address="10.57.191.246",
    user="vrf4_sg4",
    password="vrf4@sg4",
    bind_interface_ip="10.57.191.246",
    expected_prompt="[vrf4_sg4@appserver ~]$ ",
    binary_path="/home/vrf4_sg4/taf_debug/iperf",
    ports=[53319, 54319])

_fastmile_data_transfer_2 = TafUeDataTransferProtocol(
    protocol_name='iperf',
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path='iperf',
    version=2)

_fastmile_2= TafUeFastmile(
    ue_pc_address='10.57.155.83',
    root_password='dP,!=,Cj:_.pmc.H',
    default_user_password='u9xYRUJ+PYANcA:q',
    ue_manage_ip='10.68.89.39',
    data_transfer=[_fastmile_data_transfer_2],
    serial_number='LPL251000062',
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version='Receiver 5Gmm28-A',
    capabilities=['REAL_FASTMILE_UE2', 'nokia_fastmile'])


tl = TestLine(
    test_pc=_test_pc,
    test_pcs=[_test_pc, _test_pc_enb],
    gnbs=[_classical_bts],
    core=RealCore(mcc=262, mnc=3),
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_fastmile_1, _fastmile_2],
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
)
