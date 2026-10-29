import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.testpc import Connection
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
from taf.config.testline.pdn import PDNTafUeAndroidDetails
from taf.config.testline.ue import TafUeFastmile, TafUeAndroid
from taf.config.testline.appserver import TafUeAppServer

__maintainer__ = "Li Mengting"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_04_01_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_04_01@internal.nsn.com>"  # TL owner's team
__email__ = "mengting.li@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# 5GRU for classicalBTS

_ru1_pdu = HBTE(addr="10.71.196.164", port_numbers=[6])

_ru1 = RU(
    ru_hw_group="AQQA",
    serial_number="DH241823207",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.0.176.45", username="nokia5g", password="noki@123"
    ),
    pdu_port=_ru1_pdu.pdu_ports[6],
    radio_type=RadioTypes.AVQC,
)

_ru2_pdu = HBTE(addr="10.71.196.171", port_numbers=[3])

_ru2 = RU(
    ru_hw_group="AHEGB",
    serial_number="EA221152116",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="root",
        password="root",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.218.231", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru2_pdu.pdu_ports[3],
    radio_type=RadioTypes.AHEGB,
)

_ru3_pdu = HBTE(addr="10.71.196.164", port_numbers=[5])

_ru3 = RU(
    ru_hw_group="AQQA",
    serial_number="1M230801935",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.218.37", username="nokia5g", password="noki@123"
    ),
    pdu_port=_ru3_pdu.pdu_ports[5],
    radio_type=RadioTypes.AQQA,
)

_ru4_pdu = HBTE(addr="10.71.196.171", port_numbers=[4])

_ru4 = RU(
    ru_hw_group="AQQA",
    serial_number="1M230801936",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", 
        username="serviceuser", 
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY="
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="root", password="umniedziala"
    ),
    pdu_port=_ru4_pdu.pdu_ports[4],
    radio_type=RadioTypes.AQQA,
)

_ru5_pdu = HBTE(addr="10.71.196.171", port_numbers=[1])

_ru5 = RU(
    ru_hw_group="AHEGB",
    serial_number="EA203761511",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="root", password="umniedziala"
    ),
    pdu_port=_ru5_pdu.pdu_ports[1],
    radio_type=RadioTypes.AHEGB,
)

_ru6_pdu = HBTE(addr="10.71.196.170", port_numbers=[2])

_ru6 = RU(
    ru_hw_group="AHEGB",
    serial_number="DH241131451",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="root", password="umniedziala"
    ),
    pdu_port=_ru6_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHEGB,
)
# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_lmp_connection_1 = SshServiceDetails(
    addr="0.0.0.0", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.71.196.173", port_numbers=[1])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.44", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
    test_pc=_gnb_test_pc_0,
)

# _gnb_pdu_1 = TopYoung(addr="10.71.196.172", port_numbers=[5])
# _common_unit_0_1 = CommonUnit(
#     lmp_connection=_lmp_connection_1,
#     capacity_units=[_capacity_unit],
#     pdu_port=_gnb_pdu_1.pdu_ports[5],
# )

_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3,_ru4,_ru5,_ru6],
    f1_m_ip_addr="10.71.213.136",
)

# CU
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.213.136", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.213.136", username="Nemuadmin", password="nemuuser"
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.71.213.137", username="toor4nsn", password="oZPS0POrRieRtu"
)
_lmp_connection_enb2 = SshServiceDetails(
    addr="10.71.213.137", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = HBTE(addr="10.71.196.173", port_numbers=[2])
_enb_pdu2 = HBTE(addr="10.71.196.173", port_numbers=[2])
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
    connections=[
        Connection(
            interface="eth1",
            device=_lte_real_enb.airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

# cloud_topology
_tl_cloud_topology = "I&V-HGZ-TL315"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=315, global_bts_id=315)

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.44", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

# CI_Detail_UE_Type='Samsung s24'
_android_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_2",
    address="10.57.191.246",
    user="vrf4_sg4",
    password="vrf4@sg4",
    bind_interface_ip="10.57.191.246",
    ports=[54610, 54110],
)

_android_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_android_appserver_1,
    interval=1,
    interface_name="rmnet_data0",
    # bind_ue_ip="172.250.188.19",
    server_close_delay=50,
    # version=3,
)

_android_pdn_1 = PDNTafUeAndroidDetails(
    entryName="dxdata1", apnName="dxdata1", apnType=["DEFAULT"]
)

_android_1 = TafUeAndroid(
    serial_number="RFCX217F2AK",
    capabilities=["REAL_ANDROID_UE1", "samsung_ue"],
    ue_pc_address="10.71.217.164",
    ue_pc_port=5555,
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    data_transfer=[_android_data_transfer_1],
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.164", username="mn5gran", password="nokia123@"
    ),
    imei="356388245114573",
    # imsi="262033100015387",
    pdns=[_android_pdn_1],
)

# CI_Detail_UE_Type='Nokia FastMile 5G Gateway 3.2'
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.246",
    user="vrf4_sg4",
    password="vrf4@sg4",
    bind_interface_ip="10.57.191.246",
    expected_prompt="[vrf4_sg4@appserver ~]$ ",
    binary_path="/home/vrf4_sg4/taf_debug/iperf",
    ports=[54315, 54815],
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
    ue_pc_address="10.57.157.44",
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
    test_pcs=[_host, _enb_pc],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    # core=RealCore(mcc=262, mnc=3),
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_fastmile_1, _android_1],
    # attenuator=_attenuator,
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
    # appserver=_appserver,
)
