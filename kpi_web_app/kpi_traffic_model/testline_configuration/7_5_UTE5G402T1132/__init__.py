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
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import AppServer

__maintainer__ = "Fengzhen Zhao"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_08_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_08@internal.nsn.com>"
__email__ = "fengzhen.zhao@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_attenuator = AHBTE(
    ip_addr="10.101.51.35",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6],
    model="PA-16-16-6-127-0.5-B-S",
)
# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.222", username="ute", password="ute"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.71.219.237", username="cmw_sg8", password="cm@8", port="58999"
)

_iperf_1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.11",
    iperf_path="/usr/bin/iperf",
    port="58080",
)

_iperf_2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.11",
    iperf_path="/usr/bin/iperf",
    port="58081",
)

_appserver = AppServer(_iperf_1)
_appserver.iperf_details.port = 58080

# CI_Detail_UE_Type='Huawei Honor 30s'
_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.222", username="nokia5G", password="noki@123"
    ),
    serial_number="9EQUT20721003460",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf_1,
    capabilities=["SG8_HONOR30s", "cell_Mapping: [1]", "huawei"],
)

_ue2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.222", username="nokia5G", password="noki@123"
    ),
    serial_number="9EQUT20721012246",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf_2,
    capabilities=["SG8_HONOR30s", "cell_Mapping: [2]", "huawei"],
)

# inseego
# _ue_config_path = os.path.join(_cfg_dir, "TestData/inseego.yml")
# if os.path.isfile(_ue_config_path):
#     with open(_ue_config_path) as f:
#         _ue_inseego = f.read()
#         qci_port = re.findall("(_iperf.*?port)", _ue_inseego)
#         for item in qci_port:
#             _ue_inseego = _ue_inseego.replace(item, str(eval(item)))
#         _ue_config = yaml.load(_ue_inseego)
# else:
#     _ue_config = ""
# inseego

# 5GRU for classicalBTS RU PB
_ru_pdu = HBTE(addr="10.101.45.206", port_numbers=[6])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.138", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[6],
    radio_type=RadioTypes.AZQF,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
    ],
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.101.45.203", port_numbers=[6])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[6],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.101.51.60")

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.101.51.60",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.51.33", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.51.60", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.51.60", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.101.51.60",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.51.33", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.101.51.60",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.51.33", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.101.51.60",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.51.33", ip_prefix_length=27),
    ),
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_SA_ASIBL_ABIOL_AEQI"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=10558, global_bts_id=1132)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    appserver=_appserver,
    ues=[_ue1, _ue2],
    core=RealCore(mcc=262, mnc=3),
    attenuator=_attenuator,
    tl_cloud_topology=_tl_cloud_topology,
)
