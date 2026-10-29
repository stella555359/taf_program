import re
import os
import yaml
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim
from taf.config.testline.core import RealCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import HBTE, TopYoung
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import Qualcomm
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
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile

__maintainer__ = "Shi Zhihao"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_04_01_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_04_01@internal.nsn.com>"  # TL owner's team
__email__ = "zhihao.shi@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.198", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS
_ru_pdu = TopYoung(addr="10.71.196.168", port_numbers=[6])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53",
        username="root",
        password="ZCS81C3RIAZegZtvIn43EaAdA4oMSNFkSBrj4iMwTuI=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[6],
    radio_type=RadioTypes.AZNA,
)

_ru1_pdu = TopYoung(addr="10.71.196.171", port_numbers=[2])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52",
        username="root",
        password="ZCS81C3RIAZegZtvIn43EaAdA4oMSNFkSBrj4iMwTuI=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AZHA,
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.71.196.163", port_numbers=[1])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru, _ru1], f1_m_ip_addr="10.71.213.107")

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.213.107",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.71.213.97/28"),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.213.107", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.213.107", username="Nemuadmin", password="nemuuser"
    ),
)


# cloud_topology
_tl_cloud_topology = "I&V-HGZ-TL604"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=604, global_bts_id=604)

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

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.71.213.109", username="toor4nsn", password="oZPS0POrRieRtu"
)

# ASIA for RealEnb
_enb_pdu = HBTE(addr="10.71.196.163", port_numbers=[2])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[2],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# CI_Detail_UE_Type='Nokia FastMile 5G Receiver 5G19-A'
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.71.207.151",
    user="vrf4_sg4",
    password="vrf4@sg4",
    bind_interface_ip="10.71.207.151",
    expected_prompt="[vrf4_sg4@appserver ~]$ ",
    binary_path="/home/vrf4_sg4/taf_debug/iperf",
    ports=[53604, 54604],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    ue_pc_address='10.57.167.198',
    root_password='aS9DMJ.5ShSNg,ug',
    default_user_password='7UH-6-T7nQxVQ.ZQ',
    ue_manage_ip='10.71.213.111',
    serial_number='KLT234301906',
    version='receiver 5g19a',
    data_transfer=[_fastmile_data_transfer_1],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
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
    ports=[54664,54777],
)

_fastmile_data_transfer_2 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_2,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_2 = TafUeFastmile(
    ue_pc_address='10.57.177.38',
    root_password='X7qWz-eho2pPi3sT',
    default_user_password='eTMZ5Ye2wvXeZiCZ',
    ue_manage_ip='10.71.205.103',
    serial_number='LPL241800A40',
    version='receiver 5g26a',
    data_transfer=[_fastmile_data_transfer_2],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"]
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    ues=[_fastmile_1, _fastmile_2],
    enbs=[_lte_real_enb],
    core=RealCore(mcc=262, mnc=3),
    tl_cloud_topology=_tl_cloud_topology,
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
)
