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
_ru_pdu = HBTE(addr="10.101.45.130", port_numbers=[4])

_ru = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.31.33", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu.pdu_ports[4],
    radio_type=RadioTypes.AEQK,
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.101.50.136", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.22")

_gnb_pdu = HBTE(addr="10.101.45.132", port_numbers=[5])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.101.50.136")

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.101.50.136",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.101.50.129", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.50.136", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.50.136", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.101.50.136",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.101.50.129", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.101.50.136",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.101.50.129", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.101.50.136",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.101.50.129", ip_prefix_length=27),
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.101.40.36", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = HBTE(addr="10.101.45.130", port_numbers=[3])

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[3],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIKL_ABILB1_AEQK"

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="2581", global_bts_id="2581"
)


_appserver_ssh = SshServiceDetails(
    addr="10.57.191.247", username="vrf4_sg5", password="vrf4@sg5", port="55945"
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
