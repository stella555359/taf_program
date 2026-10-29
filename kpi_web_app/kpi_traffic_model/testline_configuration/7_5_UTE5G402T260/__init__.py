import os
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
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import (
    FACOM,
    PduPort,
    Pdu,
    EPC,
    ATEN,
    RRB,
    APC,
    Gude,
    HBTE,
    FPFH,
    TopYoung,
)

# from taf.config.testline.attenuator import HBTE as AHBTE
# from taf.config.testline.attenuator import AttenuationPort
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)  # added in taf.meta.5.4
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.hardware_controller import (
    AmiaFanHardwareController,
    GPSPowerHardwareController,
)
from taf.config.testline.signal_analyzer import KeysightN9935A
from taf.config.testline.nms import Netact
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.appserver import AppServer

from taf.config.testline.pdn import PDNTafUeAndroidDetails
from taf.config.testline.ue import TafUeAndroid

__maintainer__ = "Shasha Liu"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_5_GMS <I_MN_5G_RAN_IV4_LINE_HZG_5@internal.nsn.com>"
)
__email__ = "shasha.liu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##host #Local VM
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.2", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##RealEnb  #SA mode
"""
_real_enb_pdu = HBTE(addr="10.71.196.211", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.214.6", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[7],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

"""

##5GRU for classicalBTS
_ru1_pdu = FPFH(addr="10.68.87.89", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AVQE,
    serial_number="L1233206045",
    product_code="476244A",
)

_ru2_pdu = HBTE(addr="10.68.87.86", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru2 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.10",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.10",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    pdu_port=_ru2_pdu.pdu_ports[5],
    radio_type=RadioTypes.AEQE,
    serial_number="1M201304457",
    product_code="474750A",
)

_ru3_pdu = FPFH(addr="10.68.87.89", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru3 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.18",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.18",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    pdu_port=_ru3_pdu.pdu_ports[5],
    radio_type=RadioTypes.AEQV,
    serial_number="1M200101573",
    product_code="475294A",
)

_ru4_pdu = HBTE(addr="10.68.87.86", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru4 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.6",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.6",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    pdu_port=_ru4_pdu.pdu_ports[4],
    radio_type=RadioTypes.AEQY,
    serial_number="1M201202404",
    product_code="475538A",
)

_ru5_pdu = FPFH(addr="10.101.45.139", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru5 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.154",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.154",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    pdu_port=_ru5_pdu.pdu_ports[5],
    radio_type=RadioTypes.AVQE,
    serial_number="L1232006466",
    product_code="476244A.X11",
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.101.50.150", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.22")

_gnb_pdu = HBTE(addr="10.101.45.132", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[7],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1, _ru2, _ru3, _ru4], f1_m_ip_addr="10.101.50.150")

##CU #Auto TL Upgrading
_cu = CU(
    backhaul_site_oam_ip="10.101.50.150",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.50.150", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.50.150", username="Nemuadmin", password="nemuuser"
    ),
)

##cloud_topology #UTE Type
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_SA_ASOE_AVQE"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=2160, global_bts_id=10922)

"""
# for FastMile CPE 3.2
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.247",
    user="vrf4_sg5",
    password="vrf4@sg5",
    bind_interface_ip="10.57.191.247",
    expected_prompt="[vrf4_sg5@appserver ~]$ ",
    binary_path="/home/vrf4_sg5/taf_debug/iperf",
    ports=[55830, 55831],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    com_port="4",
    ue_pc_address="10.101.47.254",
    root_password="96ca38c29bd2",
    ue_manage_ip="192.168.1.1",
    serial_number="LPL221400517",
    data_transfer=[_fastmile_data_transfer_1],
    version="3.2",
    ue_pc_port=5555,
    capabilities=["REAL_FASTMILE_UE2", "nokia_fastmile"],
)
"""

# AppServer info
_app_server_1 = TafUeAppServer(
    app_server_name="APP_1",
    address="10.57.191.247",
    user="vrf4_sg5",
    password="vrf4@sg5",
    ports=[55845, 55846],
)

_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_app_server_1,
    interval=1,
    interface_name="rmnet_data0",
    #    bind_ue_ip="172.252.65.54",
    server_close_delay=50,
)

_pdn1 = PDNTafUeAndroidDetails(
    #    entryName="wustatic", apnName="wustatic", apnType=["DEFAULT"],
    entryName="dxdata1",
    apnName="dxdata1",
    apnType=["DEFAULT"],
)

# UE info
# CI_Detail_UE_Type='samsung S21'
_android_1 = TafUeAndroid(
    serial_number="R3CRB0NHPAT",
    #    capabilities=["samsung S21", "cell_Mapping: [1]", "samsung"],
    capabilities=["REAL_UE", "samsung_ue"],
    ue_pc_address="10.68.86.225",
    data_transfer=[_data_transfer_iperf],
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.225", username="mn5gran", password="nokia123@"
    ),
    ue_pc_port="8080",
    imei="350264683112666",
    imsi="262033100001094",
    pdns=[_pdn1],
    #    service_call_attach="17",
    #    service_call_detach="17",
    #    proxy_mngr_port="5555",
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    ues=[_android_1],
    #    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
)
