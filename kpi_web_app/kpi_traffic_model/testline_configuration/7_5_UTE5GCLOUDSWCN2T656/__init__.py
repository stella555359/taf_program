__maintainer__ = "NSB MN 5G&SC SW Eng 2 CN T&A 2 SG"
__team__ = "NSB MN 5G&SC SW Eng 2 CN T&A 2 SG"
__email__ = "I_UTE_5G_SW_CN2@internal.nsn.com"
__owner_email__ = "MG_5G_HZ_SW_CN2"


import os
from taf.config.testline.testline import TestLine
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import NetworkAddress, RoutingInformation, Airphone
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
from taf.config.testline.core import LTEEmuCore
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline import Airphone
from taf.config.testline.pdu import ATEN, APC, FACOM


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

## PDU  port5= gNB  port6= Airphone#_pdu = APC(#    addr='10.46.139.52',#    port_numbers=[5,6])

# LteEmu
_lteemu = LTEEmuCore(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.71.187.191", username="ute", password="ute"
    ),
    dir_path="/opt/WTS",
    cfg_filename="basic_setup.cfg",
    mme_ip="10.0.2.1",
    mcc="311",
    mnc="489",
    tac=333,
    edaemon_port="22222",
    egate_port="10000",
)

_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.57.138.18", username="TL655", tenant="TL655", password="5GNokia!123"
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.138.18", username="TL655", password="5GNokia!"
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="1.1.1.1", username="unknown", password="unknown"
    ),
)

_ncir = NCIR(control_nodes=[_control_0], version="NCIR19", compute_nodes=[])
# GNB

_cbts_flavor = DeploymentFlavorStack(
    name="TL656_5gbts_flavors",
    env_files=[os.path.join(_CFG_DIR, "config_flavor.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_flavor.yaml"),
    default_vnf_prefix="tl655-5gbts",
)

_cbts_net = DeploymentNetworkStack(
    name="TL656_5gbts_ext",
    env_files=[os.path.join(_CFG_DIR, "config_ext_net.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="TL656_5gbts_rac",
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

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.71.187.191", username="ute", password="ute"
    )
)

_pdu = FACOM(addr="10.71.182.48", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_pdus = [_pdu]

_capacity_unit = CapacityUnit(addr="192.168.253.22")

_common_unit = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
    pdu_port=_pdus[0].pdu_ports[2],
)

_airscale = Airscale([_common_unit])

_cu = CU(
    backhaul_site_oam_ip="192.168.125.10",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.125.10", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.125.10", username="Nemuadmin", password="nemuuser", port=443
    ),
    x2c=NetworkAddress(v4="10.0.1.2", vlan_id=1674),
    x2u=NetworkAddress(v4="10.0.1.3", vlan_id=1674),
    s1u=NetworkAddress(v4="10.0.1.3", vlan_id=1674),
    f1u=NetworkAddress(v4="10.0.3.3", vlan_id=1674),
)
_abil1_gnb_1_master = CapacityUnit(addr="192.168.253.20")
_asik_gnb_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil1_gnb_1_master],
    pdu_port=_pdus[0].pdu_ports[2],
)

_airscale_gnb_1 = Airscale(common_units=[_asik_gnb_1])

_du = DU(airscale=_airscale_gnb_1)

_cbts = CloudBts(
    cu=_cu, dus=[_du], cloud_deployment=_cloud_deployment, vnf_name="tl655-5gbts"
)


# TODO convert to new TL config
Baseband = "ABIL"
airscaleNodeID = ["0x10", "0x12"]


# AirPhone


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
                pdu_port=_pdus[0].pdu_ports[1],
            )
        ]
    ),
)


tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    core=_lteemu,
    tl_cloud_topology="CLOUD_5G_CLOUD_AP",
    ues=[_ue],
    pdus=_pdus,
)

__all__ = ["tl"]
