import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.testpc import Connection
from taf.config.testline.core import EPCSim
from taf.config.testline import RU, DU
from taf.config.testline.pdu import HBTE
from taf.config.testline.pdu import TopYoung
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import Android
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import RealEnb
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.attenuator import AttenuationPort
from taf.config.testline.appserver import AppServer

from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.pdn import PDNTafUeAndroidDetails
from taf.config.testline.ue import TafUeFastmile, TafUeAndroid, TafUeAt
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.lmi import LMI, Local
from taf.config.testline.attenuator import HBTE as HBTEAttenuator


__maintainer__ = "Li Guiqi"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_04_01@internal.nsn.com"  # TL owner's team
__email__ = "guiqi.li@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_ru_lmi_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.71.217.56", username="mn5gran", password="nokia123@"
    )
)

_ru_lmi_pc_2 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.71.218.81", username="mn5gran", password="nokia123@"
    )
)

_ru_lmi1 = LMI(product_code="",
              host=_ru_lmi_pc_1,
              uart_mapping=[Local(port="COM40"), Local(port="COM41")])

_ru_lmi2 = LMI(product_code="",
              host=_ru_lmi_pc_2,
              uart_mapping=[Local(port="COM21"), Local(port="COM22")])

# 5GRU for classicalBTS
_ru1_pdu = HBTE(addr="10.71.196.166", port_numbers=[5])

_ru1 = RU(
    ru_hw_group="AEQZ",
    serial_number="1M202406689",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4="
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru1_pdu.pdu_ports[5],
    radio_type=RadioTypes.AEQZ,
)

_ru2_pdu = HBTE(addr="10.71.196.162", port_numbers=[5])

_ru2 = RU(
    ru_hw_group="AEQZ",
    serial_number="1M211808421",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4="
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru2_pdu.pdu_ports[5],
    radio_type=RadioTypes.AEQZ,
)

_ru3_pdu = HBTE(addr="10.71.196.170", port_numbers=[6])

_ru3 = RU(
    ru_hw_group="AEQZ",
    serial_number="1M222701263",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru3_pdu.pdu_ports[6],
    radio_type=RadioTypes.AEQZ,
)


_ru4_pdu = HBTE(addr="10.71.196.166", port_numbers=[4])

_ru4 = RU(
    ru_hw_group="AHEGB",
    serial_number="EA221152117",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="root", password="umniedziala"
    ),
    pdu_port=_ru4_pdu.pdu_ports[4],
    radio_type=RadioTypes.AHEGB,
)

_ru5_pdu = HBTE(addr="10.71.196.162", port_numbers=[3])

_ru5 = RU(
    ru_hw_group="AHEGB",
    serial_number="DH241131483",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="root", password="umniedziala"
    ),
    pdu_port=_ru5_pdu.pdu_ports[3],
    radio_type=RadioTypes.AHEGB,
)

_ru6_pdu = HBTE(addr="10.71.196.176", port_numbers=[6])

_ru6 = RU(
    ru_hw_group="AVQC",
    serial_number="1M242710768",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.56", username="mn5gran", password="nokia123@"
    ),
    pdu_port=_ru6_pdu.pdu_ports[6],
    radio_type=RadioTypes.AVQC,
    lmi=_ru_lmi1
)

_ru7_pdu = HBTE(addr="10.71.196.178", port_numbers=[4])

_ru7 = RU(
    ru_hw_group="AVQC",
    serial_number="1M242710771",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.218.81", username="mn5gran", password="nokia123@"
    ),
    pdu_port=_ru7_pdu.pdu_ports[4],
    radio_type=RadioTypes.AVQC,
    lmi=_ru_lmi2
)

_ru8_pdu = HBTE(addr="10.71.196.166", port_numbers=[6])

_ru8 = RU(
    ru_hw_group="AVQC",
    serial_number="1M251002403",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="mn5gran", password="nokia123@"
    ),
    pdu_port=_ru8_pdu.pdu_ports[6],
    radio_type=RadioTypes.AVQC,
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.71.196.164", port_numbers=[1])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.63", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
    test_pc=_gnb_test_pc_0,
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6, _ru7, _ru8],
    f1_m_ip_addr="10.71.213.112",
)

# CU
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.213.112", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.213.112", username="Nemuadmin", password="nemuuser"
    ),
)

# RealEnb
# _enb_ru5_pdu5 = TopYoung(addr="10.71.196.167", port_numbers=[5])
# _enb_ru5 = RU(
#     ru_hw_group="FHEB",
#     serial_number="EA172612614",
#     default_ssh_connection_details=SshServiceDetails(
#         addr="192.168.100.1", username="root", password="root"
#     ),
#     lmp_connection=SshServiceDetails(
#         addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
#     ),
#     pdu_port=_enb_ru5_pdu5.pdu_ports[5],
#     radio_type=RadioTypes.FHEB,
# )

_lmp_connection_enb = SshServiceDetails(
    addr="10.71.213.113", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = HBTE(addr="10.71.196.165", port_numbers=[8])
_enb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.190", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
)
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[8],
    test_pc=_enb_test_pc_0,
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(
    airscale=_real_enb,
    system_module=_real_enb,
    oam_ip=NetworkAddress(v4="10.71.213.113"),
    instance_id=611,
    rms=[]
)

