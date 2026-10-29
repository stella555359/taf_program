import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim
from taf.config.testline import RU, DU
from taf.config.testline.pdu import HBTE
from taf.config.testline.pdu import TopYoung
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
from taf.config.testline.attenuator import AttenuationPort
from taf.config.testline.appserver import AppServer
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer

__maintainer__ = "Li Mengting"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_04_01_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_04_01@internal.nsn.com>"  # TL owner's team
__email__ = "mengting.li@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# 5GRU for classicalBTS

_ru1_pdu = HBTE(addr="10.68.87.116", port_numbers=[2])

_ru1 = RU(
    ru_hw_group="AVQC",
    serial_number="1M235231332",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.15", username="nokia5G", password="noki@123"
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AVQC,
)

_ru2_pdu = HBTE(addr="10.68.87.113", port_numbers=[2])

_ru2 = RU(
    ru_hw_group="AVQC",
    serial_number="1M242100014",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0=",
    ),
    lmp_connection=SshServiceDetails(
        addr="0.0.0.0", username="nokia5G", password="noki@123"
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AVQC,
)

_ru3_pdu = HBTE(addr="10.68.87.113", port_numbers=[5])

_ru3 = RU(
    ru_hw_group="AVQC",
    serial_number="1M242100004",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0=",
    ),
    lmp_connection=SshServiceDetails(
        addr="0.0.0.0", username="nokia5G", password="noki@123"
    ),
    pdu_port=_ru3_pdu.pdu_ports[5],
    radio_type=RadioTypes.AVQC,
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_lmp_connection_1 = SshServiceDetails(
    addr="0.0.0.0", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.68.87.114", port_numbers=[2])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.15", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
    test_pc=_gnb_test_pc_0,
)

_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3],
    f1_m_ip_addr="10.68.89.40",
)

# CU
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.89.40", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.89.40", username="Nemuadmin", password="nemuuser"
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.71.213.137", username="toor4nsn", password="oZPS0POrRieRtu"
)
_lmp_connection_enb2 = SshServiceDetails(
    addr="10.71.213.137", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = HBTE(addr="10.68.87.114", port_numbers=[2])
_enb_pdu2 = HBTE(addr="10.68.87.114", port_numbers=[2])
# enbPC
_enb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.48", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
)
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[2],
    test_pc=_enb_test_pc_0,
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(
        system_module=_real_enb,
        airscale=_real_enb, 
        rms=None,
        oam_ip=NetworkAddress(
        v4="10.71.213.137"),    # eNB BTS MPLANE
        )

# enbPC
_enb_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.48", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[_lte_real_enb],
)

# cloud_topology
_tl_cloud_topology = "I&V-HGZ-TL570"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=570, global_bts_id=570)

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.15", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[_classical_bts],
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.163.51", username="cmw_sg4", password="Zvmsg04_159357!", port=53570
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.51",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port=54570,
)

_appserver = AppServer(_iperf)

# CI_Detail_UE_Type='Huawei Honor 30s;Huawei Honor 30s'
_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.135", username="nokia5G", password="noki@123"
    ),
    serial_number="QKX4C20616002444",  #"9EQUT20903003330", '9YS0220103005528',##'L8K5T19919002146',#QKX4C20616002865
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["SG4_HONOR30s", "cell_Mapping: [511]", "huawei"],
)

# CI_Detail_UE_Type='Nokia FastMile 5G Gateway 3.2'
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.163.51",
    user="cmw_sg4",
    password="Zvmsg04_159357!",
    bind_interface_ip="10.57.163.51",
    expected_prompt="[cmw_sg4@smw_sg4 ~]$ ",
    binary_path="/home/cmw_sg4/taf_debug/iperf",
    ports=[53570, 54570],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    com_port="3",
    ue_pc_address="10.57.159.15",
    root_password="2afa7e62fd25",
    ue_manage_ip="10.71.205.210",
    serial_number="LPL2214004ED",
    data_transfer=[_fastmile_data_transfer_1],
    ue_pc_port=5555,
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
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

# _attenuator = TopYoung(ip_addr="x.x.x.x", port=23, attenuation_port_numbers=[7, 8])

tl = TestLine(
    test_pc=_host,
    test_pcs=[_host,_enb_pc],
    gnbs=[_classical_bts],
    # enbs=[_lte_real_enb],
    # core=RealCore(mcc=262, mnc=3),
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_fastmile_1],
    # attenuator=_attenuator,
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
    appserver=_appserver,
)
