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
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)  # added in taf.meta.5.4
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import HBTE, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.testline import TestLine
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch

# added in taf.meta 5.4
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
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
from taf.config.testline.appserver import AppServer

from taf.config.testline import LicenseKeeper

__maintainer__ = "Wang Debbie"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04@internal.nsn.com"
__email__ = "debbie.wang@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.203", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.178.18", username="mmw_sg4", password="mm@4", port="44171"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.18",
    iperf_path="/usr/bin/iperf",
    port="44171",
    ports=[44171, 44172],
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.18",
    iperf_path="iperf",
    port="44171",
)
_appserver = AppServer(_iperf_details_on_appserver)

# #5GRU_1 for cloudBTS
_ru1 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    radio_type="AEUD",
)

# RealEnb
_real_enb_pdu = HBTE(addr="10.108.135.112", port_numbers=[4])

_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.216.136", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[4],
)

_real_enb = Airscale(common_units=[_common_unit_1])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# #DU_0 for cloudlBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.71.216.134", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.20")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[
        _capacity_unit_0,
    ],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[
        _ru1,
    ],
    f1_m_ip_addr="10.71.216.134",
)

_licensekeeper = LicenseKeeper(username="HAZ3_SG4", password="HAZ3_SG4")

_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.141", username="nokia5G", password="noki@123"
    ),
    # serial_number='UQG5T20804006374',
    serial_number="5eb4b6cb",
    server_dir="C:/Program Files (x86)/Spark1.1.2001.110/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    # qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    # diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "askey_sigspark"],
    imsi="262033032996900",
    licensekeeper=_licensekeeper,
)

# #CU
_f1c = NetworkAddress(
    v4="10.57.251.38",
    vlan_id=None,
    routing=RoutingInformation(gateway="10.57.251.33", ip_prefix_length=27),
)
_f1u = NetworkAddress(
    v4="10.57.251.39",
    vlan_id=None,
    routing=RoutingInformation(gateway="10.57.251.33", ip_prefix_length=27),
)
_x2c = NetworkAddress(
    v4="10.57.251.70",
    vlan_id=None,
    routing=RoutingInformation(gateway="10.57.251.65", ip_prefix_length=27),
)
_x2u = NetworkAddress(
    v4="10.57.251.71",
    vlan_id=None,
    routing=RoutingInformation(gateway="10.57.251.65", ip_prefix_length=27),
)
_s1u = NetworkAddress(
    v4="10.57.251.71",
    vlan_id=None,
    routing=RoutingInformation(gateway="10.57.251.65", ip_prefix_length=27),
)
_tracing = NetworkAddress(
    v4="10.57.250.x",
    vlan_id=None,
    routing=RoutingInformation(gateway="10.57.250.129", ip_prefix_length=25),
)

_cu = CU(
    backhaul_site_oam_ip="10.71.216.134",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.216.134", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.216.134", username="Nemuadmin", password="nemuuser"
    ),
)

# #cloudbts
_control = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.57.137.2",
        username="nokiauser",
        tenant="FiveG",
        password="NOki@456!",
        port=5000,
        protocol="https",
        version="v3",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.137.2", username="nokiauser", password="HZnoki@123!"
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="5.5.5.5", username="admin", password="admin"
    ),
)

_ncir = NCIR(
    compute_nodes=[],
    control_nodes=[_control],
    version="ncir_19",
    cloud_deployments=None,
)

_cbts_flavor = DeploymentFlavorStack(
    name="mmw_tl716_cbtsflavor",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_flavor.env"),
        os.path.join(_cfg_dir, "config_flavor_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="cbts_prefix",
)

_cbts_net = DeploymentNetworkStack(
    name="mmw_tl716_ext_net",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_ext_net.env"),
        os.path.join(_cfg_dir, "config_ext_net_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="mmw_tl716_cbts_deploy",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_heat.env"),
        os.path.join(_cfg_dir, "config_bts_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_heat.yaml"),
)

_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)

_cbts = CloudBts(
    cu=_cu,
    dus=[_du],
    instance_id="716",
    global_bts_id="716",
    cloud_deployment=_cloud_deployment,
)

# #cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    ues=[_android],
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
)
