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
from taf.config.testline.pdu import (
    FACOM,
    PduPort,
    Pdu,
    EPC,
    ATEN,
    RRB,
    APC,
    Gude,
    FPFH,
    HBTE,
)
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
from taf.config.testline.appserver import AppServer, TafUeAppServer
from taf.config.testline.ue import (
    Qualcomm,
    QualcommUeType,
    Android,
    MediaTek,
    TafUeAndroid,
)
from taf.config.testline import (
    NetworkAddress,
    RoutingInformation,
    TafUeDataTransferProtocol,
)
from taf.config.testline.pdn import PDNTafUeAndroidDetails


__maintainer__ = "Zhang Xuewen"
__team__ = (
    "I_NSB_MN_RAN_RD_VRF_HAZ4_05_GMS <I_NSB_MN_RAN_RD_VRF_HAZ4_05@internal.nsn.com>"
)
__email__ = "xuewen.zhang@nokia-sbell.com"

__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

ue_config_path = os.path.join(_cfg_dir, "inseego.yml")
if os.path.isfile(ue_config_path):
    with open(ue_config_path) as f:
        ue_config = yaml.load(f)
else:
    ue_config = ""

_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.62", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CI_Detail_UE_Type='Xiaomi 12 Pro'
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.247", username="vrf4_sg5", password="vrf4@sg5", port=55267
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.247",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port=55268,
)

_appserver = AppServer(_iperf)

_app_server_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.247",
    user="vrf4_sg5",
    password="vrf4@sg5",
    bind_interface_ip="10.57.191.247",
    expected_prompt="[vrf4_sg5@appserver ~]$ ",
    binary_path="/home/vrf4_sg5/taf_debug/iperf",
    ports=[55257, 55258],
)


_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_app_server_1,
    interface_name="dxdata2",
    interval=1,
    binary_path="/data/data/com.nokia.android.application/",
    version=2,
)

_pdn1 = PDNTafUeAndroidDetails(
    entryName="dxdata2", apnName="dxdata2", apnType=["DEFAULT"]
)

_android1 = TafUeAndroid(
    serial_number="77164a57",
    capabilities=["REAL_ANDROID_UE", "cell_Mapping: [1]", "Xiaomi_ue"],
    ue_pc_address="10.57.130.32",
    data_transfer=[_data_transfer_iperf],
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.32", username="mn5gran", password="nokia123@"
    ),
    ue_pc_port="9090",
    pdns=[_pdn1],
    imei="868701057847034",
    imsi="262033100013170",
)


# #RealEnb
_real_enb_pdu0 = HBTE(addr="10.57.247.211", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_0 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.149.50", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu0.pdu_ports[6],
)

_real_enb0 = Airscale(common_units=[_common_unit_0])

_lte_real_enb0 = RealEnb(airscale=_real_enb0, instance_id=2618)

# #Real Core
_realcore = RealCore(four_g=None, five_g=None, mcc="262", mnc="3", pdns=None)

# #attenuator
_hbte_params = {
    "ip_addr": "10.57.230.20",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}

_ru1_pdu = FPFH(addr="10.57.247.209", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129",
        username="root",
        password="a2%FgSz3$fHmdusap354xujw7a",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.2",
        username="root",
        password="a2%FgSz3$fHmdusap354xujw7a",
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AENB,
)

_ru2_pdu = FPFH(addr="10.57.247.209", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru2 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129",
        username="root",
        password="a2%FgSz3$fHmdusap354xujw7a",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.2",
        username="root",
        password="a2%FgSz3$fHmdusap354xujw7a",
    ),
    pdu_port=_ru1_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEQY,
)


_lmp_connection = SshServiceDetails(
    addr="10.57.149.50", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")
_capacity_unit_11 = CapacityUnit(addr="192.168.253.21")

_gnb_pdu1 = HBTE(addr="10.57.247.211", port_numbers=[6])

_gnb_pdu2 = HBTE(addr="10.57.247.211", port_numbers=[4])


_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit, _capacity_unit_11],
    pdu_port=_gnb_pdu1.pdu_ports[6],
)

_airscale = Airscale(common_units=[_common_unit_0])


_du = DU(
    airscale=_airscale,
    rus=[_ru1],
    f1_m_ip_addr="10.57.149.50",
    f1_c_ip_addr="10.57.149.50",
    f1_u_ip_addr="10.57.149.50",
)

_lmp_connection1 = SshServiceDetails(
    addr="10.57.149.48", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit1 = CapacityUnit(addr="10.57.149.48")

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection1,
    capacity_units=[_capacity_unit1],
    pdu_port=_gnb_pdu2.pdu_ports[4],
)

_airscale1 = Airscale(common_units=[_common_unit_1])

_du1 = DU(
    airscale=_airscale1,
    rus=[_ru1],
    f1_m_ip_addr="10.57.149.48",
    f1_c_ip_addr="10.57.149.48",
    f1_u_ip_addr="10.57.149.48",
)

# _f1m = NetworkAddress(v6="2a00:8a00:8000:136:10:57:229:40")

# #CU
_cu = CU(
    backhaul_site_oam_ip="10.57.149.50",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.149.50", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.149.50", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.57.149.50",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.57.149.33", ip_prefix_length=27),
    ),
)

_cu1 = CU(
    backhaul_site_oam_ip="10.57.149.48",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.149.48", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.149.48", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.57.149.48",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.57.149.33", ip_prefix_length=27),
    ),
)

_classical_bts0 = ClassicalBts(dus=[_du], cu=_cu, instance_id=2168)

_classical_bts1 = ClassicalBts(dus=[_du1], cu=_cu1, instance_id=2158)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts0, _classical_bts1],
    core=_realcore,
    enbs=[_lte_real_enb0],
    ues=[_android1],
    appserver=_appserver,
    attenuator=[],
    tl_cloud_topology=_tl_cloud_topology,
)
