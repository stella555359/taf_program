import os
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.testpc import Connection
from taf.config.testline.core import RealCore
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE, FPFH
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
)  # added in taf.meta 5.4
from taf.config.testline.attenuator import HBTE as att_HBTE
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.appserver import AppServer
# from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android, MediaTek

__maintainer__ = "Song Jiana"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_3_GMS <I_MN_5G_RAN_IV4_LINE_HZG_3@internal.nsn.com>"
)
__email__ = "jiana.song@nokia.com"

__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

ue_config_path = os.path.join(_cfg_dir, "inseego.yml")
if os.path.isfile(ue_config_path):
    with open(ue_config_path) as f:
        ue_config = yaml.load(f)
else:
    ue_config = ""

_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.217.83", username="ute", password="uteUTE!"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.245",
    username="vrf4_sg3",
    password="Haz4_vrf_sg3",
    port="53383",
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.245",
    iperf_path="/cygdrive/c/iperf",
    port="53483",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.245",
    iperf_path="iperf",
    port="53383",
)
_appserver = AppServer(_iperf_details_on_appserver2)

_ue_host_ssh = SshServiceDetails(
    addr="10.64.57.26", username="mn5gran", password="nokia123@"
)

_mtk_appserver_ssh = SshServiceDetails(
    addr="10.57.191.245", username="vrf4_sg3", password="Haz4_vrf_sg3", port="53383"
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_mtk_appserver_ssh,
    network_interface_address="10.57.191.245",
    iperf_path="iperf",
    port=53483,
)

_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.64.57.26", username="mn5gran", password="nokia123@"
    ),
    serial_number="4e353959",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Users/mn5gran/AppData/Local/Programs/Python/Python310/python.exe",
    iperf_details=_iperf,
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["qct_dx50", "REAL_ANDROID_UE", "qct_dx50"],
    imsi="262033100001266",
    sec_key="12001000312",
    pdn=["stdata1", "mdrb.nokia.com", "mdrb1.nokia.com"],
)

# #RealEnb
_pdu = FPFH(addr='10.64.49.82', port_numbers=[1, 2, 3, 4, 5, 6], login="admin", password="admin")
_pdu1 = FPFH(addr='10.64.49.84', port_numbers=[1, 2, 3, 4, 5, 6], login="admin", password="admin")
_common_unit_0 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.64.53.69", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_pdu.pdu_ports[1],
    hardware_type="ASIL",
)

_real_enb0 = Airscale(common_units=[_common_unit_0])

_lte_real_enb0 = RealEnb(airscale=_real_enb0, instance_id=355)

_pdns = [PDN(PDPTypes.IP.value, 'stdata1'), PDN(PDPTypes.IP.value, 'mdrb.nokia.com'),
         PDN(PDPTypes.IP.value, 'mdrb1.nokia.com')]

# #Real Core
_realcore = RealCore(four_g=None, five_g=None, mcc="262", mnc="03", pdns=_pdns)

# #attenuator
_attenuator = TopYoung(
    ip_addr="10.64.56.34",
    port=23,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="TAS16T16-51-120-1N-DES",
)

_ru1 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.37.128",
        username="rfsw",
        password="PD6N1DB0lWmwomtNL2qd3ISypbiocdGRy7U+Lipiksk=",
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_pdu.pdu_ports[4],
    radio_type=RadioTypes.AZNA,
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_ru2 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.37.129",
        username="rfsw",
        password="PD6N1DB0lWmwomtNL2qd3ISypbiocdGRy7U+Lipiksk=",
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_pdu.pdu_ports[6],
    radio_type=RadioTypes.AHFIB,
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
)

_ru3 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="PD6N1DB0lWmwomtNL2qd3ISypbiocdGRy7U+Lipiksk=",
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_pdu1.pdu_ports[5],
    radio_type=RadioTypes.AZQJ,
    attenuation_ports=[
    ],
)

_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20",
                              hardware_type="ABIO", 
                              rus=[_ru3],
)
_capacity_unit_11 = CapacityUnit(addr="192.168.253.21",
                              hardware_type="ABIO", 
                              rus=[_ru1, _ru2],
)

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit, _capacity_unit_11],
    pdu_port=_pdu.pdu_ports[1],
    hardware_type="ASIL",
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3],
    f1_m_ip_addr="10.64.53.69",
    f1_c_ip_addr="10.64.53.69",
    f1_u_ip_addr="10.64.53.69",
)

# _f1m = NetworkAddress(v6="2a00:8a00:8000:136:10:57:229:40")

# #CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(v4='10.64.53.69', vlan_id=None,
                                             routing=RoutingInformation(gateway='10.64.53.65', ip_prefix_length=27)),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.64.53.69", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.64.53.69", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4='10.64.53.69', vlan_id=None,
                       routing=RoutingInformation(gateway='10.64.53.65', ip_prefix_length=27)
    ),
    x2u=NetworkAddress(v4='10.64.53.69', vlan_id=None,
                       routing=RoutingInformation(gateway='10.64.53.65', ip_prefix_length=27)
    ),
    s1u=NetworkAddress(v4='10.64.53.69', vlan_id=None,
                       routing=RoutingInformation(gateway='10.64.53.65', ip_prefix_length=27)
    )
)

_cbts = ClassicalBts(dus=[_du], cu=_cu, global_bts_id=355, instance_id=355)

_classical_bts = ClassicalBts(dus=[_du], cu=_cu, global_bts_id=355, instance_id=355)

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_QC_SA_ASILL_2xABIO_2xAZNA_AZQJ"

_gnb_testpc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.217.83", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

tl = TestLine(
    test_pc=_host,
    test_pcs=[_gnb_testpc],  
    gnbs=[_cbts],
    core=_realcore,
    enbs=[],
    ues=[_android],
    appserver=_appserver,
    attenuator=_attenuator,
    tl_cloud_topology=_tl_cloud_topology,
)
