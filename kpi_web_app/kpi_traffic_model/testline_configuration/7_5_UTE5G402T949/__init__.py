import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.optical_switch import Calient
from taf.config.testline.pdu import HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
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
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline.pdu import HBTE, TopYoung
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer


__maintainer__ = "zhulinghui"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_08_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_08@internal.nsn.com>"
__email__ = "linghui.zhu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_optical_switch = Calient(
    addr="10.71.204.85", model="S320", port=3083, username="admin", password="pxc***"
)

_attenuator = AHBTE(
    ip_addr="10.101.51.41",
    port=5000,
    attenuation_port_numbers=[13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)
# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.113", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# epcsim
_epc_sim = EPCSim(
    mme_ip="10.110.66.198",
    mcc="262",
    mnc="3",
    tac="270",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.70.112.199", username="test", password="NOKIA123"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)

_mtk_appserver_ssh = SshServiceDetails(
    addr="10.57.191.239",
    username="vrf3_sg8",
    password="vrf3@sg8",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_mtk_appserver_ssh,
    network_interface_address="10.57.191.239",
    iperf_path="iperf",
    port=48020,
)

_appserver = AppServer(_iperf_details_on_appserver)
# for FastMile CPE 1
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name='APP_SERVER_2',
    address='10.57.191.239',
    user='vrf3_sg8',
    password='vrf3@sg8',
    bind_interface_ip='10.57.191.239',
    expected_prompt='[vrf3_sg8@APPServer-3 ~]$ ',
    binary_path='/usr/bin/iperf',
    ports=[48020, 48021])

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name='iperf',
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path='iperf',
    version=2)

_fastmile_1= TafUeFastmile(
    com_port='4',
    ue_pc_address='10.71.217.26',
    root_password='7c4a5282aad6',
    ue_manage_ip='192.168.1.1',
    serial_number='LPL22140053B',
    data_transfer=[_fastmile_data_transfer_1],
    ue_pc_port=5555,
    version='3.2',
    capabilities=['REAL_FASTMILE_UE1', 'nokia_fastmile'])

# 5GRU for classicalBTS RU PB
_ru_pdu = HBTE(addr="10.71.195.211", port_numbers=[6])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    pdu_port=_ru_pdu.pdu_ports[6],
    radio_type=RadioTypes.AZQC,
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.71.210.217", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = TopYoung(addr="10.71.195.214", port_numbers=[2])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
    hardware_type="ASIL",
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.71.210.217")

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.210.217",
        routing=RoutingInformation(gateway="10.71.210.193", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.210.217", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.210.217", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.210.217",
        routing=RoutingInformation(gateway="10.71.210.193", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.71.210.217",
        routing=RoutingInformation(gateway="10.71.210.193", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.71.210.217",
        routing=RoutingInformation(gateway="10.71.210.193", ip_prefix_length=27),
    ),
)

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=949, global_bts_id=1109)


tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    appserver=_appserver,
    ues=[_fastmile_1],
    core=_epc_sim,
    attenuator=_attenuator,
    optical_switches=[_optical_switch],
)
