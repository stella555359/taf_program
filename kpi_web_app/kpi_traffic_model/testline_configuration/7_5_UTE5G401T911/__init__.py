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
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.appserver import AppServer

__maintainer__ = "Fu, Hongye"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_03_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_03@internal.nsn.com>"
)
__email__ = "hongye.fu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.127", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS
_ru_pdu = FACOM(addr="10.68.90.158", port_numbers=[2])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[2],
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.68.90.130", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.68.90.157", port_numbers=[1])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.68.90.130")

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.68.90.131", username="toor4nsn", password="oZPS0POrRieRtu"
)
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_gnb_pdu.pdu_ports[1],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb)

## switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.0.0.0", port="1/6", username="xx", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

## switch Mtor
_dell_s4048ton_ssh = SshServiceDetails(
    addr="10.0.0.0", port="1/9", username="xx", password="nokia123"
)
_dell_s4048ton_switch = DellS4048TONSwitch(_dell_s4048ton_ssh)

##CU
_cu_oam_ip = "10.57.159.14"
_f1m = NetworkAddress(v4="10.57.159.72", v6="xxxx", vlan_id="xxxx")
_f1c = NetworkAddress(v4="10.57.159.73", v6="xxxx", vlan_id="xxxx")
_f1u = NetworkAddress(v4="10.57.159.74", v6="xxxx", vlan_id="xxxx")
_x2c = NetworkAddress(v4="10.57.159.152", v6="xxxx", vlan_id="xxxx")
_x2u = NetworkAddress(v4="10.57.159.153", v6="xxxx", vlan_id="xxxx")
_s1c = NetworkAddress(v4="10.57.159.152", v6="xxxx", vlan_id="xxxx")
_s1u = NetworkAddress(v4="10.57.159.153", v6="xxxx", vlan_id="xxxx")
_tracing = NetworkAddress(v4="xxxx", v6="xxxx", vlan_id="xxxx")

_cu = CU(
    backhaul_site_oam_ip=_cu_oam_ip,
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.14", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.159.14", username="Nemuadmin", password="nemuuser"
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
        ip_addr="10.57.137.34",
        username="nokiauser",
        tenant="FiveG",
        password="NOki@890!",
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
    name="mmW-SG03-TL911-flavor",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_flavor.env"),
        os.path.join(_cfg_dir, "config_flavor_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="cbts_prefix",
)

_cbts_net = DeploymentNetworkStack(
    name="mmw-sg03-tl911_ext_net",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_ext_net_dedicate.env"),
        os.path.join(_cfg_dir, "config_ext_net_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="mmW-SG03-TL911-deploy",
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

_cbts = CloudBts(
    dus=[_du],
    cu=_cu,
    vnf_name=_cbts_vnf.name,
    instance_id=911,
    global_bts_id=911,
    cloud_deployment=_cloud_deployment,
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# epc_sim
_epc_sim = EPCSim(
    mme_ip="10.107.182.164",
    mcc=262,
    mnc=3,
    tac=6666,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.127", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    dir_path="/opt/iphy/WTS/",
    cfg_filename="epc_standalone.lua",
)

# iperf server
_appserver_ssh = SshServiceDetails(
    addr="10.70.222.51", username="mmw_sg3", password="mm@3", port="43340"
)


_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.70.222.51",
    iperf_path="/usr/bin/iperf",
    port="43429",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.70.222.51",
    iperf_path="iperf",
    port="44029",
)
_appserver = AppServer(_iperf_details_on_appserver2)


# Qualcomm UE as Android
_samsung0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.106", username="nokia5G", password="noki@123"
    ),
    # serial_number='R5CN20LYX0Y',
    serial_number="R5CN1037CHB",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=IperfDataTransferDetails(
        ssh_connection_details=_appserver_ssh,
        network_interface_address="10.70.222.51",
        iperf_path="/usr/bin/iperf",
        port="43429",
    ),
    capabilities=["REAL_ANDROID_UE4"],
)

_samsung1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.106", username="nokia5G", password="noki@123"
    ),
    # serial_number='R5CN20LYX0Y',
    serial_number="R5CN20RA45L",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=IperfDataTransferDetails(
        ssh_connection_details=_appserver_ssh,
        network_interface_address="10.70.222.51",
        iperf_path="/usr/bin/iperf",
        port="43430",
    ),
    capabilities=["REAL_ANDROID_UE3"],
)

_samsung2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.106", username="nokia5G", password="noki@123"
    ),
    # serial_number='R5CN20LYX0Y',
    serial_number="R3CN600NGGR",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=IperfDataTransferDetails(
        ssh_connection_details=_appserver_ssh,
        network_interface_address="10.70.222.51",
        iperf_path="/usr/bin/iperf",
        port="43431",
    ),
    capabilities=["REAL_ANDROID_UE2"],
)

_samsung3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.106", username="nokia5G", password="noki@123"
    ),
    # serial_number='R5CN20LYX0Y',
    serial_number="R5CN207PNJE",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=IperfDataTransferDetails(
        ssh_connection_details=_appserver_ssh,
        network_interface_address="10.70.222.51",
        iperf_path="/usr/bin/iperf",
        port="43432",
    ),
    capabilities=["REAL_ANDROID_UE1"],
)

# Qualcomm UE as Android
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.29", username="hongye.fu", password="Noki@123"
    ),
    serial_number="e4320026",
    # serial_number="88f8a21b",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python38/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=IperfDataTransferDetails(
        ssh_connection_details=_appserver_ssh,
        network_interface_address="10.70.222.51",
        iperf_path="/usr/bin/iperf",
        port="43433",
    ),
    capabilities=["REAL_ANDROID_UE0", "qct_dx50"],
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_cbts],
    enbs=[_lte_real_enb],
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
    ues=[_samsung0, _samsung1, _samsung2, _samsung3, _android],
    core=_epc_sim,
)

# tl = TestlineWrapper(tl)
