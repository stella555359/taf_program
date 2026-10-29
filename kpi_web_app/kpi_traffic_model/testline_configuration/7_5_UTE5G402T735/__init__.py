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
from taf.config.testline import DU, RU, RadioTypes
from taf.config.testline.attenuator import (
    AttenuationPort,
    HBTE,
)  # added in taf.meta 5.4
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.radio import RadioModule
from taf.config.testline import IperfDataTransferDetails
from taf.config.testline import Mitron
from taf.config.testline.appserver import AppServer

_cfg_dir = os.path.dirname(os.path.abspath(__file__))
_optical_switch = Mitron(addr="10.101.36.198", model="OXC1000-32X32-SM-1356-DD-50-LP")
_attenuator = HBTE(
    ip_addr="10.71.207.66",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
    model="PA-16-16-6-127-0.5-B-S",
)

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.246", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_cu = CU(
    backhaul_site_oam_ip="10.68.88.67",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.88.67", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.88.67", username="Nemuadmin", password="nemuuser"
    ),
)

_cu1 = CU(
    backhaul_site_oam_ip="10.68.88.74",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.88.74", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.88.74", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
_common_unit_pdu = FACOM(addr="10.68.88.67", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_lmp_connection_0 = SshServiceDetails(
    addr="10.68.88.67", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.17")

_gnb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.71.218.166", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
)

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[6],
    hardware_type="ASIM",
    test_pc=_gnb_test_pc,
)


# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])

# 5G RU
_ru_pdu = FACOM(addr="10.68.87.246", port_numbers=[1, 2, 3, 4, 5, 6, 9, 10])

_ru = RU(
    ru_hw_group="AWHHF",
    serial_number="EB1944R0610",
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AWHHF,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="root",
        password="root",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.218.166", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
)

_du_0 = DU(airscale=_airscale_0, rus=[_ru], f1_m_ip_addr="10.68.88.67")

_du_1 = DU(airscale=_airscale_0, rus=[_ru], f1_m_ip_addr="10.68.88.74")

_cbts = ClassicalBts(cu=_cu, dus=[_du_0], instance_id="37790", global_bts_id="37790")

_cbts1 = ClassicalBts(cu=_cu1, dus=[_du_1], instance_id="37792", global_bts_id="37792")

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.148", username="vrf3_sg4", password="vrf3@sg4", port="44371"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.148",
    iperf_path="/usr/bin/iperf",
    # iperf_path='/cygdrive/c/iperf',
    port="44371",
    ports=[
        "44371",
        "44372",
        "44373",
        "44374",
        "44375",
        "44376",
        "44377",
        "44378",
        "44379",
        "44380",
    ],
)

# #Qualcomm

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.148",
    iperf_path="iperf",
    port="44371",
)

_appserver = AppServer(_iperf_details_on_appserver)


_epcsim = EPCSim(
    mme_ip="192.168.4.1",
    mcc=777,
    mnc=44,
    tac=777,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.204", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    dir_path="/opt/wts/latest",
    cfg_filename="TL101_basic_cfg_realLteEnb.cfg",
    edaemon_port="22222",
    egate_port="20021",
)


tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts, _cbts1],
    core=_epcsim,
    attenuator=_attenuator,
    ues=[],
    appserver=_appserver,
    pdus=[_ru_pdu],
)


__all__ = ["tl"]
