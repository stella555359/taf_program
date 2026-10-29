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
from taf.config.testline.pdu import TopYoung, FACOM, HBTE
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
from taf.config.testline.attenuator import HBTE as AHBTE
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
from taf.config.testline import LicenseKeeper

__maintainer__ = "ying.15.li"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_03_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_03@internal.nsn.com>"
)
__email__ = "ying.15.li@nokia-sbell.com"

__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.88", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.157.107",
    username="ute",
    password="iW_K#8.ute%A10h0m0ra",
    port="53386",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.157.107",
    iperf_path="iperf",
    port="53386",
)

# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.0.176.24", username="mn5gran", password="nokia123@"
)

_appserver = AppServer(_iperf_details_on_appserver)

# spark license
_licensekeeper = LicenseKeeper(username="hongye.fu@nokia-sbell.com", password="nokia123")

_sigspark1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="921abaa1",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.45/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262030030000539",
    licensekeeper=_licensekeeper,
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="886c936c",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.27/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262030030000365",
    licensekeeper=_licensekeeper,
)


_realcore = RealCore(four_g=None, five_g=None, mcc="262", mnc="3", pdns=None)

# #attenuator
_hbte_params1 = {
    "ip_addr": "10.71.203.137",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4],
    "model": "PA-8-2-6-127-0.5-B-S",
    "version": None,
}
_attenuator1 = AHBTE(**_hbte_params1)

_hbte_params2 = {
    "ip_addr": "10.71.203.137",
    "port": 5000,
    "attenuation_port_numbers": [9, 10, 11, 12],
    "model": "PA-8-2-6-127-0.5-B-S",
    "version": None,
}
_attenuator2 = AHBTE(**_hbte_params2)

_hbte_params3 = {
    "ip_addr": "10.71.203.137",
    "port": 5000,
    "attenuation_port_numbers": [13, 14, 15, 16],
    "model": "PA-8-2-6-127-0.5-B-S",
    "version": None,
}
_attenuator3 = AHBTE(**_hbte_params3)

_hbte_params4 = {
    "ip_addr": "10.71.203.150",
    "port": 5000,
    "attenuation_port_numbers": [13, 14, 15, 16],
    "model": "PA-8-2-6-127-0.5-B-S",
    "version": None,
}
_attenuator4 = AHBTE(**_hbte_params4)

_ru1_pdu = HBTE(addr="10.71.195.122", port_numbers=[1])
_ru2_pdu = HBTE(addr="10.71.195.122", port_numbers=[2])
_ru3_pdu = HBTE(addr="10.71.195.120", port_numbers=[1])
_ru4_pdu = HBTE(addr="10.71.195.122", port_numbers=[5])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.128", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.33.128", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[1],
    radio_type=RadioTypes.AHFIB,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator1.attenuator_ports[1],
        _attenuator1.attenuator_ports[2],
        _attenuator1.attenuator_ports[3],
        _attenuator1.attenuator_ports[4],
    ],
)
_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.2", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[2],
    radio_type=RadioTypes.AZQO,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator2.attenuator_ports[9],
        _attenuator2.attenuator_ports[10],
        _attenuator2.attenuator_ports[11],
        _attenuator2.attenuator_ports[12],
    ],
)

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.2", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2", username="root", password="umniedziala"
    ),
    pdu_port=_ru3_pdu.pdu_ports[1],
    radio_type=RadioTypes.AZQO,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator3.attenuator_ports[13],
        _attenuator3.attenuator_ports[14],
        _attenuator3.attenuator_ports[15],
        _attenuator3.attenuator_ports[16],
    ],
)

_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.2", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2", username="root", password="umniedziala"
    ),
    pdu_port=_ru4_pdu.pdu_ports[5],
    radio_type=RadioTypes.AHCA,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator4.attenuator_ports[13],
        _attenuator4.attenuator_ports[14],
        _attenuator4.attenuator_ports[15],
        _attenuator4.attenuator_ports[16],
    ],
)

_lmp_connection = SshServiceDetails(
    addr="10.71.209.66", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.71.195.110", port_numbers=[5])

_gnb_pdu1 = HBTE(addr="10.71.195.110", port_numbers=[1])


_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=_capacity_unit,
    pdu_port=_gnb_pdu.pdu_ports[5],
)

_airscale = Airscale(common_units=[_common_unit_0])


_du = DU(
    airscale=_airscale,
    rus=[_ru1],
    f1_m_ip_addr="10.71.209.66",
)

_lmp_connection1 = SshServiceDetails(
    addr="10.71.209.77", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit1 = CapacityUnit(addr="192.168.253.20")

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection1,
    capacity_units=_capacity_unit1,
    pdu_port=_gnb_pdu1.pdu_ports[1],
)

_airscale1 = Airscale(common_units=[_common_unit_1])

_du1 = DU(
    airscale=_airscale1,
    rus=[_ru2, _ru3, _ru4],
    f1_m_ip_addr="10.71.209.77",
)

# #CU
_cu = CU(
    backhaul_site_oam_ip="10.71.209.66",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.209.66", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.209.66", username="Nemuadmin", password="nemuuser"
    ),
)

_cu1 = CU(
    backhaul_site_oam_ip="10.71.209.77",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.209.77", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.209.77", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts0 = ClassicalBts(dus=[_du], cu=_cu, instance_id=10206)

_classical_bts1 = ClassicalBts(dus=[_du1], cu=_cu1, instance_id=11675)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts0, _classical_bts1],
    core=_realcore,
    ues=[_sigspark1, _sigspark2],
    appserver=_appserver,
    attenuator=[_attenuator1, _attenuator2, _attenuator3, _attenuator4],
    tl_cloud_topology=_tl_cloud_topology,
)
