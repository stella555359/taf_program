__maintainer__ = "Lukasz Rzodeczko"
__team__ = "5G_PZ_MMW_KRK_3_SG"
__email__ = "lukasz.rzodeczko@nokia.com"

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
from taf.config.testline import NetworkAddress, RealEnb
from taf.config.testline.nom import NOM
from taf.config.testline.nms import Netact
from taf.config.testline.pdu import FPFH

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT174.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.83.190.225",
        username="5Guser1",
        tenant="5Gtenant1",
        password="5Guser@10",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.83.190.225", username="5Guser1", password="5Guser@10"
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_compute = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password="")
)

_ncir = NCIR(compute_nodes=[_compute], control_nodes=[_control_0], version="ncir_19")

_cbts_flavor = DeploymentFlavorStack(
    name="TL_7_7_UTE5GCLOUDT174_FLAVOR",
    env_files=[os.path.join(_CFG_DIR, "config_flavor.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_flavor.yaml"),
    default_vnf_prefix="5gbts-174",
)

_cbts_net = DeploymentNetworkStack(
    name="TL_7_7_UTE5GCLOUDT174_EXT_NET",
    env_files=[os.path.join(_CFG_DIR, "config_ext_net.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="TL_7_7_UTE5GCLOUDT174_BTS",
    env_files=[os.path.join(_CFG_DIR, "config_bts.env")],
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
    backhaul_site_oam_ip="192.168.255.129",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.83.182.174", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.83.182.174", username="Nemuadmin", password="nemuuser"
    ),
)

_pdu1 = FPFH(
    port_numbers=[4],
    addr="10.253.166.99",
    login="admin",
    password="admin",
)

_abil1_du1 = CapacityUnit(addr="192.168.253.20")

_asod_du1 = CommonUnit(
    pdu_port=_pdu1.pdu_ports[4],
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil1_du1],
)

_ru_du1 = RU(
    ru_hw_group="",
    default_ssh_connection_details=SshServiceDetails(addr="", username=""),
    lmp_connection=SshServiceDetails(addr="", username=""),
    radio_type="AEUD",
)

_du_m_ip = NetworkAddress(
    v4="10.83.251.8",
    v6="2a00:8a02:60:3e:ffff:ffff:ffff:174",
)


_du1 = DU(Airscale(common_units=[_asod_du1]), rus=[_ru_du1], f1_m_ip_addr=_du_m_ip)

_cbts = CloudBts(
    cu=_cu,
    cloud_deployment=_cloud_deployment,
    vnf_name="5gbts-174",
    dus=[_du1],
    instance_id=174,
    global_bts_id=174,
)
# 4G radio units

_radio_units_enb = [RU(ru_hw_group="LTE_RADIO", radio_type="AHCA")]

# 4G anchor BTS

_capacity_units_enb = [CapacityUnit(addr="192.168.253.20", hardware_type="ABIA")]

_common_unit_enb = CommonUnit(
    hardware_type="ASIA",
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
        proxy=SshServiceDetails(
            addr="sc5g-enb-008.sc5g.krk-lab.nsn-rdnet.net",
            username="ute",
            password="ute",
        ),
    ),
    capacity_units=_capacity_units_enb,
)

_airscale_enb = Airscale(common_units=[_common_unit_enb])
_enb = RealEnb(
    system_module=_airscale_enb,
    rms=_radio_units_enb,
    oam_ip=NetworkAddress(v4="172.16.2.8"),
    instance_id=10008,
    global_bts_id=10008,
    x2_link_addr=NetworkAddress(v4="172.16.2.8"),
)
_netAct = Netact(
    addr="srnclab1050lbwas.srnblr.nsn-rdnet.net",
    nom=NOM(
        ssh_connections_info=SshServiceDetails(
            addr="10.63.2.98", username="omc", password="Nokia_150"
        )
    ),
)

_lss = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.83.178.2", username="coam", password="zO&n1W*ktp7"
    ),
    connections=[
        NetworkAddress(v4="10.83.177.28", v6="2a00:8a02:60:3a:5054:f2ff:fef2:1e0"),
        NetworkAddress(v4="10.83.182.252", v6="2a00:8a02:60:1c::1:100"),
    ],
)
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    test_pcs=[_lss],
    cloud_hostings=[_ncir],
    tl_cloud_topology="CLOUD_5G_ASOD_AEUD_LSS_BRANCH",
    enbs=[_enb],
    nms=_netAct,
)

__all__ = ["tl"]

