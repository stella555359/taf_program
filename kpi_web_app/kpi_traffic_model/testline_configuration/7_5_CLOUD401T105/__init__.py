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
from taf.config.testline import RealEnb
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU
from taf.config.testline import DU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.170.54", username="root", password="nokia123"
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

# CU
_cu = CU(
    backhaul_site_oam_ip="10.57.170.5",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.170.5", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.170.5", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
# DU1
_common_unit_pdu = FACOM(addr="10.57.242.12", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="ip")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[2],
)

# DU2
_lmp_connection_1 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_1 = CapacityUnit(addr="6.6.6.6")

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_1, capacity_units=[_capacity_unit_1]
)

_lmp_connection_2 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_2 = CapacityUnit(addr="6.6.6.6")

_common_unit_2 = CommonUnit(
    lmp_connection=_lmp_connection_2, capacity_units=[_capacity_unit_2]
)

# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])

_airscale_1 = Airscale(common_units=[_common_unit_1])

_airscale_2 = Airscale(common_units=[_common_unit_2])
# DU
_du_0 = DU(airscale=_airscale_0, rus=[], f1_m_ip_addr="172.18.5.32")

_du_1 = DU(airscale=_airscale_1, rus=[], f1_m_ip_addr="172.18.5.35")

# enb
_real_enb = RealEnb(airscale=_airscale_2)

# CloudBts
flavor_env_files = [os.path.join(_cfg_dir, "5gbts_flavor.env")]

net_env_files = [os.path.join(_cfg_dir, "5gbts_ext_net.env")]

vnf_env_files = [
    os.path.join(_cfg_dir, "5gbts_heat.env"),
    os.path.join(_cfg_dir, "5gbts_heat_qt.env"),
]

_cbts_flavor = DeploymentFlavorStack(
    name="hgz-tl105_flavor",
    env_files=flavor_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="hgz-tl105",
)

_cbts_net = DeploymentNetworkStack(
    name="HGZ-TL105-BH-FH",
    env_files=net_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="HGZ-TL105-STACK",
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
    dus=[_du_0, _du_1], cu=_cu, cloud_deployment=_cloud_deployment, vnf_name="hgz-tl105"
)

# PDU
_common_pdu_0 = FACOM(addr="10.57.242.12", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_common_pdu_1 = FACOM(addr="10.57.241.142", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_real_enb],
    tl_cloud_topology="CLOUD_5G_BB3_18A",
)

__all__ = ["tl"]
