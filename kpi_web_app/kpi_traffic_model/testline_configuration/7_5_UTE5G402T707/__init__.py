__maintainer__ = "chen zheyuan"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04_GMS "
__email__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04@internal.nsn.com"
)
__owner_email__ = "zheyuan.chen@nokia-sbell.com"

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
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.radio import RadioModule
from taf.config.testline import IperfDataTransferDetails
from taf.config.testline.appserver import AppServer
from taf.config.testline.pdu import HBTE as hbte

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_attenuator = HBTE(
    ip_addr="10.101.48.87", port="5000", attenuation_port_numbers=[1, 2, 3, 4, 5, 6]
)

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.53", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_cu = CU(
    backhaul_site_oam_ip="10.68.88.72",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.88.72", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.88.72", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
_common_unit_pdu0 = hbte(addr="10.68.87.40", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_common_unit_pdu1 = hbte(addr="10.68.87.41", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_lmp_connection_0 = SshServiceDetails(
    addr="10.68.88.72", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.17")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu0.pdu_ports[4],
)

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu1.pdu_ports[1],
)

# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0, _common_unit_1])

# 5G RU1
_ru_pdu1 = FACOM(addr="10.68.87.37", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu1.pdu_ports[1],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
    ],
)

# 5G RU2
_ru_pdu2 = FACOM(addr="10.68.87.36", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu2.pdu_ports[5],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
    ],
)

# 5G RU3
_ru_pdu3 = FACOM(addr="10.68.87.247", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu3.pdu_ports[1],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
    ],
)

# 5G RU4
_ru_pdu4 = FACOM(addr="10.68.87.62", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu4.pdu_ports[4],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
    ],
)

# 5G RU5
_ru_pdu5 = FACOM(addr="10.68.87.62", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu5.pdu_ports[5],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
    ],
)

# 5G RU5
_ru_pdu6 = FACOM(addr="10.68.87.39", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru6 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu6.pdu_ports[7],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
    ],
)

_du_0 = DU(
    airscale=_airscale_0,
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6],
    f1_m_ip_addr="10.68.88.72",
)

_cbts = ClassicalBts(cu=_cu, dus=[_du_0], instance_id="37412", global_bts_id="37412")

_appserver_ssh = SshServiceDetails(
    addr="10.101.49.49", username="mmw_sg4", password="mm@4", port="44120"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.101.49.49",
    iperf_path="/usr/bin/iperf",
    # iperf_path='/cygdrive/c/iperf',
    port="44120",
    ports=[44120, 44121, 44122, 44123, 44124, 44125],
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
    network_interface_address="10.70.222.53",
    iperf_path="iperf",
    port="44081",
    ports=[44081, 44082, 44083, 44084],
)

_appserver = AppServer(_iperf_details_on_appserver)

# UE1
_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.9", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCT325VWBD",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.4/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung"],
    imsi="262033100011511",
)

# UE2
_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.2", username="nokia5G", password="noki@123"
    ),
    serial_number="R3CW10X1P0T",
    server_dir="C:/Program Files (x86)/Spark1.1.1998.2/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung"],
    imsi="262033100008419",
)

# eNB1
_eNB_capacity_unit = CapacityUnit(addr="192.168.253.36")
_real_enb_pdu = FACOM(addr="10.108.135.48", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_eNB_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.42.243", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_real_enb_pdu.pdu_ports[1],
    capacity_units=[_eNB_capacity_unit],
)
_enb_airscale = Airscale(common_units=[_eNB_common_unit])
_enb_0 = RealEnb(airscale=_enb_airscale, instance_id="37412", global_bts_id="37412")


tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_enb_0],
    attenuator=_attenuator,
    ues=[_android_0, _android_1],
    appserver=_appserver,
)


__all__ = ["tl"]
