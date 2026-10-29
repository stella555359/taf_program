import os
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
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
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline.core import RealCore
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import (
    FACOM,
    PduPort,
    Pdu,
    EPC,
    ATEN,
    RRB,
    APC,
    Gude,
    HBTE,
    TopYoung,
)
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

# from taf.config.testline.attenuator import AttenuationPort, TopYoung  # added in taf.meta 5.4
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
from taf.config.testline.appserver import AppServer

__maintainer__ = "Shasha Liu"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_5_GMS <I_MN_5G_RAN_IV4_LINE_HZG_5@internal.nsn.com>"
)
__email__ = "shasha.liu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##host #Local VM
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.12", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##RealEnb
_real_enb_pdu = HBTE(addr="10.10.10.10", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="0.0.0.0", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[3],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

##5GRU for classicalBTS

# _attenuator = TopYoung(ip_addr='10.68.87.55', port=1, attenuation_port_numbers=[13, 14, 15, 16])

_ru_pdu = HBTE(addr="10.71.196.196", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.128",
        username="root",
        password="",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.33.128",
        username="root",
        password="",
    ),
    pdu_port=_ru_pdu.pdu_ports[4],
    radio_type=RadioTypes.AZQC,  # radio_type='AEQP'
    #    attenuation_ports=[_attenuator.attenuator_ports[13], _attenuator.attenuator_ports[14],
    #                       _attenuator.attenuator_ports[15], _attenuator.attenuator_ports[16]]
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.71.213.198", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.22")

_gnb_pdu = HBTE(addr="10.71.196.195", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[6],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.71.213.198")

##CU #Auto TL Upgrading
_cu = CU(
    backhaul_site_oam_ip="10.71.213.198",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.213.198", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.213.198", username="Nemuadmin", password="nemuuser"
    ),
)

##cloud_topology #UTE Type
_tl_cloud_topology = "CLOUD_5G_RPI_SB_ASIKA102R_ABILA102B4_AEQP_19B"

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="2595", global_bts_id="2595"
)

# switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="4.4.4.4", port="1/18", username="5gran", password="nokia123"
)  # EIF1 Port
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

# switch Mtor
_dell_s4048ton_ssh = SshServiceDetails(
    addr="5.5.5.5", port="1/18", username="5gran", password="nokia123"
)
_dell_s4048ton_switch = DellS4048TONSwitch(_dell_s4048ton_ssh)

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.152", username="vrf4_sg5", password="vrf4@sg5", port="55886"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.152",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port=55887,
)
_appserver = AppServer(_iperf)

# _ue1 = Qualcomm(
# ssh_connection_details=SshServiceDetails(
# addr="10.101.47.217", username="nokia5G", password="noki@123"
# ),
# serial_number="86cdc2b4",
# qxdm_version="5.1.300.1",
# ue_type="android",
# com_port="18",
# heartbeat_port="18",
# server_command_input_port="22",
# server_qxdm_messages_port="17",
# server_command_output_port="22",
# message_stream_port="17",
# iperf_details=_iperf,
# capabilities=["qct_dx50", "cell_Mapping: [1]", "qct_dx50"],
# licensekeeper,
# channel_emulator_ports,
# license_type,
# )

_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.218", username="nokia5G", password="noki@123"
    ),
    serial_number="49069371",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "qct_dx50"],
)


# ---------UE qualcomm1------
# _ue_ctrl_pc_2_ssh_details = SshServiceDetails(
#    addr="10.101.47.174", username="nokia5G", password="noki@123"
# )
# _ue1 = Android(
#    ssh_connection_details=_ue_ctrl_pc_2_ssh_details,
#    capabilities=["REAL_UE", "REAL_ANDROID_UE", "REAL_QUALCOMM_UE"],
#    serial_number="N10PFV5XP",
#    server_dir="C:/pyro_server",
#    python_path="C:/Python27/python.exe",
#    iperf_details=IperfDataTransferDetails(
#        network_interface_address="",
#        ssh_connection_details=_ue_ctrl_pc_2_ssh_details,
#        iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
#    ),
#    diag_cfg_path="C:/pyro_server/DIAG.cfg",
#    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
# )
#
# # netact - qin1
_netact = Netact("10.107.178.203")

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    nms=_netact,
    enbs=[_lte_real_enb],
    core=RealCore(mcc=262, mnc=3),
    ues=[_ue1],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
)

# old version keyword under robotws5g/resource compatibility workaround
# tl = TestlineWrapper(tl)
