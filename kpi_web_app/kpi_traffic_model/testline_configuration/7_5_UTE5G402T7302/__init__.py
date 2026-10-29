__maintainer__ = "Lu Miao"
__team__ = "I_MN_5G_RAN_IV4_QT_HZG_GMS <I_MN_5G_RAN_IV4_QT_HZG@internal.nsn.com>"
__email__ = "I_MN_5G_RAN_IV4_QT_HZG@internal.nsn.com"
__owner_email__ = "fangmin.wu@nokia-sbell.com"

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
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.enb import RealEnb
from taf.config.testline.ue import TM500, Android
from taf.config.testline import DU, RU
from taf.config.testline.attenuator import (
    AttenuationPort,
    HBTE,
)  # added in taf.meta 5.4
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.radio import RadioModule
from taf.config.testline import IperfDataTransferDetails
from taf.config.testline.appserver import AppServer

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_attenuator = HBTE(
    ip_addr="10.57.251.250", port="5000", attenuation_port_numbers=[1, 2, 3, 4]
)

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.176", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_cu = CU(
    backhaul_site_oam_ip="10.57.247.178",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.247.178", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.247.178", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
_common_unit_pdu = FACOM(addr="10.57.242.11", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_lmp_connection_0 = SshServiceDetails(
    addr="10.57.247.178", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.17")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[5],
)

# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])

# 5G RU
_ru_pdu = FACOM(addr="10.57.243.10", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])


_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.17",
        username="root",
        password="XwcvfotfCCOIAqtk7uQjN38d8sG5Yp2Pb2/p6Eqw8+Y=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[8],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_du_0 = DU(airscale=_airscale_0, rus=[_ru], f1_m_ip_addr="10.57.247.178")

_cbts = ClassicalBts(cu=_cu, dus=[_du_0], instance_id="10429", global_bts_id="1")

_appserver_ssh = SshServiceDetails(
    addr="10.57.178.18", username="mmw_sg4", password="mm@4", port="44321"
)

# #Qualcomm

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.18",
    iperf_path="/usr/bin/iperf",
    port="44321",
    ports=[44321, 44322, 44323, 44324, 44325, 44326],
)

_cobham = TM500(
    tma_host=SshServiceDetails(
        addr="10.57.130.139", username="nokia5G", password="noki@123"
    ),
    tma_command_port=5004,
    iperf_details=_iperf_details_on_appserver,
    tma_path="/cygdrive/c/Program Files (x86)/Aeroflex/TM500/5G NR - NLA latest_version/"
    "Test Mobile Application/TmaApplication.exe",
)


_appserver = AppServer(_iperf_details_on_appserver)

# CI_Detail_UE_Type='Samsung;Samsung;Samsung;Samsung'
_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.220", username="nokia5G", password="noki@123"
    ),
    serial_number="R5CN20KSFSX",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.3/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032994024",
    capabilities=["REAL_ANDROID_UE", "samsung", "huawei_sigspark"],
)

_android_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.220", username="nokia5G", password="noki@123"
    ),
    serial_number="RFCR103LMCN",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.3/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032994023",
    capabilities=["REAL_ANDROID_UE", "samsung", "huawei_sigspark"],
)

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.220", username="nokia5G", password="noki@123"
    ),
    serial_number="R3CW10X1P0T",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.3/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032994025",
    capabilities=["REAL_ANDROID_UE", "samsung", "huawei_sigspark"],
)
# #Qualcomm

_epcsim = EPCSim(
    mme_ip="192.168.4.1",
    mcc=777,
    mnc=44,
    tac=777,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.47.199.241", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    dir_path="/opt/wts/latest",
    cfg_filename="TL101_basic_cfg_realLteEnb.cfg",
    edaemon_port="22222",
    egate_port="20021",
)
_eNB_capacity_unit = CapacityUnit(addr="192.168.253.36")
_real_enb_pdu = FACOM(addr="10.57.241.158", port_numbers=[2])
_eNB_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.247.178", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_real_enb_pdu.pdu_ports[2],
    capacity_units=[_eNB_capacity_unit],
)
_enb_airscale = Airscale(common_units=[_eNB_common_unit])
_enb = RealEnb(airscale=_enb_airscale)


tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    core=_epcsim,
    enbs=[_enb],
    attenuator=_attenuator,
    ues=[_android_0, _android_1, _android_2],
    appserver=_appserver,
)


__all__ = ["tl"]
