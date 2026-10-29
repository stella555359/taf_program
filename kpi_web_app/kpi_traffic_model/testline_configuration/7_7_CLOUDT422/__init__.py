import os

__maintainer__ = "Bartosz Odziomek"
__team__ = "I_MN_5G_SC_SEP_VERIFICATION"
__email__ = "bartosz.odziomek@nokia.com"

from taf.config.cbts import create_configuration_data
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    TelnetConnectionDetails,
    BmcConnectionDetails,
    OpenStackConnectionDetails,
)
from taf.config.testline.gnb import CU, DU
from taf.config.testline import (
    NetworkAddress,
    RU,
    CloudBts,
    CloudDeployment,
    DeploymentVnfStack,
    DeploymentNetworkStack,
    DeploymentFlavorStack,
    NCIR,
    ComputeNode,
    ControlNode,
    EPCSim,
)
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import PduPort, ATEN
from taf.config.testline.enb import RealEnb

# The most commonly used testline configuration. #
_test_pc_gnb_default_ssh_connection_details = SshServiceDetails(
    addr="sc5g-enb-422.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
)

_test_pc_enb_default_ssh_connection_details = SshServiceDetails(
    addr="sc5g-enb-041.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
)

_ncir_control0_ip = "10.83.245.124"

_gnb_oam_ip = NetworkAddress(
    v6="2a00:8a02:60:1c::1:422",
    vlan_id=503,
)
_gnb_instance_id = 10422
_gnb_global_bts_id = 2
_gnb_du_common_unit_hardwarde_type = "ASIK"
_gnb_ru_ip = NetworkAddress(v4="192.168.254.34")
_gnb_ru_hw_group = "AEUD"

_enb_oam_ip = NetworkAddress(v6="2a00:8a02:60:1c::41")
_enb_instance_id = 41
_enb_global_bts_id = 100041
_enb_du_common_unit_hardware_type = "ASIA"
_enb_du_capacity_unit_hardware_type = "ABIA"

##############################################################
# Default values
_CFG_DIR = os.path.dirname(os.path.abspath(__file__))
vnf_env_files = [os.path.join(_CFG_DIR, "5gbts_heat.env")]
vnf_config = create_configuration_data(vnf_env_files, deep_merge_enabled=False)

_default_ssh_lmp_connection = SshServiceDetails(
    addr=_gnb_oam_ip.v6,
    username="robot",
    password="rastre1",
)

_default_oam_http_connection = HttpConnectionDetails(
    addr="[2a00:8a02:60:1c::1:422]",
    username="Nemuadmin",
    password="nemuuser",
)
##############################################################


# Important!: check below and change if other than default #

# Test PCs
_test_pc_gnb = TestPc(
    default_ssh_connection_details=_test_pc_gnb_default_ssh_connection_details
)
_test_pc_enb = TestPc(
    default_ssh_connection_details=_test_pc_enb_default_ssh_connection_details
)

# cloud section
_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr=_ncir_control0_ip, username="admin", tenant="admin", password="uteadmin"
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr=_ncir_control0_ip, username="wrsroot", password="uteadmin"
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="10.0.0.0", username="admin", password="admin"
    ),
)

_compute = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(
        addr="10.0.0.0", username="admin", password="admin"
    )
)

_ncir = NCIR(compute_nodes=[_compute], control_nodes=[_control_0], version="ncir_19")

