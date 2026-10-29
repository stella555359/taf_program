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
from taf.compatibility.configuration import TestlineWrapper
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

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.119", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_epc_sim = EPCSim(
    mme_ip="10.70.112.39",
    mcc="262",
    mnc="3",
    tac="20000",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.149.7", username="ccris", password="Nokia@1q3q"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/WTS_7577/",
    cfg_filename="1927_tl233_QCM.cfg",
)

# #Qualcomm
_appserver_ssh = SshServiceDetails(
    addr="10.57.163.50",
    username="cmw_sg3",
    password="iW_K#8.ute%A10h0m0ra",
    port="53333",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.50",
    iperf_path="iperf",
    port="53333",
)
_iperf_1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.50",
    iperf_path="/cygdrive/c/iperf",
    port="53233",
)

_iperf_2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.50",
    iperf_path="/cygdrive/c/iperf",
    port="53333",
)

_iperf_3 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.50",
    iperf_path="/cygdrive/c/iperf",
    port="53433",
)
_appserver = AppServer(_iperf_details_on_appserver2)

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.71", username="nokia5G", password="noki@123"
    ),
    serial_number="R5CN21GR36Y",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_1,
    capabilities=["samsung", "samsung"],
)

# CI_Detail_UE_Type='sumsungS22_HPA'
_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.71", username="nokia5G", password="noki@123"
    ),
    serial_number="R5CRC31ZYVB",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_2,
    capabilities=["samsung", "samsung"],
)

# CI_Detail_UE_Type='sumsungS21_MPS'
_android_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.71", username="nokia5G", password="noki@123"
    ),
    serial_number="R5CT335X4NB",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_3,
    capabilities=["samsung", "samsung"],
)

# #RealEnb
_real_enb1_pdu = FACOM(addr="10.57.246.233", port_numbers=[5])

_real_enb2_pdu = FACOM(addr="10.57.246.233", port_numbers=[4])

_common_unit_0 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.226.239", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb1_pdu.pdu_ports[5],
)

_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.226.241", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb2_pdu.pdu_ports[4],
)

_real_enb_0 = Airscale(common_units=[_common_unit_0])
_real_enb_1 = Airscale(common_units=[_common_unit_1])

_lte_real_enb_0 = RealEnb(airscale=_real_enb_0, rms=None, instance_id=23321)
_lte_real_enb_1 = RealEnb(airscale=_real_enb_1, rms=None, instance_id=23322)

_hbte_params = {
    "ip_addr": "10.57.249.41",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}

_attenuator = HBTE(**_hbte_params)

_ru1_pdu = FACOM(addr="10.57.246.233", port_numbers=[7])
_ru2_pdu = FACOM(addr="10.57.246.230", port_numbers=[4])
_ru3_pdu = FACOM(addr="10.57.246.233", port_numbers=[8])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.128", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.128", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[7],
    radio_type=RadioTypes.AWHHF,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.128", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.128", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[4],
    radio_type=RadioTypes.AHLOA,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.128", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.128", username="root", password="umniedziala"
    ),
    pdu_port=_ru3_pdu.pdu_ports[8],
    radio_type=RadioTypes.AWHHF,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
)

# #DU for classicalBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.57.226.238", username="toor4nsn", password="oZPS0POrRieRtu"
)

_lmp_connection_1 = SshServiceDetails(
    addr="10.57.226.240", username="toor4nsn", password="oZPS0POrRieRtu"
)


_capacity_unit_0 = CapacityUnit(addr="192.168.253.20")
_capacity_unit_1 = CapacityUnit(addr="192.168.253.21")

_gnb1_pdu = FACOM(addr="10.57.246.233", port_numbers=[5])

_gnb2_pdu = FACOM(addr="10.57.246.233", port_numbers=[4])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0, _capacity_unit_1],
    pdu_port=_gnb1_pdu.pdu_ports[5],
)

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_1,
    capacity_units=_capacity_unit_0,
    pdu_port=_gnb2_pdu.pdu_ports[4],
)

_airscale_0 = Airscale(common_units=[_common_unit_0])

_airscale_1 = Airscale(common_units=[_common_unit_1])

_du_0 = DU(
    airscale=_airscale_0,
    rus=[_ru1, _ru2],
    f1_m_ip_addr="10.57.226.238",
    f1_c_ip_addr="10.57.226.238",
    f1_u_ip_addr="10.57.226.238",
)

_du_1 = DU(
    airscale=_airscale_1,
    rus=[_ru3],
    f1_m_ip_addr="10.57.226.240",
    f1_c_ip_addr="10.57.226.240",
    f1_u_ip_addr="10.57.226.240",
)

# #CU
_cu_0 = CU(
    backhaul_site_oam_ip="10.57.226.238",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.226.238", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.226.238", username="Nemuadmin", password="nemuuser"
    ),
)

_cu_1 = CU(
    backhaul_site_oam_ip="10.57.226.240",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.226.240", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.226.240", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts
_classical_bts_0 = ClassicalBts(dus=[_du_0], cu=_cu_0, instance_id=23311)

_classical_bts_1 = ClassicalBts(dus=[_du_1], cu=_cu_1, instance_id=23312)


# #cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts_0, _classical_bts_1],
    enbs=[_lte_real_enb_0, _lte_real_enb_1],
    ues=[_android_0, _android_1, _android_2],
    appserver=_appserver,
    core=_epc_sim,
    attenuator=[_attenuator],
    tl_cloud_topology=_tl_cloud_topology,
)
