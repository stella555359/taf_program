###############################
#      TL007 CLOUD AP NPS     #
###############################
__maintainer__ = "Regulski Thomas"
__team__ = "MN_5G_SC_NPS_ET"
__email__ = "thomas.regulski@nokia.com"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline import NetworkAddress, RoutingInformation, Airphone
from taf.config.testline import RealEnb, LTEEmuEnb
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
)
from taf.config.testline.gnb import CloudBts, CU, DU
from taf.config.testline.pdu import ATEN
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.cbts import create_configuration_data
from taf.config.testline.core import EPCSim, LTEEmuCore

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# PDU  port7= gNB  port8= Airphone
_pdu = ATEN(addr="10.5.112.86", port_numbers=[7, 8])

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.0.108.18", username="ute", password="ute"
    )
)

_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.5.112.193", username="admin", tenant="admin", password="uteadmin"
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.5.112.193", username="wrsroot", password="uteadmin"
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="1.1.1.1", username="unknown", password="unknown"
    ),
)

_ncir = NCIR(control_nodes=[_control_0], version="NCIR19", compute_nodes=[])

# GNB

_cbts_flavor = DeploymentFlavorStack(
    name="tl07-5gbts_flavor",
    env_files=[os.path.join(_CFG_DIR, "5gbts_flavor.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_flavor.yaml"),
    default_vnf_prefix="TL015",
)

_cbts_net = DeploymentNetworkStack(
    name="tl07-5gbts_ext_net",
    env_files=[os.path.join(_CFG_DIR, "5gbts_ext_net.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="CLOUD5GPSECETL07_BTS",
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
    backhaul_site_oam_ip=NetworkAddress(v4="10.5.113.18", vlan_id=1100),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.5.113.18", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.5.113.18", username="Nemuadmin", password="nemuuser", port=443
    ),
    x2c=NetworkAddress(v4="10.0.1.2", vlan_id=1426),
    x2u=NetworkAddress(v4="10.0.1.3", vlan_id=1426),
    s1u=NetworkAddress(v4="10.0.1.3", vlan_id=1426),
    f1u=NetworkAddress(v4="10.0.3.3", vlan_id=2226),
)

# ABIL
_capacity_unit_1 = CapacityUnit(addr="192.168.253.20")

# ASIK
_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.5.113.223", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit_1],
    pdu_port=_pdu.pdu_ports[7],
)

_airscale_1 = Airscale(common_units=[_common_unit_1])

_du_1 = DU(airscale=_airscale_1)

_cbts = CloudBts(
    cu=_cu, dus=[_du_1], cloud_deployment=_cloud_deployment, vnf_name="TL007"
)

# AirPhone
_ue = Airphone(
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    Airscale(
        [
            CommonUnit(
                SshServiceDetails("10.5.113.9", "toor4nsn", password="oZPS0POrRieRtu"),
                [CapacityUnit(addr="192.168.253.84")],
                pdu_port=_pdu.pdu_ports[8],
            )
        ]
    ),
)

# ====== WTS ========
_lteemu = LTEEmuCore(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.28.3.185", username="ute", password="ute"
    ),
    dir_path="/home/ute/WTS/",
    cfg_filename="basic_step2.cfg",
    mme_ip="",
    edaemon_port="22222",
    egate_port="20000",
)

_lteSim = LTEEmuEnb(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.5.112.51", username="ute", password="ute"
    ),
    dir_path="/home/ute/WTS/",
    cfg_filename="basic_step2.cfg",
)

# Testline
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    tl_cloud_topology="CLOUD_5G_ASIK_AP",
    pdus=[_pdu],
    ues=[_ue],
)

__all__ = ["tl"]
