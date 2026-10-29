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
from taf.config.testline.pdu import HBTE
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
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import AppServer

__maintainer__ = "Shi Zhihao"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_04_01_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_04_01@internal.nsn.com>"  # TL owner's team
__email__ = "zhihao.shi@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.199", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS
_ru_pdu = HBTE(addr="10.101.45.100", port_numbers=[6])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.2",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[6],
    radio_type=RadioTypes.AQQY,
)

_ru1_pdu = HBTE(addr="10.101.45.100", port_numbers=[5])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.2",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[5],
    radio_type=RadioTypes.AQQY,
)

_ru2_pdu = HBTE(addr="10.101.45.100", port_numbers=[4])

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.2",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[4],
    radio_type=RadioTypes.AQQA,
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.101.45.113", port_numbers=[2])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru, _ru1, _ru2], f1_m_ip_addr="10.101.50.78")

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.101.50.78",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.101.50.65/27"),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.50.78", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.50.78", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.101.50.78",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.101.50.65/27"),
    ),
    x2u=NetworkAddress(
        v4="10.101.50.78",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.101.50.65/27"),
    ),
    s1u=NetworkAddress(
        v4="10.101.50.78",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.101.50.65/27"),
    ),
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.163.51",
    username="cmw_sg4",
    password="Zvmsg04_159357!",
    port=54589,
)

_appserver_ssh_2 = SshServiceDetails(
    addr="10.57.163.51",
    username="cmw_sg4",
    password="Zvmsg04_159357!",
    port=54706,
)

_appserver_ssh_3 = SshServiceDetails(
    addr="10.57.163.51",
    username="cmw_sg4",
    password="Zvmsg04_159357!",
    port=54707,
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.51",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port=53589,
)

_iperf_2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_2,
    network_interface_address="10.57.163.51",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port=53706,
)

_iperf_3 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_3,
    network_interface_address="10.57.163.51",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port=53707,
)

_appserver = AppServer(_iperf)

# CI_Detail_UE_Type='Nokia FastMile 5G Gateway 3.1'
ue_config_path = os.path.join(_cfg_dir, "TestData/ue.yml")
if os.path.isfile(ue_config_path):
    with open(ue_config_path) as f:
        _ue_read = f.read()
        qci_port = re.findall("(_iperf.*?port)", _ue_read)
        for item in qci_port:
            _ue_read = _ue_read.replace(item, str(eval(item)))
        _ue_config = yaml.load(_ue_read, Loader=yaml.FullLoader)
else:
    _ue_config = ""

# RealEnb

# cloud_topology
_tl_cloud_topology = "I&V-HGZ-TL589"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=589, global_bts_id=589)

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

_attenuator = TopYoung(ip_addr="x.x.x.x", port=23, attenuation_port_numbers=[7, 8])

_core = RealCore(mcc=262, mnc=3)
_core.default_ssh_connection_details = SshServiceDetails(
    addr="", username="", password=""
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_core,
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_ue_config],
    attenuator=_attenuator,
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
)
