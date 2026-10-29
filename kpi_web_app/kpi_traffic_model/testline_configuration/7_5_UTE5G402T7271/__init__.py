__maintainer__ = "Wu Fangmin"
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
from taf.config.testline.pdu import HBTE, PduPort, Pdu, EPC
from taf.config.testline.radio import RadioModule
from taf.config.testline import IperfDataTransferDetails
from taf.config.testline.appserver import AppServer

from taf.config.testline.gnb.du import Cablink, Endpoint

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_attenuator = hbte(
    ip_addr="10.101.52.41",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4],
)

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.70.230.18", username="ute", password="uteUTE!"
    )
)
_cu = CU(
    backhaul_site_oam_ip="10.57.131.115",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.131.115", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.131.115", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
_common_unit_pdu = HBTE(addr="10.57.246.201", port_numbers=[3])
_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.17")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[3],
)

# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])

# 5G RU
_ru_pdu = HBTE(addr="10.101.45.50", port_numbers=[2])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.101.52.41", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.52.41", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[2],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit_0, label="SFP", port_id=1),
        target=Endpoint(unit=_ru, label="SFP", port_id=1),
    )
]

_du_0 = DU(
    airscale=_airscale_0, rus=[_ru], f1_m_ip_addr="10.57.131.115", cablinks=_ru_cablinks
)

_cbts = ClassicalBts(cu=_cu, dus=[_du_0], instance_id="7271", global_bts_id="7271")

_appserver_ssh = SshServiceDetails(
    addr="10.57.178.18", username="mmw_sg4", password="mm@4", port="44291"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.18",
    iperf_path="/usr/bin/iperf",
    port=44291,
    ports=[44291, 44292],
)

# #Qualcomm
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.7", username="nokia5G", password="noki@123"
    ),
    serial_number="R5CN20B0SGH",
    server_dir="C:/Program Files (x86)/Spark1.1.2001.110/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["SamsungS20+", "samsung"],
    imsi="262033032996900",
)

# _iperf_details_on_appserver = IperfDataTransferDetails(
#     ssh_connection_details=_appserver_ssh,
#     network_interface_address="10.57.178.18",
#     iperf_path="iperf",
#     port="44291",
#     ports=[44291, 44292],
# )

_appserver = AppServer(_iperf)

# #Qualcomm

# _epcsim = EPCSim(
#     mme_ip="192.168.4.1",
#     mcc=777,
#     mnc=44,
#     tac=777,
#     default_ssh_connection_details=SshServiceDetails(
#         addr="10.57.155.74", username="ute", password="iW_K#8.ute%A10h0m0ra"
#     ),
#     dir_path="/opt/wts/latest",
#     cfg_filename="TL101_basic_cfg_realLteEnb.cfg",
#     edaemon_port="22222",
#     egate_port="20021",
# )

# RealEnb
_eNB_capacity_unit = CapacityUnit(addr="192.168.253.36")
_real_enb_pdu = HBTE(addr="10.101.45.48", port_numbers=[4])
_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.152.137", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_real_enb_pdu.pdu_ports[4],
    capacity_units=[_eNB_capacity_unit],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(
    airscale=_real_enb, rms=None, instance_id=716, global_bts_id=716
)

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASKEY_ASIKL_ABILB1_AWEUA"

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_lte_real_enb],
    core=RealCore(mcc=262, mnc=3),
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
    ues=[_android],
    appserver=_appserver,
    pdus=[_common_unit_pdu],
)

__all__ = ["tl"]
