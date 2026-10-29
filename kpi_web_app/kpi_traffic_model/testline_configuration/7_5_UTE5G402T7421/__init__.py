__maintainer__ = "Tian chun"
__team__ = "I_MN_5G_RAN_IV4_QT_HZG_GMS <I_MN_5G_RAN_IV4_QT_HZG@internal.nsn.com>"
__email__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04@internal.nsn.com"
__owner_email__ = "chun.tian@nokia-sbell.com"

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
from taf.config.testline.testpc import Connection
from taf.config.testline.core import EPCSim, RealCore
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
from taf.config.testline import Mitron, HBTE_PDU
from taf.config.testline.appserver import AppServer

_cfg_dir = os.path.dirname(os.path.abspath(__file__))
_optical_switch = Mitron(addr="10.101.63.120", model="OXC1000-32X32-SM-1356-DD-50-LP")
_attenuator = HBTE(
    ip_addr="10.101.52.41",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
)

_cu = CU(
    backhaul_site_oam_ip="10.71.209.200",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.209.200", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.209.200", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
_common_unit_pdu = HBTE_PDU(addr="10.71.195.141", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.17",
    hardware_type="ABIN",
)

_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.17",
    hardware_type="ABIO",
)

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0, _capacity_unit_1],
    pdu_port=_common_unit_pdu.pdu_ports[6],
    hardware_type="ASIM",
)

# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])

# 5G RU
_ru_pdu_1 = HBTE_PDU(addr="10.71.195.145", port_numbers=[1, 2, 3, 4, 5, 6, 9, 10])
_ru_pdu_2 = HBTE_PDU(addr="10.71.195.144", port_numbers=[1, 2, 3, 4, 5, 6, 9, 10])

_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.71.195.145", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.195.145", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_1.pdu_ports[1],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.71.195.144", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.195.144", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_2.pdu_ports[3],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_du_0 = DU(airscale=_airscale_0, rus=[_ru_1, _ru_2], f1_m_ip_addr="192.168.255.129", )

_cbts = ClassicalBts(cu=_cu, dus=[_du_0], instance_id="11088", global_bts_id="11088")

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(addr="10.70.230.189", username="ute", password="ute"),
    connections=[Connection(interface="eth1", device=_cbts.dus[0].airscale.common_units[0], interface_type="lmp")],
)

_appserver_ssh = SshServiceDetails(
    addr="10.101.49.49", username="mmw_sg4", password="mm@4", port="44001"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.18",
    iperf_path="/usr/bin/iperf",
    # iperf_path='/cygdrive/c/iperf',
    port="44001",
    ports=[
        "44001",
        "44002",
        "44003",
        "44004",
        "44005",
        "44006",
        "44007",
        "44008",
        "44009",
        "44010",
    ],
)

_cobham = TM500(
    tma_host=SshServiceDetails(
        addr="10.71.217.177", username="nokia5G", password="noki@123"
    ),
    tma_command_port=5004,
    iperf_details=_iperf,
    tma_path="",
)

# #Qualcomm

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.24",
    iperf_path="iperf",
    port="44351",
)

_appserver = AppServer(_iperf_details_on_appserver)

_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.177", username="nokia5G", password="noki@123"
    ),
    serial_number="5d39a55f",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["xiaomi12", "xiaomi"],
)

# # inseego
# _ue_config_path = os.path.join(_cfg_dir, "TestData/inseego.yml")
# if os.path.isfile(_ue_config_path):
#     with open(_ue_config_path) as f:
#         _ue_inseego = f.read()
#         qci_port = re.findall("(_iperf.*?port)", _ue_inseego)
#         for item in qci_port:
#             _ue_inseego = _ue_inseego.replace(item, str(eval(item)))
#         _ue_config = yaml.load(_ue_inseego)
# else:
#     _ue_config = ""
# # inseego


_epcsim = EPCSim(
    mme_ip="192.168.4.1",
    mcc=777,
    mnc=44,
    tac=777,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.248", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    dir_path="/opt/wts/latest",
    cfg_filename="TL101_basic_cfg_realLteEnb.cfg",
    edaemon_port="22222",
    egate_port="20021",
)
_eNB_capacity_unit = CapacityUnit(
    addr="192.168.253.36",
    hardware_type="ABIA",
)

_real_enb_pdu = HBTE_PDU(addr="10.71.195.151", port_numbers=[4])
_eNB_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.209.236", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_eNB_capacity_unit],
    hardware_type="ASIA",
)
_enb_airscale = Airscale(common_units=[_eNB_common_unit])
_enb_0 = RealEnb(airscale=_enb_airscale, instance_id="725", global_bts_id="725")

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_ASIMR_ABIOB5_ABINB4_2XAHEGB"

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_enb_0],
    core=RealCore(mcc=262, mnc=3),
    attenuator=_attenuator,
    ues=[_ue1, _cobham],
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
)


__all__ = ["tl"]


