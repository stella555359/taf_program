__maintainer__ = "ChenXu"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05_GMS"
__email__ = "xu.2.chen@nokia-sbell.com"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline.pdu import Gude, HBTE, TopYoung, PduPort
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer, TafUeAppServer
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline import DU, RU
from taf.config.testline.core import RealCore5G
from taf.config.testline import RealEnb, NetworkAddress, RoutingInformation
from taf.config.testline.ue import Android, Qualcomm, TafUeFastmile
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.ue import MediaTek
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.18", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_abil_master = CapacityUnit(addr="fsp-5a")
_abil_slave = CapacityUnit(addr="fsp-5b")
_abil_loner = CapacityUnit(addr="192.168.253.22")

# _pdu_1 = Gude("10.44.206.32", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "EPC", "8221-1")

_pdu_1 = HBTE(addr="10.71.195.74", port_numbers=[5])
_common_unit_0_pdu_port = PduPort(pdu=_pdu_1, port_no="5")
_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.106.223.229", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil_master, _abil_slave, _abil_loner],
    pdu_port=_common_unit_0_pdu_port,
)

_airscale = Airscale(common_units=[_common_unit])

# #CU
_cu = CU(
    backhaul_site_oam_ip="10.106.223.229",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.106.223.229", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.106.223.229", username="Nemuadmin", password="nemuuser"
    ),
)

_attenuator = AHBTE(
    ip_addr="10.71.203.130",
    port=5000,
    attenuation_port_numbers=[1, 2, 7, 8, 5, 6],
    model="PA-16-16-6-127-0.5-B-S",
)

# _ru_pdu = HBTE(addr="10.71.195.74", port_numbers=[5])
_ru_pdu = TopYoung(addr="10.71.195.79", port_numbers=[1])

_ru0 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="rfsw", password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.77.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    # attenuation_ports=[
    #     _attenuator.attenuator_ports[1],
    #     _attenuator.attenuator_ports[2],
    # ],
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AQQQA,

)

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_common_unit,label="SFP", port_id=1),
        target=Endpoint(unit=_ru0 ,label="SFP", port_id=3),
    )
]

_du = DU(airscale=_airscale, rus=[_ru0], f1_m_ip_addr="10.106.223.229",cablinks=_ru_cablinks)

_classical_bts = ClassicalBts(cu=_cu, dus=[_du], global_bts_id=11542, instance_id=1932)

_core = RealCore5G(mcc=262, mnc=3)

_core_ssh = SshServiceDetails(addr="10.42.61.65", username="5g", password="2019H@slo")

_common_unit_lte_ssh = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_common_unit_lte = CommonUnit(
    _common_unit_lte_ssh, capacity_units=[_capacity_unit], pdu_port=None
)

_abia = CapacityUnit(addr="192.168.253.20")

_asia = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.208.203", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abia],
)

_lteenb = RealEnb(
    airscale=Airscale(common_units=[_asia]),
    x2_link_addr=NetworkAddress(
        v4="10.71.208.203",
        routing=RoutingInformation(gateway="10.71.208.193", ip_prefix_length=27),
    ),
    global_bts_id=10080, instance_id=1968
)

_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.44.149.64", username="ute", password="ute"
    ),
    connections=[_lteenb],
)

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.139", username="vrf3_sg5", password="vrf3@sg5", port="45932"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.139",
    port="45932",
    ports=["45832", "45932"],
)

# 10.71.217.58
# noklab\nokia5g
# noki@123
_ue_pc_ssh = SshServiceDetails(
    addr="10.106.223.68", username="nokia5g", password="noki@123"
)

_samsung1 = Android(
    ssh_connection_details=_ue_pc_ssh,
    serial_number="RFCR11CSPTZ",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    iperf_directory="/data/data/com.nokia.android.application/",
    capabilities=["REAL_ANDROID_UE", "samsung", "UE_1"],
    service_call_attach="16",
)


_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.71.207.139",
    user="vrf3_sg5",
    password="vrf3@sg5",
    bind_interface_ip="10.71.207.139",
    expected_prompt="[vrf3_sg5@appserver ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=[45832, 45932],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    ue_pc_address="10.57.177.18",
    root_password='4HU9CNDA3h65b435',
    default_user_password='4NdN4A96yiL.wncS',
    ue_manage_ip="10.106.223.87",
    data_transfer=[_fastmile_data_transfer_1],
    serial_number='KLT232200B14',
    ue_pc_port=5555,
    version='receiver 5g19a',
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

