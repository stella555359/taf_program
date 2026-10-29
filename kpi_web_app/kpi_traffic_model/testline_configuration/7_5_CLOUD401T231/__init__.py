import os
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    DeploymentSecurityGroupStack,
    ComputeNode,
    OSP,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)  # added in taf.meta.5.4
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
)  # added in taf.meta 5.4
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.hardware_controller import (
    AmiaFanHardwareController,
    GPSPowerHardwareController,
)
from taf.config.testline.signal_analyzer import KeysightN9935A
from taf.config.testline.nms import Netact
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.optical_switch import Leoni

__maintainer__ = "Cheng Huimin"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_3_GMS <I_MN_5G_RAN_IV4_LINE_HZG_3@internal.nsn.com>"
)
__email__ = "huimin.1.cheng@nokia-sbell.com"

# common
__all__ = ["tl"]

PARAMS_TO_MODIFY_TL = [
    # dict(value='10.57.227.1', dist_name='MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPRT-1', p_name='gateway'),
    dict(
        value="172.18.5.30",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-4/IPNO-1/IPIF-1/IPADDRESSV4-1",
        p_name="localIpAddr",
    ),
    dict(
        value="172.18.5.31",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-4/IPNO-1/IPIF-1/IPADDRESSV4-2",
        p_name="localIpAddr",
    ),
    dict(
        value="172.18.5.32",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-4/IPNO-1/IPIF-1/IPADDRESSV4-3",
        p_name="localIpAddr",
    ),
]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.45", username="root", password="nokia123"
    )
)

# #Prisma
_airmosaic_ssh = SshServiceDetails(
    addr="10.57.130.155", username="nokia5G", password="noki@123"
)

_airmosaic_harness = HttpConnectionDetails(addr="10.57.130.155", port=8090)

_lsu_uu_ssh = SshServiceDetails(addr="10.57.234.90", username="user", password="user")

_tstm_uu_ssh = SshServiceDetails(addr="10.57.234.90", username="user", password="user")

_appserver_ssh = SshServiceDetails(
    addr="10.57.163.50", username="cmw_sg3", password="cmw_sg3"
)

_prisma_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.50",
    iperf_path="/cygdrive/c/iperf",
)

_prisma_ue = Prisma(
    airmosaic_ssh_connection_details=_airmosaic_ssh,
    airmosaic_harness_connection_details=_airmosaic_harness,
    lsu_uu_ssh_connection_details=_lsu_uu_ssh,
    iperf_details=_prisma_iperf,
    tstm_uu_ssh_connection_details=_tstm_uu_ssh,
)

# #RealEnb
_real_enb_pdu = FACOM(
    addr="10.57.242.60", port_numbers=[2], model="111", version="1.1.1"
)

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.231.5", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[2],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None, instance_id=231)

# #5GRU for classicalBTS
# attenuator
_attenuator = TopYoung(
    ip_addr="10.57.234.92",
    port=3000,
    attenuation_port_numbers=[5, 6, 7, 8],
    model="TAS16T16-51-120-1SDES",
)

_ru_pdu = FACOM(addr="10.57.243.5", port_numbers=[5])

_ru = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[5],
    radio_type=RadioTypes.AEUA,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

# #5GRU_0 for cloudBTS
_ru_0_pdu = FACOM(addr="10.57.243.5", port_numbers=[5])

_ru_0 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    pdu_port=_ru_0_pdu.pdu_ports[5],
    attenuation_ports=[
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_ru_1 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    pdu_port=_ru_0_pdu.pdu_ports[5],
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
    ],
)

