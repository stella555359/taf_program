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

__maintainer__ = "Li guiqi"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_04_01@internal.nsn.com"  # TL owner's team
__email__ = "guiqi.li@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))


# 5GRU for classicalBTS
_ru1_pdu = HBTE(addr="10.71.196.174", port_numbers=[4])

_ru1 = RU(
    ru_hw_group="AEQZ",
    serial_number="1M202406690",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.187", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru1_pdu.pdu_ports[4],
    radio_type=RadioTypes.AEQZ,
)

_ru2_pdu = HBTE(addr="10.71.196.174", port_numbers=[2])

_ru2 = RU(
    ru_hw_group="AEQZ",
    serial_number="1M202406696",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.188", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru2_pdu.pdu_ports[2],
    radio_type=RadioTypes.AEQZ,
)

_ru3_pdu = HBTE(addr="10.71.196.174", port_numbers=[3])

_ru3 = RU(
    ru_hw_group="AEQZ",
    serial_number="1M202406691",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.189", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru3_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEQZ,
)

# 5GRU for classicalBTS_2
_ru4_pdu = HBTE(addr="10.71.196.174", port_numbers=[5])

_ru4 = RU(
    ru_hw_group="AHEGB",
    serial_number="EA203761501",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="root", password="umniedziala"
    ),
    pdu_port=_ru4_pdu.pdu_ports[5],
    radio_type=RadioTypes.AHEGB,
)
_ru5_pdu = HBTE(addr="10.71.196.174", port_numbers=[6])

_ru5 = RU(
    ru_hw_group="AHEGB",
    serial_number="EA203761502",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="root", password="umniedziala"
    ),
    pdu_port=_ru5_pdu.pdu_ports[6],
    radio_type=RadioTypes.AHEGB,
)

_ru6_pdu = TopYoung(addr="10.71.196.176", port_numbers=[6])

_ru6 = RU(
    ru_hw_group="AHEGB",
    serial_number="K9182308029",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="root", password="umniedziala"
    ),
    pdu_port=_ru6_pdu.pdu_ports[6],
    radio_type=RadioTypes.AHEGB,
)

_host0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.138", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = TopYoung(addr="10.71.196.172", port_numbers=[6])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.190", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_common_unit = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[6],
    test_pc=_gnb_test_pc_0,
)

_airscale = Airscale(common_units=[_common_unit])
_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6],
    f1_m_ip_addr="10.71.213.130",
)

# CU
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.213.130", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.213.130", username="Nemuadmin", password="nemuuser"
    ),
)

# RealEnb
_enb_ru1_pdu1 = TopYoung(addr="10.71.196.181", port_numbers=[3])
_enb_ru1 = RU(
    ru_hw_group="FHEL",
    serial_number="EA170782339",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_enb_ru1_pdu1.pdu_ports[3],
    radio_type=RadioTypes.FHEL,
)

_enb_ru2_pdu2 = TopYoung(addr="10.71.196.170", port_numbers=[5])
_enb_ru2 = RU(
    ru_hw_group="FHEL",
    serial_number="EA173681103",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_enb_ru2_pdu2.pdu_ports[5],
    radio_type=RadioTypes.FHEL,
)


_enb_ru3_pdu3 = TopYoung(addr="10.71.196.181", port_numbers=[4])
_enb_ru3 = RU(
    ru_hw_group="FHEL",
    serial_number="EA170782559",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_enb_ru3_pdu3.pdu_ports[4],
    radio_type=RadioTypes.FHEL,
)

_enb_ru4_pdu4 = TopYoung(addr="10.71.196.182", port_numbers=[5])
_enb_ru4 = RU(
    ru_hw_group="FHDB",
    serial_number="1M171210363",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_enb_ru4_pdu4.pdu_ports[5],
    radio_type=RadioTypes.FHDB,
)

_enb_ru5_pdu5 = TopYoung(addr="10.71.196.177", port_numbers=[6])
_enb_ru5 = RU(
    ru_hw_group="FRHG",
    serial_number="K9170807539",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_enb_ru5_pdu5.pdu_ports[6],
    radio_type=RadioTypes.FHDB,
)

_enb_ru6_pdu6 = TopYoung(addr="10.71.196.171", port_numbers=[5])
_enb_ru6 = RU(
    ru_hw_group="FHDB",
    serial_number="1M165153251",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_enb_ru6_pdu6.pdu_ports[5],
    radio_type=RadioTypes.FHDB,
)

_enb_ru7_pdu7 = TopYoung(addr="10.71.196.182", port_numbers=[6])
_enb_ru7 = RU(
    ru_hw_group="FHDB",
    serial_number="1M171210331",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_enb_ru7_pdu7.pdu_ports[6],
    radio_type=RadioTypes.FHDB,
)

_enb_ru9_pdu9 = TopYoung(addr="10.71.196.120", port_numbers=[5])
_enb_ru9 = RU(
    ru_hw_group="FRHG",
    serial_number="K9171617099",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_enb_ru9_pdu9.pdu_ports[5],
    radio_type=RadioTypes.FRHG,
)

_enb_ru10_pdu10 = TopYoung(addr="10.71.196.120", port_numbers=[6])
_enb_ru10 = RU(
    ru_hw_group="FRHG",
    serial_number="K9171617098",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_enb_ru10_pdu10.pdu_ports[6],
    radio_type=RadioTypes.FRHG,
)

_lmp_connection_enb = SshServiceDetails(
    addr="10.71.213.113", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = TopYoung(addr="10.71.196.172", port_numbers=[1])
_enb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.190", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
)
_common_unit_enb1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[1],
    test_pc=_enb_test_pc_0,
)
_real_enb = Airscale(common_units=[_common_unit_enb1])
_lte_real_enb = RealEnb(
    airscale=_real_enb,
    system_module=_real_enb,
    oam_ip=NetworkAddress(v4="10.71.213.113"),
    instance_id=611,
    rms=[_enb_ru1, _enb_ru2, _enb_ru3, _enb_ru4, _enb_ru5, _enb_ru6, _enb_ru7, _enb_ru9, _enb_ru10]
)

# cloud_topology
_tl_cloud_topology = "I&V-HGZ-TL611"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=596, global_bts_id=596)

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.190", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_lte_real_enb.airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

# enbPC
_enb_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.190", username="ute", password="iW_K#8.ute%A10h0m0ra"
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
    addr="10.57.163.51", username="cmw_sg4", password="Zvmsg04_159357!", port=53596
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.51",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port=54596,
)


_appserver = AppServer(_iperf)

# CI_Detail_UE_Type='Huawei Honor 30s;Huawei Honor 30s'
_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.98", username="nokia5G", password="noki@123"
    ),
    serial_number="9EQUT20903003026",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["SG4_HONOR30s", "cell_Mapping: [1]", "huawei"],
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
    ports=[53596, 54596],
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
    ue_pc_address="10.57.155.138",
    root_password="2d4ab6b2a864",
    ue_manage_ip="10.71.205.195",
    serial_number="LPL2214004D9",
    data_transfer=[_fastmile_data_transfer_1],
    ue_pc_port=5555,
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
    test_pc=_enb_pc,
    test_pcs=[_enb_pc],
    #gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    ###core=RealCore(mcc=262, mnc=3),
    tl_cloud_topology=_tl_cloud_topology,
    ues=[],
    # attenuator=_attenuator,
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
    appserver=_appserver,
)
