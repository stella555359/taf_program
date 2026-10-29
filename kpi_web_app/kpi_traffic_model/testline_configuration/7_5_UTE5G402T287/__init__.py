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
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.attenuator import (
    AttenuationPort,
    HBTE,
)

__maintainer__ = "Chen Yin 4"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_07_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_07@internal.nsn.com>"
__email__ = "yin.4.chen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.10", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_attenuator = HBTE(
    ip_addr="10.57.235.163",
    port="5000",
    model="PA-16-16-6-127-0.5-B-S",
    attenuation_port_numbers=[r for r in range(1, 17)],
)

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# Second TL287

# 5GRU for classicalBTS
# _ru_pdu = HBTE(addr="10.57.249.35", port_numbers=[1])
_ru_pdu = FACOM(addr="10.57.241.148", port_numbers=[5])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.1.5", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.157.10", username="root", password="nokia123"
    ),
    pdu_port=_ru_pdu.pdu_ports[5],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
    ],
)

_ru_pdu_1 = FACOM(addr="10.57.241.148", port_numbers=[6])
_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.1.5", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.167.19", username="root", password="nokia123"
    ),
    pdu_port=_ru_pdu_1.pdu_ports[6],
    attenuation_ports=[
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.227.162", username="toor4nsn", password="oZPS0POrRieRtu"
)
# _capacity_unit = CapacityUnit(addr="192.168.253.20")
_capacity_cpue = CapacityUnit(addr="192.168.253.20")
_capacity_loki = CapacityUnit(addr="192.168.253.21")
# _gnb_pdu = HBTE(addr="10.57.241.145", port_numbers=[4])
_gnb_pdu = FACOM(addr="10.57.241.145", port_numbers=[4])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_cpue, _capacity_loki],
    pdu_port=_gnb_pdu.pdu_ports[4],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru, _ru_1], f1_m_ip_addr="10.57.227.162")

# CU
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.227.162", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.227.162", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts
_classical_bts_287 = ClassicalBts(
    dus=[_du], cu=_cu, instance_id=10125, global_bts_id=10125
)

# Huawei UE
_appserver_ssh = SshServiceDetails(
    addr="10.57.162.10", username="cmw_sg7", password="Nokia07!"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.10",
    iperf_path="/usr/bin/iperf",
    port=57287,
)
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.197", username="nokia5G", password="noki@123"
    ),
    serial_number="L8K5T19923005184",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["ANDROID_UE0", "huawei"],
)

_android1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.197", username="nokia5G", password="noki@123"
    ),
    serial_number="L8K5T19923004906",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["ANDROID_UE0", "huawei"],
)

_tce_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.101.60.40",
        username="dcapuser",
        password="dcapadmin!",
        port=49148,
    )
)

tl = TestLine(
    test_pc=_host,
    test_pcs=[_tce_pc],
    gnbs=[_classical_bts_287],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIL_ABIO_AEQN",
    ues=[_android, _android1],
    attenuator=_attenuator,
)
