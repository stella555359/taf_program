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
from taf.config.testline.pdu import HBTE, TopYoung
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import Android
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.gnb.du import Cablink, Endpoint
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
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer

__maintainer__ = "Zhihao Shi"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_04_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_04@internal.nsn.com>"  # TL owner's team
__email__ = "zhihao.shi@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# 5GRU for classicalBTS
_ru_pdu = TopYoung(addr="10.71.196.118", port_numbers=[3])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.49",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.218.38", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEQY,
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.71.196.116", port_numbers=[4])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru, label="SFP", port_id=1),
    )
]

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[4],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.71.212.212", cablinks=_ru_cablinks
)

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.212.212",
        vlan_id=1,
        routing_v4=RoutingInformation(gateway="10.57.223.129/27"),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.212.212", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.212.212", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.212.212",
        vlan_id=1,
        routing_v4=RoutingInformation(gateway="10.57.223.129/27"),
    ),
    x2u=NetworkAddress(
        v4="10.71.212.212",
        vlan_id=1,
        routing_v4=RoutingInformation(gateway="10.57.223.129/27"),
    ),
    s1u=NetworkAddress(
        v4="10.71.212.212",
        vlan_id=1,
        routing_v4=RoutingInformation(gateway="10.57.223.129/27"),
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.71.212.213", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = HBTE(addr="10.71.196.116", port_numbers=[4])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[4],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIKL_ABILB1_AEQY"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=577, global_bts_id=577)

# test pc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.99", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.132", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[_lte_real_enb],
)

# _iperf_2 = IperfDataTransferDetails(
#    ssh_connection_details=_appserver_ssh,
#    network_interface_address="10.57.163.51",
#    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
#    port=54578,
# )

# CI_Detail_UE_Type='Nokia FastMile 5G Gateway 3.1'
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.71.219.232",
    user="cmw_sg4",
    password="Zvmsg04_159357!",
    bind_interface_ip="10.71.219.232",
    expected_prompt="[cmw_sg4@appserver ~]$ ",
    binary_path="/home/cmw_sg4/taf_debug/iperf",
    ports=[53577,54577],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_ue1 = TafUeFastmile(
    ue_pc_address='10.57.167.99',
    root_password='2d4ab6b2a864',
    ue_manage_ip='10.71.212.217',
    serial_number='LPL2214004D9',
    version='3.2',
    data_transfer=[_fastmile_data_transfer_1],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"]
)

# CI_Detail_UE_Type='Huawei Honor 30s'
#_ue1 = Android(
#    ssh_connection_details=SshServiceDetails(
#        addr="10.71.217.245", username="nokia5G", password="noki@123"
#    ),
#    serial_number="QKX4C20616002722",  #'9YS0220103005528',##'L8K5T19919002146','QKX4C20415011221'
#    server_dir="/cygdrive/c/pyro_server",
#    python_path="/cygdrive/c/Python27/python.exe",
#    iperf_details=_iperf,
#    capabilities=["SG4_HONOR30s", "cell_Mapping: [1]", "huawei"],
#)

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

tl = TestLine(
    test_pc=_test_pc,
    test_pcs=[_test_pc, _test_pc_enb],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    core=RealCore(mcc=262, mnc=3),
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_ue1],
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
)
