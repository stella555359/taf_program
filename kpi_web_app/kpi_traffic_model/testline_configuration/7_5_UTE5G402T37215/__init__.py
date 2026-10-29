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
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
    MediaTek,
    LicenseKeeper,
)
from taf.config.testline import (
    Enb,
    SimEnb,
    RealEnb,
    RadioModule,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.appserver import TafUeAppServer, AppServer

__maintainer__ = "Chen Tong"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_2_GMS <I_MN_5G_RAN_IV4_LINE_HZG_2@internal.nsn.com>"
)
__email__ = "tong.chen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.81", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.236", username="vrf4_sg2", password="VERIFICATION@sg2", port="52725"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.236",
    iperf_path="/usr/bin/iperf",
    port="52725",
)

_appserver = AppServer(_iperf_details_on_appserver)

# #Qualcomm
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.130.102",
    iperf_path="/cygdrive/c/tools",
    port="52725",
)

_qcom = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.102", username="mn5gran", password="nokia123@"
    ),
    serial_number="93f08c14",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Users/mn5gran/AppData/Local/Programs/Python/Python37/python.exe",
    qcat_path="C:/Program Files/Qualcomm/QCAT7/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sdx70", "qct_dx50"],
    clear_server_files="yes",
    clear_logs="yes",
    network_mode_switch_method="keyevents",
    mobile_network_text="SIMs",
    setting_network_mode_text="Preferred network type",
)

_appserver_ssh_mtk = SshServiceDetails(
    addr="10.57.191.236", username="vrf4_sg2", password="VERIFICATION@sg2", port="52726"
)

_iperf_mtk = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.102", username="mn5gran", password="nokia123@"
    ),
    network_interface_address="10.57.130.102",
    iperf_path="/data/local/tmp/iperf",
    port="52726",
)

_mtk = MediaTek(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.102", username="mn5gran", password="nokia123@"
    ),
    serial_number="M80_figeac",
    server_dir="C:/pyro_server_mtk",
    #python_path="/cygdrive/c/Users/nokia5g/AppData/Local/Programs/Python/Python37/python.exe",
    server_port=8080,
    edb_file_path="auto",
    log_filter="2.Gen98_Default_Standard",
    imei="887239942947310",
    imsi="262033100012807",
    apn_url="dxdata2",
    iperf_details=_iperf_mtk,
    capabilities=["REAL_MTK_UEPC_32", "SA"],
)

# 5GRU for classicalBTS
_ru_0_pdu = HBTE(addr="10.57.172.92", port_numbers=[1])

_ru_0 = RU(
    #'AEQB'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.2", username="serviceuser", password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2", username="root", password="umniedziala"
    ),
    pdu_port=_ru_0_pdu.pdu_ports[1],
    radio_type=RadioTypes.AQQY,
    serial_number="1M232007503",
)

_ru_1_pdu = HBTE(addr="10.57.172.99", port_numbers=[2])

_ru_1 = RU(
    #'AEQB'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.37.128", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.37.128", username="root", password="umniedziala"
    ),
    pdu_port=_ru_1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHEGB,
    serial_number="DH232542074",
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.57.172.91", port_numbers=[3])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru_0,_ru_1], f1_m_ip_addr="10.57.224.200")

_cu = CU(
    backhaul_site_oam_ip="10.57.224.200",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.224.200", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.224.200", username="Nemuadmin", password="nemuuser"
    ),
)


# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=37215, global_bts_id=37215)

tl = TestLine(
    test_pc=_host,
    appserver=_appserver,
    gnbs=[_classical_bts],
    ues=[_qcom,_mtk],
    tl_cloud_topology=_tl_cloud_topology,
)

# compatibility workaround
#tl = TestlineWrapper(tl)
