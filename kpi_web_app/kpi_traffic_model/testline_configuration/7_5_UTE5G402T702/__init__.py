__maintainer__ = "Zhangshanshan"
__team__ = "I_MN_5G_RAN_IV4_QT_HZG_GMS <I_MN_5G_RAN_IV4_QT_HZG@internal.nsn.com>"
__email__ = "I_MN_5G_RAN_IV4_QT_HZG@internal.nsn.com"
__owner_email__ = "shanshan.zhang@nokia-sbell.com"

import os
import yaml
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
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
# from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.core import EPCSim
from taf.config.testline.enb import RealEnb
from taf.config.testline.ue import TM500, Android
from taf.config.testline import DU, RU
from taf.config.testline.attenuator import (
    AttenuationPort,
    HBTE,
)

# added in taf.meta 5.4
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
    ASC,
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
from taf.config.testline.appserver import AppServer
from taf.config.testline.ue import MediaTek

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_attenuator = HBTE(
    ip_addr="10.101.37.240",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.74", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_cu = CU(
    backhaul_site_oam_ip="10.101.48.66",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.48.66", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.48.66", username="Nemuadmin", password="nemuuser"
    ),
)

_cu_1 = CU(
    backhaul_site_oam_ip="10.101.48.79",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.48.79", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.48.79", username="Nemuadmin", password="nemuuser"
    ),
)


# DU
_common_unit_pdu = FACOM(addr="10.71.197.130", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_common_unit_pdu1 = FACOM(addr="10.71.197.131", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_lmp_connection_0 = SshServiceDetails(
    addr="10.101.48.66", username="toor4nsn", password="oZPS0POrRieRtu"
)

_lmp_connection_1 = SshServiceDetails(
    addr="10.101.48.79", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.17")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[2],
)

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_1,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu1.pdu_ports[2],
)


# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])
_airscale_1 = Airscale(common_units=[_common_unit_1])

# 5G RU
_ru_pdu = FACOM(addr="10.57.243.10", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])


_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[8],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)

_du_0 = DU(airscale=_airscale_0, rus=[_ru], f1_m_ip_addr="10.101.48.66")
_du_1 = DU(airscale=_airscale_1, rus=[_ru], f1_m_ip_addr="10.101.48.79")


_cbts = ClassicalBts(cu=_cu, dus=[_du_0], global_bts_id="11154", instance_id="11154")
_cbts_1 = ClassicalBts(
    cu=_cu_1, dus=[_du_1], global_bts_id="37394", instance_id="37394"
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.197", username="vrf3_sg4", password="vrf3@sg4", port="44311"
)

_mtk_host_ssh = SshServiceDetails(
    addr="10.71.217.236", username="nokia5G", password="noki@123"
)

_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="",
    iperf_path="C:/Tool/iperf-2.0.9-win64/iperf",
    port="44252",
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.70.222.53",
    iperf_path="/usr/bin/iperf",
    # iperf_path='/cygdrive/c/iperf',
    port="44251",
    ports=[44251, 44252, 44253, 44254, 44255, 44256, 44257, 44258, 44259, 44260],
)

_iperf_1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.24",
    iperf_path="/usr/bin/iperf",
    # iperf_path='/cygdrive/c/iperf',
    port="44251",
    ports=[44900, 44901, 44902, 44903, 44904, 44905, 44906, 44258, 44259, 44260],
)


_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.191", username="nokia5g", password="noki@123"
    ),
    serial_number="782b8dcb",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Users/nokia5G/AppData/Local/Programs/Python/Python310/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    imsi="262030100011588",
    capabilities=["qct_dx50", "X55"],
)

_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.191", username="nokia5g", password="noki@123"
    ),
    serial_number="ad52015b",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Users/nokia5G/AppData/Local/Programs/Python/Python310/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    imsi="262033032994023",
    capabilities=["qct_dx50", "X551"],
)

_android_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.191", username="nokia5g", password="noki@123"
    ),
    serial_number="ebf15aec",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Users/nokia5G/AppData/Local/Programs/Python/Python310/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_1,
    imsi="262033032994025",
    capabilities=["qct_dx50", "X70"],
)

_android_3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.191", username="nokia5g", password="noki@123"
    ),
    serial_number="5c8e459f",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Users/nokia5G/AppData/Local/Programs/Python/Python310/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    imsi="262033100010732",
    capabilities=["qct_dx50", "X55"],
)

# _mtk = MediaTek(
#     ssh_connection_details=_mtk_host_ssh,
#     server_dir="c:/pyro_server",
#     server_port=8080,
#     edb_file_path=r"C:\Users\nokia5g\Desktop\MDDB_MT6298_S00_NR16_R2_MP_W22_33_P8.EDB",
#     log_filter="2.Gen98_Default_Standard",
#     imei="12345678901234",
#     imsi="262033100007824",
#     apn_url="dxdata1",
#     iperf_details=_iperf_details_on_mtk,
#     capabilities=["REAL_MEDIATEK_UE", "NSA"],
# )

# #Qualcomm

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.70.222.53",
    iperf_path="iperf",
    port="44251",
)

_appserver = AppServer(_iperf_details_on_appserver)

# CI_Detail_UE_Type='Samsung;Samsung;Samsung;Samsung'
# #Qualcomm

_epcsim = EPCSim(
    mme_ip="192.168.4.1",
    mcc=777,
    mnc=44,
    tac=777,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.76", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    dir_path="/opt/wts/latest",
    cfg_filename="TL101_basic_cfg_realLteEnb.cfg",
    edaemon_port="22222",
    egate_port="20021",
)
# #RealEnb---------------------------------------------------------
# eNB-251
_enb1_pdu = FACOM(addr="10.71.197.130", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_enb1_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.216.8", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_enb1_pdu.pdu_ports[2],
)

_real_enb_1 = Airscale(common_units=[_enb1_common_unit])

_lte_real_enb_1 = RealEnb(airscale=_real_enb_1, instance_id=10705, global_bts_id=10705)

# eNB-48
_enb2_pdu = FACOM(addr="10.71.197.131", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_enb2_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.216.3", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_enb2_pdu.pdu_ports[2],
)

_real_enb_2 = Airscale(common_units=[_enb2_common_unit])

_lte_real_enb_2 = RealEnb(airscale=_real_enb_2, instance_id=10706, global_bts_id=10706)


tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts, _cbts_1],
    core=_epcsim,
    enbs=[_lte_real_enb_1, _lte_real_enb_2],
    attenuator=_attenuator,
    ues=[_android_0, _android_1, _android_2, _android_3],
    appserver=_appserver,
)


__all__ = ["tl"]
