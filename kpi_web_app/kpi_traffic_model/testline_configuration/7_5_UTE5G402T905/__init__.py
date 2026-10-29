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
        addr="10.57.189.23", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)



# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.101.41.70", username="spark", password="spark"
)

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.147", username="vrf3_sg3", password="vrf3@sg3", port="43567"
)


_iperf = IperfDataTransferDetails(	
	ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.147",
    iperf_path="iperf",
    port="43381",
)

_appserver = AppServer(_iperf)


# spark license
_licensekeeper = LicenseKeeper(username="ning.4.liu@nokia-sbell.com", password="nokia123")

_sigspark1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="129f8d47",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.42/Bin/Spark.exe",
    python_path="C:/Python310",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033100017596",
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="d9feee2",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.42/Bin/Spark.exe",
    python_path="C:/Python310",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033100017595",
)

_sigspark3 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="a66f4f4",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.42/Bin/Spark.exe",	            
    python_path="C:/Python310",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033100017597",
)

_sigspark4 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="e0b1c8da",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.42/Bin/Spark.exe",
    python_path="C:/Python310",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033100017599",
)

_sigspark5 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="26d62dc2",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.42/Bin/Spark.exe",
    python_path="C:/Python310",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033100017598",
)

_sigspark6 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="b6e81d31",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.42/Bin/Spark.exe",
    python_path="C:/Python310",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033100017593",
)


_realcore = RealCore(four_g=None, five_g=None, mcc="262", mnc="3", pdns=None)

# attenuator
_attenuator = AHBTE(
    ip_addr="10.101.41.74",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)


# 5GRU for classicalBTS
_ru_pdu = TopYoung(addr="10.101.45.230", port_numbers=[2, 3])



_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="lucent", password="password"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHPJ,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
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
    pdu_port=_ru_pdu.pdu_ports[3],
    radio_type=RadioTypes.AQQJ,
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)



_lmp_connection = SshServiceDetails(
    addr="10.101.51.168", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.101.45.234", port_numbers=[7])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=_capacity_unit,
    pdu_port=_gnb_pdu.pdu_ports[7],
)

_airscale = Airscale(common_units=[_common_unit_0])


_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2],
    f1_m_ip_addr="10.101.51.168",
)


# #CU
_cu = CU(
    backhaul_site_oam_ip="10.101.51.168",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.51.168", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.51.168", username="Nemuadmin", password="nemuuser"
    ),
)


_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=10462, global_bts_id=10462)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_realcore,
    ues=[_sigspark1, _sigspark2, _sigspark3, _sigspark4, _sigspark5, _sigspark6],
    appserver=_appserver,
    attenuator=_attenuator,

)
