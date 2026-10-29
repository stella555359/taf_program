
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
from taf.config.testline.radio import RadioModule
from taf.config.testline import IperfDataTransferDetails
from taf.config.testline import Mitron
from taf.config.testline.appserver import AppServer
from taf.config.testline import LicenseKeeper
from taf.config.testline.pdu import HBTE as hbte

_cfg_dir = os.path.dirname(os.path.abspath(__file__))
_licensekeeper = LicenseKeeper(username="HAZ3_SG4", password="HAZ3_SG4")

_attenuator = HBTE(
    ip_addr="10.71.207.66",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
)

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.161", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_cu = CU(
    backhaul_site_oam_ip="10.71.209.247",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.209.247", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.209.247", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
_common_unit_pdu = hbte(addr="10.71.195.151", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_lmp_connection_0 = SshServiceDetails(
    addr="10.71.209.247", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.17")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[7],
)

# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])

# 5G RU
_ru_pdu = TopYoung(addr="10.71.195.148", port_numbers=[1, 2, 3, 4, 5, 6, 9, 10])
_ru_pdu_2 = TopYoung(addr="10.71.195.140", port_numbers=[1, 2, 3, 4, 5, 6, 9, 10])


_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[3],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[2],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_2.pdu_ports[5],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_2.pdu_ports[6],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_du_0 = DU(airscale=_airscale_0, rus=[_ru1, _ru2, _ru3,  _ru4], f1_m_ip_addr="10.71.209.247")

_cbts = ClassicalBts(cu=_cu, dus=[_du_0], instance_id="37521", global_bts_id="37521")

_appserver_ssh = SshServiceDetails(
    addr="10.71.219.24", username="mmw_sg4", password="mm@4", port="44371"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.24",
    iperf_path="/usr/bin/iperf",
    # iperf_path='/cygdrive/c/iperf',
    port="44371",
    ports=["44371", "44372", "44373", "44374"],
)

# #Qualcomm

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.24",
    iperf_path="iperf",
    port="44371",
)

_appserver = AppServer(_iperf_details_on_appserver)

spark_UE_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.236", username="nokia5g", password="noki@123"
    ),
    serial_number="921aba66",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sigspark_multiUE", "sigspark"],
    imsi="460023100012831",
    licensekeeper=_licensekeeper,
)

spark_UE_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.236", username="nokia5g", password="noki@123"
    ),
    serial_number="921abab6",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sigspark_multiUE", "sigspark"],
    imsi="460023100012831",
    licensekeeper=_licensekeeper,
)

_eNB_capacity_unit = CapacityUnit(addr="192.168.253.36")
_real_enb_pdu = TopYoung(addr="10.57.241.158", port_numbers=[2])
_eNB_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.209.247", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_real_enb_pdu.pdu_ports[2],
    capacity_units=[_eNB_capacity_unit],
)
_enb_airscale = Airscale(common_units=[_eNB_common_unit])
_enb = RealEnb(airscale=_enb_airscale, global_bts_id="37521", instance_id="11195")

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_enb],
    attenuator=_attenuator,
    ues=[spark_UE_0, spark_UE_1],
    appserver=_appserver,
    pdus=[_common_unit_pdu, _ru_pdu, _ru_pdu_2],
)


__all__ = ["tl"]