# cloud_topology
_tl_cloud_topology = "I&V-HGZ-TL596"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=596, global_bts_id=596)

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.63", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

# enbPC
_enb_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.190", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_lte_real_enb.airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

# for FastMile CPE
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name='APP_SERVER_1',
    address='10.57.191.246',
    user='vrf4_sg4',
    password='vrf4@sg4',
    bind_interface_ip='10.57.191.246',
    expected_prompt='[vrf4_sg4@smw_sg4 ~]$ ',
    binary_path='/home/vrf4_sg4/taf_debug/iperf',
    ports=[54596, 54696])
 
_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name='iperf',
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path='iperf',
    version=2)


_fastmile_1 = TafUeFastmile(
    ue_pc_address='10.57.155.63',
    root_password='Xo6SL7Tcfb@CF6Td',
    default_user_password='J!jrkTR.,CQXtug:',
    ue_manage_ip='10.71.213.148',
    serial_number='KLT232200D5E',
    version='receiver 5g19a',
    data_transfer=[_fastmile_data_transfer_1],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"]
)

# Shared PDN configuration
_android_pdn_1 = PDNTafUeAndroidDetails(
    entryName="dxstatic8", apnName="dxstatic8", apnType=["DEFAULT"]
)

def create_android_ue(ue_number, serial_number, capabilities, bind_ue_ip, imei=None, imsi=None,
                     interface_name=None, qualcomm_prototype=False, port_offset=0):
    """Create Android UE configuration with app server and data transfer"""
    base_port = 54610 + ue_number
    
    appserver = TafUeAppServer(
        app_server_name="APP_SERVER_2",
        address="10.57.191.246",
        user="vrf4_sg4",
        password="vrf4@sg4",
        bind_interface_ip="10.57.191.246",
        binary_path='/home/vrf4_sg4/taf_debug/iperf',
        ports=[base_port + port_offset, base_port + port_offset - 500],
    )
    
    data_transfer_kwargs = {
        "protocol_name": "iperf",
        "app_server": appserver,
        "interval": 1,
        "bind_ue_ip": bind_ue_ip,
        "server_close_delay": 50,
        "binary_path": '/data/local/tmp/iperf',
    }
    if interface_name:
        data_transfer_kwargs["interface_name"] = interface_name
    
    data_transfer = TafUeDataTransferProtocol(**data_transfer_kwargs)
    
    ue_kwargs = {
        "serial_number": serial_number,
        "capabilities": capabilities,
        "ue_pc_address": "10.0.176.195",
        "proxy_mngr_port": 9955,
        "ueproxy_force_release": True,
        "data_transfer": [data_transfer],
        "ssh_connection_details": SshServiceDetails(
            addr="10.0.176.195", username="mn5gran", password="nokia123@"
        ),
        "imei": imei,
        "imsi": imsi,
        "pdns": [_android_pdn_1],
        "allow_kw_logs": False,
    }
    if qualcomm_prototype:
        ue_kwargs["qualcomm_prototype"] = True
    
    return TafUeAndroid(**ue_kwargs)

# CI_Detail_UE_Type='Samsung s24'
_android_1 = create_android_ue(
    ue_number=1,
    serial_number="RFCX217F2ER",
    capabilities=["REAL_ANDROID_UE1", "samsung"],
    bind_ue_ip="10.64.21.183",
    interface_name="rmnet_data0",
    port_offset=1
)

# CI_Detail_UE_Type='MTK MT6986D k6991'
_android_2 = create_android_ue(
    ue_number=2,
    serial_number="abdc12541ge",
    capabilities=["REAL_ANDROID_UE2", "mtk"],
    bind_ue_ip="10.64.21.191",
    interface_name="wwan2",
    port_offset=2
)

_android_3 = create_android_ue(
    ue_number=3,
    serial_number="0123456789ABCDEF",
    capabilities=["REAL_ANDROID_UE3", "mtk"],
    bind_ue_ip="10.64.21.188",
    interface_name="wwan2",
    port_offset=3
)

# CI_Detail_UE_Type='MTP DX85'
_android_4 = create_android_ue(
    ue_number=4,
    serial_number="3df2fa49",
    capabilities=["REAL_ANDROID_UE4", "qualcomm"],
    bind_ue_ip="10.64.21.184",
    qualcomm_prototype=True,
    port_offset=4
)

_android_5 = create_android_ue(
    ue_number=5,
    serial_number="549178b1",
    capabilities=["REAL_ANDROID_UE5", "xiaomi"],
    bind_ue_ip="10.64.21.192",
    interface_name="rmnet_data0",
    port_offset=5
)

_android_6 = create_android_ue(
    ue_number=6,
    serial_number="a770fdb4",
    capabilities=["REAL_ANDROID_UE6", "qualcomm"],
    bind_ue_ip="10.64.21.187",
    qualcomm_prototype=True,
    port_offset=6
)


_hbte_attenuator = HBTEAttenuator(ip_addr="10.71.205.178",
                                  port=5000,
                                  attenuation_port_numbers=[1, 2, 3, 4, 9, 10, 11, 12],
                                  model='PA-16-16-6-127-0.5-B-S')


tl = TestLine(
    test_pc=_host,
    test_pcs=[_host, _enb_pc],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_fastmile_1, _android_1, _android_2, _android_3, _android_4, _android_5, _android_6],
    attenuators=[_hbte_attenuator]
)
