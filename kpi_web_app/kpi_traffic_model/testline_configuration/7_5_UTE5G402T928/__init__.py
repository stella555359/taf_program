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
        addr="10.57.157.107", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.157.107",
    username="ute",
    password="iW_K#8.ute%A10h0m0ra",
    port="43500",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.157.107",
    iperf_path="iperf",
    port="43500",
)

# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.68.86.210", username="mn5gran", password="nokia123@"
)

_appserver = AppServer(_iperf_details_on_appserver)

# spark license
_licensekeeper = LicenseKeeper(username="zhaori.deng@nokia-sbell.com", password="nokia123")

_sigspark1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="16357389",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.45/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033100000052",
    licensekeeper=_licensekeeper,
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="45911c07",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.45/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033031394044",
	licensekeeper=_licensekeeper,
)


_realcore = RealCore(four_g=None, five_g=None, mcc="262", mnc="3", pdns=None)

# #attenuator
#_hbte_params1 = {
#    ip_addr="10.101.41.66",
#    port=5000,
#    attenuation_port_numbers=[13, 14, 15, 16],
#    model="PA-16-16-6-127-0.5-B-S",
#}
#_attenuator1 = AHBTE(**_hbte_params1)



_ru1_pdu = HBTE(addr="10.101.45.232", port_numbers=[4])
_ru2_pdu = HBTE(addr="10.101.45.232", port_numbers=[6])
_ru3_pdu = HBTE(addr="10.101.45.230", port_numbers=[1])


_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="lucent", password="password"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[4],
    radio_type=RadioTypes.AVQC,
#    attenuation_ports=[
#        _attenuator.attenuator_ports[13],
#        _attenuator.attenuator_ports[14],
#        _attenuator.attenuator_ports[15],
#        _attenuator.attenuator_ports[16],
#    ],
)
_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.2", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[6],
    radio_type=RadioTypes.AVQC,
#    attenuation_ports=[
#        _attenuator.attenuator_ports[13],
#        _attenuator.attenuator_ports[14],
#        _attenuator.attenuator_ports[15],
#        _attenuator.attenuator_ports[16],
#    ],
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
    radio_type=RadioTypes.AHFIB,
#    attenuation_ports=[
#        _attenuator.attenuator_ports[13],
#        _attenuator.attenuator_ports[14],
#        _attenuator.attenuator_ports[15],
#        _attenuator.attenuator_ports[16],
#    ],
)

_lmp_connection = SshServiceDetails(
    addr="10.101.51.163", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.101.45.234", port_numbers=[2])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=_capacity_unit,
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit_0])


_du = DU(
    airscale=_airscale,
    rus=[_ru1],
    f1_m_ip_addr="10.101.51.163",
)


# #CU
_cu = CU(
    backhaul_site_oam_ip="10.101.51.163",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.51.163", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.51.163", username="Nemuadmin", password="nemuuser"
    ),
)


_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=10208, global_bts_id=928)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_realcore,
    ues=[_sigspark1, _sigspark2],
    appserver=_appserver,
#    attenuator=_attenuator,

)
