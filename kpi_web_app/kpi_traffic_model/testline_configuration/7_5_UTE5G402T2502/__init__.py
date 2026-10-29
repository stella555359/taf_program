import os
import yaml
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
from taf.config.testline.core import (
    EPCSim,
    LTEEmuCore,
    PrismaCore,
    RealCore,
    RealCore4GDetails,
    RealCore5GDetails,
    AMF,
    MME,
)
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
from taf.config.testline.attenuator import AttenuationPort, TopYoung, HBTE
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
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android, MediaTek


__maintainer__ = "Ye Jing"
__team__ = (
    "I_NSB_MN_RAN_RD_VRF_HAZ3_06_GMS<I_NSB_MN_RAN_RD_VRF_HAZ3_06@internal.nsn.com>"
)
__email__ = "jing.ye@nokia-sbell.com"

__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.67", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.71.187.227",
    username="nokia",
    password="nokia123",
    port="59122",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.187.227",
    iperf_path="iperf",
    port="59122",
)

# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.71.180.199", username="tester5g", password="Nokia123!"
)

_spark_appserver_ssh2 = SshServiceDetails(
    addr="10.71.187.227", username="nokia", password="nokia123"
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh2,
    network_interface_address="10.71.187.227",
    iperf_path="iperf",
    port=59122,
)

_appserver = AppServer(_iperf_details_on_appserver)
#spark license
_sigspark1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="10012881",
    server_dir="C:/tools/Spark/Spark1.1.2009.3/Bin/Spark.exe",    
    python_path="C:/Users/tester5g/AppData/Local/Programs/Python/Python39",
    iperf_details=_iperf_details_on_appserver2,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262038001004007",
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="67094539",
    server_dir="C:/tools/Spark/Spark1.1.2009.3/Bin/Spark.exe",
    python_path="C:/Users/tester5g/AppData/Local/Programs/Python/Python39",
    iperf_details=_iperf_details_on_appserver2,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262038001004008",
)


# #Real Core
_realcore = RealCore(four_g=None, five_g=None, mcc="262", mnc="3", pdns=None)

# #attenuator
_hbte_params = {
    "ip_addr": "10.71.180.200",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-8-2-6-127-0.5-B-S",
    "version": None,
}
_attenuator = HBTE(**_hbte_params)

_ru1_pdu = FACOM(addr="10.71.180.194", port_numbers=[1])
_ru2_pdu = FACOM(addr="10.71.180.194", port_numbers=[2])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEQV,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
    ],
)
_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.130", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.130", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHLOA,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_lmp_connection = SshServiceDetails(
    addr="10.106.170.130", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.71.180.196", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=_capacity_unit,
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])


_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2],
    f1_m_ip_addr="10.106.170.130",
    f1_c_ip_addr="10.106.170.130",
    f1_u_ip_addr="10.106.170.130",
)

# #CU
_cu = CU(
    backhaul_site_oam_ip="10.106.170.130",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.106.170.130", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.106.170.130", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts0 = ClassicalBts(dus=[_du], cu=_cu, instance_id=37335)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[
        _classical_bts0,
    ],
    core=_realcore,
    ues=[
        _sigspark1,
        _sigspark2,
    ],
    appserver=_appserver,
    attenuator=[_attenuator],
    tl_cloud_topology=_tl_cloud_topology,
)
