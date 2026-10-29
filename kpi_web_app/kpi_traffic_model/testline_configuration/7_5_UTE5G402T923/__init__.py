import os
import yaml
import re
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
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)  # added in taf.meta.5.4
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
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline.testpc import Connection
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import AppServer
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
    MediaTek,
)  # added in taf.meta.5.4

__maintainer__ = "xinzhu"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_03_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_03@internal.nsn.com>"
)
__email__ = "xinran.zhu@nokia-sbell.com"


# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_attenuator = AHBTE(
    ip_addr="10.101.36.167",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4],
    model="PA-16-16-6-127-0.5-B-S",
)

# 5GRU for classicalBTS RU PB
_ru_pdu = HBTE(addr="10.68.87.92", port_numbers=[1])

_ru = RU(
    ru_hw_group="AHPB",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.37.128", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.37.128", username="root", password="root"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type="AHPB",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(
    addr="192.168.253.20",
    #rus=[_ru],
    hardware_type="ABIN",
)

_gnb_pdu = HBTE(addr="10.68.87.124", port_numbers=[5])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    hardware_type="ASIB",
    pdu_port=_gnb_pdu.pdu_ports[5],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.68.88.254")

# CU
_cu = CU(
    backhaul_site_oam_ip="10.68.88.254",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.88.254", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.88.254", username="Nemuadmin", password="nemuuser"
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.68.88.252", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = HBTE(addr="10.68.87.124", port_numbers=[6])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[6],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb)


# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIBR_ABIOB1_AHPB"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=10042, global_bts_id=10042)

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.63", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)


_docker_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.150.41", username="utfuser", password="utfadmin!", port=443
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.235",
    username="vrf3_sg3",
    password="vrf3@sg3",
    port="43111",
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.235",
    iperf_path="/usr/bin/iperf",
    port="43021",
)

_appserver = AppServer(_iperf)

# CI_Detail_UE_Type='Qualcomm'
# Qualcomm
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.116", username="nokia5G", password="noki@123"
    ),
    serial_number="2867e6fc",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "inseego"],
)

# inseego
_ue_config_path = os.path.join(_cfg_dir, "TestData/inseego.yml")
if os.path.isfile(_ue_config_path):
    with open(_ue_config_path) as f:
        _ue_inseego = f.read()
        qci_port = re.findall("(_iperf.*?port)", _ue_inseego)
        for item in qci_port:
            _ue_inseego = _ue_inseego.replace(item, str(eval(item)))
        _ue_config = yaml.safe_load(_ue_inseego)
else:
    _ue_config = ""

# _ue_config_path = os.path.join(_cfg_dir, 'TestData/inseego.yml')
# if os.path.isfile(_ue_config_path):
#    with open(_ue_config_path) as f:
#        _ue_config = yaml.load(f)
# else:
#    _ue_config = ''

# inseego

# for MTK UE, just a placeholder for now, TL config not supported yet.
_mtk_host_ssh = SshServiceDetails(
    addr="10.101.47.116", username="nokia5G", password="noki@123"
)
_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="10.57.191.235",
    iperf_path="iperf",
    port="43021",
)

_mtk = MediaTek(
    ssh_connection_details=_mtk_host_ssh,
    #                serial_number='2867e6fc',
    server_dir="C:/pyro_server",
    server_port=8080,
    edb_file_path=r"C:\MTK\sw\w19.41_1400/MDDB_MT6297_S00_VMOLY_W19_43_P3.EDB",
    #                python_path='C:/Python27/python.exe',
    imei="352569090028547",
    apn_url="wap2.nokia.com",
    #                qcat_path='C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe',
    #                diag_cfg_path='C:/pyro_server/DIAG.cfg',
    iperf_details=_iperf,
    capabilities=["REAL_MEDIATEK_UE"],
)
_mtk.inject_file = r"C:\MTK\ELT\nsa_tl923.tcl"


tl = TestLine(
    test_pc=_host,
    host=[_docker_pc],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    appserver=_appserver,
    ues=[_ue_config, _mtk],
    attenuator=_attenuator,
    tl_cloud_topology=_tl_cloud_topology,
)
