__maintainer__ = "Jiang Hongyu"
__team__ = "I_NSB_MN_RAN_RD_VRF_HAZ3_04@internal.nsn.com"
__email__ = "I_NSB_MN_RAN_RD_VRF_HAZ3_04@internal.nsn.com"
__owner_email__ = "pengliang.wu@nokia-sbell.com"

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
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline import IperfDataTransferDetails
from taf.config.testline import Mitron
from taf.config.testline.appserver import AppServer
from taf.config.testline import LicenseKeeper
from taf.config.testline.pdu import HBTE as hbte

_cfg_dir = os.path.dirname(os.path.abspath(__file__))
_licensekeeper = LicenseKeeper(username="HAZ3_SG4", password="HAZ3_SG4")

_attenuator = HBTE(
    ip_addr="10.71.203.205",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.60", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_cu = CU(
    backhaul_site_oam_ip="10.71.209.250",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.209.250", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.209.250", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
_common_unit_pdu = hbte(addr="10.71.195.151", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_lmp_connection_0 = SshServiceDetails(
    addr="10.71.209.250", username="toor4nsn", password="oZPS0POrRieRtu"
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
_ru_pdu_1 = hbte(addr="10.71.195.138", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
_ru_pdu_2 = hbte(addr="10.71.195.137", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
_ru_pdu_3 = hbte(addr="10.71.195.141", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

_ru1 = RU(
    ru_hw_group="AWHQN",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_2.pdu_ports[8],
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
    pdu_port=_ru_pdu_2.pdu_ports[7],
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
    pdu_port=_ru_pdu_2.pdu_ports[2],
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
    pdu_port=_ru_pdu_2.pdu_ports[1],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru5 = RU(
    ru_hw_group="AWHQU",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.0.176.199", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_pdu_2.pdu_ports[3],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
    radio_type=RadioTypes.AWHQU,
    serial_number="EB2313R0183"
)

_ru6 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_2.pdu_ports[4],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru7 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_3.pdu_ports[5],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru8 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_3.pdu_ports[6],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru9 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_3.pdu_ports[3],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru10 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_3.pdu_ports[4],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru11 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_1.pdu_ports[2],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru12 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_1.pdu_ports[3],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_du_0 = DU(
    airscale=_airscale_0,
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6, _ru7, _ru8, _ru9, _ru10, _ru11, _ru12],
    f1_m_ip_addr="10.71.209.250"
)

_cbts = ClassicalBts(cu=_cu, dus=[_du_0], instance_id="37600", global_bts_id="37600")

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.148", username="vrf3_sg4", password="vrf3@sg4", port="44371"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.148",
    iperf_path="/usr/bin/iperf",
    # iperf_path='/cygdrive/c/iperf',
    port="44371",
    ports=["44171", "44172", "44173", "44174", "44175", "44176", "44177", "44178"],
)

# #Qualcomm

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.148",
    iperf_path="iperf",
    port="44371",
)

_appserver = AppServer(_iperf_details_on_appserver)

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.123", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCT31FMCGJ",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.4/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    imsi="262033031393789",
)

_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.123", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCW20HHJZP",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.4/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    imsi="262033100007824",
)

_android_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.123", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R5CRC3MAWNM",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.4/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung"],
    imsi="262033032996904",
)


tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    attenuator=_attenuator,
    ues=[_android_0, _android_1, _android_2],
    appserver=_appserver,
    pdus=[_common_unit_pdu, _ru_pdu_1, _ru_pdu_2, _ru_pdu_3],
)


__all__ = ["tl"]
