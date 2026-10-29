import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.core import RealCore
from taf.config.testline import DU
from taf.config.testline.pdu import HBTE
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.radio import RadioTypes, RU
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.mcs import TopYoung
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeAt, TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.lmi import LMI, Local

__maintainer__ = "Jie Li"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_04_04_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_04_01@internal.nsn.com>"  # TL owner's team
__email__ = "jie.2.li@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# 5GRU for classicalBTS
_ru_pdu = HBTE(addr="10.68.87.113", port_numbers=[1])

_ru_lmi_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.86.20", username="mn5gran", password="nokia123@"
    )
)

_ru_lmi = LMI(product_code="",
              host=_ru_lmi_pc,
              uart_mapping=[Local(port="COM5"), Local(port="COM6")])

_ru = RU(
    ru_hw_group="AVQC",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.20", username="mn5gran", password="nokia123@"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AVQC,
    serial_number="1M240403906",
    lmi=_ru_lmi
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20", hardware_type="ABIP")
_gnb_pdu = HBTE(addr="10.68.87.115", port_numbers=[4])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[4],
    hardware_type="ASIM",)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.68.89.48")

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.68.89.48",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.68.89.33/27"),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.89.48", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.89.48", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.68.89.48",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.68.89.33/27"),
    ),
    x2u=NetworkAddress(
        v4="10.68.89.48",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.68.89.33/27"),
    ),
    s1u=NetworkAddress(
        v4="10.68.89.48",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.68.89.33/27"),
    ),
)

# cloud_topology
_tl_cloud_topology = "I&V-HGZ-TL320"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=536870818, global_bts_id=536870818)


# TL578 classical bts
_lmp_connection_tl578 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit_tl578 = CapacityUnit(addr="192.168.253.20", hardware_type="ABIP")

_gnb_pdu_tl578 = HBTE(addr="10.68.87.115", port_numbers=[8])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_tl578,
    capacity_units=[_capacity_unit_tl578],
    pdu_port=_gnb_pdu_tl578.pdu_ports[8],
    hardware_type="ASIM",)
_airscale_tl578 = Airscale(common_units=[_common_unit_0])

_du_tl578 = DU(
    airscale=_airscale_tl578,
    rus=[_ru],
    f1_m_ip_addr="10.68.89.35",
)

# CU
_cu_tl578 = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.68.89.35",
        vlan_id=1,
        routing=RoutingInformation(gateway="10.68.89.33", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.89.35", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.89.35", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.68.89.35",
        vlan_id=1,
        routing=RoutingInformation(gateway="10.68.89.33", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.68.89.35",
        vlan_id=1,
        routing=RoutingInformation(gateway="10.68.89.33", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.68.89.35",
        vlan_id=1,
        routing=RoutingInformation(gateway="10.68.89.33", ip_prefix_length=27),
    ),
)

# classicalbts
_classical_bts_tl578 = ClassicalBts(dus=[_du_tl578], cu=_cu_tl578, instance_id=578, global_bts_id=578)


# test pc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.22", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_topyoung_mcs = TopYoung(
    ip_addr="10.68.86.113",
    port=28888,
    mcs_port_numbers=[9, 10, 11, 12, 13, 14, 15, 16],
    model="MCS2350A2-64B16-B1",
    version="",
)

# CI_Detail_UE_Type='Qualcomm CPE DX65'
_at_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.246",
    user="vrf4_sg4",
    password="vrf4@sg4",
    bind_interface_ip="10.57.191.246",
    expected_prompt="\$",
    binary_path="/home/vrf4_sg4/taf_debug/iperf",
    ports=[54420, 54320],
)

# _at_data_transfer_1 = TafUeDataTransferProtocol(
#     protocol_name="iperf",
#     app_server=_at_appserver_1,
#     interval=1,
#     binary_path="/cygdrive/c/Tools/",
#     interface_name="Ethernet 7",
#     server_close_delay=50,
#     version=2,
#     dt_from_uepc=True,
# )

