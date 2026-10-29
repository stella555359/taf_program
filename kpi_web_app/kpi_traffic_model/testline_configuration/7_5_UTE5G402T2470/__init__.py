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
__maintainer__ = "Zhu Ruifang"
__team__ = "I_NSB_MN_RAN_RD_VRF_HAZ3_07_GMS <I_NSB_MN_RAN_RD_VRF_HAZ3_07@internal.nsn.com>"
__email__ = "ruifang.zhu@nokia-sbell.com"

# common
__all__ = ["tl"]
_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.31", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# UE
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.179.233", username="vrf3_sg7", password="vrf3@sg7"
    ),
    network_interface_address="10.57.179.233",
    iperf_path="iperf",
    port="47678",
)

_licensekeeper = LicenseKeeper(username="ruifang.zhu@nokia-sbell.com", password="nokia123")
_appserver = AppServer(_iperf_details_on_appserver)
_sigspark_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.64.57.47", username="mn5gran", password="nokia123@"
    ),
    serial_number="57e5341",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.45\Bin\Spark.exe",
    python_path="C:/Users/tester5g/AppData/Local/Programs/Python/Python39",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100017536",
    licensekeeper=_licensekeeper,
    capabilities=["huawei_sigspark"],
)
_sigspark_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.64.57.47", username="mn5gran", password="nokia123@"
    ),
    serial_number="57e52ae",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.45\Bin\Spark.exe",
    python_path="C:/Users/tester5g/AppData/Local/Programs/Python/Python39",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100017537",
    licensekeeper=_licensekeeper,
    capabilities=["huawei_sigspark"],
)
# Attenuator
_attenuator = HBTE(
    ip_addr="10.64.56.195",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
    model="PA-32-32-6-127-0.5",
)


_pdu_0 = pdu_HBTE(addr="10.64.49.4", port_numbers=[1, 2, 3, 4, 5, 6])
_pdu_1 = pdu_HBTE(addr="10.64.49.6", port_numbers=[1, 2, 3, 4, 5, 6])


# 5GRU for classicalBTS_AHFIB_BL2305V0GPQ_NRCELL11_NRCELL12
_ru_0 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_1.pdu_ports[1],
    radio_type=RadioTypes.AHFIB.value,
    serial_number="BL2305V0GPQ",
    attenuation_ports=[#addothers
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
        _attenuator.attenuator_ports[21],
        _attenuator.attenuator_ports[22],
    ],
)

# 5GRU for classicalBTS_AHLOA_BL2235G14FK_NRCELL13
_ru_1 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_1.pdu_ports[4],
    radio_type=RadioTypes.AHLOA.value,
    serial_number="BL1930G11TF",
    attenuation_ports=[#TBD
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[19],
        _attenuator.attenuator_ports[20],
    ],
)

# 5GRU for classicalBTS_AEQV_1M200802154_NRCELL5
_ru_2 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_1.pdu_ports[3],
    radio_type=RadioTypes.AEQV.value,
    serial_number="1M200802154",
    attenuation_ports=[#TBD
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

# 5GRU for classicalBTS_AEQV_1M212615247_NRCELL6
_ru_3 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_0.pdu_ports[6],
    radio_type=RadioTypes.AEQV.value,
    serial_number="1M212615247",
    attenuation_ports=[#TBD
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
)

# 5GRU for classicalBTS_AEHC_AH243304150_NRCELL4
_ru_4 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_1.pdu_ports[5],
    radio_type=RadioTypes.AHLOA.value,
    serial_number="AH243304150",
    attenuation_ports=[#TBD
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

# 5GRU for classicalBTS_AHFB_AH210800616_NRCELL14
_ru_5 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_1.pdu_ports[2],
    radio_type=RadioTypes.AHFB.value,
    serial_number="AH210800616",
    attenuation_ports=[#TBD
        _attenuator.attenuator_ports[17],
        _attenuator.attenuator_ports[18],
        _attenuator.attenuator_ports[23],
        _attenuator.attenuator_ports[24],
    ],
)


# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.64.54.132", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = pdu_HBTE(addr="10.64.49.4", port_numbers=[1, 2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru_0, _ru_1, _ru_2, _ru_3, _ru_4, _ru_5], f1_m_ip_addr="10.64.54.132")

# CU
_cu = CU(
    backhaul_site_oam_ip="10.64.54.132",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.64.54.132", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.64.54.132", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=37562, global_bts_id=37562)

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "Refers to TAF UTE TL Type"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_sigspark_0,
         _sigspark_1],
    appserver=_appserver,
    attenuator=[_attenuator],
)


if __name__ == "__main__":
    print("Example use of new TL config")
    print("UE_IP is:{}".format(tl.ues[0].data_transfer[0].bind_ue_ip))
