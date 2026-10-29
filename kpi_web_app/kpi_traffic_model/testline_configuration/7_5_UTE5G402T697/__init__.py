import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import RealCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import HBTE
from taf.config.testline.pdu import TopYoung as PBTopYoung
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

__maintainer__ = "Shasha Liu"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_05_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_05@internal.nsn.com>"  # TL owner's team
__email__ = "shasha.liu@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.130", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS
_ru1_pdu = PBTopYoung(addr="10.71.196.200", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    pdu_port=_ru1_pdu.pdu_ports[6],
    radio_type=RadioTypes.AEQI,
)

_ru2_pdu = PBTopYoung(addr="10.71.196.212", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru2 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.132", username="root", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.33.132", username="root", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru2_pdu.pdu_ports[2],
    radio_type=RadioTypes.AEQE,
)

_ru3_pdu = PBTopYoung(addr="10.71.196.213", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru3 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.130", username="root", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.33.130", username="root", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru3_pdu.pdu_ports[2],
    radio_type=RadioTypes.AWHQV,
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.71.214.3", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.22")

_gnb_pdu = PBTopYoung(addr="10.71.196.211", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru1, _ru2, _ru3], f1_m_ip_addr="10.71.214.3")

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.214.3",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.71.214.1", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.214.3", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.214.3", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.214.3",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.71.214.1", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.71.214.3",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.71.214.1", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.71.214.3",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.71.214.1", ip_prefix_length=27),
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.71.214.2", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = PBTopYoung(addr="10.71.196.211", port_numbers=[6])

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[6],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIKL_ABILB1_AEQK"

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="2597", global_bts_id="2597"
)


_appserver_ssh = SshServiceDetails(
    addr="10.71.207.152", username="vrf4_sg5", password="vrf4@sg5", port="55945"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.247",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port=55949,
)
_appserver = AppServer(_iperf)
_appserver.iperf_details.port = 55949

# CI_Detail_UE_Type='Huawei Honor 30s'

_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.70", username="nokia5G", password="noki@123"
    ),
    serial_number="9EQUT20903003344",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["HONOR30s", "huawei"],
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

_attenuator = TopYoung(ip_addr="x.x.x.x", port=23, attenuation_port_numbers=[7, 8])

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_ue1],
    attenuator=_attenuator,
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
    appserver=_appserver,
)
