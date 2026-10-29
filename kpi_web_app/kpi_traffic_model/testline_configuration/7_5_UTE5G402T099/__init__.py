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
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore, RealCore4G
from taf.config.testline import RU, DU, AppServer
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500, Android
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.dcap import DcapRnD, DcapBasic
from taf.config.testline.nms import Netact

__maintainer__ = "Casbo"
__team__ = (
    "I_NSB_MN_5GSC_5G_PZ_HZ_07_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_07_GMS@internal.nsn.com>"
)
__email__ = "casbo.xing@nokia-sbell.com"

__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# VM
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.40", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# QualComm UE
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.238", username="vrf3_sg6", password="vrf3@sg6", port="59099"
)

_iperf0 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.238",
    iperf_path="/usr/bin/iperf",
    port=57099,
)

_iperf1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.238",
    iperf_path="iperf",
    port=58099,
)
_appserver = AppServer(iperf_details=_iperf0)
_appserver.iperf_details.port = 58000

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.220", username="mn5gran", password="nokia123@"
    ),
    serial_number="9YS0220110015223",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf0,
    capabilities=["REAL_ANDROID_UE", "HONOR"],
)


_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.220", username="mn5gran", password="nokia123@"
    ),
    serial_number="becf8866",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf1,
    capabilities=["REAL_ANDROID_UE", "askey"],
)

_netact = Netact("10.108.248.82")

# ENB
_real_enb_pdu = FACOM(
    addr="10.68.87.107", port_numbers=[2], model="111", version="1.1.1"
)

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.68.89.27", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[2],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None, instance_id=4099)

_ru1_pdu = FACOM(addr="10.68.87.109", port_numbers=[3])
_ru2_pdu = FACOM(addr="10.68.87.104", port_numbers=[2])
_ru3_pdu = FACOM(addr="10.68.87.109", port_numbers=[4])
_ru4_pdu = FACOM(addr="10.68.87.107", port_numbers=[3])
_ru5_pdu = FACOM(addr="10.68.87.109", port_numbers=[2])
_ru6_pdu = FACOM(addr="10.68.87.107", port_numbers=[6])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="0.0.0.0",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    pdu_port=_ru1_pdu.pdu_ports[3],
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="0.0.0.0",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    pdu_port=_ru2_pdu.pdu_ports[2],
)

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="0.0.0.0",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    pdu_port=_ru3_pdu.pdu_ports[4],
)

_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="0.0.0.0",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    pdu_port=_ru4_pdu.pdu_ports[3],
)

_ru5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="0.0.0.0",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    pdu_port=_ru5_pdu.pdu_ports[2],
)

_ru6 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="0.0.0.0",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    pdu_port=_ru6_pdu.pdu_ports[6],
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="193.168.253.17")

_gnb_pdu = FACOM(addr="10.68.87.109", port_numbers=[2])

_common_unit = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit])

_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6],
    f1_m_ip_addr="10.68.89.26",
    f1_c_ip_addr="10.68.89.26",
    f1_u_ip_addr="10.68.89.26",
)

_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.89.26", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.89.26", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts = ClassicalBts(dus=[_du], cu=_cu, global_bts_id=99, instance_id=99)

_lmp_connection1 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit1 = CapacityUnit(addr="193.168.253.17")

_gnb_pdu1 = FACOM(addr="10.68.87.106", port_numbers=[2])

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection1,
    capacity_units=[_capacity_unit1],
    pdu_port=_gnb_pdu1.pdu_ports[2],
)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
    # ues=[_android],
    ues=[_android_0, _android_1],
    # test_pcs=[_dcap_1, _dcap_2],
    appserver=_appserver,
)
