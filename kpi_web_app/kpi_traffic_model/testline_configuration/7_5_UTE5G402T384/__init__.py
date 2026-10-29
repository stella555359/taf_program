import os
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    DeploymentSecurityGroupStack,
    ComputeNode,
    OSP,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline.core import RealCore

# from taf.config.testline.gnb.du import DU
from taf.config.testline import RU, DU
from taf.config.testline.gnb.du import Cablink, Endpoint

# from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.testline import TestLine

# from taf.config.testline import HBTE_PDU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE

# from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
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
from taf.config.testline.attenuator import HBTE as hbte
from taf.config.testline.gnb.networkaddress import (
    NetworkAddress,
    RoutingInformation,
)  # add in taf.meta 5.4
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.hardware_controller import (
    AmiaFanHardwareController,
    GPSPowerHardwareController,
)
from taf.config.testline.signal_analyzer import KeysightN9935A
from taf.config.testline.nms import Netact
from taf.config.testline.optical_switch import Leoni
from taf.config.testline.appserver import AppServer

__maintainer__ = "tizeng"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_3_GMS <I_MN_5G_RAN_IV4_LINE_HZG_3@internal.nsn.com>"
)
__email__ = "jack.zeng@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))


_epc_sim = EPCSim(
    mme_ip="10.70.112.39",
    mcc="262",
    mnc="03",
    tac="20000",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.149.7", username="ccris", password="Nokia@1q3q"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/WTS_7577/",
    cfg_filename="1927_tl347_QCM.cfg",
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.245",
    username="vrf4_sg3",
    password="Haz4_vrf_sg3",
    port="54384",
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.245",
    iperf_path="/cygdrive/c/iperf",
    port="53384",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.245",
    iperf_path="iperf",
    port="53384",
)
_appserver = AppServer(_iperf_details_on_appserver2)

# CI_Detail_UE_Type='Huawei_5G_Mate_30_Pro'
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.136", username="mn5gran", password="nokia123@"
    ),
    serial_number="R3CW10X08QJ",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["samsung", "samsung"],
)

_android2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.136", username="mn5gran", password="nokia123@"
    ),
    serial_number="R3CW201VCRX",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["samsung", "samsung"],
)

# #RealEnb
_real_enb_pdu = HBTE(addr="10.57.176.150", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.227.141", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
    hardware_type="ASIL",
)

_real_enb_0 = Airscale(common_units=[_common_unit_0])

_lte_real_enb_0 = RealEnb(airscale=_real_enb_0, rms=None, instance_id=38421)

# #5GRU for classicalBTS
# attenuator
# ##_hbte_params = {
#     "ip_addr": "10.71.206.19",
#     "port": 5000,
#     "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
#     "model": "PA-16-16-6-127-0.5-B-S",
#     "version": None,
# }

# _attenuator = hbte(**_hbte_params)

_attenuator = TopYoung(
    ip_addr="10.57.230.73",
    port=3000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="TAS16T16-51-120-1S-DES",
)

_ru1_pdu = HBTE(addr="10.57.176.150", port_numbers=[2])
_ru2_pdu = HBTE(addr="10.57.176.150", port_numbers=[3])
_ru3_pdu = HBTE(addr="10.57.176.150", port_numbers=[4])
_ru4_pdu = HBTE(addr="10.57.176.150", port_numbers=[5])


# #5GRU for classicalBTS
_ru1 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AWHHF,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru2 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru2_pdu.pdu_ports[3],
    radio_type=RadioTypes.AWHHF,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_ru3 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru3_pdu.pdu_ports[4],
    radio_type=RadioTypes.AHFB,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)

_ru4 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.1.154", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.1.154", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    pdu_port=_ru4_pdu.pdu_ports[5],
    radio_type=RadioTypes.AEHC,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
)

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20", hardware_type="ABIO")

_gnb_pdu = HBTE(addr="10.57.176.150", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
    hardware_type="ASIL",
)

_airscale = Airscale(common_units=[_common_unit_0])

# DU
# Cablinks should be defined in the bottom of DU section
_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru1, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=2),
        target=Endpoint(unit=_ru1, label="SFP", port_id=2),
    ),
]

_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3, _ru4],
    f1_m_ip_addr="192.168.255.129",
    f1_c_ip_addr="10.57.227.141",
    f1_u_ip_addr="10.57.227.141",
    cablinks=_ru_cablinks,
)

_du1 = DU(
    airscale=_airscale,
    rus=[_ru1],
    f1_m_ip_addr="10.57.227.143",
    f1_c_ip_addr="10.57.227.143",
    f1_u_ip_addr="10.57.227.143",
    cablinks=_ru_cablinks,
)

# #CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.57.227.141",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.227.129", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.227.141", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.227.141", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.57.227.141",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.227.129", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.57.227.141",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.227.129", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.57.227.141",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.227.129", ip_prefix_length=27),
    ),
)

_cu1 = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.57.227.143",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.227.129", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.227.143", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.227.143", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.57.227.143",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.227.129", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.57.227.143",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.227.129", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.57.227.143",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.227.129", ip_prefix_length=27),
    ),
)
# #host


_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=38411, global_bts_id=38411)


_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.38", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

# #cloud_topology
# _tl_cloud_topology = "CLOUD_5G_BB3"
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_ASIBL_ABIOB1_2xAWHHF_ENB"
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb_0],
    ues=[_android, _android2],
    core=RealCore(mcc=460, mnc=2),  # Use RealCore() for Real Core TL
    appserver=_appserver,
    attenuator=[_attenuator],
    tl_cloud_topology=_tl_cloud_topology,
)
