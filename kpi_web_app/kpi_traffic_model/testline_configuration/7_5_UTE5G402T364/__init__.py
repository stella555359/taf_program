import os
import yaml
import re
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
from taf.config.testline.core import RealCore
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

__maintainer__ = "zhang qingqing"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_03_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_03@internal.nsn.com>"
__email__ = "qingqing.zhang@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.132", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.245",
    username="vrf4_sg3",
    password="Haz4_vrf_sg3",
    port="53664",
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.245",
    iperf_path="iperf",
    port="53664",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.245",
    iperf_path="iperf",
    port="53664",
)

_ue_host_ssh = SshServiceDetails(
    addr="10.57.239.230", username="root", password="123456"
)

_appserver = AppServer(_iperf_details_on_appserver2)

# CI_Detail_UE_Type='Qualcomm'
_sigspark_1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="11375e40",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---05301356/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["pioneer", "huawei_sigspark"],
    imsi="310260032994017",
    pdn="wap2.nokia.com",
)

_sigspark_2 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="81d39eb3",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---05301356/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260310001706",
)

_sigspark_3 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="90bc04e1",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---05301356/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100001213",
)

_sigspark_4 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="baf4623d",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---05301356/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100001211",
)

_sigspark_5 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="d10d1f35",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---05301356/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100001218",
)

_sigspark_6 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="edda48dc",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---05301356/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100001212",
)

_sigspark_7 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="8e1985f2",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---05301356/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100001216",
)

_sigspark_8 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="7c0260e2",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---05301356/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033100001217",
)

# CI_Detail_UE_Type='Askey'
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.239.230", username="root", password="123456"
    ),
    serial_number="5101394b",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE"],
)


# #RealEnb
# _real_enb_pdu = FACOM(addr="10.57.249.12", port_numbers=[7])
#
# _common_unit_2 = CommonUnit(
#     lmp_connection=SshServiceDetails(
#         addr="10.57.227.98", username="toor4nsn", password="oZPS0POrRieRtu"
#     ),
#     capacity_units=[],
#     pdu_port=_real_enb_pdu.pdu_ports[7],
# )
#
# _real_enb = Airscale(common_units=[_common_unit_2])
#
# _lte_real_enb = RealEnb(airscale=_real_enb, rms=None, instance_id=905)

# #5GRU for classicalBTS
# attenuator

_attenuator = TopYoung(
    ip_addr="10.57.239.229",
    port=28888,
    attenuation_port_numbers=[1, 2, 3, 4],
    model="MCS2350A2-128B16-E6",
)


_ru1_pdu = FACOM(addr="10.57.176.76", port_numbers=[1])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEHC,
    signal_analyzer=None,
    # attenuation_ports=[_attenuator.attenuator_ports[11], _attenuator.attenuator_ports[12]]
)

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.227.102", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.57.176.74", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=_capacity_unit,
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru1],
    f1_m_ip_addr="10.57.227.102",
    f1_c_ip_addr="10.57.227.102",
    f1_u_ip_addr="10.57.227.102",
)

# #CU
_cu = CU(
    backhaul_site_oam_ip="10.57.227.102",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.227.102", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.227.102", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts0 = ClassicalBts(dus=[_du], cu=_cu, instance_id=36411, global_bts_id=3641199999)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts0],
    # enbs=[_lte_real_enb],
    appserver=[_appserver, _iperf_details_on_appserver2],
    ues=[
        _sigspark_1,
        _sigspark_2,
        _sigspark_3,
        _sigspark_4,
        _sigspark_5,
        _sigspark_6,
        _sigspark_7,
        _sigspark_8,
    ],
    core=RealCore(mcc=310, mnc=260),
    attenuator=[_attenuator],
    tl_cloud_topology=_tl_cloud_topology,
)
