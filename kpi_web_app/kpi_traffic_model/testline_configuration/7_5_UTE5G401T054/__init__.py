import os
import yaml
import re
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
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.compatibility.configuration import TestlineWrapper

# added in taf.meta 5.4
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.appserver import AppServer
from taf.config.testline.gnb.du import FHGW
from taf.config.testline.gnb.du import VDU
from taf.config.testline.core import RealCore, PCF
from taf.config.testline.gnb.du import Cablink, Endpoint

__maintainer__ = "Wang Yixiang"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_01@internal.nsn.com"
__email__ = "yixiang.x.wang@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))


# host for light weight CI
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.9", username="ute", password="ute"
    )
)

# for ute cloud
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.161.71", username="ute", password="uteUTE!"
    )
)

# Appserver/UL ports
_appserver_ssh = SshServiceDetails(
    addr="10.57.162.4", username="mmw_sg1", password="mm@1", port="41035"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.4",
    iperf_path="iperf",
    port="41090",
    ports=[
        "41090",
        "46090",
        "47090",
        "49090",
        "45090",
        "40090",
        "51090",
        "56090",
        "57090",
        "59090",
        "55090",
        "50090",
    ],
)

_appserver = AppServer(_iperf_details_on_appserver)

# #UE1
# DL ports
_iperf_0 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.4",
    iperf_path="/cygdrive/c/iperf",
    port="41091",
    ports=["46091", "47091", "49091", "45091", "40091"],
)

# CI_Detail_UE_Type='Samsung;Samsung'
_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.56.18.142", username="nokia5G", password="noki@123"
    ),
    serial_number="R5CN214HPBD",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_0,
    capabilities=["REAL_ANDROID_UE", "samsung"],
)
# #UE1

# #UE2
# DL ports
_iperf_1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.4",
    iperf_path="/cygdrive/c/iperf",
    port="51091",
    ports=["56091", "57091", "59091", "55091", "50091"],
)

_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.56.18.142", username="nokia5G", password="noki@123"
    ),
    serial_number="R5CN2138YHL",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_1,
    capabilities=["REAL_ANDROID_UE", "samsung"],
)
# #UE2


# RealEnb---------------------------------------------------------
_real_enb_pdu = HBTE(addr="10.56.18.177", port_numbers=[5])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.56.18.141", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[5],
)

_real_enb = Airscale(common_units=[_common_unit_2])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None, instance_id=54, global_bts_id=54)

# 5GRU------------------------------------
# add 2 more 5g ru info
# ru_hw_group: Above6GHZ or Below6GHZ
_ru1_pdu = HBTE(addr="10.56.18.174", port_numbers=[7])

_ru1 = RU(
    ru_hw_group="Above6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru1_pdu.pdu_ports[7],
    radio_type=RadioTypes.AEUB,
)

# #DU
_lmp_connection = SshServiceDetails(
    addr="10.56.18.140", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.56.18.177", port_numbers=[5])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru1, label="SFP", port_id=1),
    ),
]
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du0 = DU(
    airscale=_airscale, rus=[_ru1], f1_m_ip_addr="10.56.18.140", cablinks=_ru_cablinks
)

# CU
_f1m = NetworkAddress(v4="10.57.173.6", v6="xxxx", vlan_id=None)
_f1c = NetworkAddress(v4="10.57.173.72", v6="xxxx", vlan_id=None)
_f1u = NetworkAddress(v4="10.57.173.73", v6="xxxx", vlan_id=None)
_x2c = NetworkAddress(v4="10.57.173.138", v6="xxxx", vlan_id=None)
_x2u = NetworkAddress(v4="10.57.173.139", v6="xxxx", vlan_id=None)
_s1c = NetworkAddress(v4="xxxx", v6="xxxx", vlan_id="None")
_s1u = NetworkAddress(v4="10.57.173.139", v6="xxxx", vlan_id=None)
_tracing = NetworkAddress(v4="xxxx", v6="xxxx", vlan_id=None)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.173.6", vlan_id=None),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.173.6", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.173.6", username="Nemuadmin", password="nemuuser"
    ),
    f1m=_f1m,
    f1c=_f1c,
    f1u=_f1u,
    x2c=_x2c,
    x2u=_x2u,
    s1c=_s1c,
    s1u=_s1u,
    tracing=_tracing,
    instance_id=54,
    global_bts_id=54,
)

# cloudbts-----------------------------------------------------
# NCIR
_control = ControlNode(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.137.90", username="nokiauser", password="HZnoki@123!"
    ),
    open_stack_connection_details=OpenStackConnectionDetails(
        username="nokiauser",
        password="NOki@234!",
        ip_addr="10.57.137.90",
        tenant="FiveG",
        port=5000,
        protocol="https",
        version="v3",
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="5.5.5.5", username="admin", password="admin"
    ),
)

_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="ncir_19")

_cbts_flavor = DeploymentFlavorStack(
    name="tl054_flavor",
    env_files=[
        #        os.path.join(_cfg_dir, "5gbts_flavor.env"),
        os.path.join(_cfg_dir, "config_flavor_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="mmw01-tl054",
)

_cbts_net = DeploymentNetworkStack(
    name="mmw01-tl054_net",
    env_files=[
        # os.path.join(_cfg_dir, "5gbts_ext_net.env"),
        os.path.join(_cfg_dir, "config_ext_net_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="mmw01-tl054_vnf",
    env_files=[
        # os.path.join(_cfg_dir, "5gbts_heat.env"),
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
    dus=[_du0],
    cu=_cu,
    cloud_deployment=_cloud_deployment,
    vnf_name="mmw01-tl054_vnf",
    instance_id=54,
    global_bts_id=54,
)
# RealCore
_pcf = PCF(
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.56.18.142", username="nokia5G", password="noki@123"
    )
)
_realcore = RealCore(pcf=_pcf)
# #cloud_topology for lightwight CI------------------------------------------------
# _tl_cloud_topology = "CLOUD_5G_BB3"

# cloud_topology for UTE CLOUD
_tl_cloud_topology = "CLOUD_5G_2xANDROID_ASIKL_ABILB1_AEWB"

tl = TestLine(
    test_pc=_host,
    enbs=[_lte_real_enb],
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    ues=[_android_0, _android_1],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_host],
    appserver=_appserver,
    core=_realcore,
)

# tl = TestlineWrapper(tl)


# Example for topyoung attenuator part
# print tl.gnbs[0].global_bts_id
# print tl.gnbs[0].dus[0].rus[0].attenuation_ports[0].port_no
# print tl.gnbs[0].dus[0].rus[0].attenuation_ports[1].port_no
# print tl.gnbs[0].dus[0].rus[0].attenuation_ports[2].port_no
# print tl.gnbs[0].dus[0].rus[0].attenuation_ports[3].port_no
# i print tl.gnbs[0].dus[0].rus[0].attenuation_ports[2].port_no
# print tl.gnbs[0].dus[0].rus[0].attenuation_ports[3].port_no
# print tl.gnbs[0].dus[0].rus[0].radio_type.value
