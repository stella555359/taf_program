import os
import yaml
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
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import SshServiceDetails
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.pdu import ATEN
from taf.config.testline.ue import TafUeAt


__maintainer__ = "Fang Ludan"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_01@internal.nsn.com"
__email__ = "ludan.fang@nokia-sbell.com"

# common
__all__ = ["tl"]
_cfg_dir = os.path.dirname(os.path.abspath(__file__))
# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.47", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# #Qualcomm
_appserver_ssh = SshServiceDetails(
    addr="10.57.178.10", username="mmw_sg1", password="mm@1", port="41210"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="XX.XX.XX.XX",
    iperf_path="iperf",
    port="41210",
)

_appserver = AppServer(iperf_details=_iperf_details_on_appserver)

# CPE
_app_server_1 = TafUeAppServer(
    app_server_name="41210",
    address="10.57.178.10",
    user="mmw_sg1",
    password="mm@1",
    bind_interface_ip="10.57.178.10",
    expected_prompt="\[mmw_sg1.*\$ ",
    ports=[41210, 41211]
)

_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_app_server_1,
    interval=1,
    binary_path="/usr/bin/",
    interface_name="Cellular 2",
    server_close_delay=50,
    bind_ue_ip="172.252.65.37",
    version=2,
    dt_from_uepc=True,
)

_data_transfer_ping = TafUeDataTransferProtocol(
    protocol_name="ping", app_server=_app_server_1, interval=1
)

_data_transfer_ftp = TafUeDataTransferProtocol(
    protocol_name="ftp", app_server=_app_server_1, interval=1
)

_at_1 = TafUeAt(
    com_port="9",
    serial_number="3ff71f82",
    capabilities=["qualcomm"],
    ue_pc_address="10.101.47.183",
    ue_pc_login="mn5gran",
    ue_pc_password="nokia123@",
    ue_pc_expected_prompt="MN5GRAN@CNHZ5GRAN2544.*$",
    data_transfer=[_data_transfer_iperf, _data_transfer_ping, _data_transfer_ftp],
    phone_number="+33100010739",
    ue_pc_port="80",
    imei="004403160695849",
    imsi="262033031398419",
)

# RealEnb---------------------------------------------------------
# 5GRU------------------------------------
# add 2 more 5g ru info
# ru_hw_group: Above6GHZ or Below6GHZ
_ru1_pdu = HBTE(addr="X.X.X.X", port_numbers=[3])

_ru1 = RU(
    ru_hw_group="AH213590050",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7",
        username="rfsw",
        password="PD6N1DB0lWmwomtNL2qd3ISypbiocdGRy7U+Lipiksk=",
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru1_pdu.pdu_ports[3],
    radio_type=RadioTypes.AWEUA,
)

# #DU
_lmp_connection = SshServiceDetails(
    addr="10.68.90.56", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.68.87.242", port_numbers=[5])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1], f1_m_ip_addr="10.68.90.56")

# CU
_cu = CU(
    backhaul_site_oam_ip="10.68.90.56",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.90.56", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.90.56", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=2101, global_bts_id=37147)

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "Refers to TAF UTE TL Type"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    ues=[_at_1],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_host],
    appserver=_appserver,
)
