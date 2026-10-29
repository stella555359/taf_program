__maintainer__ = "Zhang Andy"
__team__ = "I_MN_5G_RAN_IV4_QT_HZG_GMS <I_MN_5G_RAN_IV4_QT_HZG@internal.nsn.com>"
__email__ = "I_MN_5G_RAN_IV4_QT_HZG@internal.nsn.com"
__owner_email__ = "andy.zhang@nokia-sbell.com"

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
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU
from taf.config.testline import DU, RU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.170.34", username="root", password="nokia123"
    )
)

# NCIR
_control = ControlNode(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.138.34", username="unit_1", password="nokia123"
    ),
    open_stack_connection_details=OpenStackConnectionDetails(
        username="unit_1", password="nokia123", ip_addr="10.57.138.34", tenant="unit_1"
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="ncir_17a")

# EPCSim
_epcsim = EPCSim(
    mme_ip="172.18.10.20",
    tac="788",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.170.34", username="nokia", password="nokia123"
    ),
    mcc="224",
    mnc="09",
    dir_path="/home/nokia/WTS_4.0.4696",
    cfg_filename="basic_wts_step1.cfg",
    edaemon_port=22222,
    egate_port=20000,
)

# CU
_cu = CU(
    backhaul_site_oam_ip="2a00:8a00:8000:136:10:57:170:4",
    oam_ssh_connection_details=SshServiceDetails(
        addr="2a00:8a00:8000:136:10:57:170:4", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="2a00:8a00:8000:136:10:57:170:4", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
_common_unit_pdu = FACOM(addr="10.57.242.4", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_lmp_connection_0 = SshServiceDetails(
    addr="10.57.231.50", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="ip")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[6],
)

# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])

# RU
_ru_pdu = FACOM(addr="10.57.249.13", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[8],
)

_du_0 = DU(airscale=_airscale_0, rus=[_ru], f1_m_ip_addr="fc00::172:18:5:32")

# CloudBts
flavor_env_files = [os.path.join(_cfg_dir, "5gbts_flavor.env")]

net_env_files = [os.path.join(_cfg_dir, "5gbts_ext_net.env")]

vnf_env_files = [
    os.path.join(_cfg_dir, "5gbts_heat.env"),
    os.path.join(_cfg_dir, "5gbts_heat_qt.env"),
]

_cbts_flavor = DeploymentFlavorStack(
    name="hgz-tl112_flavor",
    env_files=flavor_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="hgz-tl112",
)

_cbts_net = DeploymentNetworkStack(
    name="EXT_NET",
    env_files=net_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="HGZ-TL112-STACK",
    env_files=vnf_env_files,
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
    dus=[_du_0], cu=_cu, cloud_deployment=_cloud_deployment, vnf_name="hgz-tl112"
)

# TestLine
tl = TestLine(
    test_pc=_test_pc, gnbs=[_cbts], core=_epcsim, tl_cloud_topology="CLOUD_5G_BB3_18A"
)

__all__ = ["tl"]
