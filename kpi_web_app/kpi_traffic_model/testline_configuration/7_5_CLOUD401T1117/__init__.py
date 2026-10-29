__maintainer__ = "penghang chen "
__team__ = "I_MN_5G_RAN_IV4_QT_HZG_GMS <I_MN_5G_RAN_IV4_QT_HZG@internal.nsn.com>"
__email__ = "I_MN_5G_RAN_IV4_QT_HZG@internal.nsn.com"
__owner_email__ = "zheng.du@nokia-sbell.com"

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
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import HBTE
from taf.config.testline.lab_infrastructure import PxeServer
from taf.config.testline.connection_details import K8SConnectionDetails
from taf.config.testline.cloud_hosting import MasterNode, K8S
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU
from taf.config.testline.enb import RealEnb
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import RU, RadioModule
from taf.config.testline.appserver import AppServer
from taf.config.testline.core import EPCSim

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.69.9.49", username="ute", password="A8CuY#6Vc^a0m4MmiT_2"
    )
)

# OSP
_control = ControlNode(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.137.74", username="root", password="root"
    ),
    open_stack_connection_details=OpenStackConnectionDetails(
        username="root",
        password="root",
        ip_addr="10.57.137.74",
        tenant="cran6",
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="ncir_19")

# EPCSim
_epcsim = EPCSim(
    mme_ip=None,
    tac=None,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.69.9.49", username="ute", password="A8CuY#6Vc^a0m4MmiT_2"
    ),
    mcc="262",
    mnc="03",
    dir_path="/opt/iphy/DEC_WTS_4.0.4696",
    cfg_filename="LRC_realgNB_cobham.cfg",
    edaemon_port=None,
    egate_port=None,
)

# CU
_cu = CU(
    backhaul_site_oam_ip="10.107.169.147",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.107.110.133", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.107.110.133", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
_common_unit_pdu = HBTE(addr="10.69.69.136", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_lmp_connection_0 = SshServiceDetails(
    addr="10.56.109.122", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.17")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[1],
)

# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])

# 5G RU
_ru_pdu = HBTE(addr="10.69.69.136", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.10.41", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.10.41", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
)
# attenuator
_attenuator = AHBTE(
    ip_addr="10.106.211.141",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

_du_0 = DU(airscale=_airscale_0, rus=[_ru], f1_m_ip_addr="10.56.109.122")

# 4G RU
_4g_ru_pdu = HBTE(addr="10.106.254.49", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_RadioModule = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="umniedziala"
    ),
    pdu_port=_4g_ru_pdu.pdu_ports[6],
)


# CloudBts
_flavor_env_files = [os.path.join(_cfg_dir, "5gbts_flavor.env")]

_net_env_files = [os.path.join(_cfg_dir, "5gbts_ext_net.env")]

_vnf_env_files = [
    os.path.join(_cfg_dir, "5gbts_heat.env"),
    os.path.join(_cfg_dir, "5gbts_heat_qt.env"),
]

_cbts_flavor = DeploymentFlavorStack(
    name="hgz-tl1117_flavor",
    env_files=_flavor_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="hgz-tl1117",
)

_cbts_net = DeploymentNetworkStack(
    name="hgz-tl1117-BH-FH",
    env_files=_net_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="hgz-tl1117-STACK",
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
    dus=[_du_0],
    cu=_cu,
    cloud_deployment=_cloud_deployment,
    vnf_name="hgz-tl1117",
    instance_id="1",
    global_bts_id="1",
)
#########UE##########
_qualcomm_pdu = HBTE(addr="1.1.1.1", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_iperf_data_transfer = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.69.9.49", username="ute", password="A8CuY#6Vc^a0m4MmiT_2"
    ),
    network_interface_address="10.69.9.49",
    iperf_path="/usr/bin/iperf",
)

_huawei = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.69.69.135", username="QT-tester", password="Nokia123!"
    ),
    serial_number="9YS0220813024727",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_data_transfer,
    capabilities=["huawei"],
)

_huawei.ue_type = "huawei"
#########app server#########
_appserver_ssh = SshServiceDetails(
    addr="10.69.9.49", username="ute", password="A8CuY#6Vc^a0m4MmiT_2"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.69.9.49",
    iperf_path="iperf",
    port=5023,
)

_appserver = AppServer(_iperf_details_on_appserver)

# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    core=_epcsim,
    ues=[_huawei],
    attenuator=_attenuator,
    tl_cloud_topology="hgz-tl1117",
    appserver=_appserver,
)

__all__ = ["tl"]
