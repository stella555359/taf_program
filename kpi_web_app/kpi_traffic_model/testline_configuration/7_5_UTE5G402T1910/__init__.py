__maintainer__ = "Sebastian Mikos"
__team__ = "MN 5G&SC 5G Pz 2 WRO 5 SG"
__email__ = "I_5GSC_5G_PZ2_WRO_5@internal.nsn.com"
__owner_email__ = "sebastian.mikos@nokia.com"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline.pdu import Gude
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline import DU, RU
from taf.config.testline.core import RealCore5G
from taf.config.testline import RealEnb, NetworkAddress, RoutingInformation
from taf.config.testline.ue import Android, Qualcomm

from taf.config.testline.ue import MediaTek

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.120", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_abil_master = CapacityUnit(addr="fsp-5a")
_abil_slave = CapacityUnit(addr="fsp-5b")
_abil_loner = CapacityUnit(addr="192.168.253.22")

_pdu_1 = Gude("10.44.206.32", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "EPC", "8221-1")

_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil_master, _abil_slave, _abil_loner],
    pdu_port=_pdu_1.pdu_ports[8],
)

_airscale = Airscale([_common_unit])


# #CU
_cu = CU(
    backhaul_site_oam_ip="10.71.208.228",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.208.228", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.208.228", username="Nemuadmin", password="nemuuser"
    ),
)

_attenuator = AHBTE(
    ip_addr="10.71.203.130",
    port=5000,
    attenuation_port_numbers=[1, 2, 7, 8, 5, 6],
    model="PA-16-16-6-127-0.5-B-S",
)

_ru0 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziela"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.77.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
    ],
)

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziela"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.77.130", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    attenuation_ports=[
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)


_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziela"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.77.131", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
    ],
)


_du = DU(airscale=_airscale, rus=[_ru0, _ru1, _ru2], f1_m_ip_addr="10.71.208.228")


_classical_bts = ClassicalBts(cu=_cu, dus=[_du], global_bts_id=10957, instance_id=1910)

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
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abia],
)

_lteenb = RealEnb(
    airscale=Airscale(common_units=[_asia]),
    x2_link_addr=NetworkAddress(
        v4="10.71.208.203",
        routing=RoutingInformation(gateway="10.71.208.193", ip_prefix_length=27),
    ),
    global_bts_id=10080,
)

_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.44.149.64", username="ute", password="ute"
    ),
    connections=[_lteenb],
)

_appserver_ssh = SshServiceDetails(
    addr="10.71.219.27", username="mmw_sg5", password="mm@5", port="45238"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.27",
    port="45338",
    ports=["45910", "45909"],
)

_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.58", username="nokia5g", password="noki@123"
    ),
    # serial_number="RFCR10X4W5A",  # R5CN20LYP5R R5CN20HRWLM R5CN212N3RX R3CR40XF36E RFCR10X4W5A
    serial_number="R5CN30YKEJK",  # R5CN20LYP5R R5CN20HRWLM R5CN212N3RX R3CR40XF36E RFCR10X4W5A
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "samsung", "UE_2"],
    #service_call_attach="14",
    service_call_attach="16",
)
_ue_pc_ssh = SshServiceDetails(
    addr="10.71.217.58", username="nokia5g", password="noki@123"
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

_samsung3 = Android(
    ssh_connection_details=_ue_pc_ssh,
    serial_number="R5CT32189CK",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    iperf_directory="/data/data/com.nokia.android.application/",
    capabilities=["REAL_ANDROID_UE","samsung","UE_1"],
    service_call_attach="16",
)


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

_appserver = AppServer(iperf_details=_iperf)

tl = TestLine(
    test_pc=_test_pc,
    test_pcs=[_test_pc, _test_pc_enb],
    gnbs=[_classical_bts],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_QC_ASIBR_ABIN1_2xAHLOA_ENB",
    core=_core,
    enbs=[_lteenb],
    #ues=[_android, _samsung2, _mtk],
    ues=[_android,  _samsung3],
    appserver=_appserver,
    attenuator=_attenuator,
)

__all__ = ["tl"]
