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
from taf.config.testline import Connection

__maintainer__ = "Zhou Lingyan"
__team__ = "I_NSB_MN_RAN_RD_VRF_HAZ3_07_GMS <I_NSB_MN_RAN_RD_VRF_HAZ3_07@internal.nsn.com>"
__email__ = "lingyan.zhou@nokia-sbell.com"

# common
__all__ = ["tl"]
_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# UE
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.179.233", username="vrf3_sg7", password="Haz4_vrf_sg3"
    ),
    network_interface_address="10.57.179.233",
    iperf_path="iperf",
    port="58004",
)

_licensekeeper = LicenseKeeper(username="VRF3_T07", password="VRF3_T07")
_appserver = AppServer(_iperf_details_on_appserver)
_sigspark_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.125", username="mn5gran", password="nokia123@"
    ),
    serial_number="27fdd06e",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Users/tester5g/AppData/Local/Programs/Python/Python39",
    iperf_details=_iperf_details_on_appserver,
    imsi="262038001004007",
    licensekeeper=_licensekeeper,
    capabilities=["huawei_sigspark"],
)
_sigspark_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.125", username="mn5gran", password="nokia123@"
    ),
    serial_number="3bae71db",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Users/tester5g/AppData/Local/Programs/Python/Python39",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100020891",
    licensekeeper=_licensekeeper,
    capabilities=["huawei_sigspark"],
)

_sigspark_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.254", username="mn5gran", password="nokia123@"
    ),
    serial_number="921aba64",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Users/tester5g/AppData/Local/Programs/Python/Python39",
    iperf_details=_iperf_details_on_appserver,
    imsi="310260100016976",
    licensekeeper=_licensekeeper,
    capabilities=["huawei_sigspark"],
)

_sigspark_3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.254", username="mn5gran", password="nokia123@"
    ),
    serial_number="921aba77",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Users/tester5g/AppData/Local/Programs/Python/Python39",
    iperf_details=_iperf_details_on_appserver,
    imsi="310260100016977",
    licensekeeper=_licensekeeper,
    capabilities=["huawei_sigspark"],
)
# Attenuator
_attenuator_0 = HBTE(
    ip_addr="10.71.206.202",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

_attenuator_1 = RadioRack(
    ip_addr="10.71.206.184",
    port=23,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
    model="8-200",
)

_attenuator_2 = RadioRack(
    ip_addr="10.71.206.185",
    port=23,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
    model="8-200",
)

_attenuator_3 = RadioRack(
    ip_addr="10.71.206.203",
    port=23,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
    model="8-200",
)

_pdu_0 = pdu_HBTE(addr="10.71.197.67", port_numbers=[1, 2, 3])
_pdu_1 = pdu_HBTE(addr="10.71.197.66", port_numbers=[1, 2, 3, 4, 5, 6])
_pdu_2 = pdu_HBTE(addr="10.71.197.69", port_numbers=[1, 2, 3])


# 5GRU for classicalBTS_AEHC_AH234900463_NRCELL301&NRCELL311
_ru_0 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_0.pdu_ports[3],
    radio_type=RadioTypes.AEHC.value,
    serial_number="AH234900463",
    attenuation_ports=[#addothers
        _attenuator_0.attenuator_ports[1],
        _attenuator_0.attenuator_ports[2],
        _attenuator_0.attenuator_ports[3],
        _attenuator_0.attenuator_ports[4],
    ],
)

# 5GRU for classicalBTS_AEHC_AH234900468_NRCELL302&NRCELL312
_ru_1 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_1.pdu_ports[5],
    radio_type=RadioTypes.AEHC.value,
    serial_number="AH234900468",
    attenuation_ports=[#addothers
        _attenuator_0.attenuator_ports[5],
        _attenuator_0.attenuator_ports[6],
        _attenuator_0.attenuator_ports[7],
        _attenuator_0.attenuator_ports[8],
    ],
)

# 5GRU for classicalBTS_AEHC_AH234900471_NRCELL303&NRCELL313
_ru_2 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_1.pdu_ports[2],
    radio_type=RadioTypes.AEHC.value,
    serial_number="AH234900471",
    attenuation_ports=[#addothers
        _attenuator_0.attenuator_ports[9],
        _attenuator_0.attenuator_ports[10],
        _attenuator_0.attenuator_ports[11],
        _attenuator_0.attenuator_ports[12],
    ],
)


