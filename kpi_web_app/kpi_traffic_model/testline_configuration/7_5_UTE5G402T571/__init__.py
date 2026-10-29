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

__maintainer__ = "Fan Geyou"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_04_01_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_04_01@internal.nsn.com>"  # TL owner's team
__email__ = "geyou.fan@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.100", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS
_ru_pdu = HBTE(addr="10.57.241.225", port_numbers=[3])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[3],
    radio_type=RadioTypes.AZHA,
)

_ru1_pdu = HBTE(addr="10.57.241.225", port_numbers=[1])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[1],
    radio_type=RadioTypes.AZHA,
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.57.241.197", port_numbers=[2])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru, _ru1], f1_m_ip_addr="10.57.229.133")

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.57.229.133",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.229.129", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.229.133", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.229.133", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.57.229.133",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.229.129", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.57.229.133",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.229.129", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.57.229.133",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.229.129", ip_prefix_length=27),
    ),
)


# cloud_topology
_tl_cloud_topology = "I&V-HGZ-TL571"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=571, global_bts_id=571)

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

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.57.237.144", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = HBTE(addr="10.57.241.224", port_numbers=[1])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[1],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    core=RealCore(mcc=262, mnc=3),
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.163.51", username="cmw_sg4", password="Zvmsg04_159357!"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.51",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port=54005,
)
_appserver = AppServer(_iperf)
_appserver.iperf_details.port = 54905

_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.20", username="nokia5G", password="noki@123"
    ),
    serial_number="L8K5T19919002146",  #'9YS0220103005528',##'L8K5T19919002146','QKX4C20415011221'
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["SG4_Mate20X", "huawei"],
    # serial_com='12',
    # reset_interface='no',
    # enable_disable_cfun='yes',
    # processes_to_kill=['ttermpro', 'ATCom'],
    # ue_class = 'QualcommNoLicenseUe',
    # turn_off_on_firewall='yes',
    # diag_com='10',
    # iperf_directory ='adb shell /data/iperf'
)

_ue2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.20", username="nokia5G", password="noki@123"
    ),
    serial_number="QKXUT20519006565",  #'9YS0220103005528',##'L8K5T19919002146',
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["SG4_HONOR30s", "huawei"],
    # serial_com='12',
    # reset_interface='no',
    # enable_disable_cfun='yes',
    # processes_to_kill=['ttermpro', 'ATCom'],
    # ue_class = 'QualcommNoLicenseUe',
    # turn_off_on_firewall='yes',
    # diag_com='10',
    # iperf_directory ='adb shell /data/iperf'
)
