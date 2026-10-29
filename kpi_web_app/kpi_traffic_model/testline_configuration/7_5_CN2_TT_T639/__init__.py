__maintainer__ = "Lukasz Fracz"
__team__ = "MN 5G RAN I&V 3 Pz cOAM 12 SG"
__email__ = "I_UTE_CORE_5G@internal.nsn.com"
__owner_email__ = "lukasz.fracz@nokia.com"


from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    OpenStackConnectionDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
)
from taf.config.testline import NetworkAddress, RoutingInformation, Airphone
from taf.config.testline.cloud_hosting import (
    NCIR,
    ControlNode,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    ComputeNode,
)
from taf.config.testline.gnb import CloudBts, CU, DU
from taf.config.testline.pdu import ATEN, EPC
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit

import os

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.23", username="ute", password="ute"
    )
)

_compute = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(
        addr="10.42.99.250", username="admin", password="admin"
    )
)

_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.57.137.202", username="TL644", tenant="TL644", password="5GNokia!"
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.137.202", username="TL639", password="5GNokia!"
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="10.57.137.202", username="TL639", password="admin"
    ),
)

_control_1 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.42.99.249", username="admin", tenant="admin", password="uteadmin"
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.42.99.249", username="wrsroot", password="uteadmin"
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="10.42.99.249", username="admin", password="admin"
    ),
)

_ncir = NCIR(
    compute_nodes=[_compute], control_nodes=[_control_0, _control_1], version="ncir_19"
)

_cbts_flavor = DeploymentFlavorStack(
    name="FLAVOR_2_16_UTE5GCLASSICAL1446",
    env_files=[os.path.join(_CFG_DIR, "config_flavor.env")],
    yaml_file=os.path.join(_CFG_DIR, "config_flavor.yaml"),
    default_vnf_prefix="C3200T05",
)

_cbts_net = DeploymentNetworkStack(
    name="EXT_NET_2_16_UTE5GCLASSICAL1446",
    env_files=[os.path.join(_CFG_DIR, "config_ext_net.env")],
    yaml_file=os.path.join(_CFG_DIR, "config_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="BTS_2_16_UTE5GCLASSICAL1446",
    env_files=[os.path.join(_CFG_DIR, "config_bts.env")],
    yaml_file=os.path.join(_CFG_DIR, "config_bts.yaml"),
)

_cloud_deployment = CloudDeployment(
    default_cfg_dir=_CFG_DIR,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(v4="192.168.255.50", vlan_id=1971),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.50", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.50", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.2", vlan_id=1691),
    x2u=NetworkAddress(v4="10.0.1.3", vlan_id=1691),
    s1u=NetworkAddress(v4="10.0.1.3", vlan_id=1691),
    f1m=NetworkAddress(v4="10.0.3.4", vlan_id=1662),
    f1u=NetworkAddress(v4="10.0.3.3", vlan_id=1662),
    f1c=NetworkAddress(v4="10.0.3.2", vlan_id=1662),
)

_pdu1 = ATEN(addr="10.71.182.49", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_pdus = [_pdu1]

_abil1_du1 = CapacityUnit(addr="192.168.253.20")

_asik_du1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil1_du1],
    pdu_port=_pdu1.pdu_ports[7],
)

_du1 = DU(Airscale(common_units=[_asik_du1]))

_cbts = CloudBts(
    cu=_cu, cloud_deployment=_cloud_deployment, vnf_name="clay-5gbts19b", dus=[_du1]
)

_ue = Airphone(
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    Airscale(
        [
            CommonUnit(
                SshServiceDetails(
                    "192.168.200.1", "toor4nsn", password="oZPS0POrRieRtu"
                ),
                [CapacityUnit(addr="192.168.253.22")],
                pdu_port=_pdu1.pdu_ports[7],
            )
        ]
    ),
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    tl_cloud_topology="CLOUD_5G_ASIK_AP",
    pdus=_pdus,
    ues=[_ue],
)

__all__ = ["tl"]