# _at_1 = TafUeAt(
#     proxy_mngr_port=9955,
#     ueproxy_force_release=True,
#     com_port="43",
#     serial_number="57a521d",
#     ue_pc_address="10.68.86.240",
#     ue_pc_login="mn5gran",
#     ue_pc_password="nokia123@",
#     ue_pc_expected_prompt="$",
#     data_transfer=[_at_data_transfer_1],
#     phone_number="",
#     imei="",
#     imsi="",
#     capabilities=["REAL_QUALCOMM_UE1", "qualcomm"],
# )

_at_appserver_2 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.246",
    user="vrf4_sg4",
    password="vrf4@sg4",
    bind_interface_ip="10.57.191.246",
    expected_prompt="\$",
    binary_path="/home/vrf4_sg4/taf_debug/iperf",
    ports=[53800, 54700],
)

# _at_data_transfer_2 = TafUeDataTransferProtocol(
#     protocol_name="iperf",
#     app_server=_at_appserver_2,
#     interval=1,
#     binary_path="/cygdrive/c/Tools/",
#     interface_name="Ethernet 9",
#     server_close_delay=50,
#     version=2,
#     dt_from_uepc=True,
# )

# _at_2 = TafUeAt(
#     proxy_mngr_port=9955,
#     ueproxy_force_release=True,
#     com_port="50",
#     serial_number="57e5338",
#     ue_pc_address="10.68.86.240",
#     ue_pc_login="mn5gran",
#     ue_pc_password="nokia123@",
#     ue_pc_expected_prompt="$",
#     data_transfer=[_at_data_transfer_2],
#     phone_number="",
#     imei="",
#     imsi="",
#     capabilities=["REAL_QUALCOMM2", "qualcomm"],
# )

# CI_Detail_UE_Type='Nokia FastMile Receiver 5Gmm28-A'
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.246",
    user="vrf4_sg4",
    password="vrf4@sg4",
    bind_interface_ip="10.57.191.246",
    expected_prompt="[vrf4_sg4@appserver ~]$ ",
    binary_path="/home/vrf4_sg4/taf_debug/iperf",
    ports=[54420, 54320]
    )

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2
    )

_fastmile_1= TafUeFastmile(
    ue_pc_address='10.57.167.22',
    root_password='Vx,uj@TiCGDTs625',
    default_user_password='G.sXZ!xZWVq@HrE,',
    ue_manage_ip='10.101.37.37',
    data_transfer=[_fastmile_data_transfer_1],
    serial_number='LPL2443001F9',
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version='Receiver 5Gmm28-A',
    capabilities=['REAL_FASTMILE_UE1', 'nokia_fastmile']
    )

_fastmile_appserver_2 = TafUeAppServer(
    app_server_name="APP_SERVER_2",
    address="10.57.191.246",
    user="vrf4_sg4",
    password="vrf4@sg4",
    bind_interface_ip="10.57.191.246",
    expected_prompt="[vrf4_sg4@appserver ~]$ ",
    binary_path="/home/vrf4_sg4/taf_debug/iperf",
    ports=[53800, 54700],
    )

_fastmile_data_transfer_2 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_2,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_2= TafUeFastmile(
    ue_pc_address='10.57.167.22',
    root_password='iVdS:6ERmQXHM+=q',
    default_user_password='Km72!6ZymbgfuaVy',
    ue_manage_ip='10.68.89.42',
    data_transfer=[_fastmile_data_transfer_2],
    serial_number='LPL244400042',
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version='Receiver 5Gmm28-A',
    capabilities=['REAL_FASTMILE_UE2', 'nokia_fastmile']
    )


tl = TestLine(
    test_pc=_test_pc,
    test_pcs=[_test_pc],
    gnbs=[_classical_bts, _classical_bts_tl578],
    enbs=[],
    core=RealCore(mcc=262, mnc=3),
    mcses=[_topyoung_mcs],
    # ues=[_at_1, _at_2],
    ues=[_fastmile_1, _fastmile_2],
    tl_cloud_topology=_tl_cloud_topology
)
