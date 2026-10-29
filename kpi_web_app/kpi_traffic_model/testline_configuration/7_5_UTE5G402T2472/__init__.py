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
from taf.config.testline.testline import TestLine
from taf.config.testline import Connection

__maintainer__ = "Lei XiaoJian"
__team__ = "I_NSB_MN_RAN_RD_VRF_HAZ3_07_GMS <I_NSB_MN_RAN_RD_VRF_HAZ3_07@internal.nsn.com>"
__email__ = "damon.lei@nokia-sbell.com"

# common
__all__ = ["tl"]
_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_tl_cloud_topology = "TL2472"

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.71.214.137", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = pdu_HBTE(addr="10.71.196.250", port_numbers=[3])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)

_airscale = Airscale(common_units=[_common_unit_0])

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.191", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

# UE
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.179.233", username="vrf3_sg7", password="vrf3@sg7"
    ),
    network_interface_address="10.57.179.233",
    iperf_path="iperf",
    port="47601",
)

_licensekeeper = LicenseKeeper(username="susana.yan@nokia-sbell.com", password="nokia123")
_appserver = AppServer(_iperf_details_on_appserver)
_sigspark_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.104", username="spark", password="spark"
    ),
    serial_number="36d65f48",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.42/Bin/Spark.exe",
    python_path="C:/Users/spark/AppData/Local/Programs/Python/Python313",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100016900",
    licensekeeper=_licensekeeper,
    capabilities=["huawei_sigspark"],
)
_sigspark_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.104", username="spark", password="spark@"
    ),
    serial_number="36c96024",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.42/Bin/Spark.exe",
    python_path="C:/Users/spark/AppData/Local/Programs/Python/Python313",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100016901",
    licensekeeper=_licensekeeper,
    capabilities=["huawei_sigspark"],
)

# Attenuator
_attenuator = HBTE(
    ip_addr="10.71.201.23",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

_attenuator_1 = HBTE(
    ip_addr="10.71.201.24",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)
# 2ah 5ae 6ah
_pdu_0 = pdu_HBTE(addr="10.71.196.250", port_numbers=[2, 3, 5, 6])
_pdu_1 = pdu_HBTE(addr="10.71.197.2", port_numbers=[1])
# _pdu_2 = pdu_HBTE(addr="10.71.197.69", port_numbers=[1, 2, 3])


# 4GRU for classicalBTS_AHLOA_LNCEL1&LNCEL2
_ru_0 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="10.71.196.250", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_0.pdu_ports[2],
    radio_type=RadioTypes.AHLOA.value,
    serial_number="BL2034G1HHW",
    attenuation_ports=[  # addothers
        _attenuator_1.attenuator_ports[1],
        _attenuator_1.attenuator_ports[2],
        _attenuator_1.attenuator_ports[3],
        _attenuator_1.attenuator_ports[4],
    ],
)

# 5GRU for classicalBTS_AHLOA_NRCELL2_14
_ru_1 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.56.154", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_0.pdu_ports[5],
    radio_type=RadioTypes.AHLOA.value,
    serial_number="K9183926414",
    attenuation_ports=[  # addothers
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

# 5GRU for classicalBTS_AEQV_NRCELL1_205
_ru_2 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.56.6", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_0.pdu_ports[6],
    radio_type=RadioTypes.AEQV.value,
    serial_number="1M200802187",
    attenuation_ports=[  # addothers
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
    ],
)

# 5GRU for classicalBTS_AEQV_NRCELL5_205_CALL
_ru_3 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.56.6", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_1.pdu_ports[1],
    radio_type=RadioTypes.AEQV.value,
    serial_number="1M194810348",
    attenuation_ports=[  # addothers
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
)

# 5GRU for classicalBTS_AEQV_NRCELL5_205--CALL

_du = DU(airscale=_airscale, rus=[_ru_0, _ru_1, _ru_2, _ru_3], f1_m_ip_addr="10.71.214.137")

# CU
_cu = CU(
    backhaul_site_oam_ip="10.71.214.137",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.214.137", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.214.137", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=37566, global_bts_id=37566)

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "Refers to TAF UTE TL Type"

tl = TestLine(
    test_pc=_host,
    test_pcs=[_host],
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_sigspark_0,
         _sigspark_1,
         ],
    appserver=_appserver,
    attenuators=[_attenuator, _attenuator_1, ]
)

if __name__ == "__main__":
    print("Example use of new TL config")
    print("UE_IP is:{}".format(tl.ues[0].data_transfer[0].bind_ue_ip))
