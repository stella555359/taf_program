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
from taf.config.testline.core import (
    EPCSim,
    LTEEmuCore,
    PrismaCore,
    RealCore4G,
    RealCore5G,
)
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
from taf.config.testline.optical_switch import Leoni
from taf.config.testline.appserver import AppServer

__maintainer__ = "Wu Xu"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_3_GMS <I_MN_5G_RAN_IV4_LINE_HZG_3@internal.nsn.com>"
)
__email__ = "xu.wu@nokia-sbell.com"

# common
__all__ = ["tl"]

PARAMS_TO_MODIFY_TL = [
    dict(
        value="10.57.229.40",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-4/IPNO-1/IPIF-1/IPADDRESSV4-1",
        p_name="localIpAddr",
    ),
    dict(
        value="10.57.229.40",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-4/IPNO-1/IPIF-1/IPADDRESSV4-2",
        p_name="localIpAddr",
    ),
    dict(
        value="10.57.229.40",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-4/IPNO-1/IPIF-1/IPADDRESSV4-3",
        p_name="localIpAddr",
    ),
    dict(
        value="27",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-4/IPNO-1/IPIF-1/IPADDRESSV4-1",
        p_name="localIpPrefixLength",
    ),
    dict(
        value="27",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-4/IPNO-1/IPIF-1/IPADDRESSV4-2",
        p_name="localIpPrefixLength",
    ),
    dict(
        value="27",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-4/IPNO-1/IPIF-1/IPADDRESSV4-3",
        p_name="localIpPrefixLength",
    ),
    # dict(value='MRBTS-1900/TNLSVC-1/TNL-4/IPNO-1/IPIF-1/IPADDRESSV4-1' dist_name='MRBTS-1900/NRBTS-1/NRDU-1', list_name='f1Cplane', p_name='ipV4AddressDN1'),
    dict(
        value="MRBTS-1900/TNLSVC-1/TNL-4/IPNO-1/IPIF-1/IPADDRESSV4-1",
        dist_name="MRBTS-1900/NRBTS-1/NRDU-1",
        list_name="f1Mplane",
        p_name="ipV4AddressDN1",
    ),
    dict(
        value="MRBTS-1900/TNLSVC-1/TNL-4/IPNO-1/IPIF-1/IPADDRESSV4-1",
        dist_name="MRBTS-1900/NRBTS-1/NRDU-1",
        list_name="f1Uplane",
        p_name="ipV4AddressDN1",
    ),
]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))


# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.120", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.163.34", username="root", password="nokia123"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.34",
    iperf_path="iperf",
    port=53410,
)

_appserver = AppServer(iperf_details=_iperf_details_on_appserver)

_iperf_details_on_ue = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="9.6.6.6",
    iperf_path="/cygdrive/d/tools/iperf",
    port=53411,
)


# #Cobham
_tm500 = TM500(
    tma_host=SshServiceDetails(
        addr="10.57.130.29", username="tester", password="tester123"
    ),
    tma_command_port=5030,
    pdu_port=None,
    iperf_details=_iperf_details_on_ue,
    tma_path="/cygdrive/d/NLA4.22.0/TM500_NR_5G_EXT-MUE_Release_NLA_4_22_0/Test Mobile Application/TmaApplication.exe",
)


# #RealEnb
_real_enb_pdu = FACOM(addr="10.57.241.169", port_numbers=[1, 2, 3, 4, 5, 6])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.229.39", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[5],
)

_common_unit_3 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.229.41", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[5],
)

_real_enb = Airscale(common_units=[_common_unit_2, _common_unit_3])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None, instance_id=34)

# PA
_attenuator = TopYoung(
    ip_addr="10.57.246.249",
    port=3000,
    attenuation_port_numbers=[1, 2, 3, 4],
    model="TAS16T16-51-120-1SDES",
)

# #5GRU_0 for cloudBTS
_ru_0_pdu = FACOM(addr="10.57.246.237", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_0 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    pdu_port=_ru_0_pdu.pdu_ports[4],
    radio_type="AEUA",
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

# #DU_0 for cloudlBTS
_lmp_connection_9 = SshServiceDetails(
    addr="10.57.229.40", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_9 = CapacityUnit(addr="192.168.253.20")

_du_0_pdu = FACOM(addr="10.57.241.169", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_9 = CommonUnit(
    lmp_connection=_lmp_connection_9,
    capacity_units=[_capacity_unit_9],
    pdu_port=_du_0_pdu.pdu_ports[5],
)

_airscale_0 = Airscale(common_units=[_common_unit_9])

_du_0 = DU(
    airscale=_airscale_0,
    rus=[_ru_0],
    f1_m_ip_addr=NetworkAddress(v4="10.57.229.40"),
    f1_c_ip_addr=NetworkAddress(v4="10.57.229.40"),
    f1_u_ip_addr=NetworkAddress(v4="10.57.229.40"),
)


# #CU

_f1m = NetworkAddress(v4="10.57.250.66", vlan_id=2403)
_f1c = NetworkAddress(v4="10.57.250.67", vlan_id=2403)
_f1u = NetworkAddress(v4="10.57.250.68", vlan_id=2403)
_x2c = NetworkAddress(v4="10.57.250.142", vlan_id=1)
_x2u = NetworkAddress(v4="10.57.250.143", vlan_id=1)
_s1c = NetworkAddress(v4="10.57.250.142", vlan_id=1)
_s1u = NetworkAddress(v4="10.57.250.143", vlan_id=1)
_tracing = NetworkAddress(v4="172.18.4.101", vlan_id=1)

_cu = CU(
    backhaul_site_oam_ip="10.57.250.8",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.250.8", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.250.8", username="Nemuadmin", password="nemuuser"
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

_osp = OSP(
    control_nodes=[_control],
    compute_nodes=[_compute],
    version="None",
    cloud_deployments=None,
)

_ncir = NCIR(
    control_nodes=[_control],
    compute_nodes=[_compute],
    version="ncir_18",
    cloud_deployments=None,
)

# #cloudbts
_cbts_flavor = DeploymentFlavorStack(
    name="sq3-tl34-flavor",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_flavor.env"),
        os.path.join(_cfg_dir, "5gbts_flavor_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="cbts_prefix",
)

_cbts_net = DeploymentNetworkStack(
    name="sq3-tl34-extnet",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_ext_net.env"),
        os.path.join(_cfg_dir, "5gbts_ext_net_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="sq3-tl34-vnf",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_heat.env"),
        os.path.join(_cfg_dir, "5gbts_heat_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_heat.yaml"),
)

_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)

_cbts = CloudBts(dus=[_du_0], cu=_cu, cloud_deployment=_cloud_deployment)

# #cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"


tl = TestLine(
    test_pc=_host,
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    enbs=[_lte_real_enb],
    ues=[_tm500],
    attenuator=[_attenuator],
    tl_cloud_topology=_tl_cloud_topology,
)
