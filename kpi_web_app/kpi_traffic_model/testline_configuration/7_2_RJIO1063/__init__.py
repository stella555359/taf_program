import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.enb import RealEnb
from taf.config.testline.radio import RU
from taf.config.testline.attenuator import TopYoung
from taf.config.testline.gnb.gnb import CU, ClassicalBts
from taf.config.testline.gnb import DU 
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import RRB
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeAndroid, TafUeAt, PluginAtClassType

__maintainer__ = "arunkumar a"
__team__ = "MN RAN PZ BLR SG02"
__email__ = "arunkumar.a@nokia.com"
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.58.238.164", username="ute", password="BT5l@bus3rl0g1n"
    )
)
_app_server_1 = TafUeAppServer(app_server_name="APP_1",
                               address="10.58.241.84",
                               user="ftpuser",
                               password="ftpuser",
                               bind_interface_ip="10.58.241.84",
                               expected_prompt="ftpuser")
_data_transfer_iperf = TafUeDataTransferProtocol(protocol_name='iperf',
                                                 app_server=_app_server_1,
                                                 interval=1,
                                                 server_close_delay=50,
                                                 version=2,
                                                 )
_data_transfer_iperf_simcom = TafUeDataTransferProtocol(protocol_name='iperf',
                                                        app_server=_app_server_1,
                                                        interval=1,
                                                        interface_name='Cellular 3',
                                                        binary_path='/cygdrive/c/iperf/',
                                                        server_close_delay=50,
                                                        version=2,
                                                        dt_from_uepc=True)
_data_transfer_ping = TafUeDataTransferProtocol(protocol_name='ping',
                                                app_server=_app_server_1,
                                                interval=1)
_data_transfer_ftp = TafUeDataTransferProtocol(protocol_name='ftp',
                                               app_server=_app_server_1,
                                               interval=1)
# UE PC loding details
ue_pc_details=SshServiceDetails(addr="10.45.150.250",
                                username='inbabtslabuser',
                                password='BT5l@bus3rl0g1n')

# taf UE config ue_1
_android1 = TafUeAndroid(serial_number='H0B9FI1LV01C2400110',
                         capabilities=['REAL_UE'],
                         ue_pc_address='10.45.150.250',
                         data_transfer=[_data_transfer_iperf,
                                        _data_transfer_ping,
                                        _data_transfer_ftp],
                         ssh_connection_details=ue_pc_details,
                         )

# taf.ue.access.simcom
_at_1 = TafUeAt(com_port='27',
                capabilities=['Simcom_UE_1'],
                ue_pc_address='10.45.150.250',
                ue_pc_login='inbabtslabuser',
                ue_pc_password='BT5l@bus3rl0g1n',
                ue_pc_expected_prompt='inbabtslabuser',
                data_transfer=[_data_transfer_iperf_simcom],
                ue_pc_port='80',
                class_name=PluginAtClassType.simcom)          

_pdu_ru_1 = RRB(
    addr="10.58.242.152",
    port_numbers=[5, 6]
)
_pdu_gnb = RRB(
    addr="10.58.242.151",
    port_numbers=[6]
)
_pdu_ru_2 = RRB(
    addr="10.58.242.154",
    port_numbers=[7]
)
_pdu_ru_1.pdu_ports[5].contactor = "NORMALLY_OPENED"
_pdu_ru_1.pdu_ports[6].contactor = "NORMALLY_OPENED"
_pdu_gnb.pdu_ports[6].contactor = "NORMALLY_OPENED"
_pdu_ru_2.pdu_ports[7].contactor = "NORMALLY_OPENED"

# attenuator configuration
_attenuator1 = TopYoung(ip_addr = "10.45.153.215",
                        port = 3001,
                        attenuation_port_numbers = [1, 2, 3, 4, 6, 7],
                        model = "TAS16T16-51-120-1N-DEJS",
                        )
# vendor = "TopYoung"
# BTS_1060 Port : 9,10,11,12,13,14
# BTS 1055 PVA IP : 10.45.153.210
# BTS_1055 Port
# PVA_1 AQQJ RMOD-1
_ru_0 = RU(
    ru_hw_group="hw_group",
    pdu_port=_pdu_ru_2.pdu_ports[7],
    radio_type="AQQJ",
    attenuation_ports=[
        _attenuator1.attenuator_ports[1],
    ],
)
# PVA_2 AQQJ RMOD-2
_ru_1 = RU(
    ru_hw_group="hw_group",
    pdu_port=_pdu_ru_1.pdu_ports[6],
    radio_type="AQQJ",
    attenuation_ports=[
        _attenuator1.attenuator_ports[2],
    ],

)
_ru_2 = RU(
    ru_hw_group="hw_group",
    pdu_port=_pdu_ru_1.pdu_ports[5],
    radio_type="AEQZ",
    attenuation_ports=[
        _attenuator1.attenuator_ports[3],
    ],
)

_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="6.6.6.6")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_pdu_gnb.pdu_ports[6],
    hardware_type="ASOE",
    hardware_version="A.103",
    serial_number="DH224013240",
    test_pc=_host
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru_0, _ru_1, _ru_2], f1_m_ip_addr="10.58.239.158",
)

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress("10.58.239.158"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.58.239.158", username="Nemuadmin", password="nemuuser"
    ),
)

_tl_cloud_topology = "RJIO_ASOE_2AQQJ_1AEQZ"

_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, global_bts_id="1063",
)

_host.connections.append(
    Connection(
        interface="eth1",
        device=_classical_bts.dus[0].airscale.common_units[0],
        interface_type="lmp",
    )
)


_lmp_connection_enb = SshServiceDetails(
    addr="10.58.239.158", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = RRB(addr="10.58.242.138", port_numbers=[2])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[2],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb, oam_ip="10.58.239.158", rms=None)


tl = TestLine(
    test_pc=_host,
    test_pcs=[_host],
    attenuator=[_attenuator1],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    ues=[_android1, _at_1,],
    tl_cloud_topology=_tl_cloud_topology,
)

__all__ = ["tl"]
