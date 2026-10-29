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

# UE
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.179.233", username="vrf3_sg7", password="Haz4_vrf_sg3"
    ),
    network_interface_address="10.57.179.233",
    iperf_path="iperf",
    port="58000",
)

_appserver = AppServer(_iperf_details_on_appserver)

_licensekeeper = LicenseKeeper(username="zhiguo.li@nokia-sbell.com", password="nokia123")

_sigspark_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.64.57.30", username="mn5gran", password="nokia123@"
    ),
    serial_number="886b92af",
    server_dir="C:/Spark1.1.2009.48/Bin/Spark.exe",
    python_path="C:/Python39",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100015421",
    licensekeeper=_licensekeeper,
    capabilities=["huawei_sigspark"],
)

_sigspark_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.64.57.30", username="mn5gran", password="nokia123@"
    ),
    serial_number="921aba9c",
    server_dir="C:/Spark1.1.2009.48/Bin/Spark.exe",
    python_path="C:/Python39",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100015432",
    licensekeeper=_licensekeeper,
    capabilities=["huawei_sigspark"],
)

# Attenuator
_attenuator0 = HBTE(
    ip_addr="10.64.56.25",
    port=5000,
    attenuation_port_numbers=[ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

_attenuator1 = HBTE(
    ip_addr="10.64.56.20",
    port=5000,
    attenuation_port_numbers=[ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

# PB
_pdu_0 = pdu_HBTE(addr="10.64.49.70", port_numbers=[1, 2, 3, 4, 5, 6])

_pdu_1 = pdu_HBTE(addr="10.64.49.68", port_numbers=[1, 2, 3, 4, 5, 6])

# LMI
_ru_lmi_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.64.57.25", username="mn5gran", password="nokia123@"
    )
)

_ru_lmi_0 = LMI(product_code="",
              host=_ru_lmi_pc,
              uart_mapping=[Local(port="COM3")])

_ru_lmi_1 = LMI(product_code="",
              host=_ru_lmi_pc,
              uart_mapping=[Local(port="COM4")])

# 5GRU for classicalBTS
_ru_0 = RU(
    ru_hw_group="AZHA",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_0.pdu_ports[6],
    radio_type=RadioTypes.AZHA.value,
    serial_number="EA204859647",
    attenuation_ports=[
        _attenuator1.attenuator_ports[5],
        _attenuator1.attenuator_ports[6],
        _attenuator1.attenuator_ports[7],
        _attenuator1.attenuator_ports[8],
    ],
    lmi=_ru_lmi_0
)

_ru_1 = RU(
    ru_hw_group="AHFIB",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_0.pdu_ports[5],
    radio_type=RadioTypes.AHFIB.value,
    serial_number="BL2119V0CH5",
    attenuation_ports=[
        _attenuator1.attenuator_ports[1],
        _attenuator1.attenuator_ports[2],
        _attenuator1.attenuator_ports[3],
        _attenuator1.attenuator_ports[4],
    ],
    lmi=_ru_lmi_1
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.64.53.41", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

# _gnb_pdu = pdu_HBTE(addr="10.64.49.70", port_numbers=[1])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    # pdu_port=_gnb_pdu.pdu_ports[1],
    pdu_port=_pdu_0.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru_0, _ru_1], f1_m_ip_addr="10.64.53.41")

# CU
_cu = CU(
    backhaul_site_oam_ip="10.64.53.41",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.64.53.41", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.64.53.41", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=2403, global_bts_id=2403)

# cloud_topology------------------------------------------------
_tl_cloud_topology = "TL2403"

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.72", username="ute", password="iW_K#8.ute%A10h0m0ra"
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
         _sigspark_1],
    appserver=_appserver,
    attenuators=[_attenuator1],
)


if __name__ == "__main__":
    print("Example use of new TL config")
    print("UE_IP is:{}".format(tl.ues[0].data_transfer[0].bind_ue_ip))
