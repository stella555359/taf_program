import os
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.testpc import Connection
from taf.config.testline.core import RealCore
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
)  # added in taf.meta 5.4
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.appserver import AppServer
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android, MediaTek, TafUeAt

from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.ue import TafUeAndroid

__maintainer__ = "Zheng Mengya"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_3_GMS <I_MN_5G_RAN_IV4_LINE_HZG_3@internal.nsn.com>"
)
__email__ = "mengya.zheng@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #test PC
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.94", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_qc_host_ssh = SshServiceDetails(
    addr="10.64.57.61", username="mn5gran", password="nokia123@"
)


_appserver_ssh = SshServiceDetails(
     addr="10.57.191.242",
     username="vrf4_sg13",
     password="vrf4@13",
     port="33803",
 )
 
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.242",
)

_appserver = AppServer(_iperf_details_on_appserver)


_app_server_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.242",
    user="vrf4_sg13",
    password="vrf4@sg13",
    bind_interface_ip="10.57.191.242",
    expected_prompt="\\[vrf4_sg13.*\\$ ",
    ports=[33802, 33801]
)

_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_app_server_1,
    interval=1,
    # binary_path="/usr/bin/",
    interface_name="dxstatic8",
    version=2,
    dt_from_uepc=False,
)

_data_transfer_ping = TafUeDataTransferProtocol(
    protocol_name="ping", app_server=_app_server_1, interval=1
)

_data_transfer_ftp = TafUeDataTransferProtocol(
    protocol_name="ftp", app_server=_app_server_1, interval=1
)

_android1 = TafUeAndroid(
   serial_number="3879376",  # import,check by "adb ls"
   # capabilities=['REAL_UE', "samsung_ue"],
   capabilities=["qualcomm"],
   ue_pc_address="10.64.57.61",
   data_transfer=[_data_transfer_iperf,
                  _data_transfer_ping,
                  _data_transfer_ftp],
   phone_number="+8613032996485",
   ue_pc_port="8080",
   imei="004403160394989",
   imsi="262033100011009",
   qualcomm_prototype=True,
   # service_call_attach='17',
   # service_call_detach='17',
)


# #5GRU for classicalBTS
# attenuator
_attenuator = TopYoung(
    ip_addr="10.69.9.130",
    port=28888,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="MCS2350A2-64B16-E6",
)

_ru1_pdu = HBTE(addr="10.64.49.32", port_numbers=[2])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.154", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.154", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AQQL.value,
)

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIO",
    rus=[_ru1],
)

_gnb_pdu = HBTE(addr="10.64.49.34", port_numbers=[8])

_ru_cablinks = [Cablink(source=Endpoint(unit=_capacity_unit, label='SFP', port_id=1), target=Endpoint(unit=_ru1, label='SFP', port_id=1)),
                Cablink(source=Endpoint(unit=_capacity_unit, label='SFP', port_id=2), target=Endpoint(unit=_ru1, label='SFP', port_id=2)),
                ]

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[8],
    hardware_type="ASIB",
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru1],
    f1_m_ip_addr="10.64.54.98",
    f1_c_ip_addr="10.64.54.98",
    f1_u_ip_addr="10.64.54.98",
    cablinks=_ru_cablinks,
)


# #CU

_cu = CU(backhaul_site_oam_ip=NetworkAddress(v4='10.64.54.98', vlan_id=None,
                                             routing=RoutingInformation(gateway='10.64.54.96', ip_prefix_length=27)),
    oam_ssh_connection_details=SshServiceDetails(addr='10.64.54.98', username='toor4nsn', password='oZPS0POrRieRtu'),
    oam_http_connection_details=HttpConnectionDetails(addr='10.64.54.98', username='Nemuadmin', password='nemuuser'),
    x2c=NetworkAddress(v4='10.64.54.98', vlan_id=None,
                       routing=RoutingInformation(gateway='10.64.54.96', ip_prefix_length=27)),
    x2u=NetworkAddress(v4='10.64.54.98', vlan_id=None,
                       routing=RoutingInformation(gateway='10.64.54.96', ip_prefix_length=27)),
    s1u=NetworkAddress(v4='10.64.54.98', vlan_id=None,
                       routing=RoutingInformation(gateway='10.64.54.96', ip_prefix_length=27)))


_classical_bts0 = ClassicalBts(dus=[_du], cu=_cu, instance_id=37363, global_bts_id=37363)

# #host
_gnb_testpc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.94", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts0.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)


tl = TestLine(
    test_pc=_gnb_testpc,
    test_pcs=[_gnb_testpc],
    gnbs=[_classical_bts0],
    core=RealCore(mcc=262,mnc=3),
    #ues=[_at1],
    #ues=[_qc3, _qc4],
    ues=[_android1],
#    #ues=[_an1, _an2, _an3, _an4],
    appserver=_appserver,
    attenuator=[_attenuator],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIL_2ABIO_AVQA_ENB",
)