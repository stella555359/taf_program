import os
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
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
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
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
    HBTE,
)  # added in taf.meta 5.4
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
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
from taf.config.testline.appserver import AppServer
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android, MediaTek

__maintainer__ = "Mao Cathy"
__team__ = "I_MN_RAN_L3_SW_3_CN_SG02_SG_GMS <I_MN_RAN_L3_SW_3_CN_SG02_SG@internal.nsn.com>"
__email__ = "cathy.mao@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.81", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.71.187.227",
    username="nokia",
    password="nokia123",
    port="53472",
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.187.227",
    iperf_path="/cygdrive/c/iperf",
    port="53372",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.187.227",
    iperf_path="iperf",
    port="53472",
)
_appserver = AppServer(_iperf_details_on_appserver2)

# CI_Detail_UE_Type='Huawei_Mate_20'
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.106.170.94", username="nokia5G", password="noki@123"
    ),
    serial_number="R5CT318LQ3M",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    qcat_path="",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Huawei", "REAL_ANDROID_UE"],
)


# #RealEnb
_real_enb_pdu = FACOM(addr="10.106.170.108", port_numbers=[3])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.106.170.88", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[3],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None, instance_id=237)

# #5GRU for classicalBTS
# attenuator
_hbte_params = {
    "ip_addr": "10.71.180.69",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": "HBTE",
}
_attenuator = HBTE(**_hbte_params)

_ru1_pdu = FACOM(addr="10.106.170.105", port_numbers=[4])
_ru2_pdu = FACOM(addr="10.106.170.107", port_numbers=[1])
_ru3_pdu = FACOM(addr="10.106.170.107", port_numbers=[2])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[4],
    radio_type=RadioTypes.AHEC,
    signal_analyzer=None,
    # attenuation_ports=[_attenuator.attenuator_ports[11], _attenuator.attenuator_ports[12]]
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[1],
    radio_type=RadioTypes.AHLOA,
    signal_analyzer=None,
    # attenuation_ports=[_attenuator.attenuator_ports[11], _attenuator.attenuator_ports[12]]
)

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.128", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.128", username="root", password="umniedziala"
    ),
    pdu_port=_ru3_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHFIB,
    signal_analyzer=None,
    # attenuation_ports=[
    #     _attenuator.attenuator_ports[9],
    #     _attenuator.attenuator_ports[10],
    #     _attenuator.attenuator_ports[11],
    #     _attenuator.attenuator_ports[12],
    # ],
)

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.71.187.203", username="toor4nsn", password="oZPS0POrRieRtu"
)

_lmp_connection_1 = SshServiceDetails(
    addr="10.71.187.148", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.106.170.108", port_numbers=[1])
_gnb2_pdu = FACOM(addr="10.106.170.108", port_numbers=[7])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=_capacity_unit,
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_1,
    capacity_units=_capacity_unit,
    pdu_port=_gnb2_pdu.pdu_ports[7],
)

_airscale = Airscale(common_units=[_common_unit_0])
_airscale_1 = Airscale(common_units=[_common_unit_1])

_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2],
    f1_m_ip_addr="10.106.174.87",
    f1_c_ip_addr="10.106.174.87",
    f1_u_ip_addr="10.106.174.87",
)

_du_1 = DU(
    airscale=_airscale_1,
    rus=[_ru3],
    f1_m_ip_addr="10.106.174.88",
    f1_c_ip_addr="10.106.174.88",
    f1_u_ip_addr="10.106.174.88",
)

# #CU
_cu = CU(
    backhaul_site_oam_ip="10.106.174.87",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.106.174.87", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.106.174.87", username="Nemuadmin", password="nemuuser"
    ),
)

_cu_1 = CU(
    backhaul_site_oam_ip="10.106.174.88",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.106.174.88", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.106.174.88", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts0 = ClassicalBts(dus=[_du], cu=_cu, instance_id=10563)
_classical_bts_1 = ClassicalBts(dus=[_du_1], cu=_cu_1, instance_id=3911)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts0, _classical_bts_1],
    enbs=[_lte_real_enb],
    ues=[_android],
    appserver=_appserver,
    attenuator=[_attenuator],
    tl_cloud_topology=_tl_cloud_topology,
)
