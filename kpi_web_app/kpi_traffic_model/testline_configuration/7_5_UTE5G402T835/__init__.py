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
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.pdu import HBTE as PduHBTE
from taf.config.testline.pdu import TopYoung as PduTopYoung
from taf.config.testline.pdu import FPFH
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500, MediaTek
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
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

__maintainer__ = "Han Ruiyu"  # TL owner name
__team__ = "I_MN_5G_RAN_IV4_LINE_HZG_8_IV@internal.nsn.com"  # TL owner's team
__email__ = "ruiyu.han@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_attenuator = HBTE(
    ip_addr="10.71.204.215",
    port="5000",
    attenuation_port_numbers=[9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
    version=None,
)

_ru_1_pdu = FACOM(addr="10.71.196.40", port_numbers=[1])
_ru_1 = RU(
    ru_hw_group="AZNA",
    serial_number="RW200800279",
    radio_type=RadioTypes.AZNA,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="root",
        password="root",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.0.176.212", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_1_pdu.pdu_ports[1],
)
_ru_2_pdu = FACOM(addr="10.71.196.41", port_numbers=[3])
_ru_2 = RU(
    ru_hw_group="AZNA",
    serial_number="RW201001217",
    radio_type=RadioTypes.AZNA,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="root",
        password="root",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.0.176.211", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_2_pdu.pdu_ports[3],
)
_ru_3_pdu = FACOM(addr="10.71.196.41", port_numbers=[1])
_ru_3 = RU(
    ru_hw_group="AQQF",
    serial_number="1M223638092",
    radio_type=RadioTypes.AQQF,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_3_pdu.pdu_ports[1],
)
_ru_4_pdu = FACOM(addr="10.71.196.41", port_numbers=[2])
_ru_4 = RU(
    ru_hw_group="AQQF",
    serial_number="1M223638099",
    radio_type=RadioTypes.AQQF,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_4_pdu.pdu_ports[2],
)
_ru_5_pdu = FACOM(addr="10.71.196.34", port_numbers=[2])
_ru_5 = RU(
    ru_hw_group="AVQF",
    serial_number="1M250900021",
    radio_type=RadioTypes.AQQF,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.0.176.205", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_5_pdu.pdu_ports[2],
)
_ru_6_pdu = FPFH(addr="10.71.196.35", port_numbers=[3])
_ru_6 = RU(
    ru_hw_group="AVQF",
    serial_number="1M251103759",
    radio_type=RadioTypes.AQQF,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.218.54", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_6_pdu.pdu_ports[3],
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_gnb_pdu = FPFH(addr="10.71.196.35", port_numbers=[2])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[],
    pdu_port=_gnb_pdu.pdu_ports[2],
    hardware_type="ASIB",
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru_1, _ru_2, _ru_3, _ru_4, _ru_5, _ru_6], f1_m_ip_addr="10.71.211.177")
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.211.177", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.211.177", username="Nemuadmin", password="nemuuser"
    ),
)

_dcap = DcapBasic(
    connection_details=HttpConnectionDetails(
        addr="10.57.195.83", port="443", username="dcapuser", password="dcapadmin!"
    )
)

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, dcap=_dcap, instance_id=835, global_bts_id=835
)


_appserver_ssh = SshServiceDetails(
    addr="10.57.191.238", username="vrf3_sg6", password="vrf3@sg6"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.238",
    iperf_path="/usr/bin/iperf",
    port=56835,
)

_appserver = AppServer(_iperf)
_appserver.iperf_details.port = 56835

# for FastMile CPE
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.238",
    user="vrf3_sg6",
    password="vrf3@sg6",
    bind_interface_ip="10.57.191.238",
    expected_prompt="[vrf3_sg6@appserver ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=[56835, 57835],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    com_port="15",
    ue_pc_address="10.0.176.3",
    root_password="4X42mMF@USo5jpPW",
    default_user_password="Ev4@x+DmnchtPa+d",
    ue_manage_ip="192.168.1.1",
    serial_number="LPL241800B5F",
    data_transfer=[_fastmile_data_transfer_1],
    version="Receiver 5G26-A",
    ueproxy_force_release=True,
    proxy_mngr_port=9955,
    capabilities=["REAL_FASTMILE_UE", "nokia_fastmile"],
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

##host
# _gnb_testpc = TestPc(
#     default_ssh_connection_details=SshServiceDetails(
#         addr="10.57.157.233", username="ute", password="iW_K#8.ute%A10h0m0ra"
#     )
# )

_gnb_testpc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.217.77", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

tl = TestLine(
    test_pc=_gnb_testpc,
    test_pcs=[_gnb_testpc],
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_fastmile_1],
    appserver=_appserver,
    attenuator=[_attenuator],
)
