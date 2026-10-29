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

# from taf.config.testline.pdu import HBTE, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.attenuator import (
    AttenuationPort,
    HBTE,
)  # added in taf.meta 5.4
from taf.config.testline.testline import TestLine
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

__maintainer__ = "Chen Kaijia"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04@internal.nsn.com"
)
__email__ = "kaijia.chen@nokia-sbell.com"


# common


_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.239", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


# RealEnb
_real_enb_pdu = HBTE(
    ip_addr="10.57.251.250", port="5000", attenuation_port_numbers=[1, 2, 3, 4]
)

_common_unit_pdu_1 = FACOM(addr="10.57.242.11", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_capacity_unit_0 = CapacityUnit(addr="192.168.253.22")


_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.48.77", username="Nemuadmin", password="nemuuser"
    ),
    capacity_units=[],
    pdu_port=_common_unit_pdu_1.pdu_ports[1],
)

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.48.78", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_common_unit_pdu_1.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)


# #5GRU_0 for cloudBTS
_ru_pdu = FACOM(addr="10.57.243.10", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[8],
    radio_type="AEWD",
)

# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.101.48.77", username="Nemuadmin", password="nemuuser", port="44151"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.3",
    iperf_path="/cygdrive/c/Tools/iPerfGui+",
    port="44151",
    ports=[44151, 44152, 44153, 44154, 44155, 44156, 44157, 44158, 44159, 44160],
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.18",
    iperf_path="iperf",
    port="41049",
)

_appserver = AppServer(_iperf_details_on_appserver)
# Qualcomm
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.217", username="nokia5G", password="noki@123"
    ),
    serial_number="R5CN20WSLYZ",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung"],
)

# #DU_0 for cloudlBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.108.174.10", username="toor4nsn", password="oZPS0POrRieRtu"
)

_du_pdu = FACOM(addr="10.57.241.158", port_numbers=[2])


_airscale = Airscale(common_units=[_common_unit_1])

_du = DU(
    airscale=_airscale,
    rus=[_ru],
    f1_c_ip_addr="2a00:8a00:8000:136:10:57:250:4048",
    f1_m_cu="2a00:8a00:8000:136:10:101:48:4d",
    f1_u_ip_addr="2a00:8a00:8001:136:10:57:250:4048",
    f1_m_ip_addr="10.101.48.77",
)


# #CU
_f1m = NetworkAddress(v4="10.101.48.77", v6="xxxx", vlan_id=2546)
_f1c = NetworkAddress(
    v4="10.57.250.48", v6="2a00:8a00:8000:136:10:57:250:4048", vlan_id=2546
)
_f1u = NetworkAddress(
    v4="10.57.250.49", v6="2a00:8a00:8000:136:10:57:250:4049", vlan_id=2546
)
_x2c = NetworkAddress(
    v4="10.57.250.82", v6="2a00:8a00:8000:136:10:57:250:8082", vlan_id=2546
)
_x2u = NetworkAddress(
    v4="10.57.250.83", v6="2a00:8a00:8000:136:10:57:250:8083", vlan_id=2546
)
_s1c = NetworkAddress(v4="xxxx", v6="xxxx", vlan_id=2546)
_s1u = NetworkAddress(
    v4="10.57.250.83", v6="2a00:8a00:8000:136:10:57:250:8083", vlan_id=2546
)
_tracing = NetworkAddress(v4="10.57.179.x", v6="xxxx", vlan_id=2546)

_cu = CU(
    backhaul_site_oam_ip="10.57.250.14",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.250.14", username="robot", password="rastre1", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.250.14", username="Nemuadmin", password="nemuuser"
    ),
    f1m=_f1m,
    f1c=_f1c,
    f1u=_f1u,
    x2c=_x2c,
    x2u=_x2u,
    s1c=_s1c,
    s1u=_s1u,
    tracing=_tracing,
)

# cloud
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
    version="ncir_18",
    cloud_deployments=None,
)

# #cloudbts
_cbts_flavor = DeploymentFlavorStack(
    name="mmw-tl714_cbtsflavor",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_flavor.env"),
        os.path.join(_cfg_dir, "config_flavor_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="cbts_prefix",
)

_cbts_net = DeploymentNetworkStack(
    name="mmw-tl714_ext_net",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_ext_net.env"),
        os.path.join(_cfg_dir, "config_ext_net_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="mmw-tl714_cbts_deploy",
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
    dus=[_du],
    cu=_cu,
    cloud_deployment=_cloud_deployment,
    instance_id="7",
    global_bts_id="714",
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"


tl = TestLine(
    test_pc=_host,
    ues=[_android],
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
    attenuator=_real_enb_pdu,
)

__all__ = ["tl"]
