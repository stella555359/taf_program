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
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.gnb.du import FHGW
from taf.config.testline.gnb.du import VDU
from taf.config.testline.core import RealCore, PCF

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

__maintainer__ = "wang yixiang"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_01@internal.nsn.com"
__email__ = "yixiang.x.wang@nokia-sbell.com"

# common
__all__ = ["tl"]


# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.137", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_docker_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.47", username="dcapuser", password="dcapuser123"
    )
)
_tce_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.47", username="dcapuser", port=49151
    )
)

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# AppServer
_appserver_ssh = SshServiceDetails(
    addr="10.57.178.10", username="mmw_sg1", password="mm@1", port="22"
)

# UL ports
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.10",
    iperf_path="iperf",
    port="41800",
    ports=[
        "41800",
        "46800",
        "47800",
        "49800",
        "45800",
        "40800",
        "51800",
        "56800",
        "57800",
        "59800",
        "55800",
        "50800",
    ],
)

_appserver = AppServer(_iperf_details_on_appserver)

# #UE1
# DL port
_iperf_android_0 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.10",
    iperf_path="/cygdrive/c/iperf",
    port="41801",
    ports=["46801", "47801", "49801", "45801", "40801"],
)

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.109", username="nokia5G", password="noki@123"
    ),
    serial_number="R5CN207PH4Z",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_android_0,
    capabilities=["REAL_ANDROID_UE", "samsung"],
)

# #UE2
# DL ports
_iperf_android_1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.10",
    iperf_path="/cygdrive/c/iperf",
    port="51801",
    ports=["56801", "57801", "59801", "55801", "50801"],
)

_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.109", username="nokia5G", password="noki@123"
    ),
    serial_number="R5CN20XMPXX",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_android_1,
    capabilities=["REAL_ANDROID_UE", "samsung"],
)

# RealEnb---------------------------------------------------------
_real_enb_pdu = FACOM(addr="10.68.90.91", port_numbers=[6])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.68.90.83", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[6],
)

_real_enb = Airscale(common_units=[_common_unit_2])
_lte_real_enb = RealEnb(
    airscale=_real_enb, rms=None, instance_id=400, global_bts_id=400
)

# 5GRU------------------------------------
# _attenuator = TopYoung(
# ip_addr='10.57.249.38',
# port=23,
# attenuation_port_numbers=[5, 6, 7, 8])
# add 2 more 5g ru info
_ru1_pdu = FACOM(addr="10.68.90.94", port_numbers=[1])

# Above6GHZ or Below6GHZ
_ru1 = RU(
    ru_hw_group="Above6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru1_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEUB,
    serial_number="L1195100993",
)

# #DU
_lmp_connection = SshServiceDetails(
    addr="10.68.90.79", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.68.90.91", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du0 = DU(airscale=_airscale, rus=[_ru1], f1_m_ip_addr="10.68.90.79")

_vdu_oam_http_connection_details = HttpConnectionDetails(
    addr="10.68.90.79", username="Nemuadmin", password="nemuuser"
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
    f1_m_ip_addr=NetworkAddress(v4="10.68.90.79"),
    f1_c_ip_addr=NetworkAddress(v4="10.68.90.79"),
    f1_u_ip_addr=NetworkAddress(v4="10.68.90.79"),
)

_du0 = DU(airscale=_airscale, rus=[_ru1], f1_m_ip_addr="10.68.90.79")

# CU
_f1m = NetworkAddress(v4="0.0.0.0", v6="xxxx", vlan_id="xxxx")
_f1c = NetworkAddress(v4="10.57.177.72", v6="xxxx", vlan_id="xxxx")
_f1u = NetworkAddress(v4="10.57.177.73", v6="xxxx", vlan_id="xxxx")
_x2c = NetworkAddress(v4="10.57.177.136", v6="xxxx", vlan_id="xxxx")
_x2u = NetworkAddress(v4="10.57.177.137", v6="xxxx", vlan_id="xxxx")
_s1c = NetworkAddress(v4="10.57.177.136", v6="xxxx", vlan_id="xxxx")
_s1u = NetworkAddress(v4="10.57.177.137", v6="xxxx", vlan_id="xxxx")
_tracing = NetworkAddress(v4="xxxx", v6="xxxx", vlan_id="xxxx")

_cu = CU(
    backhaul_site_oam_ip="10.57.177.6",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.6", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.177.6", username="Nemuadmin", password="nemuuser"
    ),
    f1m=_f1m,
    f1c=_f1c,
    f1u=_f1u,
    x2c=_x2c,
    x2u=_x2u,
    s1c=_s1c,
    s1u=_s1u,
    tracing=_tracing,
    instance_id=400,
    global_bts_id=400,
)

# classicalbts------------------------------------------------
# _classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=45, global_bts_id=45)

# cloudbts-----------------------------------------------------
# NCIR
_control = ControlNode(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.138.244", username="nokiauser", password="HZnoki@123!"
    ),
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.57.138.244",
        username="nokiauser",
        tenant="FiveG",
        password="NOki@678!",
        port=5000,
        protocol="https",
        version="v3",
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
    name="mmw-sg01-tl400-flavor",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_flavor.env"),
        os.path.join(_cfg_dir, "config_flavor_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="mmw-sg01-tl400",
)

_cbts_net = DeploymentNetworkStack(
    name="mmw-sg01-tl400-intnet",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_ext_net.env"),
        os.path.join(_cfg_dir, "config_ext_net_ci.env"),
    ],
)

_cbts_vnf = DeploymentVnfStack(
    name="mmw-sg01-tl400-vnfc",
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
    vnf_name="mmw-sg01-tl400-vnfc",
    instance_id=400,
    global_bts_id=400,
)

# RealCore
_pcf = PCF(
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.47.109", username="nokia5G", password="noki@123"
    )
)
_realcore = RealCore(pcf=_pcf)

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    test_pcs=[_docker_pc, _tce_pc],
    enbs=[_lte_real_enb],
    gnbs=[_cbts],
    ues=[_android_0, _android_1],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
    core=_realcore,
)

# tl = TestlineWrapper(tl)


# Example for topyoung attenuator part
# print tl.gnbs[0].global_bts_id
# print tl.gnbs[0].dus[0].rus[0].attenuation_ports[0].port_no
# print tl.gnbs[0].dus[0].rus[0].attenuation_ports[1].port_no
# print tl.gnbs[0].dus[0].rus[0].attenuation_ports[2].port_no
# print tl.gnbs[0].dus[0].rus[0].attenuation_ports[3].port_no
