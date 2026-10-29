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
from taf.config.testline.pdu import HBTE as pdu_HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline import Connection
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
    MediaTek,
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
    JFW,
    HBTE,
    Hytem,
    RadioRack,
)
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
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
from taf.config.testline.optical_switch import Leoni, Calient
from taf.config.testline.appserver import AppServer
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline import LicenseKeeper
from taf.config.testline.attenuator import RadioRack
from taf.config.testline.lmi import LMI, Local

__maintainer__ = "Yin Zhang"
__team__ = "I_NSB_MN_RAN_RD_VRF_HAZ3_07@nokia.com"
__email__ = "yin.zhang@nokia-sbell.com"

# common
__all__ = ["tl"]
_cfg_dir = os.path.dirname(os.path.abspath(__file__))


# spark 2UE
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.179.233", username="vrf3_sg7", password="Haz4_vrf_sg3"
    ),
    network_interface_address="10.57.179.233",
    iperf_path="iperf",
    port="58000",
)

_licensekeeper = LicenseKeeper(username="yin.zhang@nokia-sbell.com", password="nokia123")
_appserver = AppServer(_iperf_details_on_appserver)
_sigspark_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.64.56.26", username="nokia5g", password="noki@123"
    ),
    serial_number="921aba78",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/python38",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100015422",
    licensekeeper=_licensekeeper,
    capabilities=["huawei_sigspark"],
)
_sigspark_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.64.56.26", username="nokia5g", password="noki@123"
    ),
    serial_number="921aba4b",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/python38",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100015424",
    licensekeeper=_licensekeeper,
    capabilities=["huawei_sigspark"],
)

# Qualcomm UE
_appserver_ssh = SshServiceDetails(
    addr="10.57.179.233",
    username="vrf3_sg7",
    password="vrf3@sg7",
    port="58010",
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.179.233",
    iperf_path="/cygdrive/c/iperf",
    port="58010",
)
 
_android_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.64.57.14", username="mn5gran", password="nokia123@"
    ),
    serial_number="52ee2753",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/python310/python.exe",
    iperf_details=_iperf,
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["qct_dx50", "REAL_ANDROID_UE", "qct_dx50"],
    imsi="262033100015431",
    sec_key="13100015431",
    pdn=["dxdata2", "mdrb.nokia.com"],
)

# Attenuator
_attenuator = HBTE(
    ip_addr="10.64.56.24",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

# 5GRU for classicalBTS
_pdu_0 = pdu_HBTE(addr="10.64.49.75", port_numbers=[1, 2, 6])

_ru_lmi_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.64.57.54", username="mn5gran", password="nokia123@"
    )
)

#_ru_lmi_2 = LMI(product_code="",
#              host=_ru_lmi_pc,
#              uart_mapping=[Local(port="COM3"), Local(port="COM4")])

_ru_lmi_2 = LMI(product_code="",
              host=_ru_lmi_pc,
              uart_mapping=[Local(port="COM3")])

_ru_lmi_0 = LMI(product_code="",
              host=_ru_lmi_pc,
              uart_mapping=[Local(port="COM6")])
_ru_0 = RU(
    ru_hw_group="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_0.pdu_ports[6],
    radio_type=RadioTypes.AHLOA.value,
    serial_number="BL1930G11PY",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
    # lmi=_ru_lmi_0
)
_ru_1 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_0.pdu_ports[1],
    radio_type=RadioTypes.AZQO.value,
    serial_number="1M210327809",
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
)
_ru_2 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_0.pdu_ports[2],
    radio_type=RadioTypes.AHFII.value,
    serial_number="BL2340N4A0O",
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
    # lmi=_ru_lmi_2
)
# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.64.53.39", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = pdu_HBTE(addr="10.64.49.74", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru_0, _ru_1, _ru_2], f1_m_ip_addr="10.64.53.39")

# CU
_cu = CU(
    backhaul_site_oam_ip="10.64.53.39",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.64.53.39", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.64.53.39", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=2405, global_bts_id=2405)

# enb
_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.64.56.23", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None, instance_id=2405)


# #cloud_topology------------------------------------------------
_tl_cloud_topology = "TL2405"

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.74", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

tl = TestLine(
    test_pc=_host,
    test_pcs=[_host],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_sigspark_0,
         _sigspark_1,
         _android_2],
    appserver=_appserver,
    attenuator=_attenuator,
)

if __name__ == "__main__":
    print("Example use of new TL config")
    print("UE_IP is:{}".format(tl.ues[0].data_transfer[0].bind_ue_ip))
