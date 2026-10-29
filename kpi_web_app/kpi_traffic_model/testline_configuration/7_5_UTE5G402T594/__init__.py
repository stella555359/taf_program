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
from taf.config.testline.gnb.networkaddress import NetworkAddress
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

from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer

__maintainer__ = "Li Guiqi"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_04_01@internal.nsn.com"  # TL owner's team
__email__ = "guiqi.li@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# 5GRU for classicalBTS
# _enb_ru5_pdu5 = TopYoung(addr="10.71.196.167", port_numbers=[5])
_ru1 = RU(
    ru_hw_group="AHPB",
    serial_number="K9200915867",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    # pdu_port=_enb_ru5_pdu5.pdu_ports[5],
    radio_type=RadioTypes.AHPB,
)
_ru2 = RU(
    ru_hw_group="AVNQA",
    serial_number="EA172612614",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    # pdu_port=_enb_ru5_pdu5.pdu_ports[5],
    radio_type=RadioTypes.AVNQA,
)
_ru3 = RU(
    ru_hw_group="AVNQA",
    serial_number="1M260105636",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    # pdu_port=_enb_ru5_pdu5.pdu_ports[5],
    radio_type=RadioTypes.AVNQA,
)
_ru4 = RU(
    ru_hw_group="AVNQA",
    serial_number="1M260105629",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    # pdu_port=_enb_ru5_pdu5.pdu_ports[5],
    radio_type=RadioTypes.AVNQA,
)
_ru5 = RU(
    ru_hw_group="AREA",
    serial_number="K9243908435",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    # pdu_port=_enb_ru5_pdu5.pdu_ports[5],
    radio_type=RadioTypes.AREA,
)

_ru6 = RU(
    ru_hw_group="ARHA",
    serial_number="1M213115852",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    # pdu_port=_enb_ru5_pdu5.pdu_ports[5],
    radio_type=RadioTypes.ARHA,
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.101.45.113", port_numbers=[4])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.232", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[4],
    test_pc=_gnb_test_pc_0,
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6],
    f1_m_ip_addr="10.101.50.72",
)

# CU
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.50.72", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.50.72", username="Nemuadmin", password="nemuuser"
    ),
)

# RealEnb
_enb_ru5_pdu5 = TopYoung(addr="10.71.196.167", port_numbers=[5])
_enb_ru5 = RU(
    ru_hw_group="FHEB",
    serial_number="EA172612614",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_enb_ru5_pdu5.pdu_ports[5],
    radio_type=RadioTypes.FHEB,
)

_lmp_connection_enb = SshServiceDetails(
    addr="10.101.50.72", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = HBTE(addr="10.101.45.113", port_numbers=[4])
_enb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.232", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
)
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[4],
    test_pc=_enb_test_pc_0,
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(
    airscale=_real_enb,
    system_module=_real_enb,
    oam_ip=NetworkAddress(v4="10.101.50.72"),
    instance_id=11395,
    rms=[]
)

# cloud_topology
_tl_cloud_topology = "I&V-HGZ-T594"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=536870830, global_bts_id=536870830)

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.232", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

# enbPC
_enb_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.49", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_lte_real_enb.airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.246", username="vrf4_sg4", password="vrf4@sg4", port=53599
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.246",
    iperf_path="/home/vrf4_sg4/taf_debug/iperf",
    port=54599,
)


_appserver = AppServer(_iperf)

# CI_Detail_UE_Type='Huawei Honor 30s;Huawei Honor 30s'
_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.94", username="nokia5G", password="noki@123"
    ),
    serial_number="9EQUT20721003474",  #'9YS0220103005528',##'L8K5T19919002146',#'9EQUT20721012224'
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["SG4_Honour30S", "cell_Mapping: [3]", "huawei"],
)

# for FastMile CPE
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name='APP_SERVER_1',
    address='10.57.191.246',
    user='vrf4_sg4',
    password='vrf4@sg4',
    bind_interface_ip='10.57.191.246',
    expected_prompt='[vrf4_sg4@appserver ~]$ ',
    binary_path='/home/vrf4_sg4/taf_debug/iperf',
    ports=[53862, 54862])
 
_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name='iperf',
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path='iperf',
    version=2)
 

_fastmile_1 = TafUeFastmile(
    ue_pc_address="10.57.157.232",
    root_password="pVmHwjq2ugjHxMz:",
    default_user_password='6xv@sX.7uta+Z@@c',
    ue_manage_ip="10.101.50.19",
    serial_number="LPL2510000B6",
    data_transfer=[_fastmile_data_transfer_1],
    ue_pc_port=5555,
    proxy_mngr_port=9955,
    version="Receiver 5Gmm29-B",
    ueproxy_force_release=True,
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)
_fastmile_appserver_2 = TafUeAppServer(
    app_server_name='APP_SERVER_1',
    address='10.57.191.246',
    user='vrf4_sg4',
    password='vrf4@sg4',
    bind_interface_ip='10.57.191.246',
    expected_prompt='[vrf4_sg4@appserver ~]$ ',
    binary_path='/home/vrf4_sg4/taf_debug/iperf',
    ports=[53863, 54863])


_fastmile_data_transfer_2 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_2,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_2 = TafUeFastmile(
    ue_pc_address="10.57.157.232",
    root_password="jjg=YpJhV3+N7w6C",
    default_user_password="d66KC3TULSUut!qd",
    ue_manage_ip="10.101.39.226",
    serial_number="LPL241800A90",
    data_transfer=[_fastmile_data_transfer_2],
    version="Receiver 5G26-A",
    ueproxy_force_release=True,
    proxy_mngr_port=9955,
    capabilities=["REAL_FASTMILE_UE", "nokia_fastmile"],
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
    test_pcs=[_host],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    ###core=RealCore(mcc=262, mnc=3),
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_fastmile_1, _fastmile_2],
    # attenuator=_attenuator,
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
    appserver=_appserver,
)
