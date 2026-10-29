__maintainer__ = "Kamil Szczurkowski"
__team__ = "MN RAN Pz KRK 5 SG"
__email__ = "I_MN_5G_SC_MMW_SC_PZ_KRK_5_SG_TEST@internal.nsn.com"
__owner_email__ = "kamil.szczurkowski@nokia.com"
import os
from taf.config.testline.testpc import TestPc
from taf.config.testline import DU
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CU
from taf.config.testline.airscale import CommonUnit, Airscale
from taf.config.testline.gnb.gnb import CloudBts
from taf.config.testline.gnb.networkaddress import NetworkAddress
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
from taf.config.testline.pdu import FPFH, PduPort

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))
_pdu = FPFH(
    addr="10.255.13.2",
    port_numbers=[1, 2, 3, 4, 5, 6],
    login="admin",
    password="admin",
    model="FPFH",
)
_pdus = [_pdu]
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK026.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)
_common_unit_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)
_common_unit = CommonUnit(
    lmp_connection=_common_unit_lmp_connection,
    capacity_units=None,
    hardware_type="ASIK",
)
_airscale = Airscale(common_units=[_common_unit])
_du = DU(airscale=_airscale)
_cu = CU(
    backhaul_site_oam_ip=None,
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.84.144.13", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.84.144.13", username="Nemuadmin", password="nemuuser"
    ),
)
_compute = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password="")
)
_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.84.160.245",
        username="za91user1",
        tenant="ZA91tenant1",
        password="5Guser@3",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.84.160.245", username="za91user1", password="5Guser@3"
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)
_ncir = NCIR(compute_nodes=[_compute], control_nodes=[_control_0], version="ncir_19")
_cbts_flavor = DeploymentFlavorStack(
    name="Flavors_p04_26",
    env_files=[os.path.join(_CFG_DIR, "config_flavor.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_flavor.yaml"),
    default_vnf_prefix="p04_26",
)
_cbts_vnf = DeploymentVnfStack(
    name="VNF_p04_26",
    env_files=[os.path.join(_CFG_DIR, "config_bts.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_heat.yaml"),
)
_cloud_deployment = CloudDeployment(
    default_cfg_dir=_CFG_DIR,
    flavors=[_cbts_flavor],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)
_cbts = CloudBts(
    cloud_deployment=_cloud_deployment,
    vnf_name="p04_26",
    cu=_cu,
    dus=[_du],
)
_cbts.m_plane = NetworkAddress(v4="10.84.190.26")
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    pdus=_pdus,
)
__all__ = ["tl"]
