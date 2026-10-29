import os
import yaml
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
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.appserver import AppServer
from taf.config.testline.gnb.du import FHGW
from taf.config.testline.gnb.du import VDU
from taf.config.testline.core import RealCore, PCF

__maintainer__ = "Wang Yixiang"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_01@internal.nsn.com"
__email__ = "yixiang.x.wang@nokia-sbell.com"

# common
__all__ = ["tl"]


_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# inseego
# ue_config_path = os.path.join(_cfg_dir, 'TestData/inseego.yml')
# if os.path.isfile(ue_config_path):
#     with open(ue_config_path) as f:
#         ue_config = yaml.load(f)
# else:
#     ue_config = ''
# inseego

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.47", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# AppServer
_appserver_ssh = SshServiceDetails(
    addr="10.57.178.10", username="mmw_sg1", password="mm@1", port="41814"
)
# UL ports
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.10",
    iperf_path="iperf",
    port="41824",
    ports=[
        "41824",
        "46824",
        "47824",
        "49824",
        "45824",
        "40824",
        "51824",
        "56824",
        "57824",
        "59824",
        "55824",
        "50824",
    ],
)

_appserver = AppServer(_iperf_details_on_appserver)

# #UE1
# DL ports
_iperf_android_0 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.10",
    iperf_path="/cygdrive/c/iperf",
    port="41825",
    ports=["46825", "47825", "49825", "45825", "40825"],
)

# CI_Detail_UE_Type='Samsung;Samsung'
_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.56.18.135", username="tester", password="tester123"
    ),
    serial_number="R5CN20T2MFX",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_android_0,
    capabilities=["REAL_ANDROID_UE", "samsung"],
)
# #UE1

# #UE2
# DL ports
_iperf_android_1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.10",
    iperf_path="/cygdrive/c/iperf",
    port="51825",
    ports=["56825", "57825", "59825", "55825", "50825"],
)

_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.56.18.135", username="tester", password="tester123"
    ),
    serial_number="R5CN20YHK2T",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_android_1,
    capabilities=["REAL_ANDROID_UE", "samsung"],
)
# #UE2

# RealEnb---------------------------------------------------------
_real_enb_pdu = FACOM(addr="10.56.18.177", port_numbers=[3])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.56.18.133", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[3],
)

_real_enb = Airscale(common_units=[_common_unit_2])
_lte_real_enb = RealEnb(
    airscale=_real_enb, rms=None, instance_id=412, global_bts_id=412
)

# 5GRU------------------------------------
# add 2 more 5g ru info
# ru_hw_group: Above6GHZ or Below6GHZ
_ru1_pdu = FACOM(addr="10.56.18.175", port_numbers=[1])

_ru1 = RU(
    ru_hw_group="Above6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7",
        username="rfsw",
        password="PD6N1DB0lWmwomtNL2qd3ISypbiocdGRy7U+Lipiksk=",
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru1_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEUD,
)

# #DU
_lmp_connection = SshServiceDetails(
    addr="10.56.18.134", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.56.18.177", port_numbers=[3])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)

_airscale = Airscale(common_units=[_common_unit_0])

_vdu_oam_http_connection_details = HttpConnectionDetails(
    addr="10.56.18.134", username="Nemuadmin", password="nemuuser"
)
_fhgw_1 = FHGW(
    user_config_path=os.path.join(_cfg_dir, "user_config.yaml"),
    rus=[_ru1],
    pxe_server=None,
)

_vdu_0 = VDU(
    cloud_deployment=None,
    oam_http_connection_details=_vdu_oam_http_connection_details,
    fhgws=[_fhgw_1],
    f1_m_ip_addr=NetworkAddress(v4="10.56.18.134"),
    f1_c_ip_addr=NetworkAddress(v4="10.57.159.86"),
    f1_u_ip_addr=NetworkAddress(v4="10.57.159.87"),
)

_du0 = DU(airscale=_airscale, rus=[_ru1], f1_m_ip_addr="10.56.18.134")

# CU
_f1m = NetworkAddress(v4="10.57.159.12", v6="xxxx", vlan_id="xxxx")
_f1c = NetworkAddress(v4="10.57.159.86", v6="xxxx", vlan_id="xxxx")
_f1u = NetworkAddress(v4="10.57.159.87", v6="xxxx", vlan_id="xxxx")
_x2c = NetworkAddress(v4="10.57.159.162", v6="xxxx", vlan_id="xxxx")
_x2u = NetworkAddress(v4="10.57.159.163", v6="xxxx", vlan_id="xxxx")
_s1c = NetworkAddress(v4="10.57.159.162", v6="xxxx", vlan_id="xxxx")
_s1u = NetworkAddress(v4="10.57.159.163", v6="xxxx", vlan_id="xxxx")
_tracing = NetworkAddress(v4="xxxx", v6="xxxx", vlan_id="xxxx")

_cu = CU(
    backhaul_site_oam_ip="10.57.159.12",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.12", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.159.12", username="Nemuadmin", password="nemuuser"
    ),
    f1m=_f1m,
    f1c=_f1c,
    f1u=_f1u,
    x2c=_x2c,
    x2u=_x2u,
    s1c=_s1c,
    s1u=_s1u,
    tracing=_tracing,
    instance_id=412,
    global_bts_id=1,
)

# cloudbts-----------------------------------------------------
# NCIR
_control = ControlNode(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.137.34", username="nokiauser", password="HZnoki@123!"
    ),
    open_stack_connection_details=OpenStackConnectionDetails(
        username="nokiauser",
        password="NOki@890!",
        ip_addr="10.57.137.34",
        tenant="FiveG",
        port=5000,
        protocol="https",
        version="v3",
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="5.5.5.5", username="admin", password="admin"
    ),
)

_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="ncir_19")

_cbts_flavor = DeploymentFlavorStack(
    name="mmw_sg01_tl412_flavor",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_flavor.env"),
        os.path.join(_cfg_dir, "config_flavor_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="mmwsg01_tl412",
)

_cbts_net = DeploymentNetworkStack(
    name="mmwsg01_tl412_net",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_ext_net.env"),
        os.path.join(_cfg_dir, "config_ext_net_ci.env"),
    ],
)

_cbts_vnf = DeploymentVnfStack(
    name="mmwsg01_tl412_vnf",
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
    vnf_name="mmwsg01_tl412_vnf",
    instance_id=412,
    global_bts_id=1,
)

# RealCore
_pcf = PCF(
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.56.18.135", username="tester", password="tester123"
    )
)
_realcore = RealCore(pcf=_pcf)

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    enbs=[_lte_real_enb],
    gnbs=[_cbts],
    ues=[_android_0, _android_1],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_host],
    appserver=_appserver,
    core=_realcore,
)

# tl = TestlineWrapper(tl)

# SCF related configuration. Keep this part in this file temporary, will
PARAMS_TO_MODIFY_SCF = [
    dict(
        value="TL412_5gDU",
        dist_name="MRBTS-" + str(tl.gnbs[0].instance_id),
        p_name="btsName",
    )
]
# Example for topyoung attenuator part
# print tl.gnbs[0].global_bts_id
# print tl.gnbs[0].dus[0].rus[0].attenuation_ports[0].port_no
# print tl.gnbs[0].dus[0].rus[0].attenuation_ports[1].port_no
# print tl.gnbs[0].dus[0].rus[0].attenuation_ports[2].port_no
# print tl.gnbs[0].dus[0].rus[0].attenuation_ports[3].port_no
# print tl.core.pcf.oam_ssh_connection_details
