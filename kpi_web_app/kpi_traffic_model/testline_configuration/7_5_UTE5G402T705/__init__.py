__maintainer__ = "Liu Steven"
__team__ = "I_MN_5G_RAN_IV4_QT_HZG_GMS <I_MN_5G_RAN_IV4_QT_HZG@internal.nsn.com>"
__email__ = "I_MN_5G_RAN_IV4_QT_HZG@internal.nsn.com"
__owner_email__ = "steven.liu@nokia-sbell.com"

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
from taf.compatibility.configuration import TestlineWrapper
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
from taf.config.testline import LicenseKeeper

_cfg_dir = os.path.dirname(os.path.abspath(__file__))
_licensekeeper = LicenseKeeper(username="HAZ3_SG4", password="HAZ3_SG4")

_attenuator = HBTE(
    ip_addr="10.101.36.66",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.160", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_cu = CU(
    backhaul_site_oam_ip="10.68.88.71",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.88.71", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.88.71", username="Nemuadmin", password="nemuuser"
    ),
)

_cu_1 = CU(
    backhaul_site_oam_ip="10.68.88.78",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.88.78", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.88.78", username="Nemuadmin", password="nemuuser"
    ),
)


# DU
_common_unit_pdu = FACOM(addr="10.68.87.41", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_lmp_connection_0 = SshServiceDetails(
    addr="10.68.88.71", username="toor4nsn", password="oZPS0POrRieRtu"
)

_lmp_connection_1 = SshServiceDetails(
    addr="10.68.88.78", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.17")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[1],
    test_pc=_test_pc,
)

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_1,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[1],
    test_pc=_test_pc,
)

# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])
_airscale_1 = Airscale(common_units=[_common_unit_1])

# 5G RU
_ru_pdu = FACOM(addr="10.68.87.35", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru = RU(
    ru_hw_group="AWHQX",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.195", username="ute", password="iW_K#8.ute%A10h0m0ra"
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
    radio_type=RadioTypes.AWHQX,
    serial_number="EB2202R0016",
)

_du_0 = DU(airscale=_airscale_0, rus=[_ru], f1_m_ip_addr="10.68.88.71")
_du_1 = DU(airscale=_airscale_1, rus=[_ru], f1_m_ip_addr="10.68.88.78")


_cbts = ClassicalBts(cu=_cu, dus=[_du_0], global_bts_id="37520", instance_id="11388")
_cbts_1 = ClassicalBts(cu=_cu_1, dus=[_du_1], global_bts_id="11385", instance_id="11385")

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.148", username="vrf3_sg4", password="vrf3@sg4", port="44378"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.148",
    iperf_path="/usr/bin/iperf",
    # iperf_path='/cygdrive/c/iperf',
    port="55300",
    ports=["55300", "55301", "55302", "55303"],
)

# #Qualcomm

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.148",
    iperf_path="/usr/bin/iperf",
    port="55300",
    ports=["55300", "55301", "55302", "55303"],
)

_appserver = AppServer(_iperf_details_on_appserver)

spark_UE_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.234", username="nokia5g", password="noki@123"
    ),
    serial_number="886c9360",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sigspark_multiUE", "sigspark"],
    imsi="262033032996917",
    licensekeeper=_licensekeeper,
)

spark_UE_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.234", username="nokia5g", password="noki@123"
    ),
    serial_number="9216badb",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sigspark_multiUE", "sigspark"],
    imsi="262033032996917",
    licensekeeper=_licensekeeper,
)

# M90
_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.234", username="nokia5g", password="noki@123"
    ),
    serial_number="705_MTK_M90_1",
    server_dir="C:\Program Files (x86)\Spark1.2.0.2\Bin\Spark.exe",
    python_path="C:/Program Files/Python38",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032996917",
    capabilities=["REAL_ANDROID_UE", "samsung", "huawei_sigspark"],
    licensekeeper=_licensekeeper,
)

_appserver = AppServer(_iperf_details_on_appserver)

# _eNB_capacity_unit = CapacityUnit(addr="192.168.253.36")
# _real_enb_pdu = FACOM(addr="10.57.241.158", port_numbers=[2])
# _eNB_common_unit = CommonUnit(
#     lmp_connection=SshServiceDetails(
#         addr="10.68.88.71", username="toor4nsn", password="oZPS0POrRieRtu"
#     ),
#     pdu_port=_real_enb_pdu.pdu_ports[2],
#     capacity_units=[_eNB_capacity_unit],
# )
# _enb_airscale = Airscale(common_units=[_eNB_common_unit])
# _enb = RealEnb(
#     airscale=_enb_airscale,
#     global_bts_id="11006",
#     instance_id="11006",
#     oam_ip=NetworkAddress(v4="10.71.209.219"),
#     system_module=_enb_airscale,
# )


tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts,_cbts_1],
    attenuator=_attenuator,
    ues=[spark_UE_0,spark_UE_1,_android_0],
    appserver=_appserver,
    pdus=[_common_unit_pdu, _ru_pdu],
)

__all__ = ["tl"]
