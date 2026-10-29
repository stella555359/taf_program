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
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
    TafUeAt,
)  # added in taf.meta.5.4

from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.pdu import HBTE
from taf.config.testline.pdu import TopYoung
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch

# added in taf.meta 5.4
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
from taf.config.testline.appserver import AppServer,  TafUeAppServer

from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol

__maintainer__ = "duqi"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02@internal.nsn.com"
__email__ = "qi.du@nokia-sbell.com"


# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.93", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_docker_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.46", username="dcapuser", password="dcapuser123"
    )
)
_tce_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.46", username="dcapuser", port=1234
    )
)

# PB INFO of ENB IS NOT CORRECT #
# 4GRU for RealEnb
_ru_enb_pdu = TopYoung(addr="10.71.196.22", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_enb = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.10.49", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_enb_pdu.pdu_ports[3],
)

# #RealEnb
_real_enb_pdu = HBTE(addr="10.57.246.195", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.251.140", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[4],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)

# #5GRU_0 for cloudBTS
_ru_pdu = TopYoung(addr="10.71.196.22", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.162", username="rfsw", password="gSDBExyEbO33komYWL6iPrtSaYc5XimHAGrsJ/K8+AY="
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    pdu_port=_ru_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEQK,
)

# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.57.162.2", username="mmw_sg2", password="mm@2", port="42332"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.2",
    iperf_path="C:/iperf-3.1.3-win64",
    port="42332",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.2",
    iperf_path="C:/iperf-3.1.3-win64",
    port="42332",
)
_appserver = AppServer(_iperf_details_on_appserver2)

# Huawei
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.111", username="nokia5G", password="noki@123"
    ),
    serial_number="L8K5T19916004089",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["huawei"],
)

# #DU_0 for cloudlBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.71.211.141", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.22")

_du_pdu = TopYoung(addr="10.71.196.23", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_du_pdu.pdu_ports[3],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.71.211.141")

_at_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.162.2",
    user="mmw_sg2",
    password="mm@2",
    bind_interface_ip="10.57.162.2",
    expected_prompt="\$",
    binary_path="/system/bin",
    ports=[42165],
)

_at_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_at_appserver_1,
    interval=1,
    binary_path="/cygdrive/c/Tools/",
    interface_name="Ethernet",
    server_close_delay=50,
    version=2,
    dt_from_uepc=True,
)

_at_1 = TafUeAt(
   # proxy_mngr_port=9955,
    ueproxy_force_release=True,
    com_port="3",
    serial_number="741c8004",
    ue_pc_address="10.0.176.121",
    ue_pc_login="mn5gran",
    ue_pc_password="nokia123@",
    ue_pc_expected_prompt="$",
    data_transfer=[_at_data_transfer_1],
    phone_number="",
    imei="",
    ue_pc_port=5000,
    imsi="262038001006245",
    capabilities=["qualcomm"],
)

# dcap
_host_dcap = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.89", username="utfuser", password="utfadmin!"
    ),
    connections=[],
)



# #CU
_cu = CU(
    backhaul_site_oam_ip="10.71.211.141",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.211.141", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.211.141", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=332, global_bts_id=332)

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIK_ABIL_AEQK_eCPRI"

tl = TestLine(
    test_pc=_host,
    test_pcs=[_docker_pc, _tce_pc],
    ues=[_at_1],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
    host=[_host_dcap],
)
