__maintainer__ = "Kamil Gorski"
__team__ = "MN 5G&SC mmW&SC Pz KRK 7 SG"
__email__ = "I_5G_PZ_MMW_KRK_7SG_TEST@internal.nsn.com"
__owner_email__ = "kamil.gorski@nokia.com"


import os
from taf.config.testline.testpc import TestPc
from taf.config.testline import DU
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CU
from taf.config.testline.airscale import CommonUnit, Airscale
from taf.config.testline.gnb.gnb import CloudBts
from taf.config.testline.connection_details import (
    SshServiceDetails,
    OpenStackConnectionDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
)
from taf.config.testline.cloud_hosting import (
    OSP,
    ControlNode,
    CloudDeployment,
    ComputeNode,
)
from taf.config.testline.cbam import Cbam

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT439.sc5g.krk-lab.nsn-rdnet.net",
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
    hardware_type="ASOD",
)
_airscale = Airscale(common_units=[_common_unit])
_du = DU(airscale=_airscale)
_cu = CU(
    backhaul_site_oam_ip="2a00:8a02:60:1c::2:439",
    oam_ssh_connection_details=SshServiceDetails(
        addr="2a00:8a02:60:1c::1:439", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="[2a00:8a02:60:1c::1:439]",
        username="Nemuadmin",
        password="nemuuser",
        port=443,
    ),
)
_compute = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password="")
)
_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.83.245.24",
        username="admin",
        tenant="admin",
        password="Q7jFl2DUsKYHvZ3QxKkFuKDMv",
        protocol="http",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.83.190.241", username="sb14user1", password="5Guser@3"
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)
_osp = OSP(compute_nodes=[_compute], control_nodes=[_control_0], version="")


_cloud_deployment = CloudDeployment(
    default_cfg_dir=_CFG_DIR,
    flavors=[],
    networks=[],
    vnfs=[],
    cloud_hosting=_osp,
)
_cbts = CloudBts(
    cloud_deployment=_cloud_deployment,
    cu=_cu,
    dus=[_du],
)
_cbam = Cbam(
    addr="10.89.0.73",
    client_id="cbam_client",
    client_secret="49c9d0d1-e7b5-45b1-b29e-6e4d71c45666",
)

tl = TestLine(test_pc=_test_pc, gnbs=[_cbts], cloud_hostings=[_osp], cbam=_cbam)

__all__ = ["tl"]
