import os
import yaml
import re
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import RealCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import HBTE
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
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import AppServer

from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc

__maintainer__ = "Qingqing Wang"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_08_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_08@internal.nsn.com>"
__email__ = "qingqing.wang.1@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# NR
_attenuator = AHBTE(
    ip_addr="10.71.204.67",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.200", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS RU PB
_ru_pdu1 = HBTE(addr="10.71.195.184", port_numbers=[2])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.64.2",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    pdu_port=_ru_pdu1.pdu_ports[2],
    radio_type=RadioTypes.AZQC,
)

_ru_pdu2 = HBTE(addr="10.71.195.184", port_numbers=[1])

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.64.2",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    pdu_port=_ru_pdu2.pdu_ports[1],
    radio_type=RadioTypes.AZQC,
)

_ru_pdu3 = HBTE(addr="10.71.195.184", port_numbers=[3])

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.64.2",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    pdu_port=_ru_pdu3.pdu_ports[3],
    radio_type=RadioTypes.AZQC,
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.101.51.42", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.71.195.187", port_numbers=[4])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[4],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru1, _ru2, _ru3], f1_m_ip_addr="10.101.51.42")

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.101.51.42",
        routing=RoutingInformation(gateway="10.101.51.33", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.51.42", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.51.42", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.101.51.42",
        routing=RoutingInformation(gateway="10.101.51.33", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.101.51.42",
        routing=RoutingInformation(gateway="10.101.51.33", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.101.51.42",
        routing=RoutingInformation(gateway="10.101.51.33", ip_prefix_length=27),
    ),
)

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=995, global_bts_id=995)

_appserver_ssh = SshServiceDetails(
    addr="10.57.173.234",
    username="vrf3_sg8",
    password="vrf3@sg8",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.173.234",
    iperf_path="iperf",
    port=48999,
)

_appserver = AppServer(_iperf_details_on_appserver)

# for FastMile CPE 1
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name='APP_SERVER_2',
    address='10.57.173.234',
    user='vrf3_sg8',
    password='vrf3@sg8',
    bind_interface_ip='10.57.173.234',
    expected_prompt='[vrf3_sg8@APPServer-3 ~]$ ',
    binary_path='/usr/bin/iperf',
    ports=[48015, 48403])

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name='iperf',
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path='iperf',
    version=2)

_fastmile_1= TafUeFastmile(
    com_port='56',
    ue_pc_address='10.71.217.104',
    root_password='6ada575253fb',
    ue_manage_ip='192.168.1.1',
    serial_number='',
    data_transfer=[_fastmile_data_transfer_1],
    ue_pc_port=5555,
    version='3.2',
    capabilities=['REAL_FASTMILE_UE2', 'nokia_fastmile'])

# for FastMile CPE 2
_fastmile_appserver_2 = TafUeAppServer(
    app_server_name='APP_SERVER_2',
    address='10.57.173.234',
    user='vrf3_sg8',
    password='vrf3@sg8',
    bind_interface_ip='10.57.173.234',
    expected_prompt='[vrf3_sg8@APPServer-3 ~]$ ',
    binary_path='/usr/bin/iperf',
    ports=[58014, 58402])

_fastmile_data_transfer_2 = TafUeDataTransferProtocol(
    protocol_name='iperf',
    app_server=_fastmile_appserver_2,
    interval=1,
    binary_path='iperf',
    version=2)

_fastmile_2= TafUeFastmile(
    com_port='4',
    ue_pc_address='10.71.217.65',
    root_password='e87a47326535',
    ue_manage_ip='192.168.1.1',
    serial_number='',
    data_transfer=[_fastmile_data_transfer_2],
    ue_pc_port=5555,
    version='3.2',
    capabilities=['REAL_FASTMILE_UE1', 'nokia_fastmile'])

# for FastMile CPE 3
_fastmile_appserver_3 = TafUeAppServer(
    app_server_name='APP_SERVER_2',
    address='10.57.173.234',
    user='cmw_sg8',
    password='Bestcm@8',
    bind_interface_ip='10.57.173.234',
    expected_prompt='[cmw_sg8@APPServer-3 ~]$ ',
    binary_path='/usr/bin/iperf',
    ports=[58016, 58404])

_fastmile_data_transfer_3 = TafUeDataTransferProtocol(
    protocol_name='iperf',
    app_server=_fastmile_appserver_3,
    interval=1,
    binary_path='iperf',
    version=2)

_fastmile_3= TafUeFastmile(
    com_port='7',
    ue_pc_address='10.71.217.38',
    root_password='cccab7b2ffa3',
    ue_manage_ip='192.168.1.1',
    serial_number='',
    data_transfer=[_fastmile_data_transfer_3],
    ue_pc_port=5555,
    version='3.2',
    capabilities=['REAL_FASTMILE_UE3', 'nokia_fastmile'])

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    appserver=_appserver,
    ues=[_fastmile_1, _fastmile_2, _fastmile_3],
    core=RealCore(mcc=262, mnc=3),
    attenuator=[_attenuator],
)
