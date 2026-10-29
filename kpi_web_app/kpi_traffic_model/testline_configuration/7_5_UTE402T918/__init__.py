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


__maintainer__ = "Rao, Shengrong"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_03_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_03@internal.nsn.com>"
)
__email__ = "shengrong.rao@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.147", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS
_ru_pdu = FACOM(addr="10.68.87.102", port_numbers=[4])


_ru = RU(
    ru_hw_group="hw_group",  # Above6GHZ or Below6GHZ
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.52", username="user", password="pass"
    ),
    pdu_port=_ru_pdu.pdu_ports[4],
    radio_type=RadioTypes.AWHQM,
)


# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.68.88.236", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = FACOM(addr="10.68.87.98", port_numbers=[5])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.68.88.236")


# CU
_cu = CU(
    backhaul_site_oam_ip="10.68.88.236",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.88.236", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.88.236", username="Nemuadmin", password="nemuuser"
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.68.88.237", username="toor4nsn", password="oZPS0POrRieRtu"
)
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_gnb_pdu.pdu_ports[5],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.0.0.0", port="1/6", username="xx", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

# switch Mtor
_dell_s4048ton_ssh = SshServiceDetails(
    addr="10.0.0.0", port="1/9", username="xx", password="nokia123"
)
_dell_s4048ton_switch = DellS4048TONSwitch(_dell_s4048ton_ssh)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu)

# epc_sim
_epc_sim = EPCSim(
    mme_ip="10.108.229.75",
    mcc=262,
    mnc=3,
    tac=10396,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.75", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    dir_path="/opt/iphy/WTS/",
    cfg_filename="epc_standalone.lua",
)


# iperf server
_appserver_ssh = SshServiceDetails(
    addr="10.57.162.3", username="mmw_sg3", password="mm@3", port="43038"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.3",
    iperf_path="/usr/bin/iperf",
    port="43039",
)
# Qualcomm UE as Android
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.64", username="nokia5G", password="noki@123"
    ),
    serial_number="L8K5T19919006382",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE"],
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_android],
    core=_epc_sim,
)

tl = TestlineWrapper(tl)
