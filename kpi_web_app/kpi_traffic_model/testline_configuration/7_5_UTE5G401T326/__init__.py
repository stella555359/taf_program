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
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import RealCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import Android
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import RealEnb
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline import NetworkAddress, RoutingInformation


__maintainer__ = "Jerry Wu"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02@internal.nsn.com>"
)
__email__ = "jerry.wu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# CI_Detail_UE_Type=''

# RealEnb
_real_enb_pdu = HBTE(addr="10.68.87.81", port_numbers=[1])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="2a00:8a00:8000:136:10:68:88:c3",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)


# #5GRU_0 for cloudBTS
_ru_pdu = HBTE(addr="10.68.87.79", port_numbers=[1])

_ru = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.10.49", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type="AEUB",
)


# DU_0 for cloudlBTS
_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

# don't know if the following detail is correct,install not need
_capacity_unit = CapacityUnit(addr="192.168.253.22")


_gnb_pdu = HBTE(addr="10.68.87.81", port_numbers=[1])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru, label="SFP", port_id=1),
    )
]

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])


_du = DU(
    airscale=_airscale, rus=[_ru], f1_m_ip_addr="192.168.255.129", cablinks=_ru_cablinks
)

# #CU

_f1m = NetworkAddress(
    v4="xxxx",
    v6="fc00::172:16:87:110",
    vlan_id=None,
    routing=RoutingInformation(gateway="fc00::172:16:87:1", ip_prefix_length=112),
)
_f1c = NetworkAddress(
    v4="xxxx",
    v6="fc00::172:16:87:120",
    vlan_id=None,
    routing=RoutingInformation(gateway="fc00::172:16:87:1", ip_prefix_length=112),
)
_f1u = NetworkAddress(
    v4="xxxx",
    v6="fc00::172:16:87:130",
    vlan_id=None,
    routing=RoutingInformation(gateway="fc00::172:16:87:1", ip_prefix_length=112),
)
_x2c = NetworkAddress(
    v4="xxxx",
    v6="2a00:8a00:8000:136:10:57:159:8138",
    vlan_id=None,
    routing=RoutingInformation(
        gateway="2a00:8a00:8000:136:10:57:159:8001", ip_prefix_length=114
    ),
)
_x2u = NetworkAddress(
    v4="xxxx",
    v6="2a00:8a00:8000:136:10:57:159:8139",
    vlan_id=None,
    routing=RoutingInformation(
        gateway="2a00:8a00:8000:136:10:57:159:8001", ip_prefix_length=114
    ),
)
_s1c = NetworkAddress(
    v4="xxxx",
    v6="2a00:8a00:8000:136:10:57:159:8138",
    vlan_id=None,
    routing=RoutingInformation(
        gateway="2a00:8a00:8000:136:10:57:159:8001", ip_prefix_length=114
    ),
)
_s1u = NetworkAddress(
    v4="xxxx",
    v6="2a00:8a00:8000:136:10:57:159:8139",
    vlan_id=None,
    routing=RoutingInformation(
        gateway="2a00:8a00:8000:136:10:57:159:8001", ip_prefix_length=114
    ),
)
_tracing = NetworkAddress(v4="xxxx", v6="xxxx", vlan_id="xxxx")

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.159.4", vlan_id=None),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.4", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.159.4", username="Nemuadmin", password="nemuuser"
    ),
    f1m=_f1m,
    f1c=_f1c,
    f1u=_f1u,
    x2c=_x2c,
    x2u=_x2u,
    s1c=_s1c,
    s1u=_s1u,
    tracing=_tracing,
)

_control = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.57.137.34",
        username="nokiauser",
        tenant="FiveG",
        password="HZ5granNOki@678!",
        port=5000,
        protocol="https",
        version="v3",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.137.34", username="nokiauser", password="HZnoki@123!"
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="5.5.5.5", username="admin", password="admin"
    ),
)

_ncir = NCIR(
    compute_nodes=[],
    control_nodes=[_control],
    version="ncir_19",
    cloud_deployments=None,
)

# #cloudbts
_cbts_flavor = DeploymentFlavorStack(
    name="hgz-tl326-flavor",
    env_files=[os.path.join(_cfg_dir, "config_flavor_ci.env")],
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="cbts_prefix",
)

_cbts_net = DeploymentNetworkStack(
    name="hgz-tl326-intnet",
    env_files=[os.path.join(_cfg_dir, "config_ext_net_ci.env")],
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="hgz-tl326-vnfc",
    env_files=[os.path.join(_cfg_dir, "config_bts_ci.env")],
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
    dus=[_du],
    cu=_cu,
    instance_id=326,
    global_bts_id=326,
    vnf_name=_cbts_vnf.name,
    cloud_deployment=_cloud_deployment,
)

# #cloud_topology
_tl_cloud_topology = "CLOUD_5G_ASIKL_ABILB1_AEUB_IPv6"


# #host
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.169.126", username="ute", password="ute"
    )
)

# switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="0.0.0.0", port="1", username="5gran", password="nokia123"
)  # EIF1 Port
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

# switch Mtor
_dell_s4048ton_ssh = SshServiceDetails(
    addr="0.0.0.0", port="1", username="5gran", password="nokia123"
)
_dell_s4048ton_switch = DellS4048TONSwitch(_dell_s4048ton_ssh)

_attenuator = TopYoung(ip_addr="x.x.x.x", port=23, attenuation_port_numbers=[7, 8])


tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    enbs=[_lte_real_enb],
    core=RealCore(mcc=489, mnc=311),
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
)
