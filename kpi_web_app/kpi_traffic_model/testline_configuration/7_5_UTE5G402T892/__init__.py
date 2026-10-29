import os
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
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.pdu import HBTE as PduHBTE
from taf.config.testline.pdu import TopYoung as PduTopYoung
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact
from taf.config.testline.appserver import AppServer
from taf.config.testline.dcap import DcapRnD, DcapBasic
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
from taf.config.testline.gnb.networkaddress import NetworkAddress

__maintainer__ = "Casbo Xing"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_07@internal.nsn.com"  # TL owner's team
__email__ = "casbo.xing@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# testPc(taf)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.90", username="ute", password="iW_K#8.ute%A10h0m0ra"
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

_tce_pc1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="0.57.195.83",
        username="utfuser",
        password="utfadmin!",
        port=443,
    )
)

_tce_pc2 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.83",
        username="utfuser",
        password="utfadmin!",
        port=443,
    )
)

_dcap = DcapBasic(
    connection_details=HttpConnectionDetails(
        addr="10.57.195.83", port="443", username="utfuser", password="utfadmin!"
    )
)

# 5GRU for classicalBTS

# PB for RU
_ru_1_pdu = FACOM(addr="10.101.45.172", port_numbers=[2])

_ru_1 = RU(
    ru_hw_group="AVQC",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_1_pdu.pdu_ports[2],
)

# gNB LMP IP
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

# ABIL internal ip
_capacity_unit_1 = CapacityUnit(addr="192.168.253.22")
_capacity_loki = CapacityUnit(addr="192.168.253.17")

# gNB PB
_gnb_pdu = FACOM(addr="10.101.45.172", port_numbers=[1])

_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.90", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit_1, _capacity_loki],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru_1],
    f1_m_ip_addr="10.101.50.238",
)

# gNB OAM M-plane IP
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.50.238", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.50.238", username="Nemuadmin", password="nemuuser"
    ),
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

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

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id=892, global_bts_id=892, dcap=_dcap
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.238", username="vrf3_sg6", password="vrf3@sg6", port="57892"
)

_iperf0 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.238",
    iperf_path="/usr/bin/iperf",
    port=58892,
)

_appserver = AppServer(iperf_details=_iperf0)
_appserver.iperf_details.port = 57892

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.178", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="9EQUT20721010203",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf0,
    capabilities=["REAL_ANDROID_UE", "HUAWEI"],
)
tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    test_pcs=[_docker_pc, _dcap, _tce_pc, _tce_pc1, _tce_pc2],
    ues=[
        _android_0,
    ],
    appserver=_appserver,
    enbs=[],
    core=_realcore,
    tl_cloud_topology=_tl_cloud_topology,
)
