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



__maintainer__ = "Keyun Ma"
__team__ = "i_mn_ran_rd_vrf_haz_03@internal.nsn.com"
__email__ = "keyun.ma@nokia.com"

# common
__all__ = ["tl"]
_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# TL info: UTE VM info
# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.121", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# UE
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.179.233", username="vrf3_sg7", password="Haz4_vrf_sg3"
    ),
    network_interface_address="10.57.179.233",
    iperf_path="iperf",
    port="47990",
)

_licensekeeper = LicenseKeeper(username="damon.lei@nokia.com", password="nokia123")
_appserver = AppServer(_iperf_details_on_appserver)


# TL info: control PC info
_ue_host_ssh_1 = SshServiceDetails(
    addr="10.64.57.49", username="mn5gran", password="nokia123@"
)

# TL info: spark info
_sigspark_1 = Android(
    ssh_connection_details=_ue_host_ssh_1,
    serial_number="921aba7b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.48/Bin/Spark.exe",
    python_path="C:/Users/mn5gran/AppData/Local/Microsoft/WindowsApps/",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["huawei_sigspark"],
    imsi="262033100016969",
    licensekeeper=_licensekeeper
)

# TL info: PA info
# Attenuator
_attenuator = HBTE(
    ip_addr="10.64.56.198",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

# RealEnb---------------------------------------------------------
# 5GRU------------------------------------
# add 2 more 5g ru info
# ru_hw_group: Above6GHZ or Below6GHZ

# TL info: RU PB 10.64.49.2 port 3 and port 1
_pdu_0 = pdu_HBTE(addr="10.64.49.4", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_pdu_1 = pdu_HBTE(addr="10.64.49.2", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_0 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.37.128", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.37.128", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_1.pdu_ports[1],
    radio_type=RadioTypes.AHFIA.value,
    serial_number="K9181645240",
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)

_ru_1 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.2", username="serviceuser", password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    pdu_port=_pdu_1.pdu_ports[3],
    radio_type=RadioTypes.AKQJ.value,
    serial_number="1M241112956",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

# TL info: gnb IP address for CU DU: 10.64.54.135
# #DU
_lmp_connection = SshServiceDetails(
    addr="10.64.54.135", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

# TL info: gNB PB 10.64.49.3 port 1
_gnb_pdu = pdu_HBTE(addr="10.64.49.3", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[8],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru_0, _ru_1], f1_m_ip_addr="10.64.54.135")

# CU
_cu = CU(
    backhaul_site_oam_ip="10.64.54.135",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.64.54.135", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.64.54.135", username="Nemuadmin", password="nemuuser"
    ),
)

# TL info: gNB ID
# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=11194, global_bts_id=11194)
#RealEnb--4G
_real_enb = Airscale(common_units=[_common_unit_0])

_lte_real_enb = RealEnb(
    airscale=_real_enb,
    system_module=_common_unit_0,
    oam_ip=NetworkAddress("10.64.54.135"),
	instance_id=11194,
)

# cloud_topology------------------------------------------------
_tl_cloud_topology = "Refers to TAF UTE TL Type"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    ues=[_sigspark_1],
    tl_cloud_topology=_tl_cloud_topology,
    enbs=[_lte_real_enb],
	appserver=_appserver,
    core=RealCore(mcc=262, mnc=3),
    test_pcs=[_host],
    attenuator=[_attenuator],
)


if __name__ == "__main__":
    print("Example use of new TL config")
    print("UE_IP is:{}".format(tl.ues[0].data_transfer[0].bind_ue_ip))
