__maintainer__ = "Tu Luofei"
__team__ = "I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_2SISO_GMS <I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_2SISO@internal.nsn.com>"
__email__ = "I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_2SISO@internal.nsn.com"
__owner_email__ = "luofei.tu@nokia-sbell.com"

import os

from taf.config.testline.cloud_hosting import (
    OSP,
    NCIR,
    ControlNode,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    DeploymentSecurityGroupStack,
    ComputeNode,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline import RealEnb
from taf.config.testline.core import RealCore
from taf.config.testline.lab_infrastructure import PxeServer
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU
from taf.config.testline import DU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN
from taf.config.testline.cbam import Cbam
from taf.config.testline.nms import NMS
from taf.config.testline.attenuator import Attenuator
from taf.config.testline.attenuator import AttenuationPort
from taf.config.testline.attenuator import HBTE
from taf.config.testline.ue import Android
from taf.config.testline.connection_details import IperfDataTransferDetails
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.gnb.networkaddress import RoutingInformation
from taf.config.testline.radio import RU
from taf.config.testline.appserver import AppServer

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc

# UTE IP address and User Name, Password
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.104", username="ute", password="ute"
    )
)
######################################## eNB start ######################################################


# enb
_lmp_connection_enb = SshServiceDetails(
    addr="10.108.135.84", username="toor4nsn", password="oZPS0POrRieRtu"
)
_common_unit_1 = CommonUnit(lmp_connection=_lmp_connection_enb, capacity_units=[])
_real_enb_lte = Airscale(common_units=[_common_unit_1])
_real_enb = RealEnb(airscale=_real_enb_lte)


############################# eNB END ############################################################
############################# PDU info  ########################################################################
# PDU oam http connection
_abil1_du1 = CapacityUnit(addr="192.168.253.20")

_asik_du1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil1_du1],
)

_ru_du1 = RU(
    ru_hw_group="",
    default_ssh_connection_details=SshServiceDetails(addr="", username=""),
    lmp_connection=SshServiceDetails(addr="", username=""),
    radio_type="AEUD",
)

# PDU global configuration
_pdu = DU(
    Airscale(common_units=[_asik_du1]),
    f1_m_ip_addr=NetworkAddress(v4="10.108.135.84"),
    rus=[_ru_du1],
)


# VCU related OSP controlNode
_control = ControlNode(
    # Configuration for SSH access
    default_ssh_connection_details=SshServiceDetails(
        addr="10.107.8.116", username="stack", password="system123"
    ),
    # Configuration for openstack connection
    open_stack_connection_details=OpenStackConnectionDetails(
        username="CBTS1user",
        password="system123",
        ip_addr="10.107.196.126",
        tenant="CBTS1",
        protocol="http",
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

# configuration of VCU related NCIR/OSP
_osp = NCIR(compute_nodes=[], control_nodes=[_control], version="osp_10")

# CU configuration
_cu = CU(
    # CU web UI ip address, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.107.169.132", username="serviceuser", password="Pl(FzaYj5~c5;q"
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(v4="10.107.169.132"),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.107.169.132", username="Nemuadmin", password="nemuuser", port="443"
    ),
    # route configuration for x2c link to ENB, v4 is network address of ENB x2c link
    x2c=NetworkAddress(
        v4="10.0.0.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.107.54.65", ip_prefix_length=8),
    ),
    # route configuration for x2u link to ENB, v4 is network address of ENB x2u link
    x2u=NetworkAddress(
        v4="10.0.0.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.107.54.65", ip_prefix_length=8),
    ),
    # route configuration for f1c link to VDU on VCU, v4 is network address of VDU f1c link
    f1c=NetworkAddress(
        v4="10.97.121.128",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.107.54.193", ip_prefix_length=25),
    ),
    # route configuration for f1u link to VDU on VCU, v4 is network address of VDU f1u link
    f1u=NetworkAddress(
        v4="10.97.121.128",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.107.54.193", ip_prefix_length=25),
    ),
    tracing=None,
)

# flavor of VCU
flavor_env_files = [os.path.join(_cfg_dir, "5gbts_flavor.env")]

# ext_net of VCU
ext_env_files = [os.path.join(_cfg_dir, "5gbts_ext_net.env")]
# int_net of vCU
int_env_files = [os.path.join(_cfg_dir, "5gbts_int_net.env")]
# oam_net of vCU
oam_env_files = [os.path.join(_cfg_dir, "5gbts_oam_net.env")]
# heat parameters
vnf_env_files = [os.path.join(_cfg_dir, "5gbts_heat.env")]

_cbts_flavor = DeploymentFlavorStack(
    name="7_5_UTE5GAIC001T111-flavor",
    env_files=flavor_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="hgz-5309",
)

_cbts_net = DeploymentNetworkStack(
    name="7_5_UTE5GAIC001T111-net",
    env_files=ext_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)

_cbts_oam = DeploymentNetworkStack(
    name="7_5_UTE5GAIC001T111_oam",
    env_files=oam_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_oam_net.yaml"),
)

_cbts_int = DeploymentNetworkStack(
    name="7_5_UTE5GAIC001T111-int",
    env_files=int_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_int_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="7_5_UTE5GAIC001T111-vnf",
    env_files=vnf_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_heat.yaml"),
)

_cbts_security = DeploymentSecurityGroupStack(
    name="7_5_UTE5GAIC001T111_security",
    env_files=[os.path.join(_cfg_dir, "5gbts_security_group.env")],
    yaml_file=os.path.join(_cfg_dir, "5gbts_security_group.yaml"),
)

# cloud deployment configuration fo VCU
_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    flavors=[_cbts_flavor],
    networks=[_cbts_net, _cbts_oam],
    vnfs=[_cbts_vnf],
    security_groups=[_cbts_security],
    cloud_hosting=_osp,
)


#  vCU global configuration
_cbts = CloudBts(
    dus=[_pdu],  # pdu related parameter
    cu=_cu,
    cloud_deployment=_cloud_deployment,
    vnf_name=_cbts_vnf.name,
    instance_id=5309,
    global_bts_id=5309,
)

# mcc, mnc configuration
_realcore = RealCore(five_g=None, mcc="262", mnc="03", pdns=None)

# Testline configuration
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_real_enb],
    tl_cloud_topology="CLOUD_5G_OSP_ASIK_ABIL_AEUA_ENB",
    cloud_hostings=[_osp],
    core=_realcore,
)

# only tl variable can be accessed by user
__all__ = ["tl"]
