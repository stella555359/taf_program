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
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch

# added in taf.meta 5.4
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

__maintainer__ = "Guo Zhenzhen"
__team__ = "I_MN_E2ECLOUDS_CRANSOLRDP_CN_CLOUDRAN6_PHOENIX@internal.nsn.com"
__email__ = "zhenzhen.guo@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.135", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


# RealEnb
_real_enb_pdu = FACOM(addr="10.68.87.98", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.68.88.228", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[3],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)


# #5GRU_0 for cloudBTS
_ru_pdu = FACOM(addr="10.68.87.101", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.81", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[4],
    radio_type="AEUB",
)
# 5GRU_1
# WL07
_ru1_pdu = FACOM(addr="10.57.249.6", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[3],
    radio_type="AEUB",
)
# 5GRU_2
# WL08
_ru2_pdu = FACOM(addr="10.57.152.210", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru2 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.113", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[6],
    radio_type="AEUB",
)

# #DU_0 for cloudlBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.68.88.239", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.26")
_capacity_unit_1 = CapacityUnit(addr="192.168.253.22")
_capacity_unit_2 = CapacityUnit(addr="192.168.253.30")

_du_pdu = FACOM(addr="10.57.241.199", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0, _capacity_unit_1, _capacity_unit_2],
    pdu_port=_du_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru, _ru1, _ru2], f1_m_ip_addr="10.68.88.239")


# #CU

_f1m = NetworkAddress(v4="10.110.176.102", v6="xxxx", vlan_id="xxxx")
_f1c = NetworkAddress(v4="10.110.176.103", v6="xxxx", vlan_id="xxxx")
_f1u = NetworkAddress(v4="10.110.176.104", v6="xxxx", vlan_id="xxxx")
_x2c = NetworkAddress(v4="10.110.176.154", v6="xxxx", vlan_id="xxxx")
_x2u = NetworkAddress(v4="10.110.176.155", v6="xxxx", vlan_id="xxxx")
_s1c = NetworkAddress(v4="10.110.176.154", v6="xxxx", vlan_id="xxxx")
_s1u = NetworkAddress(v4="10.110.176.155", v6="xxxx", vlan_id="xxxx")
_tracing = NetworkAddress(v4="xxxx", v6="xxxx", vlan_id="xxxx")

_cu = CU(
    backhaul_site_oam_ip="10.110.176.15",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.110.176.15", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.110.176.15", username="Nemuadmin", password="nemuuser"
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
        ip_addr="10.110.8.244",
        username="admin",
        tenant="admin",
        password="HZnokia123!",
        port=5000,
        protocol="https",
        version="v3",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.8.244", username="sqg07", password="Nokia07!"
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
    name="sg03-tl916",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_flavor.env"),
        os.path.join(_cfg_dir, "config_flavor_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="cbts_prefix",
)

_cbts_net = DeploymentNetworkStack(
    name="tl916_ext_net",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_ext_net.env"),
        os.path.join(_cfg_dir, "config_ext_net_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="sg03-tl916",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_heat.env"),
        os.path.join(_cfg_dir, "config_bts_ci.env"),
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

_cbts = CloudBts(dus=[_du], cu=_cu, cloud_deployment=_cloud_deployment)

# #######Cobham########
_iperf_details = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.162.2", username="mmw_sg2", password="mm@2"
    ),
    network_interface_address="192.168.10.70",
    iperf_path=None,
    port=42122,
)

_tm500 = TM500(
    tma_host=SshServiceDetails(
        addr="10.57.161.6",
        username="nokia5G",
        password="noki@123",
        private_key="CNHZ5GRAN1366",
    ),
    tma_command_port=5030,
    pdu_port=None,
    iperf_details=_iperf_details,
    tma_path="/cygdrive/c/Program Files (x86)/Aeroflex/TM500/5G NR - NLA 4.25.0/Test Mobile Application/TMA.exe",
)

# #cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    ues=[_tm500],
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
)
