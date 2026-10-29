import re
import os
import yaml
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
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
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeAndroid
from taf.config.testline.testpc import TestPc, Connection

__maintainer__ = "Shi Zhihao"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_04_01_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_04_01@internal.nsn.com>"  # TL owner's team
__email__ = "zhihao.shi@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# 5GRU for classicalBTS
_ru_pdu = TopYoung(addr="10.71.196.170", port_numbers=[4])

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
    pdu_port=_ru_pdu.pdu_ports[4],
    radio_type=RadioTypes.AZNA,
)

_ru1_pdu = TopYoung(addr="10.71.196.170", port_numbers=[3])

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
    pdu_port=_ru1_pdu.pdu_ports[3],
    radio_type=RadioTypes.AZNA,
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20", hardware_type="ABIO")
_gnb_pdu = HBTE(addr="10.71.196.165", port_numbers=[3])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
    hardware_type="ASIL",
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru, _ru1], f1_m_ip_addr="10.71.213.104")

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.213.104",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.71.213.97/28"),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.213.104", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.213.104", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.213.104",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.71.213.97/28"),
    ),
    x2u=NetworkAddress(
        v4="10.71.213.104",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.71.213.97/28"),
    ),
    s1u=NetworkAddress(
        v4="10.71.213.104",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.71.213.97/28"),
    ),
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASILL_ABIOB1_2xAZNA_ENB"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=602, global_bts_id=602)

# CI_Detail_UE_Type='Samsung Galaxy S21'
_app_server_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.71.207.151",
    user="vrf4_sg4",
    password="vrf4@sg4",
    bind_interface_ip="10.71.207.151",
    expected_prompt="[vrf4_sg4@appserver ~]$ ",
    binary_path="/home/vrf4_sg4/taf_debug/iperf",
    ports=[54603, 54604],
)
 
_data_transfer_iperf_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_app_server_1,
    interface_name="rmnet0",
    interval=1,
    version=2,
)


_android1 = TafUeAndroid(serial_number='RFCR110GENL',
                         ue_pc_address='10.71.217.143',
                         data_transfer=[_data_transfer_iperf_1],
                         ue_pc_port='5555',
                         imei='352454780520006',
                         imsi='357926910520001',
                         qualcomm_prototype=True,
                         service_call_attach='17',
                         service_call_detach='17',
                         capabilities=["REAL_ANDROID_UE1", "samsung_ue"])

# test pc
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.34", username="ute", password="uteUTE!"
    ),
    connections=[Connection(interface="eth1", device=_classical_bts.dus[0].airscale.common_units[0], interface_type="lmp")],
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

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.71.213.105", username="toor4nsn", password="oZPS0POrRieRtu"
)

# 4GDU for RealEnb
_enb_pdu = HBTE(addr="10.71.196.165", port_numbers=[4])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[4],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    ues=[
        _android1,
    ],
    enbs=[_lte_real_enb],
    core=RealCore(mcc=262, mnc=3),
    tl_cloud_topology=_tl_cloud_topology,
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
)
