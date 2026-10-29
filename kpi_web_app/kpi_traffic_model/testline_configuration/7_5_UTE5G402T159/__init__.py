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
from taf.config.testline.testpc import Connection
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)  # added in taf.meta.5.4
from taf.config.testline.core import RealCore
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import TopYoung, HBTE
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
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
from taf.config.testline.appserver import AppServer
from taf.config.testline.hardware_controller import (
    AmiaFanHardwareController,
    GPSPowerHardwareController,
)

__maintainer__ = "meng.yan"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02@internal.nsn.com"
__email__ = "meng.yan@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))


# PB INFO of ENB IS NOT CORRECT #
# 4GRU for RealEnb
_ru_enb_pdu = HBTE(addr="10.56.18.175", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_enb = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.8.128", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_enb_pdu.pdu_ports[2],
)


# #RealEnb
_real_enb_pdu = HBTE(addr="10.106.223.138", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.106.223.157", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[7],
    hardware_type="ASIA",
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)


# #5GRU_0 for cloudBTS
_ru_1_pdu = HBTE(addr="10.106.223.145", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.56.2", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.56.2", username="root", password="umniedziala"
    ),
    pdu_port=_ru_1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AEWD,
)

_ru_2_pdu = HBTE(addr="10.106.223.145", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.56.154", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.56.154", username="root", password="umniedziala"
    ),
    pdu_port=_ru_2_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEWD,
)

# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.57.178.20", username="mmw_sg2_3", password="mm@2@3", port="43147"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.20",
    iperf_path="/system/bin",
    port="44147",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.20",
    iperf_path="iperf",
    port="42147",
)
_appserver = AppServer(_iperf_details_on_appserver2)

# CI_Detail_UE_Type='Samsung'

# Qualcomm
_android1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.106.223.170", username="nokia5G", password="noki@123"
    ),
    serial_number="R3CRB0NHPAT",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["samsungS21", "samsung", "REAL_ANDROID_UE"],
)

_android2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.106.223.171", username="nokia5G", password="noki@123"
    ),
    serial_number="RFCR4049B3T",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["samsungS21", "samsung", "REAL_ANDROID_UE"],
)

# #DU_0 for cloudlBTS
_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ASOE",
)

_du_pdu = HBTE(addr="10.108.135.43", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_du_pdu.pdu_ports[2],
    hardware_type="ASOE",
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru_1, _ru_2], f1_m_ip_addr="10.108.135.32")


# #CU
_cu = CU(
    backhaul_site_oam_ip="10.108.135.32",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.108.135.32", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.108.135.32", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=159, global_bts_id=1)

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.70.230.182", username="ute", password="ute"
    ),
    connections=[Connection(interface="eth1",device=_classical_bts.dus[0].airscale.common_units[0],interface_type="lmp")],
)

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASOE_2xAEWD_ENB"

tl = TestLine(
    test_pc=_host,
    ues=[_android1, _android2],
    gnbs=[_classical_bts],
    #enbs=[_lte_real_enb],
    core=RealCore(mcc=310,mnc=410),
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
)
