__maintainer__ = "Fan kongshuai"
__team__ = "I_MN_5G_RAN_IV4_QT_HZG_GMS <I_MN_5G_RAN_IV4_QT_HZG@internal.nsn.com>"
__email__ = "I_MN_5G_RAN_IV4_QT_HZG@internal.nsn.com"
__owner_email__ = "kongshuai.fan@nokia-sbell.com"

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
from taf.config.testline.core import EPCSim
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU
from taf.config.testline.enb import RealEnb
from taf.config.testline.ue import TM500
from taf.config.testline import DU, RU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.radio import RadioModule
from taf.config.testline.appserver import AppServer
from taf.config.testline.attenuator import AttenuationPort, HBTE

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.183.101", username="root", password="nokia123"
    )
)

# OSP
_control = ControlNode(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.107.99.12", username="stack", password="nokia123"
    ),
    open_stack_connection_details=OpenStackConnectionDetails(
        username="admin", password="system123", ip_addr="10.107.99.2", tenant="admin"
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="osp_16")

# EPCSim
_epcsim = EPCSim(
    mme_ip=None,
    tac=None,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.183.101", username="nokia", password="nokia123"
    ),
    mcc="262",
    mnc="03",
    dir_path="/home/ute/WTS_4.0.12248",
    cfg_filename="LRC_realgNB_cobham_new.cfg",
    edaemon_port=None,
    egate_port=None,
)

# CU
_cu = CU(
    backhaul_site_oam_ip="10.107.96.2",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.107.96.2", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.107.96.2", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
_common_unit_pdu = FACOM(addr="10.57.242.11", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_lmp_connection_0 = SshServiceDetails(
    addr="10.57.231.172", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.17")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[5],
)

# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])

# 5G RU
_ru_pdu = FACOM(addr="10.57.243.10", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[8],
)
# attenuator
_attenuator = HBTE(
    ip_addr="10.106.211.141",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

_du_0 = DU(airscale=_airscale_0, rus=[_ru], f1_m_ip_addr="10.57.223.172")

# 4G RU
_4g_ru_pdu = FACOM(addr="10.57.243.6", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_RadioModule = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    pdu_port=_4g_ru_pdu.pdu_ports[4],
)


# Real ENB
_real_enb_pdu = FACOM(addr="10.57.241.141", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_enb = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.235.100", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[3],
    hardware_type="ASIA",
    hardware_version="A.103",
)

_real_enb = Airscale(common_units=[_common_unit_enb])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=[_RadioModule])
#

# CloudBts
_flavor_env_files = [os.path.join(_cfg_dir, "5gbts_flavor.env")]

_net_env_files = [os.path.join(_cfg_dir, "5gbts_ext_net.env")]

_vnf_env_files = [
    os.path.join(_cfg_dir, "5gbts_heat.env"),
    os.path.join(_cfg_dir, "5gbts_heat_qt.env"),
]

_cbts_flavor = DeploymentFlavorStack(
    name="hgz-tl109_flavor",
    env_files=_flavor_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="hgz-tl109",
)

_cbts_net = DeploymentNetworkStack(
    name="EXT_NET",
    env_files=_net_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="HGZ-TL109-STACK",
    env_files=_vnf_env_files,
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
    dus=[_du_0], cu=_cu, cloud_deployment=_cloud_deployment, vnf_name="hgz-tl109"
)

#########UE##########
_appserver_ssh = SshServiceDetails(
    addr="10.108.183.101", username="root", password="nokia123"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.108.183.101",
    iperf_path="iperf",
    port=5411,
)

_appserver = AppServer(_iperf_details_on_appserver)

_iperf_data_transfer = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.106.164.55", username="root", password="uteadmin"
    ),
    network_interface_address="10.106.164.55",
    iperf_path="/usr/bin/iperf",
    port=59995,
)

_cobham = TM500(
    tma_host=SshServiceDetails(
        addr="10.57.243.157", username="CNHZ5GRAN1241+tester", password="tester123"
    ),
    tma_command_port=5004,
    tma_path=(
        r"C:\\Program Files (x86)\\Aeroflex\\TM500\\5G NR - NLA 4.23.0"
        r"\\Test Mobile Application\\TmaApplication.exe"
    ),
    iperf_details=_iperf_data_transfer,
)
_cobham.ue_type = "viavi"

# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_lte_real_enb],
    core=_epcsim,
    ues=[_cobham],
    appserver=_appserver,
    attenuator=_attenuator,
    tl_cloud_topology="hgz-tl109",
)

__all__ = ["tl"]
