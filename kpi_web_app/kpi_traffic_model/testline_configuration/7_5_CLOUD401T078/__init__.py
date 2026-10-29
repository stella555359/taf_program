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
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500
from taf.config.testline import (
    Enb,
    SimEnb,
    RealEnb,
    RadioModule,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper

__maintainer__ = "Yu Shaojie"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_6_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "shaojie.yu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.109", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


# #Cobham
# _tm500 = TM500(
#     tma_host=SshServiceDetails(addr='9.9.9.9', username='user', password='pass'),
#     tma_command_port=30000,
#     pdu_port=None)


# #Prisma
_airmosaic_ssh = SshServiceDetails(
    addr="10.57.249.82", username="CNHZ5GRAN1112+tester", password="nokia123"
)

_airmosaic_harness = HttpConnectionDetails(addr="10.57.249.82", port=8090)

_lsu_uu_ssh = SshServiceDetails(addr="10.57.249.83", username="user", password="user")

_tstm_uu_ssh = SshServiceDetails(addr="10.57.249.83", username="user", password="user")

_prisma_ue = Prisma(
    airmosaic_ssh_connection_details=_airmosaic_ssh,
    airmosaic_harness_connection_details=_airmosaic_harness,
    lsu_uu_ssh_connection_details=_lsu_uu_ssh,
    tstm_uu_ssh_connection_details=_tstm_uu_ssh,
)


# #RealEnb
_real_enb_pdu = FACOM(addr="10.57.242.15", port_numbers=[4])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[4],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)


# #5GRU_0 for cloudBTS
_ru_0_pdu = FACOM(addr="5.5.5.5", port_numbers=[3])

_ru_0 = RU(
    ru_hw_group="Above6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    pdu_port=_ru_0_pdu.pdu_ports[3],
    radio_type="AEUD",
)

# #DU_0 for cloudlBTS
_lmp_connection_9 = SshServiceDetails(
    addr="10.57.231.246", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_9 = CapacityUnit(addr="192.168.253.20")

_du_0_pdu = FACOM(addr="10.57.242.15", port_numbers=[3])

_common_unit_9 = CommonUnit(
    lmp_connection=_lmp_connection_9,
    capacity_units=[_capacity_unit_9],
    pdu_port=_du_0_pdu.pdu_ports[3],
)

_airscale_0 = Airscale(common_units=[_common_unit_9])

_du_0 = DU(airscale=_airscale_0, rus=[_ru_0])


# #5GRU_1 for cloudBTS
_ru_1_pdu = FACOM(addr="5.5.5.5", port_numbers=[3])

_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_1_pdu.pdu_ports[3],
)

# #DU_1 for cloudlBTS
_lmp_connection_8 = SshServiceDetails(
    addr="5.5.5.5", username="user5", password="password5"
)

_capacity_unit_8 = CapacityUnit(addr="6.6.6.6")

_du_1_pdu = FACOM(addr="5.5.5.5", port_numbers=[3])

_common_unit_8 = CommonUnit(
    lmp_connection=_lmp_connection_8,
    capacity_units=[_capacity_unit_8],
    pdu_port=_du_1_pdu.pdu_ports[3],
)

_airscale_1 = Airscale(common_units=[_common_unit_8])

_du_1 = DU(airscale=_airscale_1, rus=[_ru_1])


# #CU
_cu = CU(
    backhaul_site_oam_ip="10.57.157.133",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.133", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.157.133", username="Nemuadmin", password="nemuuser"
    ),
)

# cloud
_control = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="1.1.1.1", username="admin", tenant="admin", password="uteadmin"
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="admin7", password="uteadmin7"
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="5.5.5.5", username="admin", password="admin"
    ),
)

_ncir = NCIR(
    compute_nodes=[],
    control_nodes=[_control],
    version="ncir_17a",
    cloud_deployments=None,
)

# #cloudbts
_cbts_flavor = DeploymentFlavorStack(
    name="cbtsflavor",
    env_files=[os.path.join(_cfg_dir, "config_flavor.env")],
    yaml_file=os.path.join(_cfg_dir, "config_flavor.yaml"),
    default_vnf_prefix="cbts_prefix",
)

_cbts_net = DeploymentNetworkStack(
    name="ext_net",
    env_files=[os.path.join(_cfg_dir, "config_ext_net.env")],
    yaml_file=os.path.join(_cfg_dir, "config_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="cbts_deploy",
    env_files=[os.path.join(_cfg_dir, "config_bts.env")],
    yaml_file=os.path.join(_cfg_dir, "config_bts.yaml"),
)

_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)

_cbts = CloudBts(dus=[_du_0, _du_1], cu=_cu, cloud_deployment=_cloud_deployment)

# #cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"


# switch
_dell_s4048on_ssh = SshServiceDetails(
    addr="1.0.0.1", port=44444, username="user", password="pass"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

tl = TestLine(
    test_pc=_host,
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    enbs=[_lte_real_enb],
    ues=[_prisma_ue],
    tl_cloud_topology=_tl_cloud_topology,
)

# old version keyword under robotws5g/resource compatibility workaround
# tl = TestlineWrapper(tl)