_cbts_flavor = DeploymentFlavorStack(
    name="TL_7_7_CLOUDT422_Flavors",
    env_files=[os.path.join(_CFG_DIR, "5gbts_flavor.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_flavor.yaml"),
    default_vnf_prefix="c2800_T02",
)

_cbts_net = DeploymentNetworkStack(
    name="TL_7_7_CLOUDT422_Networks",
    env_files=[os.path.join(_CFG_DIR, "5gbts_ext_net.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="TL_7_7_CLOUDT422_BTS",
    env_files=[os.path.join(_CFG_DIR, "5gbts_heat.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_heat.yaml"),
    configuration_data=vnf_config,
)
# tl.gnbs[0].cloud_deployment.vnfs[0].configuration_data['parameters']['external_networks']['f1c']['fixed_ips'][0]['ip_address']}
_cloud_deployment = CloudDeployment(
    default_cfg_dir=_CFG_DIR,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)

# eNB section

_du_lmp_connection_enb = _default_ssh_lmp_connection
_du_lmp_connection_enb.proxy = _test_pc_enb_default_ssh_connection_details

_du_capacity_unit_enb = CapacityUnit(
    addr="192.168.253.22",
    hardware_type=_enb_du_capacity_unit_hardware_type,
    hardware_version="M02",
)

_du_common_unit_enb = CommonUnit(
    lmp_connection=_du_lmp_connection_enb,
    capacity_units=[_du_capacity_unit_enb],
    hardware_type=_enb_du_common_unit_hardware_type,
    hardware_version="M01",
)

_airscale_enb = Airscale(common_units=[_du_common_unit_enb])

_enb = RealEnb(
    system_module=_airscale_enb,
    oam_ip=_enb_oam_ip,
    instance_id=_enb_instance_id,
    global_bts_id=_enb_global_bts_id,
    x2_link_addr=_enb_oam_ip,
)

# gNB section

_cu_gnb = CU(
    backhaul_site_oam_ip=_gnb_oam_ip.v6,
    oam_ssh_connection_details=_default_ssh_lmp_connection,  # replace if other than default
    oam_http_connection_details=_default_oam_http_connection,  # replace if other than default
    f1m=NetworkAddress(v6="2a00:2222:2222:2222:2222:2222:2222:101"),
    f1c=NetworkAddress(v6="2a00:2222:2222:2222:2222:2222:2222:102"),
    f1u=NetworkAddress(v6="2a00:2222:2222:2222:2222:2222:2222:103"),
    x2c=NetworkAddress(v6="2a00:8a02:60:1c:0:0:2:422"),
    x2u=NetworkAddress(v6="2a00:8a02:60:1c:0:0:3:422"),
)

_du_lmp_connection_gnb = _default_ssh_lmp_connection
_du_lmp_connection_gnb.proxy = _test_pc_gnb_default_ssh_connection_details

_abil_master_gnb = CapacityUnit(addr="192.168.253.20")
_abil_slave_gnb = CapacityUnit(addr="192.168.253.21")
_abil_loner_gnb = CapacityUnit(addr="192.168.253.22")

_du_common_unit_gnb = CommonUnit(
    lmp_connection=_du_lmp_connection_gnb,
    capacity_units=[_abil_master_gnb, _abil_slave_gnb, _abil_loner_gnb],
    hardware_type=_gnb_du_common_unit_hardwarde_type,
    hardware_version="M01",
)

_ru_gnb0 = RU(
    ru_hw_group=_gnb_ru_hw_group,
    default_ssh_connection_details=SshServiceDetails(
        addr=_gnb_ru_ip.v4,
        username="root",
        password="umniedziala",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    pdu_port=PduPort(
        pdu=ATEN(
            addr="pe8108g.sc5g-leg.krk-lab.nsn-rdnet.net",
            port_numbers=[0, 1, 2, 3, 4, 5, 6, 7, 8],
        ),
        port_no=8,
    ),
)

_ru_gnb1 = RU(
    ru_hw_group=_gnb_ru_hw_group,
    default_ssh_connection_details=SshServiceDetails(
        addr=_gnb_ru_ip.v4,
        username="root",
        password="umniedziala",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    pdu_port=PduPort(
        pdu=ATEN(
            addr="pe8108g.sc5g-leg.krk-lab.nsn-rdnet.net",
            port_numbers=[0, 1, 2, 3, 4, 5, 6, 7, 8],
        ),
        port_no=7,
    ),
)

_airscale_gnb = Airscale(common_units=[_du_common_unit_gnb])

_du0_gnb = DU(
    airscale=_airscale_gnb,
    rus=[_ru_gnb0],
    f1_m_ip_addr="2a00:2222:2222:2222:2222:2222:2222:60",
    f1_c_ip_addr="2a00:2222:2222:2222:2222:2222:2222:61",
    f1_u_ip_addr="2a00:2222:2222:2222:2222:2222:2222:62",
)

_du1_gnb = DU(
    airscale=_airscale_gnb,
    rus=[_ru_gnb1],
    f1_m_ip_addr="2a00:2222:2222:2222:2222:2222:2222:80",
    f1_c_ip_addr="2a00:2222:2222:2222:2222:2222:2222:81",
    f1_u_ip_addr="2a00:2222:2222:2222:2222:2222:2222:82",
)

_cbts = CloudBts(
    cu=_cu_gnb,
    cloud_deployment=_cloud_deployment,
    vnf_name="TL_7_7_CLOUDT422_BTS",
    dus=[_du0_gnb, _du1_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

_core = EPCSim(
    default_ssh_connection_details=SshServiceDetails(
        addr="sc5g-enb-041.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
    ),
    dir_path="/home/ute/epcsim",
    cfg_filename="sim.cfg",
    mme_ip="2a00:8a02:60:1d::41",
    mcc=244,
    mnc=8,
    tac=1024,
    edaemon_port=60002,
    egate_port=60001,
)

# Testline

tl = TestLine(
    test_pc=_test_pc_gnb,
    core=_core,
    enbs=[_enb],
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    tl_cloud_topology="CLOUD_5G",
)

__all__ = ["tl"]
