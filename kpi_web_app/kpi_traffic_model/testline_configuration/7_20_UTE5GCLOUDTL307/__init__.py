__maintainer__ = "Aroul Selvaradjou"
__team__ = "5G_PZ_MMW_KRK_4_SG"
__email__ = "aroul.selvaradjou@nokia.com"

import os
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
from taf.config.testline import DU, RU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline import RealEnb
from taf.config.testline.pdu import ATEN

_gnb_instance_id = 307
_gnb_global_bts_id = 1
_gnb_du_common_unit_hardwarde_type = "ASIK"
_gnb_ru_hw_group = "AEWD"


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ["INIT_CONFIG_FILE_PATH"] = os.path.dirname(os.path.abspath(__file__))
os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "ue_config.yaml"
)

_ute_vm = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.28.0.87", username="ute", password="ute"
    )
)

_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.14.62.120", username="admin", tenant="admin", password="uteadmin"
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.14.62.120", username="wrsroot", password="uteadmin"
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="10.14.62.111", username="admin", password="admin"
    ),
)

_compute = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(
        addr="10.14.62.113", username="admin", password="admin"
    )
)

_ncir = NCIR(compute_nodes=[_compute], control_nodes=[_control_0], version="ncir_19")

_cbts_flavor = DeploymentFlavorStack(
    name="TL_7_20_UTE5GCLOUDTL307_FLAVOR",
    env_files=[os.path.join(_CFG_DIR, "5gbts_flavor.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_flavor.yaml"),
    default_vnf_prefix="5gbts-307",
)

_cbts_net = DeploymentNetworkStack(
    name="TL_7_20_UTE5GCLOUDTL307_EXT_NET",
    env_files=[os.path.join(_CFG_DIR, "5gbts_ext_net.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="TL_7_20_UTE5GCLOUDTL307_BTS",
    env_files=[os.path.join(_CFG_DIR, "5gbts_heat.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_heat.yaml"),
)

_cloud_deployment = CloudDeployment(
    default_cfg_dir=_CFG_DIR,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.14.49.77",
        vlan_id=1000,
        routing_v4=RoutingInformation(gateway="10.14.49.254", ip_prefix_length=23),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.49.77", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.49.77", username="Nemuadmin", password="nemuuser"
    ),
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
    x2c=NetworkAddress(v4="10.28.11.121", vlan_id=4002),
    x2u=NetworkAddress(v4="10.28.11.122", vlan_id=4002),
    s1u=NetworkAddress(v4="10.28.11.122", vlan_id=4002),
)

_abil1_du1 = CapacityUnit(addr="192.168.253.20")

_asik_du1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil1_du1],
)

_ru_pdu = ATEN(addr="", port_numbers=[4])

_ru_du1 = RU(
    ru_hw_group="",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    radio_type=_gnb_ru_hw_group,
    pdu_port=_ru_pdu.pdu_ports[4],
)

# gnb_oam_ip = NetworkAddress(v4="10.14.49.77")

_du1 = DU(
    Airscale(common_units=[_asik_du1]),
    instance_id=191,
    global_bts_id=307,
    rus=[_ru_du1],
    # oam_ip=None,
    # f1_m_ip_addr=None,
    f1_c_ip_addr="192.168.2.105",
    f1_u_ip_addr="192.168.2.106",
)

_cbts = CloudBts(
    cu=_cu, cloud_deployment=_cloud_deployment, vnf_name="5gbts-307", dus=[_du1]
)

_enb = RealEnb(
    oam_ip=NetworkAddress(v4="10.14.49.82"),
    instance_id=100023,
    global_bts_id=22144,
    x2_link_addr=NetworkAddress(v4="10.28.11.153"),
)

tl = TestLine(
    test_pc=_ute_vm,
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    tl_cloud_topology="CLOUD_5G_ASIKL_ABILB1_AEWD",
    enbs=[_enb],
)


__all__ = ["tl"]