_fastmile_2 = TafUeFastmile(
    ue_pc_address="10.57.177.18",
    root_password='YY,nroLuLvUMYJL7',
    default_user_password='SpCW,.GAX62UATpt',
    ue_manage_ip="10.106.223.86",
    data_transfer=[_fastmile_data_transfer_1],
    serial_number='KLT232200A7C',
    ue_pc_port=5555,
    version='receiver 5g19a',
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

_fastmile_3 = TafUeFastmile(
    ue_pc_address="10.57.177.18",
    root_password='mY!Zd3=UnrSduKVh',
    default_user_password='Ec+iL_c29exiC+y5',
    ue_manage_ip="10.106.223.88",
    data_transfer=[_fastmile_data_transfer_1],
    serial_number='KLT232200C2C',
    ue_pc_port=5555,
    version='receiver 5g19a',
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

_fastmile_4 = TafUeFastmile(
    ue_pc_address="10.57.177.18",
    root_password='zbMvLtRU4oFrre6T',
    default_user_password='omau4:.:wmAx2KQJ',
    ue_manage_ip="10.106.223.89",
    data_transfer=[_fastmile_data_transfer_1],
    serial_number='KLT232200A2A',
    ue_pc_port=5555,
    version='receiver 5g19a',
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

_fastmile_5 = TafUeFastmile(
    ue_pc_address="10.57.177.18",
    root_password='ibDznNYq,CfWDG5u',
    default_user_password='JjLxZx=VztHUKxWf',
    ue_manage_ip="10.106.223.92",
    data_transfer=[_fastmile_data_transfer_1],
    serial_number='KLT232200AF5',
    ue_pc_port=5555,
    version='receiver 5g19a',
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

_fastmile_6 = TafUeFastmile(
    ue_pc_address="10.57.177.18",
    root_password='xgYnT3q@G4d4UdKM',
    default_user_password='oA@MRcsXLWz9umHP',
    ue_manage_ip="10.106.223.93",
    data_transfer=[_fastmile_data_transfer_1],
    serial_number='KLT232200C7B',
    ue_pc_port=5555,
    version='receiver 5g19a',
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

_fastmile_7 = TafUeFastmile(
    ue_pc_address="10.57.177.18",
    root_password='As9SgPULzM94:@:c',
    default_user_password='bp7-+sMc+YDwrRoQ',
    ue_manage_ip="10.106.223.94",
    data_transfer=[_fastmile_data_transfer_1],
    serial_number='KLT232200CF5',
    ue_pc_port=5555,
    version='receiver 5g19a',
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

_fastmile_8 = TafUeFastmile(
    ue_pc_address="10.57.177.18",
    root_password='vrtMas+xAo+a:vnj',
    default_user_password='pKUczMdsAKpC4M-m',
    ue_manage_ip="10.108.135.198",
    data_transfer=[_fastmile_data_transfer_1],
    serial_number='KLT232200CD0',
    ue_pc_port=5555,
    version='receiver 5g19a',
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

_fastmile_9 = TafUeFastmile(
    ue_pc_address="10.57.177.18",
    root_password='8KTAx%4AtG82n5cH',
    default_user_password='jaPdGPFsfji+U2QV',
    ue_manage_ip="10.108.135.199",
    data_transfer=[_fastmile_data_transfer_1],
    serial_number='KLT230800002',
    ue_pc_port=5555,
    version='receiver 5g19a',
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

_fastmile_10 = TafUeFastmile(
    ue_pc_address="10.57.177.18",
    root_password='XofwUfr.29dk@C:H',
    default_user_password='Mr.w=e,Hdxm:X!Rd',
    ue_manage_ip="10.108.135.200",
    data_transfer=[_fastmile_data_transfer_1],
    serial_number='KLT232200B38',
    ue_pc_port=5555,
    version='receiver 5g19a',
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

_appserver = AppServer(iperf_details=_iperf)

tl = TestLine(
    test_pc=_test_pc,
    test_pcs=[_test_pc, _test_pc_enb],
    gnbs=[_classical_bts],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_QC_ASIBR_ABIN1_2xAHLOA_ENB",
    core=_core,
    enbs=[_lteenb],
    # ues=[_android, _samsung2, _mtk],
    ues=[_fastmile_1, _fastmile_2, _fastmile_3, _fastmile_4, _fastmile_5, _fastmile_6, _fastmile_7, _fastmile_8, _fastmile_9, _fastmile_10],
    appserver=_appserver,
    attenuator=_attenuator,
)

__all__ = ["tl"]
