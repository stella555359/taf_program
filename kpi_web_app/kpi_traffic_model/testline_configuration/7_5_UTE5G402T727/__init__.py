__maintainer__ = "lu miao"  # TL owner name
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04@internal.nsn.com"  # TL owner's team
__email__ = "miao.1.lu@nokia-sbell.com"  # TL owner's email


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
from taf.config.testline.core import EPCSim, RealCore
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.enb import RealEnb
from taf.config.testline.ue import TM500, Android
from taf.config.testline import DU, RU
from taf.config.testline.attenuator import (
    AttenuationPort,
)  # added in taf.meta 5.4
from taf.config.testline.attenuator import HBTE as hbte
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE
from taf.config.testline.radio import RadioModule
from taf.config.testline import IperfDataTransferDetails
from taf.config.testline import Mitron
from taf.config.testline.appserver import AppServer

from taf.config.testline.gnb.du import Cablink, Endpoint

_cfg_dir = os.path.dirname(os.path.abspath(__file__))
_optical_switch = Mitron(addr="10.101.36.194", model="OXC1000-32X32-SM-1356-DD-50-LP")
_attenuator = hbte(
    ip_addr="10.101.52.41",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
)

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.118", username="ute", password="ute"
    )
)
_cu = CU(
    backhaul_site_oam_ip="10.101.49.66",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.49.66", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.49.66", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
_common_unit_pdu = HBTE(addr="10.101.45.48", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.17")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[2],
)

# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])

# 5G RU
_ru_pdu = FACOM(addr="10.101.45.50", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru = RU(
    ru_hw_group="AWHQE",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.101.52.41", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.52.41", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[3],
    optical_switch_channels=[
        _optical_switch.modules[9].channels[9],
        _optical_switch.modules[10].channels[10],
        _optical_switch.modules[11].channels[11],
        _optical_switch.modules[12].channels[12],
    ],
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

_ru_pdu1 = FACOM(addr="10.101.45.48", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.101.52.41", username="serviceuser", password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.52.41", username="serviceuser", password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
    ),
    pdu_port=_ru_pdu1.pdu_ports[6],
)

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit_0, label="SFP", port_id=1),
        target=Endpoint(unit=_ru, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit_0, label="QSFP", port_id=1),
        target=Endpoint(unit=_ru, label="SFP", port_id=2),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit_0, label="SFP", port_id=2),
        target=Endpoint(unit=_ru1, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit_0, label="QSFP", port_id=2),
        target=Endpoint(unit=_ru1, label="SFP", port_id=2),
    ),
]

_du_0 = DU(
    airscale=_airscale_0,
    rus=[_ru, _ru1],
    f1_m_ip_addr="10.101.49.66",
    cablinks=_ru_cablinks,
)

_cbts = ClassicalBts(cu=_cu, dus=[_du_0], instance_id="37451", global_bts_id="37451")

_appserver_ssh = SshServiceDetails(
    addr="10.57.178.18", username="mmw_sg4", password="mm@4", port="44001"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.18",
    iperf_path="/usr/bin/iperf",
    # iperf_path='/cygdrive/c/iperf',
    port="44000",
    ports=["44000", "44001", "44002", "44003"],
)

_cobham = TM500(
    tma_host=SshServiceDetails(
        addr="10.68.86.224", username="nokia5G", password="noki@123"
    ),
    tma_command_port=5004,
    iperf_details=_iperf,
    tma_path="",
)

# #Qualcomm

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.18",
    iperf_path="iperf",
    port="44000",
)

_appserver = AppServer(_iperf_details_on_appserver)

# _android_0 = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.101.47.66", username="nokia5G", password="noki@123"
#     ),
#     serial_number="4e562bfe",
#     server_dir="/cygdrive/c/pyro_server",
#     python_path="C:/Python27/python.exe",
#     qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
#     diag_cfg_path="C:/pyro_server/DIAG.cfg",
#     iperf_details=_iperf,
#     capabilities=["REAL_ANDROID_UE", "askey"],
# )
# #Qualcomm

# CI_Detail_UE_Type='Huawei Honor 30s'
_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.224", username="nokia5G", password="noki@123"
    ),
    serial_number="9EQUT20903003014",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["SG8_HONOR30s", "huawei"],
)

_ue2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.151", username="nokia5G", password="noki@123"
    ),
    serial_number="R5CN302EQCR",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["SamsungS20+", "samsung"],
)

_epcsim = EPCSim(
    mme_ip="192.168.4.1",
    mcc=777,
    mnc=44,
    tac=777,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.118", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    dir_path="/opt/wts/latest",
    cfg_filename="TL101_basic_cfg_realLteEnb.cfg",
    edaemon_port="22222",
    egate_port="20021",
)

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_SA_ASIBL_ABILB1_2xAWHHF"

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    core=RealCore(mcc=262, mnc=3),
    attenuator=_attenuator,
    ues=[_ue1, _cobham, _ue2],
    appserver=_appserver,
    optical_switches=[_optical_switch],
    pdus=[_ru_pdu],
    tl_cloud_topology=_tl_cloud_topology,
)

__all__ = ["tl"]
