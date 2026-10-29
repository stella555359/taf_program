import os
import re
import yaml
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
from taf.config.testline.core import RealCore
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

# from taf.config.testline.attenuator import AttenuationPort, TopYoung  # added in taf.meta 5.4
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

# from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.appserver import AppServer
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
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
        addr="10.57.157.93", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

"""
##RealEnb
_real_enb_pdu = HBTE(addr="10.68.87.53", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.68.88.138", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[3],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(
    system_module=[_common_unit_2],
    airscale=_real_enb,
    oam_ip=NetworkAddress("10.101.50.148"),
    instance_id=2593,
    global_bts_id=2593,
)
"""

##5GRU for classicalBTS

# _attenuator = TopYoung(ip_addr='10.68.87.55', port=1, attenuation_port_numbers=[13, 14, 15, 16])

_ru_pdu_1 = FPFH(addr="10.68.87.89", port_numbers=[2])

_ru_1 = RU(
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
    pdu_port=_ru_pdu_1.pdu_ports[2],
    radio_type=RadioTypes.AVQE,  # radio_type='AEQP'
    serial_number="L1233206045",
    #    attenuation_ports=[_attenuator.attenuator_ports[13], _attenuator.attenuator_ports[14],
    #                       _attenuator.attenuator_ports[15], _attenuator.attenuator_ports[16]]
)
_ru_pdu_2 = HBTE(addr="10.101.45.130", port_numbers=[1, 2, 3, 4, 5, 6])

_ru_2 = RU(
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
    pdu_port=_ru_pdu_2.pdu_ports[4],
    radio_type=RadioTypes.AQQL,  # radio_type='AEQP'
    serial_number="L1214204805",
    #    attenuation_ports=[_attenuator.attenuator_ports[13], _attenuator.attenuator_ports[14],
    #                       _attenuator.attenuator_ports[15], _attenuator.attenuator_ports[16]]
)
_ru_pdu_3 = HBTE(addr="10.68.87.152", port_numbers=[1, 2, 3, 4, 5, 6])

_ru_3 = RU(
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
    pdu_port=_ru_pdu_3.pdu_ports[5],
    radio_type=RadioTypes.AQQL,  # radio_type='AEQP'
    serial_number="L1212604424",
    #    attenuation_ports=[_attenuator.attenuator_ports[13], _attenuator.attenuator_ports[14],
    #                       _attenuator.attenuator_ports[15], _attenuator.attenuator_ports[16]]
)

_ru_pdu_4 = FPFH(addr="10.101.45.139", port_numbers=[1, 2, 3, 4, 5, 6])

_ru_4 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.162",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.162",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    pdu_port=_ru_pdu_4.pdu_ports[5],
    radio_type=RadioTypes.AVQE,  # radio_type='AEQP'
    serial_number="L1243304458",
)


##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.101.50.148", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.22")

_gnb_pdu = HBTE(addr="10.101.45.132", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale, rus=[_ru_1, _ru_2, _ru_3, _ru_4], f1_m_ip_addr="10.101.50.148"
)

##CU #Auto TL Upgrading
_cu = CU(
    backhaul_site_oam_ip="10.101.50.148",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.50.148", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.50.148", username="Nemuadmin", password="nemuuser"
    ),
)

##cloud_topology #UTE Type
_tl_cloud_topology = "CLOUD_5G_RPI_SB_ASIKA102R_ABILA102B4_AEQP_19B"

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="2593", global_bts_id="2593"
)

# switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="4.4.4.4", port="1/18", username="5gran", password="nokia123"
)  # EIF1 Port
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

# switch Mtor
_dell_s4048ton_ssh = SshServiceDetails(
    addr="5.5.5.5", port="1/18", username="5gran", password="nokia123"
)
_dell_s4048ton_switch = DellS4048TONSwitch(_dell_s4048ton_ssh)

# for FastMile CPE 3.2
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.247",
    user="vrf4_sg5",
    password="vrf4@sg5",
    bind_interface_ip="10.57.191.247",
    expected_prompt="[vrf4_sg5@appserver ~]$ ",
    binary_path="/home/vrf4_sg5/taf_debug/iperf",
    ports=[55930, 55931],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)


_fastmile_1 = TafUeFastmile(
    com_port="8",
    ue_pc_address="10.68.86.97",
    root_password="a7fabcb294d8",
    ue_manage_ip="192.168.1.1",
    serial_number="LPL2214005B8",
    data_transfer=[_fastmile_data_transfer_1],
    version="3.2",
    ue_pc_port="5555",
    capabilities=["REAL_FASTMILE_UE2", "nokia_fastmile"],
)


# CI_Detail_UE_Type='Nokia FastMile 5G Gateway 3.1'
# ue_config_path = os.path.join(_cfg_dir, "TestData/ue.yml")
# if os.path.isfile(ue_config_path):
#    with open(ue_config_path) as f:
#        _ue_read = f.read()
#        qci_port = re.findall("(_iperf.*?port)", _ue_read)
#        for item in qci_port:
#            _ue_read = _ue_read.replace(item, str(eval(item)))
#        _ue_config = yaml.load(_ue_read, Loader=yaml.FullLoader)
# else:
#    _ue_config = ""


# for android ue
# AppServer info
_app_server_1 = TafUeAppServer(
    app_server_name="APP_1",
    address="10.57.191.247",
    user="vrf4_sg5",
    password="vrf4@sg5",
    ports=[55932, 55933],
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
    ue_pc_port="5555",
    imei="350264683112666",
    imsi="262033100001094",
    pdns=[_pdn1],
    #    service_call_attach="17",
    #    service_call_detach="17",
    #    proxy_mngr_port="5555",
)

_netact = Netact("10.107.178.203")

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    nms=_netact,
    #    enbs=[_lte_real_enb],
    core=RealCore(mcc=262, mnc=3),
    ues=[_fastmile_1, _android_1],
    tl_cloud_topology=_tl_cloud_topology,
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
)
