__maintainer__ = "Chen Kaijia"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04_GMS"
__email__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04@internal.nsn.com"
__owner_email__ = "kaijia.chen@nokia-sbell.com"

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
from taf.config.testline.attenuator import AttenuationPort
from taf.config.testline.attenuator import HBTE as hbte

# added in taf.meta 5.4
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import PduPort, Pdu, EPC, HBTE
from taf.config.testline.radio import RadioModule, RadioTypes
from taf.config.testline import IperfDataTransferDetails
from taf.config.testline import Mitron
from taf.config.testline.appserver import AppServer
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.gnb.networkaddress import NetworkAddress

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
        addr="10.57.157.248", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_cu = CU(
    backhaul_site_oam_ip="10.71.209.204",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.209.204", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.209.204", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
_common_unit_pdu = HBTE(addr="10.71.195.141", port_numbers=[6])
_lmp_connection_0 = SshServiceDetails(
    addr="10.71.209.204", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.17")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[6],
    test_pc=_test_pc,
)

# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])

# 5G RU
_ru_pdu = HBTE(addr="10.71.195.145", port_numbers=[1])


_ru = RU(
    ru_hw_group="AHEGB",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.100", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
    optical_switch_channels=[
        _optical_switch.modules[7].channels[5],
        _optical_switch.modules[8].channels[6],
        _optical_switch.modules[9].channels[7],
        _optical_switch.modules[10].channels[8],
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
    radio_type=RadioTypes.AHEGB,
    serial_number="K9195201558",
)

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit_0, label="SFP", port_id=1),
        target=Endpoint(unit=_ru, label="SFP", port_id=1),
    )
]

_du_0 = DU(
    airscale=_airscale_0, rus=[_ru], f1_m_ip_addr="10.71.209.204", cablinks=_ru_cablinks
)

_cbts = ClassicalBts(cu=_cu, dus=[_du_0], instance_id="11144", global_bts_id="11144")

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.148", username="vrf3_sg4", password="vrf3@sg4", port="44001"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.148",
    iperf_path="/usr/bin/iperf",
    # iperf_path='/cygdrive/c/iperf',
    port="44351",
    ports=["44352", "44353", "44354", "44355"],
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
    network_interface_address="10.71.207.148",
    iperf_path="iperf",
    port="44351",
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
        addr="10.71.217.177", username="nokia5G", password="noki@123"
    ),
    serial_number="5d39a55f",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["xiaomi12", "xiaomi"],
)

# _epcsim = EPCSim(
#     mme_ip="192.168.4.1",
#     mcc=777,
#     mnc=44,
#     tac=777,
#     default_ssh_connection_details=SshServiceDetails(
#         addr="10.57.155.147", username="ute", password="iW_K#8.ute%A10h0m0ra"
#     ),
#     dir_path="/opt/wts/latest",
#     cfg_filename="TL101_basic_cfg_realLteEnb.cfg",
#     edaemon_port="22222",
#     egate_port="20021",
# )
_eNB_capacity_unit = CapacityUnit(addr="192.168.253.36")
_real_enb_pdu = HBTE(addr="10.101.45.48", port_numbers=[5])
_eNB_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.49.74", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_real_enb_pdu.pdu_ports[5],
    capacity_units=[_eNB_capacity_unit],
)
_enb_airscale = Airscale(common_units=[_eNB_common_unit])
_enb_0 = RealEnb(
    airscale=_enb_airscale,
    instance_id="710",
    oam_ip=NetworkAddress(v4="10.101.49.74"),
    system_module=_enb_airscale,
)

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_SA_ASOE_AEQE"

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    # core=_epcsim,
    core=RealCore(mcc=262, mnc=3),
    enbs=[_enb_0],
    attenuator=_attenuator,
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_ue1, _cobham],
    appserver=_appserver,
    optical_switches=[_optical_switch],
    pdus=[_common_unit_pdu],
)


__all__ = ["tl"]
