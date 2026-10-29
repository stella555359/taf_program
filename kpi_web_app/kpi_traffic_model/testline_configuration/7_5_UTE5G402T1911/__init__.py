__maintainer__ = "Sebastian Mikos"
__team__ = "MN 5G&SC 5G Pz 2 WRO 5 SG"
__email__ = "I_5GSC_5G_PZ2_WRO_5@internal.nsn.com"
__owner_email__ = "sebastian.mikos@nokia.com"

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
from taf.config.testline import Connection

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))



_abil_master = CapacityUnit(addr="fsp-5a")
_abil_slave = CapacityUnit(addr="fsp-5b")
_abil_loner = CapacityUnit(addr="192.168.253.22")

# _pdu_1 = Gude("10.44.206.32", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "EPC", "8221-1")

_pdu_1 = HBTE(addr="10.71.195.74", port_numbers=[5])
_common_unit_0_pdu_port = PduPort(pdu=_pdu_1, port_no="5")
_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.208.229", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil_master, _abil_slave, _abil_loner],
    pdu_port=_common_unit_0_pdu_port,
)



# #CU
_cu = CU(
    backhaul_site_oam_ip="10.71.208.229",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.208.229", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.208.229", username="Nemuadmin", password="nemuuser"
    ),
)

_attenuator = AHBTE(
    ip_addr="10.71.203.130",
    port=5000,
    attenuation_port_numbers=[1, 2, 7, 8, 5, 6],
    model="PA-16-16-6-127-0.5-B-S",
)

# _ru_pdu = HBTE(addr="10.71.195.74", port_numbers=[5])

#AQQQA_Port1
_ru0_pdu = TopYoung(addr="10.71.195.79", port_numbers=[1])
_ru0 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="serviceuser", password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.77.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    # attenuation_ports=[
    #     _attenuator.attenuator_ports[1],
    #     _attenuator.attenuator_ports[2],
    # ],
    pdu_port=_ru0_pdu.pdu_ports[1],
    radio_type=RadioTypes.AQQQA,
)

#AQQQA_Port2
_ru1_pdu = TopYoung(addr="10.71.195.79", port_numbers=[2])
_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="serviceuser", password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.77.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    # attenuation_ports=[
    #     _attenuator.attenuator_ports[1],
    #     _attenuator.attenuator_ports[2],
    # ],
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AQQQA,
)

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_common_unit,label="SFP", port_id=1),
        target=Endpoint(unit=_ru0 ,label="SFP", port_id=3),
    )
]


_airscale = Airscale(common_units=[_common_unit])

_du = DU(airscale=_airscale, rus=[_ru0, _ru1], f1_m_ip_addr="10.71.208.229",cablinks=_ru_cablinks)

_classical_bts = ClassicalBts(cu=_cu, dus=[_du], global_bts_id=10958, instance_id=1911)

_core = RealCore5G(mcc=460, mnc=2)

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


_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.120", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_airscale.common_units[0],
            interface_type="lmp",
        )
            ],
)

_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.44.149.64", username="ute", password="ute"
    ),
    connections=[_lteenb],
)

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.139", username="vrf3_sg5", password="vrf3@sg5", port="45814"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.139",
    port="45914",
    ports=["45910", "45909"],
)

# 10.71.217.58
# noklab\nokia5g
# noki@123
_ue_pc_ssh = SshServiceDetails(
    addr="10.71.217.185", username="mn5gran", password="nokia123@"
)

_android_2 = Android(
    ssh_connection_details=_ue_pc_ssh,
    serial_number="9YS0220114010803",
    server_dir="C:/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei"],
)

_android_1 = Android(
    ssh_connection_details=_ue_pc_ssh,
    serial_number="RFCRA1HYDHV",
    server_dir="C:/pyro_server/",
    python_path="C:/Python27/python.exe",
#   qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
#   diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    iperf_directory="/data/data/com.nokia.android.application/",
    capabilities=["REAL_ANDROID_UE", "samsung"],
)

# _samsung2 = Android(
#     ssh_connection_details=_ue_pc_ssh,
#     serial_number="R3CR40XF36E",
#     server_dir="/cygdrive/c/pyro_server",
#     python_path="C:/Python27/python.exe",
#     qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
#     diag_cfg_path="C:/pyro_server/DIAG.cfg",
#     iperf_details=_iperf,
#     iperf_directory="/data/data/com.nokia.android.application/",
#     capabilities=["UE_1"],
# )
#

# _mtk_host_ssh = SshServiceDetails(
#    addr="10.71.217.92", username="nokia5g", password="noki@123"
# )


# _mtk = MediaTek(
#     ssh_connection_details=_ue_pc_ssh,
#     server_dir="c:/pyro_server",
#     server_port=8080,
#     # if use petrus mtk, the edb_file_path should be set "auto"
#     edb_file_path="C:/tools/MDDB_MT6879_S00_NR16_R2_MP_W22_03_P20.EDB",
#     # edb_file_path="C:/tools/MDDB_MT6879_S00_NR16_R2_MP_W21_48_P8.EDB",
#     imei="678965432376775",  # 手机编号
#     # imei="888876547657775",  #手机编号
#     # huashang手机编号
#     # slot1  888876547657775
#     # slot2
#     # slot1 678965432376775
#     # slot2 124578905432007
#     apn_url="dxdata2",
#     iperf_details=_iperf,
#     capabilities=["REAL_MEDIATEK_UE"],
#     serial_number="0123456789ABCDEF",
# )
# CI_Detail_UE_Type='Nokia FastMile 5G Gateway 3.1'
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.71.207.139",
    user="vrf3_sg5",
    password="vrf3@sg5",
    bind_interface_ip="10.71.207.139",
    expected_prompt="[mmw_sg5@appserver ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=[45811, 45911],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    ue_pc_address="10.57.167.120",
    root_password='V4ahj4NFvr!s9zaH',
    default_user_password='ypZx==2JdbrDGCow',
    ue_manage_ip="10.71.203.139",
    data_transfer=[_fastmile_data_transfer_1],
    serial_number='KLT234301905',
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
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
    ues=[_android_1, _android_2, _fastmile_1],
    appserver=_appserver,
    attenuator=_attenuator,
)

__all__ = ["tl"]
