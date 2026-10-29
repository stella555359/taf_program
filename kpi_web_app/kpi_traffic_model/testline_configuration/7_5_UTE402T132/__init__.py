import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.core import LTEEmuCore
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline import RU, DU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit

from taf.config.testline.legacy import SCF

from taf.config.testline.ue import MediaTek
from taf.config.testline.connection_details import (
    SshServiceDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc

__maintainer__ = "Jerry Wu"
__team__ = "5G&SC mmW&SC Pz 2 CN 02 SG"
__email__ = "I_MN_5G_RAN_IV4_LINE_HZG_7@internal.nsn.com"
__owner_email__ = "jerry.wu@nokia-sbell.com"

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# #######common########
__all__ = ["tl"]

_PARAMS_TO_MODIFY_SCF = [
    dict(value="L1R6_SA_AEQA_TL1043", dist_name="MRBTS-1043", p_name="btsName"),
    dict(value="10.110.90.66", dist_name="LTE_x2", p_name="amfIPAddress"),
    dict(value="10.57.249.220", dist_name="CU_x2Cplane", p_name="localIpAddr"),
    dict(value="10.57.249.220", dist_name="CU_s1Uplane", p_name="localIpAddr"),
    dict(value="10.57.249.220", dist_name="CU_x2Uplane", p_name="localIpAddr"),
]


# gNB webUI info
_cu = CU(
    backhaul_site_oam_ip="10.57.249.220",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.249.220", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.249.220", username="Nemuadmin", password="nemuuser"
    ),
)


# _du = DU(airscale = Airscale([]))

# info for FACOM(PowerStation).
_gnb_pdu = FACOM(addr="10.57.246.196", port_numbers=[8])

_common_unit_0 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.249.220", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=None,
    pdu_port=_gnb_pdu.pdu_ports[8],
)

_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=None)

_cbts = ClassicalBts(cu=_cu, dus=[_du])

# Testpc for run robot FRT cases##########
_testpc_ssh = SshServiceDetails(
    addr="10.57.167.114", username="ute", password="iW_K#8.ute%A10h0m0ra"
)
_test_pc = TestPc(default_ssh_connection_details=_testpc_ssh)

# LteEmu##########

_scf = SCF(
    project="5G19B", name="SBTS5G18A_5g_classical.xml", scf_params=_PARAMS_TO_MODIFY_SCF
)


# Iperf##########
_appserver_ssh = SshServiceDetails(
    addr="10.57.163.50", username="root", password="nokia123"
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.50",
    iperf_path="iperf",
    port=57101,
)
_appserver = AppServer(_iperf_details_on_appserver)

# Control PC##########
_ue_host_ssh = SshServiceDetails(
    addr="10.57.130.156", username="nokia5G", password="noki@123"
)
_iperf_details_on_ue = IperfDataTransferDetails(
    ssh_connection_details=_ue_host_ssh,
    network_interface_address="10.57.130.156",
    iperf_path="iperf",
    port=57102,
)
_mtk_ue = MediaTek(
    ssh_connection_details=_ue_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="C:/bach-mp-dnr-m70-of.w19.41.p9_v1_3GPP_15.6_June(VMOLY.W19.43.p3_IODTCBr.20191022.Build20191227.1400)/MDDB_MT6297_S00_VMOLY_W19_43_P3.EDB",
    imei="262033032993637",
    apn_url="wap1.nokia.com",
    iperf_details=_iperf_details_on_ue,
    capabilities=["REAL_MEDIATEK_UE"],
)


# Testline
_tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="classical",
    ues=[_mtk_ue],
    appserver=_appserver,
)

tl = _tl

tl.scf = _scf  # still a WA
# PACKAGE_SERVER_IP = '10.183.71.27'
# PACKAGE_SERVER_USER = 'root'
# PACKAGE_SERVER_PWD = 'nokia123'
# gNB_Package_path = '/ephemeral/package'
# YAFT_path = '/ephemeral/yaft'
# package_url = 'https://artifactory-espoo1.ext.net.nokia.com/artifactory/mnp5g-central-public-local/System_Release/'