# #DU_0 for cloudlBTS
_lmp_connection_9 = SshServiceDetails(
    addr="10.57.231.19", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_9 = CapacityUnit(addr="192.168.253.20")

_du_0_pdu = FACOM(addr="10.57.242.59", port_numbers=[2])

_common_unit_9 = CommonUnit(
    lmp_connection=_lmp_connection_9,
    capacity_units=[_capacity_unit_9],
    pdu_port=_du_0_pdu.pdu_ports[2],
)

_airscale_0 = Airscale(common_units=[_common_unit_9])

_du_0 = DU(
    airscale=_airscale_0,
    rus=[_ru_0],
    f1_m_ip_addr=NetworkAddress(v4="172.18.5.32", vlan_id=2402),
    f1_c_ip_addr=NetworkAddress(v4="172.18.5.30", vlan_id=2402),
    f1_u_ip_addr=NetworkAddress(v4="172.18.5.31", vlan_id=2402),
)

_du_1 = DU(
    airscale=_airscale_0,
    rus=[_ru_1],
    f1_m_ip_addr=NetworkAddress(v4="172.18.5.32", vlan_id=2405),
    f1_c_ip_addr=NetworkAddress(v4="172.18.5.30", vlan_id=2405),
    f1_u_ip_addr=NetworkAddress(v4="172.18.5.31", vlan_id=2405),
)
# #CU

_f1m = NetworkAddress(v4="172.18.5.106", vlan_id=2402)
_f1c = NetworkAddress(v4="172.18.5.100", vlan_id=2402)
_f1u = NetworkAddress(v4="172.18.5.103", vlan_id=2402)
_x2c = NetworkAddress(v4="10.57.250.138", vlan_id=1)
_x2u = NetworkAddress(v4="10.57.250.139", vlan_id=1)
_s1c = NetworkAddress(v4="10.57.250.138", vlan_id=1)
_s1u = NetworkAddress(v4="10.57.250.139", vlan_id=1)
_tracing = NetworkAddress(v4="172.18.4.101", vlan_id=1)

_f1m1 = NetworkAddress(v4="172.18.5.106", vlan_id=2405)
_f1c1 = NetworkAddress(v4="172.18.5.100", vlan_id=2405)
_f1u1 = NetworkAddress(v4="172.18.5.103", vlan_id=2405)
_x2c1 = NetworkAddress(v4="10.57.250.148", vlan_id=1)
_x2u1 = NetworkAddress(v4="10.57.250.148", vlan_id=1)
_s1c1 = NetworkAddress(v4="10.57.250.149", vlan_id=1)
_s1u1 = NetworkAddress(v4="10.57.250.149", vlan_id=1)
_tracing1 = NetworkAddress(v4="172.18.4.101", vlan_id=1)

_cu = CU(
    backhaul_site_oam_ip="10.57.250.6",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.250.6", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.250.6", username="Nemuadmin", password="nemuuser"
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

_cu1 = CU(
    backhaul_site_oam_ip="10.57.250.12",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.250.12", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.250.12", username="Nemuadmin", password="nemuuser"
    ),
    f1m=_f1m1,
    f1c=_f1c1,
    f1u=_f1u1,
    x2c=_x2c1,
    x2u=_x2u1,
    s1c=_s1c1,
    s1u=_s1u1,
    tracing=_tracing1,
)
# cloud
_control = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.57.137.2",
        username="sqg03",
        tenant="sqg03",
        password="Nokia03!",
        port=5000,
        protocol="https",
        version="v3",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.137.2", username="sqg03", password="Nokia03!"
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="2.2.2.2", username="admin2", password="uteadmin2"
    ),
)

_compute = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(
        addr="3.3.3.3", username="admin3", password="uteadmin3"
    )
)

_control2 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.57.137.2",
        username="sqg03",
        tenant="sqg03",
        password="Nokia03!",
        port=5000,
        protocol="https",
        version="v3",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.137.2", username="sqg03", password="Nokia03!"
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="2.2.2.2", username="admin2", password="uteadmin2"
    ),
)

_compute2 = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(
        addr="3.3.3.3", username="admin3", password="uteadmin3"
    )
)
_ncir = NCIR(
    control_nodes=[_control],
    compute_nodes=[_compute],
    version="ncir_18",
    cloud_deployments=None,
)

_ncir2 = NCIR(
    control_nodes=[_control2],
    compute_nodes=[_compute2],
    version="ncir_18",
    cloud_deployments=None,
)
# #cloudbts
_cbts_flavor = DeploymentFlavorStack(
    name="sg3-tl231-flavor",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_flavor.env"),
        os.path.join(_cfg_dir, "5gbts_flavor_ci1.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="cbts_prefix",
)

_cbts_net = DeploymentNetworkStack(
    name="sg3-tl231-externetwork",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_ext_net.env"),
        os.path.join(_cfg_dir, "5gbts_ext_net_ci1.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="sg3-tl231-vnf",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_heat.env"),
        os.path.join(_cfg_dir, "5gbts_heat_ci1.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_heat.yaml"),
)

# #cloudbts2
_cbts_flavor2 = DeploymentFlavorStack(
    name="sg3-tl231-2-flavor",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_flavor.env"),
        os.path.join(_cfg_dir, "5gbts_flavor_ci2.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="cbts_prefix",
)

_cbts_net2 = DeploymentNetworkStack(
    name="sg3-tl231-2-externetwork",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_ext_net.env"),
        os.path.join(_cfg_dir, "5gbts_ext_net_ci2.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)

_cbts_vnf2 = DeploymentVnfStack(
    name="sg3-tl231-2-vnf",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_heat.env"),
        os.path.join(_cfg_dir, "5gbts_heat_ci2.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_heat.yaml"),
)

_cloud_deployment1 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)

_cloud_deployment2 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    flavors=[_cbts_flavor2],
    networks=[_cbts_net2],
    vnfs=[_cbts_vnf2],
    cloud_hosting=_ncir2,
)

_cbts = CloudBts(
    dus=[_du_0], cu=_cu, cloud_deployment=_cloud_deployment1, instance_id=231
)
_cbts1 = CloudBts(
    dus=[_du_1], cu=_cu1, cloud_deployment=_cloud_deployment2, instance_id=231 - 2
)
# #cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_cbts, _cbts1],
    cloud_hostings=[_ncir, _ncir2],
    enbs=[_lte_real_enb],
    ues=[_prisma_ue],
    attenuator=[_attenuator],
    tl_cloud_topology=_tl_cloud_topology,
)

# old version keyword under robotws5g/resource compatibility workaround
# tl = TestlineWrapper(tl)
