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


__maintainer__ = "zhang bo"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_3_GMS <I_MN_5G_RAN_IV4_LINE_HZG_3@internal.nsn.com>"
)
__email__ = "bo.5.zhang@nokia-sbell.com"

__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.65", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.245",
    username="vrf4_sg3",
    password="Haz4_vrf_sg3",
    port="53381",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.245",
    iperf_path="iperf",
    port="53481",
)

# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.57.246.42", username="Topyoung", password="nokia123@"
)
_ue_host_ssh1 = SshServiceDetails(
    addr="10.57.130.234", username="mn5gran", password="noki@123"
)

_spark_appserver_ssh2 = SshServiceDetails(
    addr="10.71.219.231", username="cmw_sg3", password="iW_K#8.ute%A10h0m0ra"
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh2,
    network_interface_address="10.71.219.231",
    iperf_path="iperf",
    port=54387,
)

_appserver = AppServer(_iperf_details_on_appserver)
# spark license
_ue0 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="6f2de091",
    server_dir="E:/Spark1.1.2008.43/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver2,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260001006301",
)


# #RealEnb
_capacity_unit2 = CapacityUnit(addr="192.168.253.33")

_real_enb_pdu0 = FACOM(addr="10.71.196.246", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.214.108", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=_capacity_unit2,
    pdu_port=_real_enb_pdu0.pdu_ports[2],
)

_real_enb0 = Airscale(common_units=[_common_unit_0])

_lte_real_enb0 = RealEnb(airscale=_real_enb0, instance_id=38721)

# #Real Core
_realcore = RealCore(four_g=None, five_g=None, mcc="310", mnc="260", pdns=None)

# #attenuator
_attenuator = TopYoung(
    ip_addr="10.57.246.42",
    port=28888,
    attenuation_port_numbers=[1, 2, 3, 4],
    model="MCS2338A2-128B16-A4",
)


_ru1_pdu = FACOM(addr="10.57.243.16", port_numbers=[1])
_ru2_pdu = FACOM(addr="10.57.243.16", port_numbers=[2])
_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[1],
    radio_type=RadioTypes.AVQL,
    signal_analyzer=None,
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
    radio_type=RadioTypes.AVQL,
    signal_analyzer=None,
)

_lmp_connection = SshServiceDetails(
    addr="10.57.224.103", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.57.243.16", port_numbers=[3])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=_capacity_unit,
    pdu_port=_gnb_pdu.pdu_ports[3],
)

_airscale = Airscale(common_units=[_common_unit_0])


_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2],
    f1_m_ip_addr="10.57.224.103",
    f1_c_ip_addr="10.57.224.103",
    f1_u_ip_addr="10.57.224.103",
)


# #CU
_cu = CU(
    backhaul_site_oam_ip="10.57.224.103",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.224.103", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.224.103", username="Nemuadmin", password="nemuuser"
    ),
)


_classical_bts0 = ClassicalBts(dus=[_du], cu=_cu, instance_id=38111)


_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts0],
    core=_realcore,
    enbs=[_lte_real_enb0],
    ues=[_ue0],
    appserver=_appserver,
    attenuator=[_attenuator],
    tl_cloud_topology=_tl_cloud_topology,
)
