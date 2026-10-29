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

__maintainer__ = "Gaofan Shi"  # TL owner name
__team__ = "I_NSB_MN_RAN_RD_VRF_HAZ4_04_01@internal.nsn.com"  # TL owner's team
__email__ = "gaofan.shi@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# 5GRU for classicalBTS
_ru_pdu = HBTE(addr="10.101.45.116", port_numbers=[1])

_ru_lmi_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.86.89", username="mn5gran", password="nokia123@"
    )
)

_ru_lmi = LMI(product_code="",
              host=_ru_lmi_pc,
              uart_mapping=[Local(port="COM5"), Local(port="COM4")])

_ru = RU(
    ru_hw_group="AVHQA",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.2",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.89", username="mn5gran", password="nokia123@"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AVHQA.value,
    serial_number="1M251000678",
    lmi=_ru_lmi
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20", hardware_type="ABIP", rus=[_ru])
_gnb_pdu = HBTE(addr="10.101.45.115", port_numbers=[8])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[8],
    hardware_type="ASIM",)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.101.50.80")

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.101.50.80",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.101.50.65/27"),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.50.80", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.50.80", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.101.50.80",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.101.50.65/27"),
    ),
    x2u=NetworkAddress(
        v4="10.101.50.80",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.101.50.65/27"),
    ),
    s1u=NetworkAddress(
        v4="10.101.50.80",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.101.50.65/27"),
    ),
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_QC_SA_ASIMR_ABIPB4_AVHQA"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=536870831, global_bts_id=536870831)

# test pc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.46", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

# CI_Detail_UE_Type='Nokia FastMile Receiver 5Gmm28-B'
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.246",
    user="vrf4_sg4",
    password="vrf4@sg4",
    bind_interface_ip="10.57.191.246",
    expected_prompt="[vrf4_sg4@appserver ~]$ ",
    binary_path="/home/vrf4_sg4/taf_debug/iperf",
    ports=[54425, 54325]
    )

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2
    )

_fastmile_1= TafUeFastmile(
    ue_pc_address='10.57.155.97',
    root_password='HmYnpvJwitzDM6:3',
    default_user_password='myknU.wGkL.Dqt!Z',
    ue_manage_ip='10.101.39.203',
    data_transfer=[_fastmile_data_transfer_1],
    serial_number='LPL24440008D',
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
    ports=[53810, 54710],
    )

_fastmile_data_transfer_2 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_2,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_2= TafUeFastmile(
    ue_pc_address='10.57.155.97',
    root_password='c!y=vY.X:fsVyqSA',
    default_user_password='J,qQJFkHRRHF6Tze',
    ue_manage_ip='10.101.39.204',
    data_transfer=[_fastmile_data_transfer_2],
    serial_number='LPL243600015',
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version='Receiver 5Gmm28-A',
    capabilities=['REAL_FASTMILE_UE2', 'nokia_fastmile']
    )

tl = TestLine(
    test_pc=_test_pc,
    test_pcs=[_test_pc],
    gnbs=[_classical_bts],
    core=RealCore(mcc=262, mnc=3),
    ues=[_fastmile_1, _fastmile_2],
    tl_cloud_topology=_tl_cloud_topology
)
