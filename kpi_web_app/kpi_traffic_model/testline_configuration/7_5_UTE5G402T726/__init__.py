__maintainer__ = "Lu Miao"
__team__ = "I_MN_5G_RAN_IV4_QT_HZG_GMS <I_MN_5G_RAN_IV4_QT_HZG@internal.nsn.com>"
__email__ = "I_MN_5G_RAN_IV4_QT_HZG@internal.nsn.com"
__owner_email__ = "fangmin.wu@nokia-sbell.com"

import os

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
)
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.core import RealCore
from taf.config.testline.core import EPCSim
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.enb import RealEnb
from taf.config.testline.ue import TM500, Android
from taf.config.testline import DU, RU
from taf.config.testline.attenuator import (
    AttenuationPort,
    HBTE,
)  # added in taf.meta 5.4
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import PduPort, Pdu, EPC
from taf.config.testline.pdu import HBTE as HBTE_pb
from taf.config.testline.radio import RadioModule
from taf.config.testline import IperfDataTransferDetails
from taf.config.testline.appserver import AppServer
from taf.config.testline import LicenseKeeper

_cfg_dir = os.path.dirname(os.path.abspath(__file__))
_licensekeeper = LicenseKeeper(username="HAZ3_SG4", password="HAZ3_SG4")

_attenuator = HBTE(
    ip_addr="10.57.251.250", port="5000", attenuation_port_numbers=[1, 2, 3, 4]
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASOH_6xAWHHF"

# 5G RU
_ru_pdu1 = HBTE_pb(addr="10.101.45.51", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru_pdu2 = HBTE_pb(addr="10.101.45.49", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru_pdu3 = HBTE_pb(addr="10.101.45.48", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru_pdu4 = HBTE_pb(addr="10.101.45.50", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru_pdu5 = HBTE_pb(addr="10.101.45.51", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru_pdu6 = HBTE_pb(addr="10.101.45.51", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="AWHHF",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.5", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_pdu1.pdu_ports[5],
    radio_type="AWHHF",
    serial_number="AH234401024",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru2 = RU(
    ru_hw_group="AWHHF",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.6", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_pdu2.pdu_ports[6],
    radio_type="AWHHF",
    serial_number="AH234401022",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru3 = RU(
    ru_hw_group="AWHHF",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.128", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_pdu3.pdu_ports[7],
    radio_type="AWHHF",
    serial_number="EB1944R0009",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru4 = RU(
    ru_hw_group="AWHHF",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.19", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_pdu4.pdu_ports[1],
    radio_type="AWHHF",
    serial_number="EB1944R0007",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru5 = RU(
    ru_hw_group="AWHHF",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.245", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_pdu5.pdu_ports[2],
    radio_type="AWHHF",
    serial_number="AH222130037",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru6 = RU(
    ru_hw_group="AWHHF",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu6.pdu_ports[6],
    radio_type="AWHHF",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_cu = CU(
    backhaul_site_oam_ip="10.101.49.68",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.49.68", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.49.68", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
_common_unit_pdu = HBTE_pb(addr="10.101.45.48", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.255.129", hardware_type="ASOH", rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6],)

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[1],
    hardware_type="ASOH",
)

# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])

_du_0 = DU(
    airscale=_airscale_0,
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6],
    f1_m_ip_addr="10.101.49.68",
)

# classicalbts
_classical_bts = ClassicalBts(cu=_cu, dus=[_du_0], global_bts_id="37485", instance_id="37485")

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.86", username="ute", password="uteUTE!"
    ),
        connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.197", username="vrf3_sg4", password="vrf3@sg4", port="44161"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.197",
    iperf_path="/usr/bin/iperf",
    port="44161",
    ports=[44161, 44162, 44163, 44164, 44165, 44166, 44167, 44168, 44169, 44170],
)

_cobham = TM500(
    tma_host=SshServiceDetails(
        addr="10.57.130.139", username="nokia5G", password="noki@123"
    ),
    tma_command_port=5004,
    iperf_details=_iperf,
    tma_path="/cygdrive/c/Program Files (x86)/Aeroflex/TM500/5G NR - NLA latest_version/"
    "Test Mobile Application/TmaApplication.exe",
)

# #Qualcomm

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.18",
    iperf_path="iperf",
    port="44161",
)

_appserver = AppServer(_iperf_details_on_appserver)

# CI_Detail_UE_Type='Samsung;Samsung;Samsung;Samsung'
_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.236", username="mn5gran", password="nokia123@"
    ),
    serial_number="RFCW2104H9R",
    #   server_dir="/cygdrive/c/pyro_server",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.45/Bin/Spark.exe",
    python_path="C:/Users/mn5gran/AppData/Local/Programs/Python/Python39/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    imsi="262038001006441",
    capabilities=["REAL_ANDROID_UE", "samsung", "huawei_sigspark"],
    licensekeeper=_licensekeeper,
)
# #Qualcomm


# _eNB_capacity_unit = CapacityUnit(addr="192.168.253.36")
# _real_enb_pdu = FACOM(addr="10.57.241.158", port_numbers=[2])
# _eNB_common_unit = CommonUnit(
#     lmp_connection=SshServiceDetails(
#         addr="10.108.135.66", username="toor4nsn", password="oZPS0POrRieRtu"
#     ),
#     pdu_port=_real_enb_pdu.pdu_ports[2],
#     capacity_units=[_eNB_capacity_unit],
# )
# _enb_airscale = Airscale(common_units=[_eNB_common_unit])
# _enb = RealEnb(airscale=_enb_airscale, global_bts_id="37485", instance_id="37485")
#

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_classical_bts],
    core=RealCore(mcc=262, mnc=3),
#    enbs=[_enb],
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=[
        _ru_pdu1,
        _ru_pdu2,
        _ru_pdu3,
        _ru_pdu4,
        _ru_pdu5,
        _ru_pdu6,
        _common_unit_pdu,
    ],
    ues=[_android_0],
    appserver=_appserver,
)


__all__ = ["tl"]

#
# if __name__ == "__main__":
#     print("YYY")
