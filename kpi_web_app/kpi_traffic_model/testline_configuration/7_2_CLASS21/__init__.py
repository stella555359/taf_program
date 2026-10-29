__maintainer__ = "Shobha K Reddy"
__team__ = "I_MN_ECE_BLR_RD_TST_SQD_ELECTRON_GMS "
__email__ = "I_MN_ECE_BLR_RD_TST_SQD_ELECTRON@internal.nsn.com"

import os
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.gnb import CloudBts, CU, DU, ClassicalBts
from taf.config.testline.appserver import AppServer
from taf.config.testline.ue import MediaTek
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
    TelnetConnectionDetails,
    SCRadioConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import Airphone, AirphoneCloud, IPHY, TM500, Qualcomm, Prisma
from taf.config.testline.traffic_generators import ParagonX, Caffeine
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.pdu import RRB, ATEN, FACOM, APC, Gude, EPC, BlackBox
from taf.config.testline.attenuator import RadioRack
from taf.config.testline.nms import Netact
from taf.config.testline.enb import RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.hardware_controller import GPSPowerHardwareController
from taf.config.testline import RU, SC5GRadio, SC4GRadio, NetworkAddress

# **********************************************************************************
_network_address = NetworkAddress(v4="0.0.0.0", v6=None, vlan_id=703)
# **********************************************************************************
_CFG_DIR = os.path.dirname(os.path.abspath(__file__))
# ********************************TestPc********************************************
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.43.204.103",
        username="ute",
        password="ute",
        port=22,
        private_key=None,
        proxy=None,
    ),
    connections=None,
)
# ********************************PDU***********************************************


# *******************************CLOUD TOPOLOGY(UTE Test Line Type)*****************
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_MTK"

# ********************************gNB***********************************************


_cu = CU(
    backhaul_site_oam_ip="10.53.190.21",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.53.190.21",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
        port=22,
        private_key=None,
        proxy=None,
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.53.190.21", username="Nemuadmin", password="nemuuser", port=443
    ),
)

_du_lmp_connection = SshServiceDetails(
    addr="10.53.190.21", username="toor4nsn", password="oZPS0POrRieRtu"
)

_du_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIL", hardware_version="A102"
)

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIK",
    hardware_version="A101",
)

_airscale = Airscale(common_units=[_du_common_unit])

_du = DU(airscale=_airscale)

_bts = ClassicalBts(cu=_cu, dus=[_du])

_cbts_flavor = ClassicalBts(cu=_cu, dus=[_du])


# *********************************UE*********************************************
_appserver_ssh = SshServiceDetails(
    addr="10.53.190.11", username="N-SGH752RW1M+tester", password="Nokia@1234"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.53.190.11",
    iperf_path="iperf",
    port=51001,
)

_appserver = AppServer(_iperf_details_on_appserver)


_ue_host_ssh = SshServiceDetails(
    addr="10.53.190.11", username="N-SGH752RW1M+tester", password="Nokia@1234"
)

_iperf_details_on_ue = IperfDataTransferDetails(
    ssh_connection_details=_ue_host_ssh,
    network_interface_address="",
    iperf_path="iperf",
    port=51002,
)

_mtk_ue = MediaTek(
    ssh_connection_details=_ue_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8000,
    edb_file_path="C:/MTK_EDB/MDDB_MT6297_S00_VMOLY_APOLLO_SQC_W19_34_P4.EDB",
    imei="35190103100403",
    apn_url="wap1.nokia.com",
    iperf_details=_iperf_details_on_ue,
    capabilities=["REAL_MEDIATEK_UE"],
)


# *********************************NetACT***************************************
_netact = Netact(addr="5.5.5.5")

# ********************************* Attenuator ****************************************

_attenuator = RadioRack(
    ip_addr="10.53.190.40", port=50000, attenuation_port_numbers=range(1, 9)
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_bts],
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_mtk_ue],
    appserver=_appserver,
    nms=_netact,
    attenuators=[_attenuator],
)

__all__ = ["tl"]
