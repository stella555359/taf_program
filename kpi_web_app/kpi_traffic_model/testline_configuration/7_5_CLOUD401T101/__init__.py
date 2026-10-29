__maintainer__ = "jiajia.3.wang"
__team__ = (
    "I_MN_SRAN_TRUNK_ENGINE_SG_HZ1_GMS <I_MN_SRAN_TRUNK_ENGINE_SG_HZ1@internal.nsn.com>"
)
__email__ = "I_MN_SRAN_TRUNK_ENGINE_SG_HZ1@internal.nsn.com"
__owner_email__ = "jiajia.3.wang@nokia-sbell.com"

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
from taf.config.testline.ue import Android
from taf.config.testline import DU, RU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.radio import RadioModule
from taf.config.testline.appserver import AppServer

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.106.164.17", username="ute", password="A8CuY#6Vc^a0m4MmiT_2"
    )
)

# OSP
_control = ControlNode(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.107.8.116", username="CBTS5user", password="system123"
    ),
    open_stack_connection_details=OpenStackConnectionDetails(
        username="CBTS5user",
        password="system123",
        ip_addr="10.107.196.126",
        tenant="CBTS5",
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="osp_16")

# EPCSim
_epcsim = EPCSim(
    mme_ip=None,
    tac=None,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.106.164.17", username="ute", password="A8CuY#6Vc^a0m4MmiT_2"
    ),
    mcc="262",
    mnc="03",
    dir_path="/home/ute/WTS_4.0.12248",
    cfg_filename="TL101_S1.cfg",
    edaemon_port=None,
    egate_port=None,
)

# CU
_cu = CU(
    backhaul_site_oam_ip="10.107.169.146",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.107.169.146", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.107.169.146", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
_common_unit_pdu = FACOM(addr="10.106.211.176", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.17")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[7],
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
#

_du_0 = DU(airscale=_airscale_0, rus=[_ru], f1_m_ip_addr="192.168.255.1")

# 4G RU
_4g_ru_pdu = FACOM(addr="10.106.211.182", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_RadioModule = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    pdu_port=_4g_ru_pdu.pdu_ports[2],
)


# Real ENB
_real_enb_pdu = FACOM(addr="10.106.211.176", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_enb = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.108.233.106", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[8],
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
    name="hgz-tl101_flavor",
    env_files=_flavor_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="hgz-tl101",
)

_cbts_net = DeploymentNetworkStack(
    name="EXT_NET",
    env_files=_net_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="HGZ-TL101-STACK",
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
    dus=[_du_0], cu=_cu, cloud_deployment=_cloud_deployment, vnf_name="hgz-tl101"
)


#########appserver##########
_appserver_ssh = SshServiceDetails(
    addr="10.106.164.17", username="ute", password="A8CuY#6Vc^a0m4MmiT_2"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.106.164.17",
    iperf_path="iperf",
    port=50200,
)

_appserver = AppServer(_iperf_details_on_appserver)

#########UE##########
_iperf_data_transfer = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.106.164.17", username="ute", password="A8CuY#6Vc^a0m4MmiT_2"
    ),
    network_interface_address="10.106.164.17",
    port=53200,
    iperf_path="/usr/bin/iperf",
)

_appserver = AppServer(_iperf_details_on_appserver)

_askey = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.108.135.98", username="tester5g", password="Nokia123!"
    ),
    serial_number="80253651",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_data_transfer,
    capabilities=["askey"],
)

_askey.ue_type = "askey"

# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_lte_real_enb],
    core=_epcsim,
    ues=[_askey],
    appserver=_appserver,
    tl_cloud_topology="hgz-tl101",
)

__all__ = ["tl"]
