import os
import yaml
import re
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
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.compatibility.configuration import TestlineWrapper

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

__maintainer__ = "Wang Yixiang"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_01@internal.nsn.com"
__email__ = "yixiang.x.wang@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

ue_config_path = os.path.join(_cfg_dir, "modules/inseego.yml")
if os.path.isfile(ue_config_path):
    with open(ue_config_path) as f:
        ue_config = yaml.load(f, Loader=yaml.FullLoader)
else:
    ue_config = ""

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.48", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_docker_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.186", username="dcapuser", password="appleseller"
    )
)

# #samsung
_appserver_ssh = SshServiceDetails(
    addr="10.57.178.10", username="mmw_sg1", password="mm@1", port="41834"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.10",
    iperf_path="/cygdrive/c/iperf",
    port="41835",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.10",
    iperf_path="iperf",
    port="41834",
)

_appserver = AppServer(iperf_details=_iperf_details_on_appserver)

# CI_Detail_UE_Type='Samsung'
_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.106.223.137", username="tester5g", password="Nokia123!"
    ),
    serial_number="R5CN20DL5HX",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung"],
)
# #samsung

# RealEnb---------------------------------------------------------
_real_enb_pdu = FACOM(addr="10.106.223.139", port_numbers=[3])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.106.223.136", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[3],
)

_real_enb = Airscale(common_units=[_common_unit_2])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None, instance_id=417, global_bts_id=1)

# 5GRU------------------------------------
# add 2 more 5g ru info
# ru_hw_group: Above6GHZ or Below6GHZ
_ru1_pdu = FACOM(addr="10.108.135.43", port_numbers=[6])

_ru1 = RU(
    ru_hw_group="Above6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7",
        username="rfsw",
        password="PD6N1DB0lWmwomtNL2qd3ISypbiocdGRy7U+Lipiksk=",
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru1_pdu.pdu_ports[6],
    radio_type=RadioTypes.AEWD,
)

# #DU
_lmp_connection = SshServiceDetails(
    addr="10.106.223.135", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.**")

_gnb_pdu = FACOM(addr="10.106.223.139", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du0 = DU(airscale=_airscale, rus=[_ru1], f1_m_ip_addr="10.106.223.135")

# CU
_f1m = NetworkAddress(v4="10.57.250.15", v6="xxxx", vlan_id="xxxx")
_f1c = NetworkAddress(v4="10.57.251.36", v6="xxxx", vlan_id="xxxx")
_f1u = NetworkAddress(v4="10.57.251.37", v6="xxxx", vlan_id="xxxx")
_x2c = NetworkAddress(v4="10.57.251.68", v6="xxxx", vlan_id="xxxx")
_x2u = NetworkAddress(v4="10.57.251.69", v6="xxxx", vlan_id="xxxx")
_s1c = NetworkAddress(v4="10.57.251.68", v6="xxxx", vlan_id="xxxx")
_s1u = NetworkAddress(v4="10.57.251.69", v6="xxxx", vlan_id="xxxx")
_tracing = NetworkAddress(v4="xxxx", v6="xxxx", vlan_id="xxxx")
_cu = CU(
    backhaul_site_oam_ip="10.57.250.15",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.250.15", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.250.15", username="Nemuadmin", password="nemuuser"
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

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du0], cu=_cu, instance_id=247, global_bts_id=1)

# cloudbts-----------------------------------------------------
# NCIR
_control = ControlNode(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.137.2", username="nokiauser", password="HZnoki@123!"
    ),
    open_stack_connection_details=OpenStackConnectionDetails(
        username="nokiauser",
        password="NOki@789!",
        ip_addr="10.57.137.2",
        tenant="FiveG",
        port=5000,
        protocol="https",
        version="v3",
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="5.5.5.5", username="admin", password="admin"
    ),
)

_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="ncir_18")

_cbts_flavor = DeploymentFlavorStack(
    name="mmw01_tl417_flavor",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_flavor.env"),
        os.path.join(_cfg_dir, "config_flavor_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="mmw01_tl417",
)

_cbts_net = DeploymentNetworkStack(
    name="mmwsg01_tl417_net",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_ext_net.env"),
        os.path.join(_cfg_dir, "config_ext_net_ci.env"),
    ],
)

_cbts_vnf = DeploymentVnfStack(
    name="mmwsg01_tl417_vnf",
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
    dus=[_du0],
    cu=_cu,
    cloud_deployment=_cloud_deployment,
    vnf_name=_cbts_vnf.name,
    instance_id=417,
    global_bts_id=1,
)

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    enbs=[_lte_real_enb],
    gnbs=[_cbts],
    ues=[_android_0],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_docker_pc],
    appserver=_appserver,
)

# tl = TestlineWrapper(tl)

# Example for topyoung attenuator part
# print tl.gnbs[0].global_bts_id
# print tl.gnbs[0].dus[0].rus[0].attenuation_ports[0].port_no
# print tl.gnbs[0].dus[0].rus[0].attenuation_ports[1].port_no
# print tl.gnbs[0].dus[0].rus[0].attenuation_ports[2].port_no
# print tl.gnbs[0].dus[0].rus[0].attenuation_ports[3].port_no
# print tl.gnbs[0].dus[0].rus[0].attenuation_ports[2].port_no
# print tl.gnbs[0].dus[0].rus[0].attenuation_ports[3].port_no