# 5GRU for classicalBTS_AHFIB_K9183827791_NRCELL21
_ru_3 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_0.pdu_ports[1],
    radio_type=RadioTypes.AHFIB.value,
    serial_number="K9183827791",
    attenuation_ports=[#addothers
        _attenuator_1.attenuator_ports[1],
        _attenuator_1.attenuator_ports[2],
        _attenuator_1.attenuator_ports[3],
        _attenuator_1.attenuator_ports[4],
    ],
)

# 5GRU for classicalBTS_AHFIB_K9183736560_NRCELL22
_ru_4 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_1.pdu_ports[1],
    radio_type=RadioTypes.AHFIB.value,
    serial_number="K9183736560",
    attenuation_ports=[#TBD
        _attenuator_1.attenuator_ports[5],
        _attenuator_1.attenuator_ports[6],
        _attenuator_1.attenuator_ports[7],
        _attenuator_1.attenuator_ports[8],
    ],
)

# 5GRU for classicalBTS_AHFIB_BL2049V0VKF_NRCELL23
_ru_5 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_2.pdu_ports[1],
    radio_type=RadioTypes.AHFIB.value,
    serial_number="BL2049V0VKF",
    attenuation_ports=[#TBD
        _attenuator_2.attenuator_ports[1],
        _attenuator_2.attenuator_ports[2],
        _attenuator_2.attenuator_ports[3],
        _attenuator_2.attenuator_ports[4],
    ],
)

# 5GRU for classicalBTS_AHLOA_BL1930G11TF_NRCELL1
_ru_6 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_2.pdu_ports[3],
    radio_type=RadioTypes.AHLOA.value,
    serial_number="BL1930G11TF",
    attenuation_ports=[#TBD
        _attenuator_2.attenuator_ports[5],
        _attenuator_2.attenuator_ports[6],
        _attenuator_2.attenuator_ports[7],
        _attenuator_2.attenuator_ports[8],
    ],
)

# 5GRU for classicalBTS_AHLOA_BL2223G1B97_NRCELL2
_ru_7 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_2.pdu_ports[2],
    radio_type=RadioTypes.AHLOA.value,
    serial_number="BL1930G11TF",
    attenuation_ports=[#TBD
        _attenuator_3.attenuator_ports[1],
        _attenuator_3.attenuator_ports[2],
        _attenuator_3.attenuator_ports[3],
        _attenuator_3.attenuator_ports[4],
    ],
)

# 5GRU for classicalBTS_AHLOA_BL2223G1B2M_NRCELL3
_ru_8 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_0.pdu_ports[2],
    radio_type=RadioTypes.AHLOA.value,
    serial_number="BL1930G11TF",
    attenuation_ports=[#TBD
        _attenuator_3.attenuator_ports[5],
        _attenuator_3.attenuator_ports[6],
        _attenuator_3.attenuator_ports[7],
        _attenuator_3.attenuator_ports[8],
    ],
)


# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.71.215.140", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = pdu_HBTE(addr="10.71.197.68", port_numbers=[1, 2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru_0, _ru_1, _ru_2, _ru_3, _ru_4, _ru_5, _ru_6,_ru_7,_ru_8], f1_m_ip_addr="10.71.215.140")

# CU
_cu = CU(
    backhaul_site_oam_ip="10.71.215.140",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.215.140", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.215.140", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=2002, global_bts_id=2002)

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "Refers to TAF UTE TL Type"

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.153", username="ute", password="iW_K#8.ute%A10h0m0ra"
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
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_sigspark_0,
         _sigspark_1,
         _sigspark_2,
         _sigspark_3],
    appserver=_appserver,
	attenuators=[_attenuator_0, _attenuator_1, _attenuator_2, _attenuator_3]
)


if __name__ == "__main__":
    print("Example use of new TL config")
    print("UE_IP is:{}".format(tl.ues[0].data_transfer[0].bind_ue_ip))
