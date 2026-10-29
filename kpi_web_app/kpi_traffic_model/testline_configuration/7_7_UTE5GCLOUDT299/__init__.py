__maintainer__ = "Jakub Hejduk"
__team__ = "5G_PZ_MMW_KRK_6_SG"
__email__ = "jakub.hejduk@nokia.com"

import os, yaml
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    OpenStackConnectionDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
)
from taf.config.testline.cloud_hosting import (
    NCIR,
    ControlNode,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    ComputeNode,
)
from taf.config.testline.gnb import CloudBts, CU
from taf.config.testline import DU, RU, RoutingInformation
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import NetworkAddress, RealEnb
from taf.config.testline.core import RealCore5G
from taf.config.testline.cbam import Cbam
from taf.config.testline.pdu import FPFH, PduPort

_5g_bts_id = 75299
_4g_bts_id = 75079

_ncir_vnf = "5gbts" + str(_5g_bts_id)

_ncir_ip = "10.83.190.225"
_ncir_user = "5Guser1"
_ncir_pass = "5Guser@9"
_ncir_tenant = "5Gtenant1"

_4g_ip = NetworkAddress(v4="10.83.251.7")

_gnb_oam_ip = NetworkAddress(
    v4="10.83.251.7/27",
    routing_v4=RoutingInformation(gateway="10.83.250.254", destIpAddr="10.83.250.160"),
    vlan_id=539,
) 
_cu_oam_ip = NetworkAddress(
    v4="10.83.250.2/27",
    routing_v4=RoutingInformation(gateway="10.83.250.30"),
)

_cu_x2c_route_du = NetworkAddress(
    v4="10.83.250.34/27",
    routing_v4=RoutingInformation(gateway="10.83.250.62", destIpAddr="10.83.182.0/23"),
)
_cu_x2u_route_du = NetworkAddress(
    v4="10.83.250.66/27",
    routing_v4=RoutingInformation(gateway="10.83.250.94", destIpAddr="10.83.182.0/23"),
)
_cu_s1u_route_du = NetworkAddress(
    v4="10.83.250.98/27",
    routing_v4=RoutingInformation(gateway="10.83.250.126"),
)
_cu_f1c_route_du = NetworkAddress(
    v4="10.83.250.130/27",
    routing_v4=RoutingInformation(gateway="10.83.250.158", destIpAddr="10.83.128.0/17"),
)
_cu_f1u_route_du = NetworkAddress(
    v4="10.83.250.162/27",
    routing_v4=RoutingInformation(
        gateway="10.83.250.190", destIpAddr="10.83.250.224/27"
    ),
)

_du_m_ip = NetworkAddress(
    v4="10.83.251.7/27",
    vlan_id=539,
    routing_v4=RoutingInformation(gateway="10.83.251.30"),
)
_du_f1c_ip = NetworkAddress(
    v4="10.83.250.199/27",
    vlan_id=537,
    routing_v4=RoutingInformation(
        gateway="10.83.250.222", destIpAddr="10.83.250.128/27"
    ),
)
_du_f1u_ip = NetworkAddress(
    v4="10.83.250.231/27",
    vlan_id=538,
    routing_v4=RoutingInformation(
        gateway="10.83.250.254", destIpAddr="10.83.250.160/27"
    ),
)

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT299-integration.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr=_ncir_ip,
        username=_ncir_user,
        tenant=_ncir_tenant,
        password=_ncir_pass,
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr=_ncir_ip,
        username=_ncir_user,
        password=_ncir_pass,
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_compute = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password="")
)

_ncir = NCIR(compute_nodes=[_compute], control_nodes=[_control_0], version="ncir_19")

_cbts_flavor = DeploymentFlavorStack(
    name="TL_7_7_UTE5GCLOUDT299_FLAVOR",
    env_files=[os.path.join(_CFG_DIR, "config_flavor.env")],
    default_vnf_prefix=_ncir_vnf,
)

_cbts_net = DeploymentNetworkStack(
    name="TL_7_7_UTE5GCLOUDT299_EXT_NET",
    env_files=[os.path.join(_CFG_DIR, "config_ext_net.env")],
)

_cbts_vnf = DeploymentVnfStack(
    name="TL_7_7_UTE5GCLOUDT299_BTS",
    env_files=[os.path.join(_CFG_DIR, "config_bts.env")],
)

_cloud_deployment = CloudDeployment(
    default_cfg_dir=_CFG_DIR,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)

