import os
import re
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
from taf.config.testline.pdu import HBTE as PduHBTE
from taf.config.testline.pdu import TopYoung as PduTopYoung
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500, MediaTek
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact
from taf.config.testline.appserver import AppServer
from taf.config.testline.dcap import DcapRnD, DcapBasic
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.attenuator import (
    AttenuationPort,
    HBTE,
)

__maintainer__ = "Wang Dali"  # TL owner name
__team__ = "I_MN_5G_RAN_IV4_LINE_HZG_8_IV@internal.nsn.com"  # TL owner's team
__email__ = "dali.wang@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))


_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.34", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_l3call_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.0.176.87", port="22", username="mn5gran", password="nokia123@"
    )
)

_dcap = DcapBasic(
    connection_details=HttpConnectionDetails(
        addr="10.57.195.83", port="443", username="dcapuser", password="dcapadmin!"
    )
)

_attenuator = HBTE(
    ip_addr="10.71.204.215",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
    model="PA-16-16-6-127-0.5-B-S",
    version=None,
)

_ru_2_pdu = FACOM(addr="10.71.196.50", port_numbers=[6])
_ru_2 = RU(
    ru_hw_group="AZNA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="root",
        password="root",
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_2_pdu.pdu_ports[6],
)
_ru_3_pdu = FACOM(addr="10.71.196.54", port_numbers=[3])
_ru_3 = RU(
    ru_hw_group="AZNA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="root",
        password="root",
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_3_pdu.pdu_ports[3],
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = FACOM(addr="10.71.196.50", port_numbers=[4])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[4],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru_2, _ru_3], f1_m_ip_addr="10.71.211.232")
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.211.232", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.211.232", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, dcap=_dcap, global_bts_id=93, instance_id=93
)


_appserver_ssh = SshServiceDetails(
    addr="10.57.191.238", username="vrf3_sg6", password="vrf3@sg6"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.238",
    iperf_path="/usr/bin/iperf",
    port=56093,
)

_appserver = AppServer(_iperf)
_appserver.iperf_details.port = 56093

# for FastMile CPE
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.238",
    user="vrf3_sg6",
    password="vrf3@sg6",
    bind_interface_ip="10.57.191.238",
    expected_prompt="[vrf3_sg6@appserver ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=[56093, 57093],
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
    ue_pc_address="10.0.176.87",
    root_password="r,nRaNDyXQ3ziRah",
    default_user_password="havf4HW@35PdMrX3",
    ue_manage_ip="192.168.1.1",
    serial_number="LPL241800BA6",
    data_transfer=[_fastmile_data_transfer_1],
    version="Receiver 5G26-A",
    ue_pc_port=5555,
    ueproxy_force_release=True,
    proxy_mngr_port=9955,
    capabilities=["REAL_FASTMILE_UE", "nokia_fastmile"],
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    test_pcs=[_l3call_pc],
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_fastmile_1],
    appserver=_appserver,
    attenuator=[_attenuator],
)
