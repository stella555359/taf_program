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

__maintainer__ = "Chen Dandan"
__team__ = "I_NSB_MN_RAN_RD_VRF_HAZ3_07_GMS <I_NSB_MN_RAN_RD_VRF_HAZ3_07@internal.nsn.com>"
__email__ = "dandan.chen@nokia-sbell.com"

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
    port="47777",
)

_licensekeeper = LicenseKeeper(username="dandan.chen@nokia-sbell.com", password="nokia123")
_appserver = AppServer(_iperf_details_on_appserver)
_sigspark_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.181", username="mn5gran", password="nokia123@"
    ),
    serial_number="FMR0224123036973",
    server_dir="C:/Program Files (x86)/Spark1.1.2011.3/Bin/Spark.exe",
    python_path="C:/Users/tester5g/AppData/Local/Programs/Python/Python39",
    iperf_details=_iperf_details_on_appserver,
    imsi="460023100020795",
    licensekeeper=_licensekeeper,
    capabilities=["huawei_sigspark"],
)

# Attenuator
_attenuator = TopYoung(
    ip_addr="10.71.206.84",
    port=23,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="TAS16T16-51-120-1S-DES",
)

_pdu_1 = pdu_HBTE(addr="10.71.197.12", port_numbers=[1, 2, 3, 4, 5, 6])


# 5GRU for classicalBTS_AQQJ_1M232102630_NRCELL1
_ru_0 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_1.pdu_ports[2],
    radio_type=RadioTypes.AQQJ.value,
    serial_number="1M232102630",
    attenuation_ports=[#addothers
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

# 5GRU for classicalBTS_AHPB_EA204457595_NRCELL2
_ru_1 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_1.pdu_ports[1],
    radio_type=RadioTypes.AHPB.value,
    serial_number="EA204457595",
    attenuation_ports=[#TBD
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
    ],
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.71.214.203", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = pdu_HBTE(addr="10.71.197.13", port_numbers=[7])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[7],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru_0, _ru_1], f1_m_ip_addr="10.71.214.203")

# CU
_cu = CU(
    backhaul_site_oam_ip="10.71.214.203",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.214.203", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.214.203", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=37694, global_bts_id=37694)

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "Refers to TAF UTE TL Type"

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.26", username="ute", password="iW_K#8.ute%A10h0m0ra"
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
    ues=[_sigspark_0],
    appserver=_appserver,
    attenuator=_attenuator,
)


if __name__ == "__main__":
    print("host is:{}".format(tl.test_pcs[0].default_ssh_connection_details.addr))
