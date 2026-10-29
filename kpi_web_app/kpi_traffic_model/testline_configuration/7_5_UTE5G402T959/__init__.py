import os
import yaml
import re
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.core import RealCore
from taf.config.testline import RU, DU
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.pdu import HBTE, TopYoung
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
from taf.config.testline.attenuator import HBTE as ATTEN_HBTE
from taf.config.testline.attenuator import TopYoung as TOPYOUNG
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import AppServer

from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc

__maintainer__ = "eleven wu"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_08_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_08@internal.nsn.com>"
__email__ = "eleven.1.wu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_attenuator = ATTEN_HBTE(
    ip_addr="10.101.49.130",
    port=5000,
    model="PA-16-16-6-127-0.5-B-S",
    attenuation_port_numbers=[
        1,
        34,
        21,
        54,
        23,
        56,
        149,
        182,
        215,
        248,
    ],
)

# 5GRU for classicalBTS RU PB
_ru_pdu = HBTE(addr="10.101.45.70", port_numbers=[5])
_ru_pdu_1 = HBTE(addr="10.101.45.68", port_numbers=[8])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.135", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[5],
    radio_type=RadioTypes.AZQF,
    attenuation_ports=[
        _attenuator.attenuator_ports[149],
        _attenuator.attenuator_ports[182],
        _attenuator.attenuator_ports[215],
        _attenuator.attenuator_ports[248],
        _attenuator.attenuator_ports[21],
        _attenuator.attenuator_ports[54],
        _attenuator.attenuator_ports[23],
        _attenuator.attenuator_ports[56],
    ],
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.135", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_1.pdu_ports[8],
    radio_type=RadioTypes.AZQD,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[34],
    ],
)



# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.101.49.155",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.49.129", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.49.155", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.49.155", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.101.49.155",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.49.129", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.101.49.155",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.49.129", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.101.49.155",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.49.129", ip_prefix_length=27),
    ),
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20", hardware_type="ASOE",)
_gnb_pdu = HBTE(addr="10.101.45.68", port_numbers=[2])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
    hardware_type="ASOE",
)
_airscale = Airscale(common_units=[_common_unit_0])
# Cablinks should be defined in the bottom of DU section
_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru1, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=7),
        target=Endpoint(unit=_ru1, label="SFP", port_id=2),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=2),
        target=Endpoint(unit=_ru2, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=8),
        target=Endpoint(unit=_ru2, label="SFP", port_id=2),
    ),
]
_du = DU(airscale=_airscale, rus=[_ru1, _ru2], f1_m_ip_addr="10.101.49.155", cablinks=_ru_cablinks)


# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=5959, global_bts_id=959)

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.71", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

_appserver_ssh = SshServiceDetails(
    addr="10.70.222.52", username="cmw_sg8", password="Bestcm@8", port="58999"
)

_iperf_1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.70.222.52",
    iperf_path="/usr/bin/iperf",
    port="58261",
)

_iperf_2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.70.222.52",
    iperf_path="/usr/bin/iperf",
    port="58262",
)

_appserver = AppServer(_iperf_1)
_appserver.iperf_details.port = 58263

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






# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_SA_ASOE_AZQD_AZQF"

# for FastMile CPE
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_2",
    address="10.70.222.52",
    user="cmw_sg8",
    password="Bestcm@8",
    bind_interface_ip="10.70.222.52",
    expected_prompt="[cmw_sg8@rocky8-KVM-nogui ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=[58006, 58056],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    com_port="23",
    ue_pc_address="10.101.47.234",
    root_password="fbbad3d233f2",
    ue_manage_ip="192.168.1.1",
    serial_number="LPL221400599",
    data_transfer=[_fastmile_data_transfer_1],
    ue_pc_port=5555,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)


# for FastMile CPE
_fastmile_appserver_2 = TafUeAppServer(
    app_server_name="APP_SERVER_2",
    address="10.70.222.52",
    user="cmw_sg8",
    password="Bestcm@8",
    bind_interface_ip="10.70.222.52",
    expected_prompt="[cmw_sg8@rocky8-KVM-nogui ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=[58007, 58057],
)

_fastmile_data_transfer_2 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_2,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_2 = TafUeFastmile(
    com_port="45",
    ue_pc_address="10.68.86.13",
    root_password="af4a4942efdc",
    ue_manage_ip="192.168.1.1",
    serial_number="LPL221400573",
    data_transfer=[_fastmile_data_transfer_2],
    ue_pc_port=5555,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE2", "nokia_fastmile"],
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    appserver=_appserver,
    ues=[_fastmile_1, _fastmile_2],
    core=RealCore(mcc=262, mnc=3),
    attenuator=_attenuator,
    tl_cloud_topology=_tl_cloud_topology,
)
