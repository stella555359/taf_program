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
from taf.config.testline.pdu import HBTE as PduHBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500, MediaTek
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact
from taf.config.testline.appserver import AppServer
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline.dcap import DcapRnD, DcapBasic
from taf.config.testline.ue import TafUeAndroid
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.pdn import PDNTafUeAndroidDetails

__maintainer__ = "Fred"
__team__ = (
    "I_NSB_MN_5GSC_5G_PZ_HZ_07_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_07_GMS@internal.nsn.com>"
)
__email__ = "lei.24.wang@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.37", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_lss = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.37", port="22", username="coam", password="zO&n1W*ktp7"
    )
)

_dcap_1 = DcapBasic(
    connection_details=HttpConnectionDetails(
        addr="10.57.195.82", port="49148", username="utfuser", password="utfadmin!"
    )
)

_dcap_2 = DcapBasic(
    connection_details=HttpConnectionDetails(
        addr="10.57.195.83", port="49148", username="utfuser", password="utfadmin!"
    )
)

# 5GRU for classicalBTS
_ru_1_pdu = PduHBTE(addr="10.101.45.170", port_numbers=[6])

_ru_1 = RU(
    ru_hw_group="AZQS",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.79", username="ute", password="3edc4rfv%TGB"
    ),
    serial_number="1M212807082",
    pdu_port=_ru_1_pdu.pdu_ports[6],
)
_ru_2_pdu = PduHBTE(addr="10.101.45.166", port_numbers=[4])
_ru_2 = RU(
    ru_hw_group="AQQY",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.70", username="ute", password="3edc4rfv%TGB"
    ),
    serial_number="1M242502030",
    pdu_port=_ru_2_pdu.pdu_ports[4],
)
_ru_3_pdu = PduHBTE(addr="10.101.45.166", port_numbers=[1])
_ru_3 = RU(
    ru_hw_group="AVQF",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.82", username="ute", password="3edc4rfv%TGB"
    ),
    serial_number="1M251103757",
    pdu_port=_ru_3_pdu.pdu_ports[1],
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_1 = CapacityUnit(addr="192.168.253.20")


_gnb_pdu = FACOM(addr="10.101.45.164", port_numbers=[6])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit_1],
    pdu_port=_gnb_pdu.pdu_ports[6],
)

_airscale = Airscale(common_units=[_common_unit_0])


_du = DU(airscale=_airscale, rus=[_ru_1, _ru_2, _ru_3], f1_m_ip_addr="10.101.50.194")

##CU
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.50.194", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.50.194", username="Nemuadmin", password="nemuuser"
    ),
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, global_bts_id=846, instance_id=846, dcap=_dcap_1
)


# _appserver_ssh = SshServiceDetails(
#     addr="10.57.191.238", username="vrf3_sg6", password="vrf3@sg6"
# )
# _iperf = IperfDataTransferDetails(
#     ssh_connection_details=_appserver_ssh,
#     network_interface_address="10.57.191.238",
#     iperf_path="/usr/bin/iperf",
#     port=57846,
# )
#
#
# # CI_Detail_UE_Type='Huawei honor 30s'
# _android = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.101.47.194", username="mn5gran", password="nokia123@"
#     ),
#     serial_number="9EQUT20721003466",
#     server_dir="/cygdrive/c/pyro_server",
#     python_path="C:/Python27/python.exe",
#     qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
#     diag_cfg_path="C:/pyro_server/DIAG.cfg",
#     iperf_details=_iperf,
#     capabilities=["REAL_ANDROID_UE", "Huawei"],
# )
_app_server_1 = TafUeAppServer(
    app_server_name="APP_1",
    address="10.57.191.238",
    user="vrf3_sg6",
    password="vrf3@sg6",
    bind_interface_ip="10.57.191.238",
    binary_path="/home/mmw_sg2/huawei_iperf/ipef",
    expected_prompt="vrf3_sg6",
    ports=["46846", "57846"],
)

_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_app_server_1,
)

_data_transfer_ping = TafUeDataTransferProtocol(
    protocol_name="ping", app_server=_app_server_1, interval=1
)

_pdn1 = PDNTafUeAndroidDetails(
    entryName="default",  # MANDATORY / use this entry point as KW argument (pdn)
    apnName="dxdata1",  # MANDATORY
    apnType=["DEFAULT", "MMS", "XCAP"],  # MANDATORY
)

_android_0 = TafUeAndroid(
    serial_number="9EQUT20721003466",
    capabilities=["REAL_UE", "HUAWEI_ANDROID"],
    ue_pc_address="10.101.47.194",
    data_transfer=[_data_transfer_iperf, _data_transfer_ping],
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.194", username="mn5GRAN", password="nokia123@"
    ),
    ueproxy_force_release=True,
    proxy_mngr_port=9955,
    imsi="460028001006067",
    pdns=[_pdn1],
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_android_0],
    test_pcs=[_lss, _lss],
)