_cu = CU(
    backhaul_site_oam_ip=_cu_oam_ip,
    oam_ssh_connection_details=SshServiceDetails(
        addr=_cu_oam_ip.v4.split("/")[0], username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr=_cu_oam_ip.v4.split("/")[0], username="Nemuadmin", password="nemuuser"
    ),
    instance_id=_5g_bts_id,
    global_bts_id=_5g_bts_id,
    f1m=_cu_oam_ip,
    f1c=_cu_f1c_route_du,
    f1u=_cu_f1u_route_du,
    x2c=_cu_x2c_route_du,
    x2u=_cu_x2u_route_du,
    s1u=_cu_s1u_route_du,
)

_pdu1 = FPFH(
    addr="fpfh-ga13-48-sc5g.sc5g-leg.krk-lab.nsn-rdnet.net",
    port_numbers=["2"],
    login="admin",
    password="admin",
)
_pdus = [_pdu1]
_pdu_port = PduPort(pdu=_pdu1, port_no=2)

_default_gnb_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc.default_ssh_connection_details,
)

_default_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_oam_ip.v4,
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)


gnb_radio_unit_0 = RU(
     ru_hw_group="AEUB",
     default_ssh_connection_details=SshServiceDetails(
        addr="172.22.58.162",
        username="root",
        password="umniedziala"),
     radio_type="AEUB",
     serial_number="AH200200144",
     product_code="474608A.102",
)

gnb_radio_unit_1 = RU(
     ru_hw_group="AEUB",
     default_ssh_connection_details=SshServiceDetails(
        addr="172.22.56.162",
        username="root",
        password="umniedziala"),
     radio_type="AEUB",
     serial_number="AH200200147",
     product_code="474608A.102",
)

gnb_radio_unit_2 = RU(
     ru_hw_group="AEUB",
     default_ssh_connection_details=SshServiceDetails(
        addr="172.22.57.162",
        username="root",
        password="umniedziala"),
     radio_type="AEUB",
     serial_number="AH200200157",
     product_code="474608A.102",
)
gnb_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.46",
    hardware_type="ABIL",
    hardware_version="B.102",
    serial_number="L1203902624",
    product_code="474020B.102",
    # slot_id=SlotId.B6
    )

gnb_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.38",
    hardware_type="ABIL",
    hardware_version="B.102",
    serial_number="L1203902596",
    product_code="474020B.102",
    # slot_id=SlotId.B4
    )

gnb_capacity_unit_2 = CapacityUnit(
    addr="192.168.253.42",
    hardware_type="ABIL",
    hardware_version="B.102",
    serial_number="L1203902625",
    product_code="474020B.102",
    # slot_id=SlotId.B5
    )

_asik_du1 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[gnb_capacity_unit_0, gnb_capacity_unit_1, gnb_capacity_unit_2],
    hardware_type="ASIK",
    hardware_version="A.101",
    serial_number="L1182604954",
    mac_addr="",
    # trs_connections=[],
    # slot_id=SlotId.C2,
)
_du1 = DU(
    Airscale(common_units=[_asik_du1]),
    instance_id=_5g_bts_id,
    global_bts_id=_5g_bts_id,
    rus=[gnb_radio_unit_0, gnb_radio_unit_1, gnb_radio_unit_2],
    f1_m_ip_addr=_du_m_ip,
    f1_c_ip_addr=_du_f1c_ip,
    f1_u_ip_addr=_du_f1u_ip,
)

_cbts = CloudBts(
    cu=_cu,
    cloud_deployment=_cloud_deployment,
    vnf_name=_ncir_vnf,
    dus=[_du1],
)

_enb = RealEnb(
    oam_ip=_4g_ip,
    instance_id=_4g_bts_id,
    global_bts_id=_4g_bts_id,
    x2_link_addr=_4g_ip,
)

_core = RealCore5G(mcc=244, mnc=8)

_cbam = Cbam(
    addr="10.89.0.73",
    client_id="cbam_client",
    client_secret="49c9d0d1-e7b5-45b1-b29e-6e4d71c45666",
)


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)

    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config

_ue_config = _set_abstract_lib_config_env("ue.yaml")

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    tl_cloud_topology="CLOUD_5G_ASIKR_ABILB4B5B6_3xAEUB_ENB",
    enbs=[_enb],
    core=_core,
    cbam=_cbam,
    pdus=_pdus,
)

__all__ = ["tl"]
