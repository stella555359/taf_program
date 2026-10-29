import os
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.testpc import Connection

# added in taf.meta 5.4
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.attenuator import HBTE as PA_HBTE
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.appserver import AppServer

__maintainer__ = "Yu Lu"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_2_GMS <I_MN_5G_RAN_IV4_LINE_HZG_2@internal.nsn.com>"
)
__email__ = "lu.1.yu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))


# CI_Detail_UE_Type='Huawei Mate 20'

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.236", username="vrf4_sg2", password="VERIFICATION@sg2"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.236",
    iperf_path="/usr/bin/iperf",
    port=52553,
)

_huawei_host_ssh = SshServiceDetails(
    addr="10.57.130.58", username="nokia5G", password="noki@123"
)

iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_huawei_host_ssh,
    network_interface_address="10.57.191.236",
    iperf_path="/cygdrive/c/iperf-2.0.8b-win64/iperf",
    port=52553,
)


_appserver = AppServer(iperf_details)


_huawei_pdu = HBTE(addr="1.1.1.1", port_numbers=[2]).pdu_ports[2]

_huawei = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.58", username="nokia5G", password="noki@123"
    ),
    serial_number="L8K5T19919006382",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "Huawei"],
)

_huawei.pdu = _huawei_pdu

# add 1 more 5g ru info
_attenuator = PA_HBTE(
    ip_addr="10.57.238.10",
    port=5000,
    attenuation_port_numbers=[1, 2],
    model="PA-16-16-6-127-0.5-B-S",
)

_ru1_pdu = HBTE(addr="10.57.131.138", port_numbers=[5])

_ru1 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7",
        username="rfsw",
        password="gSDBExyEbO33komYWL6iPrtSaYc5XimHAGrsJ/K8+AY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="8.8.8.8",
        username="rfsw",
        password="gSDBExyEbO33komYWL6iPrtSaYc5XimHAGrsJ/K8+AY=",
    ),
    pdu_port=_ru1_pdu.pdu_ports[5],
    radio_type=RadioTypes.AEQE.value,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
    ],
    serial_number="1M203304677",
)

# #DU
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIO",
)

_gnb_pdu = HBTE(addr="10.57.242.37", port_numbers=[8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[8],
    hardware_type="ASIB",
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1], f1_m_ip_addr="10.57.223.204")

# CU
_cu = CU(
    backhaul_site_oam_ip="10.57.223.204",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.223.204", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.223.204", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id=4294967295, global_bts_id=134217653
)

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.55", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)


# #cloud_topology------------------------------------------------
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_ASIBL_ABIOB1_AEQE"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    ues=[_huawei],
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
    test_pcs=[_host],
    appserver=_appserver,
)
