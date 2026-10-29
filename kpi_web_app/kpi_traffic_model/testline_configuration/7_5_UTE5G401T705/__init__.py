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
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)  # added in taf.meta.5.4
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import HBTE, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
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

__maintainer__ = "Wang Debbie"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04@internal.nsn.com"
)
__email__ = "wang.Debbie@nokia-sbell.com"


PARAMS_TO_MODIFY_TL = [
    dict(
        value="10.68.90.130",
        dist_name="MRBTS-701/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-1",
        p_name="localIpAddr",
    ),
]

LIST_ITEM_TO_ADD_TL = [
    dict(
        dist_name="MRBTS-701/MNL-1/MNLENT-1/SYNC-1/CLOCK-1/TOP-1/TOPP-1",
        list_name="topMasterList",
        elements={
            "localPriority": "128",
            "masterIpAddr": "10.57.249.62",
            "phaseErrorComp": "0",
            "phaseErrorComp": "0",
        },
    ),
    dict(
        dist_name="MRBTS-701/TNLSVC-1/TNL-2/IPNO-1/IPRT-1",
        list_name="staticRoutes",
        elements={
            "destIpAddr": "10.68.90.131",
            "destinationIpPrefixLength": "32",
            "gateway": "10.57.159.129",
            "preference": "1",
        },
    ),
    dict(
        dist_name="MRBTS-701/TNLSVC-1/TNL-4/IPNO-1/IPRT-1",
        list_name="staticRoutes",
        elements={
            "destIpAddr": "0.0.0.0",
            "destinationIpPrefixLength": "0",
            "gateway": "10.68.90.129",
            "preference": "1",
        },
    ),
]

# common
__all__ = ["tl", "PARAMS_TO_MODIFY_TL", "LIST_ITEM_TO_ADD_TL"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.230", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


# RealEnb
_real_enb_pdu = HBTE(addr="10.68.87.90", port_numbers=[4])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.48.78", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[4],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)


# #5GRU_0 for cloudBTS
_ru_pdu = HBTE(addr="10.57.241.167", port_numbers=[4])

_ru = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.10.41", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[4],
    radio_type="AEUD",
)

# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.57.178.18", username="mmw_sg4", password="mm@4", port="44061"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.3",
    iperf_path="/usr/bin/iperf",
    port=44061,
)

# Qualcomm
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.219", username="nokia5G", password="noki@123"
    ),
    serial_number="62428a2",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE"],
)

# #DU_0 for cloudlBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.101.48.68", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.22")

_du_pdu = HBTE(addr="10.68.87.91", port_numbers=[6])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_du_pdu.pdu_ports[6],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.101.48.68")


# #CU

_f1m = NetworkAddress(v4="xxxx", v6="xxxx", vlan_id=0)
_f1c = NetworkAddress(v4="10.57.173.80", v6="xxxx", vlan_id=0)
_f1u = NetworkAddress(v4="10.57.173.81", v6="xxxx", vlan_id=0)
_x2c = NetworkAddress(v4="10.57.173.136", v6="xxxx", vlan_id=0)
_x2u = NetworkAddress(v4="10.57.173.137", v6="xxxx", vlan_id=0)
_s1c = NetworkAddress(v4="xxxx", v6="xxxx", vlan_id=0)
_s1u = NetworkAddress(v4="10.57.173.137", v6="xxxx", vlan_id=0)
_tracing = NetworkAddress(v4="10.57.179.x", v6="xxxx", vlan_id=0)

_cu = CU(
    backhaul_site_oam_ip="10.57.173.5",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.173.5", username="robot", password="rastre1", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.173.5", username="Nemuadmin", password="nemuuser"
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
        ip_addr="10.57.137.90",
        username="nokiauser",
        tenant="FiveG",
        password="NOki@234!",
        port=5000,
        protocol="https",
        version="v3",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.137.90", username="nokiauser", password="HZnoki@123!"
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
    name="tl705_cbtsflavor",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_flavor.env"),
        os.path.join(_cfg_dir, "config_flavor_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="cbts_prefix",
)

_cbts_net = DeploymentNetworkStack(
    name="tl705_ext_net",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_ext_net.env"),
        os.path.join(_cfg_dir, "config_ext_net_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="tl705_cbts_deploy",
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
    cloud_deployment=_cloud_deployment,
    instance_id="705",
    global_bts_id="6",
)

# #cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    ues=[_android],
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    pdus=[_du_pdu, _ru_pdu],
)

__all__ = ["tl"]
