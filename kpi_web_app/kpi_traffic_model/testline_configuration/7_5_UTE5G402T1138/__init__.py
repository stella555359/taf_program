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

_attenuator = AHBTE(
    ip_addr="10.71.210.210",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4],
    model="PA-16-16-6-127-0.5-B-S",
)
# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.24", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS RU PB
_ru_pdu = HBTE(addr="10.71.195.211", port_numbers=[1])

_ru = RU(
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
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AZQC,
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.101.50.50", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.71.195.215", port_numbers=[7])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[7],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.101.50.50")

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.101.50.50",
        routing=RoutingInformation(gateway="10.71.210.97", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.50.50", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.50.50", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.101.50.50",
        routing=RoutingInformation(gateway="10.71.210.97", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.71.210.105",
        routing=RoutingInformation(gateway="10.71.210.97", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.101.50.50",
        routing=RoutingInformation(gateway="10.71.210.97", ip_prefix_length=27),
    ),
)

# RealEnb  enb&enb_HBTE ip_addr
_lmp_connection_enb = SshServiceDetails(
    addr="10.101.51.43", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = HBTE(addr="10.68.87.125", port_numbers=[6])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[6],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb)

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=998, global_bts_id=1130)

_appserver_ssh = SshServiceDetails(
    addr="10.70.222.52",
    username="cmw_sg8",
    password="Bestcm@8",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.70.222.52",
    iperf_path="iperf",
    port=58999,
)

_appserver = AppServer(_iperf_details_on_appserver)

# for FastMile CPE
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name='APP_SERVER_2',
    address='10.70.222.52',
    user='cmw_sg8',
    password='Bestcm@8',
    bind_interface_ip='10.70.222.52',
    expected_prompt='[cmw_sg8@APPServer-3 ~]$ ',
    binary_path='/usr/bin/iperf',
    ports=[58002, 58488])

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name='iperf',
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path='iperf',
    version=2)

_fastmile_1= TafUeFastmile(
    com_port='12',
    ue_pc_address='10.71.218.198',
    root_password='5caa68c27dba',
    ue_manage_ip='192.168.1.1',
    serial_number='',
    data_transfer=[_fastmile_data_transfer_1],
    ue_pc_port=5555,
    version='3.2',
    capabilities=['REAL_FASTMILE_UE1', 'nokia_fastmile'])

_fastmile_appserver_2 = TafUeAppServer(
    app_server_name='APP_SERVER_2',
    address='10.70.222.52',
    user='cmw_sg8',
    password='Bestcm@8',
    bind_interface_ip='10.70.222.52',
    expected_prompt='[cmw_sg8@APPServer-3 ~]$ ',
    binary_path='/usr/bin/iperf',
    ports=[58002, 58488])

_fastmile_data_transfer_2 = TafUeDataTransferProtocol(
    protocol_name='iperf',
    app_server=_fastmile_appserver_2,
    interval=1,
    binary_path='iperf',
    version=2)

_fastmile_2= TafUeFastmile(
    com_port='3',
    ue_pc_address='10.71.218.199',
    root_password='b5bab572e852',
    ue_manage_ip='192.168.1.1',
    serial_number='',
    data_transfer=[_fastmile_data_transfer_2],
    ue_pc_port=5555,
    version='3.2',
    capabilities=['REAL_FASTMILE_UE2', 'nokia_fastmile'])

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    appserver=_appserver,
    ues=[_fastmile_1, _fastmile_2],
    core=RealCore(mcc=262, mnc=3),
    attenuator=_attenuator,
)
