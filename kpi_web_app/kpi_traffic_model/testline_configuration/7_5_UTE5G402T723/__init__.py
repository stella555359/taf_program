__maintainer__ = "Jiang Hongyu"
__team__ = "I_MN_5G_RAN_IV4_QT_HZG_GMS <I_MN_5G_RAN_IV4_QT_HZG@internal.nsn.com>"
__email__ = "I_MN_5G_RAN_IV4_QT_HZG@internal.nsn.com"
__owner_email__ = "fangmin.wu@nokia-sbell.com"

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
)
from taf.config.testline.testpc import TestPc
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
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, TopYoung
from taf.config.testline.pdu import HBTE as hbte
from taf.config.testline.radio import RadioModule
from taf.config.testline import IperfDataTransferDetails
from taf.config.testline import Mitron
from taf.config.testline.appserver import AppServer
from taf.config.testline import LicenseKeeper

_cfg_dir = os.path.dirname(os.path.abspath(__file__))
_licensekeeper = LicenseKeeper(username="HAZ3_SG4", password="HAZ3_SG4")

_attenuator = HBTE(
    ip_addr="10.71.203.244",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.47", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_cu = CU(
    backhaul_site_oam_ip="10.68.88.69",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.88.69", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.88.69", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
_common_unit_pdu = hbte(addr="10.68.87.40", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_lmp_connection_0 = SshServiceDetails(
    addr="10.68.88.69", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.17")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[4],
)

# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])

# 5G RU
_AHFIB_pdu = hbte(addr="10.68.87.35", port_numbers=[1, 2, 3, 4, 5, 6, 9, 10])
_ARHA_pdu = hbte(addr="10.68.87.62", port_numbers=[1, 2, 3, 4, 5, 6, 9, 10])
RMOD_3_pdu = hbte(addr="10.68.87.38", port_numbers=[1, 2, 3, 4, 5, 6, 9, 10])
RMOD_7_pdu = hbte(addr="10.101.45.43", port_numbers=[1, 2, 3, 4, 5, 6, 9, 10])


_AHFIB = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    pdu_port=_AHFIB_pdu.pdu_ports[3],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
    ],
)

_ARHA = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    pdu_port=_ARHA_pdu.pdu_ports[2],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

RMOD_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    pdu_port=_ARHA_pdu.pdu_ports[3],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

RMOD_3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    pdu_port=RMOD_3_pdu.pdu_ports[1],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

RMOD_4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    pdu_port=_ARHA_pdu.pdu_ports[5],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
    ],
)

RMOD_7 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    pdu_port=RMOD_7_pdu.pdu_ports[3],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
    ],
)

RMOD_9 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    pdu_port=_AHFIB_pdu.pdu_ports[1],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
    ],
)

_du_0 = DU(
    airscale=_airscale_0,
    rus=[_AHFIB, _ARHA, RMOD_1, RMOD_3, RMOD_4, RMOD_7, RMOD_9],
    f1_m_ip_addr="10.68.88.69",
)

_cbts = ClassicalBts(cu=_cu, dus=[_du_0], instance_id="37610", global_bts_id="37610")

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.197", username="vrf3_sg4", password="vrf3@sg4", port="44379"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.197",
    iperf_path="/usr/bin/iperf",
    # iperf_path='/cygdrive/c/iperf',
    port="44379",
    ports=["44379", "44380", "44381", "44382", "44383", "44384"],
)

# #Qualcomm

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.197",
    iperf_path="iperf",
    port="44379",
)

_appserver = AppServer(_iperf_details_on_appserver)

UE_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.247", username="mn5gran", password="nokia123@"
    ),
    serial_number="90c99bee",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung", "huawei_sigspark"],
    imsi="262033100011511",
    licensekeeper=_licensekeeper,
)

UE_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.247", username="mn5gran", password="nokia123@"
    ),
    serial_number="R3CW10X2ECD",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung", "huawei_sigspark"],
    imsi="262033032996542",
    licensekeeper=_licensekeeper,
)

UE_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.247", username="mn5gran", password="nokia123@"
    ),
    serial_number="RFCT325VWBD",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung", "huawei_sigspark"],
    imsi="262033100010094",
    licensekeeper=_licensekeeper,
)

_eNB_capacity_unit = CapacityUnit(addr="192.168.253.36")
_real_enb_pdu = hbte(addr="10.71.195.151", port_numbers=[6])
_eNB_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.68.88.69", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_real_enb_pdu.pdu_ports[6],
    capacity_units=[_eNB_capacity_unit],
)
_enb_airscale = Airscale(common_units=[_eNB_common_unit])
_enb = RealEnb(airscale=_enb_airscale, global_bts_id="37610", instance_id="37610")


tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_enb],
    attenuator=_attenuator,
    ues=[UE_2, UE_1, UE_0],
    appserver=_appserver,
    pdus=[_common_unit_pdu, _AHFIB_pdu, _ARHA_pdu],
)


__all__ = ["tl"]
