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
from taf.config.testline.pdu import FPFH
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
__maintainer__ = "Xiang Kang"
__team__ = "I_NSB_MN_RAN_RD_VRF_HAZ3_07_GMS <I_NSB_MN_RAN_RD_VRF_HAZ3_07@internal.nsn.com>"
__email__ = "kang.xiang@nokia.com"

# common
__all__ = ["tl"]
_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.85", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# UE
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.179.237", username="vrf3_sg7", password="vrf3@sg7"
    ),
    network_interface_address="10.57.179.237",
    iperf_path="/cygdrive/c/iperf",
    port="58010",
)

_licensekeeper = LicenseKeeper(username="ruifang.zhu@nokia-sbell.com", password="nokia123")
_appserver = AppServer(_iperf_details_on_appserver)

#samsung
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.64.57.31", username="mn5gran", password="nokia123@"
    ),
    serial_number="RFCR10NTXLW",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/python310/python.exe",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["samsung", "samsung_lte"],
    imsi="262033100015430",
    sec_key="13100015430",
    pdn=["dxdata2", "mdrb.nokia.com"]
)

# _sigspark_0 = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="1.1.1.1", username="mn5gran", password="nokia123@"
#     ),
#     serial_number="57e5341",
#     server_dir="C:\Program Files (x86)\Spark1.1.2009.45\Bin\Spark.exe",
#     python_path="C:/Users/tester5g/AppData/Local/Programs/Python/Python39",
#     iperf_details=_iperf_details_on_appserver,
#     imsi="262033100017536",
#     licensekeeper=_licensekeeper,
#     capabilities=["huawei_sigspark"],
# )
# _sigspark_1 = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="1.1.1.2", username="mn5gran", password="nokia123@"
#     ),
#     serial_number="57e52ae",
#     server_dir="C:\Program Files (x86)\Spark1.1.2009.45\Bin\Spark.exe",
#     python_path="C:/Users/tester5g/AppData/Local/Programs/Python/Python39",
#     iperf_details=_iperf_details_on_appserver,
#     imsi="262033100017537",
#     licensekeeper=_licensekeeper,
#     capabilities=["huawei_sigspark"],
# )
# Attenuator
_attenuator = HBTE(
    ip_addr="10.64.56.69",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

_pdu_0 = FPFH(addr="10.64.49.79", port_numbers=[1, 2, 3, 4, 5, 6],login="admin", password="admin")
_pdu_1 = FPFH(addr="10.64.49.80", port_numbers=[1, 2, 3, 4, 5, 6],login="admin", password="admin")


# 5GRU for classicalBTS_AHPMDG_K9252520998_NRCELL111_LTECELL21_LTECELL31_GSMCell1
_ru_0 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_0.pdu_ports[1],
    radio_type=RadioTypes.AHFIB.value,
    serial_number="K925252099",
    attenuation_ports=[#addothers
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

# 5GRU for classicalBTS_AHPMDG_K9252520993_NRCELL112_LTECELL22_LTECELL32_GSMCell2
_ru_1 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_0.pdu_ports[4],
    radio_type=RadioTypes.AHLOA.value,
    serial_number="K9252520993",
    attenuation_ports=[#TBD
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

# 5GRU for classicalBTS_AHPMDG_K9251151204_NRCELL113_LTECELL23_LTECELL33_GSMCell3
_ru_2 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_1.pdu_ports[1],
    radio_type=RadioTypes.AEQV.value,
    serial_number="K9251151204",
    attenuation_ports=[#TBD
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
)

# 5GRU for classicalBTS_AHCA_K9251151204_NRCELL114_NRCELL115_NRCELL116
_ru_3 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_1.pdu_ports[4],
    radio_type=RadioTypes.AEQV.value,
    serial_number="1M212615247",
    attenuation_ports=[#TBD
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)


# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.64.54.162", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FPFH(addr="10.64.49.79", port_numbers=[1, 2, 3, 4, 5, 6],login="admin", password="admin")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[6],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru_0, _ru_1, _ru_2, _ru_3], f1_m_ip_addr="10.64.54.132")

# CU
_cu = CU(
    backhaul_site_oam_ip="10.64.54.162",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.64.54.162", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.64.54.162", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=2410, global_bts_id=2410)

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "Refers to TAF UTE TL Type"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_android],
    appserver=_appserver,
    attenuator=[_attenuator],
)


if __name__ == "__main__":
    print("Example use of new TL config")
    print("UE_IP is:{}".format(tl.ues[0].data_transfer[0].bind_ue_ip))
