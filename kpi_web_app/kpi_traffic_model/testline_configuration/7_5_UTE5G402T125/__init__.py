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
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.appserver import AppServer

# added in taf.meta 5.4
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline import TafUeDataTransferProtocol, TafUeAtDataTransferProtocol
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import SshServiceDetails
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.pdu import ATEN
from taf.config.testline.ue import TafUeAt
from taf.config.testline import LicenseKeeper
from taf.config.testline.dcap import DcapBasic

__maintainer__ = "Xueqin Deng"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02@internal.nsn.com"
__email__ = "xueqin.deng@nokia-sbell.com"

# common
__all__ = ["tl"]
_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.198", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# dcap
_host_dcap = DcapBasic(
    connection_details=HttpConnectionDetails(
        addr="10.101.60.48", username="dcapuser", password="dcapadmin!"
    )
)

#appserver
_appserver_ssh = SshServiceDetails(
    addr="10.57.178.11", username="mmw_sg2", password="mm@2", port="45125"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="XX.XX.XX.XX",
    iperf_path="/cygdrive/c/iperf/iperftest/iperf",
    port="42125",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="XX.XX.XX.XX",
    iperf_path="iperf",
    port="43125",
)

_appserver = AppServer(iperf_details=_iperf_details_on_appserver)

#LicenseKeeper
_licensekeeper = LicenseKeeper(username="HAZ3_SG2", password="HAZ3_SG2")

# spark
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.183", username="mn5gran", password="nokia123@"
    ),
    serial_number="9d87b1a7",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.37/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100012845",
    licensekeeper=_licensekeeper,
)

# RealEnb---------------------------------------------------------
# 5GRU------------------------------------
_ru1_pdu = HBTE(addr="X.X.X.X", port_numbers=[3])

_ru1 = RU(
    ru_hw_group="Above6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7",
        username="rfsw",
        password="PD6N1DB0lWmwomtNL2qd3ISypbiocdGRy7U+Lipiksk=",
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru1_pdu.pdu_ports[3],
    radio_type=RadioTypes.AWEUC,
)

# #DU
_lmp_connection = SshServiceDetails(
    addr="10.68.90.90", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.68.90.91", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1], f1_m_ip_addr="10.68.90.90")

# CU
_cu = CU(
    backhaul_site_oam_ip="10.68.90.90",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.90.90", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.90.90", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=125, global_bts_id=125)

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "Refers to TAF UTE TL Type"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    ues=[_android],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_host_dcap],
    appserver=_appserver,
)
