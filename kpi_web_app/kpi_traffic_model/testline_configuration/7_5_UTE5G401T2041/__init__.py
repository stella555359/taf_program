__maintainer__ = "Xu, Echo"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05@internal.nsn.com"  # TL owner's team
__email__ = "echo.xu@nokia-sbell.com"

import os
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
)
from taf.config.testline.testline import TestLine
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
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.appserver import AppServer
from taf.config.testline.attenuator import (
    AttenuationPort,
    RadioRack,
)  # added in taf.meta 5.4

__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_attenuator = RadioRack(
    ip_addr="10.57.238.18", port="23", attenuation_port_numbers=[1, 2, 3, 4]
)

_ru_pdu = FACOM(addr="10.71.197.102", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru = RU(
    ru_hw_group="Below6GHZ",  # Above6GHZ or Below6GHZ
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[8],
    radio_type=RadioTypes.AEWB,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)
#########5G_gNB_Start##########

_gnb_pdu = FACOM(addr="10.71.197.102", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_capacity_unit = CapacityUnit(addr="192.168.253.18")
_capacity_unit2 = CapacityUnit(addr="192.168.253.16")
_common_unit_0 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.215.234", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit, _capacity_unit2],
    pdu_port=_gnb_pdu.pdu_ports[7],
)
_airscale = Airscale(common_units=[_common_unit_0])

#########CU##########
_cu_oam_ip = "10.57.250.5"
_f1m = NetworkAddress(v4="10.10.10.10", v6="xxxx", vlan_id="xxxx")
_f1c = NetworkAddress(v4="10.57.250.42", v6="xxxx", vlan_id="xxxx")
_f1u = NetworkAddress(v4="10.57.250.43", v6="xxxx", vlan_id="xxxx")
_x2c = NetworkAddress(v4="10.57.250.74", v6="xxxx", vlan_id="xxxx")
_x2u = NetworkAddress(v4="10.57.250.75", v6="xxxx", vlan_id="xxxx")
_s1c = NetworkAddress(v4="10.57.250.74", v6="xxxx", vlan_id="xxxx")
_s1u = NetworkAddress(v4="10.57.250.75", v6="xxxx", vlan_id="xxxx")
_tracing = NetworkAddress(v4="xxxx", v6="xxxx", vlan_id="xxxx")


_cu = CU(
    backhaul_site_oam_ip=_cu_oam_ip,
    oam_ssh_connection_details=SshServiceDetails(
        addr=_cu_oam_ip, username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr=_cu_oam_ip, username="Nemuadmin", password="nemuuser"
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
        username="nokiauser",
        tenant="FiveG",
        password="NOki@456!",
        port=5000,
        protocol="https",
        version="v3",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.137.2", username="nokiauser", password="HZnoki@123!"
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="5.5.5.5", username="admin", password="admin"
    ),
)

_ncir = NCIR(
    compute_nodes=[],
    control_nodes=[_control],
    version="ncir_18",
    cloud_deployments=None,
)

# #cloudbts
_cbts_flavor = DeploymentFlavorStack(
    name="mmw5-tl2041-flavor",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_flavor.env"),
        os.path.join(_cfg_dir, "config_flavor_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="cbts_prefix",
)

_cbts_net = DeploymentNetworkStack(
    name="mmw5-tl2041_ext_net",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_ext_net.env"),
        os.path.join(_cfg_dir, "config_ext_net_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="mmw5-tl2041-vnf",
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

_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.71.215.234")

_cbts = CloudBts(
    dus=[_du], cu=_cu, vnf_name=_cbts_vnf.name, cloud_deployment=_cloud_deployment
)

# #cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"


#########5G_gNB_Stop##########

#########4G_eNB_Start##########
_real_enb_pdu = FACOM(addr="10.71.197.102", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.215.235", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[6],
)

_real_enb = Airscale(common_units=[_common_unit_2])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)
#########4G_eNB_Stop##########

#########Testpc##########
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.188", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


########LteEmu##########
_lteemu = LTEEmuCore(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.238.5", username="nokia", password="nokia123"
    ),
    dir_path="/home/nokia/LTEemu_core2_64_3252",
    cfg_filename="basic_wts_step1.cfg",
    mme_ip="",
    edaemon_port="22222",
    egate_port="9880",
)


_appserver_ssh = SshServiceDetails(
    addr="10.70.222.54", username="mmw_sg5", password="mm@5", port="42333"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.70.222.54",
    iperf_path="/usr/bin/iperf",
    port="45333",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.70.222.54",
    iperf_path="iperf",
    port="46333",
)
_appserver = AppServer(_iperf_details_on_appserver2)

# CI_Detail_UE_Type='Samsung'

_qualcomm = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.47", username="nokia5G", password="noki@123"
    ),
    serial_number="RFCR10X4W5A",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung"],
)

# Testline
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_lte_real_enb],
    core=_lteemu,
    # attenuator=_attenuator,
    tl_cloud_topology="",
    appserver=_appserver,
    ues=[_qualcomm],
)

# print tl.gnbs[0].dus[0].airscale.common_units[0].capacity_units[1].addr
