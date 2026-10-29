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
from taf.config.testline.core import (
    EPCSim,
    LTEEmuCore,
    PrismaCore,
    RealCore,
    RealCore4GDetails,
    RealCore5GDetails,
    AMF,
    MME,
)
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress

__maintainer__ = "Xing Pan"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_8_GMS <I_MN_5G_RAN_IV4_LINE_HZG_8@internal.nsn.com>"
)
__email__ = "casbo.xing@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# testPC(TAF)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.14", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_docker_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.163",
        username="dcapuser",
        password="iW_K#8.ute%A10h0m0ra",
        port=49151,
    )
)

_tce_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.163",
        username="dcapuser",
        password="iW_K#8.ute%A10h0m0ra",
        port=49151,
    )
)


# ==================================================================================
# ==================================================================================
# ==================================================================================
# 5GRU for classicalBTS
_ru_pdu = FACOM(addr="10.57.241.236", port_numbers=[1])
_ru = RU(
    ru_hw_group="AAHF",
    serial_number="6Q184131097",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.31", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
)

_ru_pdu2 = FACOM(addr="10.57.241.226", port_numbers=[3])
_ru2 = RU(
    ru_hw_group="AAHF",
    serial_number="1M194304945",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu2.pdu_ports[3],
)

# ==================================================================================
# ==================================================================================
# ==================================================================================
# gnb_0
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = FACOM(addr="10.57.241.226", port_numbers=[5])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.14", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
    test_pc=_gnb_test_pc_0,
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru, _ru2])
_cu = CU(
    backhaul_site_oam_ip="10.57.226.66",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.226.66", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.226.66", username="Nemuadmin", password="nemuuser"
    ),
)
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=288, global_bts_id=288)

# ==================================================================================
# ==================================================================================
# ==================================================================================
# enb_0
_lmp_connection_enb = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_real_enb_pdu = FACOM(addr="10.57.241.226", port_numbers=[5])
_enb_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.80", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[5],
    test_pc=_enb_pc_1,
    hardware_type=None,
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(
    system_module=_real_enb,
    oam_ip=NetworkAddress(v4="10.57.226.67"),
    rms=[_ru, _ru2],
    instance_id=288,
)

# ==================================================================================
# ==================================================================================
# ==================================================================================
# Real Core
_real_5g_core_details = RealCore5GDetails(
    amf=AMF(
        oam_ssh_connection_details=SshServiceDetails(
            addr="10.110.66.198", username="xxx", password="xxx"
        ),
        n2=NetworkAddress(v4="xxx.xxx.xx.xx", v6="xxx:xx::xxx", vlan_id=1),
    )
)
_realcore = RealCore(five_g=_real_5g_core_details, mcc="262", mnc="3")


# ==================================================================================
# ==================================================================================
# ==================================================================================
# QualComm UE
_appserver_ssh = SshServiceDetails(
    addr="10.57.162.10", username="cmw_sg7", password="Nokia07!"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.10",
    iperf_path="/usr/bin/iperf",
    port=57288,
)

# CI_Detail_UE_Type='Samsung'
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.47", username="nokia5G", password="noki@123"
    ),
    serial_number="R5CN208KEDY",
    # serial_number='6df52295',
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung"],
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

## switch port to EIF1
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.57.129.215", port="1/1", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

# instance_id=MRBTS_ID

# Netact IP
# _netact=Netact('10.107.178.214')
_netact = Netact("10.106.161.25")


# ==================================================================================
# ==================================================================================
# ==================================================================================

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    # test_pcs=[_docker_pc, _tce_pc],
    enbs=[_lte_real_enb],
    # core=_realcore,
    tl_cloud_topology=_tl_cloud_topology,
    switches=[_dell_s4048on_switch],
    nms=_netact,
    ues=[_android],
)

# tl = TestlineWrapper(tl)
