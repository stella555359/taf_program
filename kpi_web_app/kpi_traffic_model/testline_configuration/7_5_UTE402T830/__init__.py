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
)
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
from taf.config.testline.gnb.networkaddress import NetworkAddress
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

__maintainer__ = "Wanglei"
__team__ = (
    "I_NSB_MN_5GSC_5G_PZ_HZ_07_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_07_GMS@internal.nsn.com>"
)
__email__ = "lei.24.wang@nokia-sbell.com"

__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# VM
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.132", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# AMF
_epc_sim = EPCSim(
    mme_ip="10.110.227.5",
    mcc="460",
    mnc="2",
    tac="210",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.227.70", username="test", password="NOKIA123"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)

# Appserver
_appserver_ssh = SshServiceDetails(
    addr="10.57.162.10", username="cmw_sg7", password="Nokia07!", port="58830"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.10",
    iperf_path="/usr/bin/iperf",
    port="58830",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.10",
    iperf_path="iperf",
    port="57830",
)
_appserver = AppServer(_iperf_details_on_appserver2)

# UE
_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.43", username="nokia5G", password="noki@123"
    ),
    serial_number="9YS0220B11000033",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE"],
)

_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.43", username="nokia5G", password="noki@123"
    ),
    serial_number="9YS0219C07034309",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE"],
)

# ENB
_real_enb_pdu = FACOM(
    addr="10.68.87.107", port_numbers=[7], model="111", version="1.1.1"
)

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.68.89.25", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[7],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None, instance_id=910)

# GNB
_hbte_params = {
    "ip_addr": "10.68.88.238",
    "port": 5000,
    "attenuation_port_numbers": [5, 6, 7, 8, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator = HBTE(**_hbte_params)

_hbte_params_1 = {
    "ip_addr": "10.68.88.238",
    "port": 5000,
    "attenuation_port_numbers": [5, 6, 7, 8, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_1 = HBTE(**_hbte_params_1)


_ru1_pdu = FACOM(addr="10.68.87.108", port_numbers=[2])
_ru2_pdu = FACOM(addr="10.68.87.104", port_numbers=[4])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.162", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.48.162", username="root", password="root"
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AEQB,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
    ],
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.128", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.128", username="root", password="root"
    ),
    pdu_port=_ru2_pdu.pdu_ports[4],
    radio_type=RadioTypes.AHPE,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator_1.attenuator_ports[7],
        _attenuator_1.attenuator_ports[8],
    ],
)


_lmp_connection = SshServiceDetails(
    addr="10.68.89.23", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.17")

_gnb_pdu = FACOM(addr="10.68.87.106", port_numbers=[2])

_common_unit = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit])

_du = DU(
    airscale=_airscale,
    rus=[_ru1],
    f1_m_ip_addr="10.68.89.23",
    f1_c_ip_addr="10.68.89.23",
    f1_u_ip_addr="10.68.89.23",
)

_cu = CU(
    backhaul_site_oam_ip="10.68.89.23",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.89.23", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.89.23", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts0 = ClassicalBts(dus=[_du], cu=_cu, instance_id=830)

_lmp_connection1 = SshServiceDetails(
    addr="10.68.89.23", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit1 = CapacityUnit(addr="192.168.253.17")

_gnb_pdu1 = FACOM(addr="10.68.87.106", port_numbers=[2])

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection1,
    capacity_units=[_capacity_unit1],
    pdu_port=_gnb_pdu1.pdu_ports[2],
)

_airscale1 = Airscale(common_units=[_common_unit_1])

_du1 = DU(
    airscale=_airscale1,
    rus=[_ru2],
    f1_m_ip_addr="10.68.89.23",
    f1_c_ip_addr="10.68.89.23",
    f1_u_ip_addr="10.68.89.23",
)

_cu1 = CU(
    backhaul_site_oam_ip="10.68.89.23",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.89.23", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.89.23", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts1 = ClassicalBts(dus=[_du1], cu=_cu1, instance_id=830)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[
        _classical_bts0,
        _classical_bts1,
    ],
    core=_epc_sim,
    enbs=[_lte_real_enb],
    ues=[_android_0, _android_1],
    appserver=_appserver,
    attenuator=[_attenuator, _attenuator_1],
    tl_cloud_topology=_tl_cloud_topology,
)
