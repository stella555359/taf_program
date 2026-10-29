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

# added in taf.meta 5.4
from taf.config.testline.attenuator import AttenuationPort, TopYoung
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
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.optical_switch import Leoni

__maintainer__ = "Hu Jay"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_6_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "jay.hu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.2", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# #realcore5g
_real_5g_core = RealCore5G(mcc=262, mnc=0o3)

# #app server
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.248", username="vrf4_sg6", password="vrf4@sg6", port="56174"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.51",
    iperf_path="/cygdrive/c",
    port="56074",
)
# #Cobham
_tm500 = TM500(
    tma_host=SshServiceDetails(addr="9.9.9.9", username="user", password="pass"),
    tma_command_port=30000,
    tma_path="/opt/tma/xxx/",
    iperf_details=_iperf,
    imsi="262032002000013",
    sec_key="xxxxxxxxxxxxx",
)

# #Prisma
_airmosaic_ssh = SshServiceDetails(
    addr="10.57.240.164", username="CNHZ5GRAN1112+tester", password="nokia123"
)

_airmosaic_harness = HttpConnectionDetails(addr="10.57.240.164", port=8090)

_lsu_uu_ssh = SshServiceDetails(addr="10.57.249.84", username="user", password="user")

_tstm_uu_ssh = SshServiceDetails(addr="10.57.249.84", username="user", password="user")

_prisma_ue = Prisma(
    airmosaic_ssh_connection_details=_airmosaic_ssh,
    airmosaic_harness_connection_details=_airmosaic_harness,
    lsu_uu_ssh_connection_details=_lsu_uu_ssh,
    tstm_uu_ssh_connection_details=_tstm_uu_ssh,
    prisma_config_file="C:/TA_scripts/prisma_config.yml",
    default_sid_file="C:/TA_scripts/full.sid",
    iperf_details=_iperf,
    imsi="262032002000013",
    sec_key="xxxxxxxxxxxxx",
)

_tstm_x2_ssh = SshServiceDetails(addr="9.9.9.9", username="user", password="pass")

_prisma_enb = PrismaEnb(tstm_x2_ssh_connection_details=_tstm_x2_ssh)

_lsu_s1_ssh = SshServiceDetails(addr="8.8.8.8", username="user", password="pass")

_tstm_s1_ssh = SshServiceDetails(addr="8.8.8.8", username="user", password="pass")

_prisma_core = PrismaCore(
    lsu_s1_ssh_connection_details=_lsu_s1_ssh,
    tstm_s1_ssh_connection_details=_tstm_s1_ssh,
)

_qualcomm = Qualcomm(
    ssh_connection_details=SshServiceDetails(
        addr="8.1.1.1", username="user", password="pwd"
    ),
    serial_number="abcd",
    qxdm_version=1,
    ue_type=QualcommUeType.android,
    com_port=9857,
    heartbeat_port=5962,
    server_command_input_port=1234,
    server_qxdm_messages_port=2345,
    server_command_output_port=3456,
    message_stream_port=4567,
    iperf_details=_iperf,
    imsi="123456777",
    sec_key="xxxxxxxxxxxxx",
    capabilities=["REAL_UE", "REAL_QUALCOMM_UE"],
)

_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="8.1.1.1", username="user", password="pwd"
    ),
    serial_number="cdef",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    imsi="123456777",
    sec_key="xxxxxxxxxxxxx",
    capabilities=["REAL_UE", "REAL_ANDROID_UE"],
)

# #5GRU for two classicalBTS
# attenuator
_attenuator = TopYoung(
    ip_addr="9.8.8.8",
    port=3000,
    attenuation_port_numbers=[7, 8, 9, 10],
    model="TAS16T16-51-120-1SDES",
)

# #5GRU for two classicalBTS
_ru0_pdu = FACOM(addr="10.57.243.26", port_numbers=[4])
_ru1_pdu = FACOM(addr="10.57.243.4", port_numbers=[3])
_ru2_pdu = FACOM(addr="10.57.243.4", port_numbers=[1])

_ru0 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="root", password="root"
    ),
    pdu_port=_ru0_pdu.pdu_ports[4],
    radio_type=RadioTypes.AZQL.value,
)

_ru1 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="root", password="root"
    ),
    pdu_port=_ru1_pdu.pdu_ports[3],
    radio_type=RadioTypes.AZQL.value,
)

_ru2 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.84", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="root", password="root"
    ),
    pdu_port=_ru2_pdu.pdu_ports[1],
    radio_type=RadioTypes.AZQL.value,
)

# #DU for two classicalBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.57.229.6", username="toor4nsn", password="oZPS0POrRieRtu"
)

_lmp_connection_1 = SshServiceDetails(
    addr="10.57.223.239", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.20")

_capacity_unit_1 = CapacityUnit(addr="192.168.253.20")

_gnb_0_pdu = FACOM(addr="10.57.241.166", port_numbers=[4])

_gnb_1_pdu = FACOM(addr="10.57.242.15", port_numbers=[5])

_common_unit_0_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_gnb_0_pdu.pdu_ports[4],
)

_common_unit_1_0 = CommonUnit(
    lmp_connection=_lmp_connection_1,
    capacity_units=[_capacity_unit_1],
    pdu_port=_gnb_1_pdu.pdu_ports[5],
)

_airscale_0 = Airscale(common_units=[_common_unit_0_0])

_airscale_1 = Airscale(common_units=[_common_unit_1_0])

_du_0_0 = DU(airscale=_airscale_0, rus=[_ru0], f1_m_ip_addr="10.57.229.6")
_du_1_0 = DU(airscale=_airscale_1, rus=[_ru1, _ru2], f1_m_ip_addr="10.57.223.239")

# #CU
_f1m = NetworkAddress(v4="9.9.1.1", v6="xxxx", vlan_id=1)
_f1c = NetworkAddress(v4="9.9.1.2", v6="xxxx", vlan_id=2)
_f1u = NetworkAddress(v4="9.9.1.3", v6="xxxx", vlan_id=3)
_x2c = NetworkAddress(v4="9.9.2.1", v6="xxxx", vlan_id=1)
_x2u = NetworkAddress(v4="9.9.2.2", v6="xxxx", vlan_id=2)
_s1c = NetworkAddress(v4="9.9.3.1", v6="xxxx", vlan_id=1)
_s1u = NetworkAddress(v4="9.9.3.2", v6="xxxx", vlan_id=2)
_tracing = NetworkAddress(v4="9.9.1.2", v6="xxxx", vlan_id=1)

_cu_0 = CU(
    backhaul_site_oam_ip="10.57.229.6",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.229.6", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.229.6", username="Nemuadmin", password="nemuuser"
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

_cu_1 = CU(
    backhaul_site_oam_ip="10.57.223.239",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.223.239", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.223.239", username="Nemuadmin", password="nemuuser"
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

# two classicalbts
_classical_bts_0 = ClassicalBts(
    dus=[_du_0_0], cu=_cu_0, instance_id=74, global_bts_id=74
)

_classical_bts_1 = ClassicalBts(
    dus=[_du_1_0], cu=_cu_1, instance_id=78, global_bts_id=78
)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts_0, _classical_bts_1],
    core=_real_5g_core,
    ues=[_prisma_ue],
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
)
