__maintainer__ = "feng.y.liu"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04_GMS "
__email__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04@internal.nsn.com"
)
__owner_email__ = "feng.y.liu@nokia-sbell.com"

import os
import yaml
import re
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
from taf.config.testline.ue import TM500, Android, MediaTek, TafUeFastmile
from taf.config.testline import DU, RU
from taf.config.testline.attenuator import (
    AttenuationPort,
    HBTE,
)  # added in taf.meta 5.4
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.pdu import TopYoung
from taf.config.testline.radio import RadioModule
from taf.config.testline import IperfDataTransferDetails
from taf.config.testline.appserver import AppServer, TafUeAppServer
from taf.config.testline import LicenseKeeper
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol


_attenuator = HBTE(
    ip_addr="10.101.41.194",
    port="5000",
    attenuation_port_numbers=[5, 6, 7, 8, 11, 12, 13, 14],
)

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.230", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_cu = CU(
    backhaul_site_oam_ip="10.68.88.77",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.88.77", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.88.77", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
_common_unit_pdu = FACOM(addr="10.68.87.41", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_lmp_connection_0 = SshServiceDetails(
    addr="10.68.88.77", username="toor4nsn", password="oZPS0POrRieRtu"
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
_ru_0_pdu = TopYoung(addr="10.68.87.36", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru_0 = RU(
    ru_hw_group="AWHQN",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="rfsw", password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4="
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="rfsw", password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4="
    ),
    pdu_port=_ru_0_pdu.pdu_ports[6],
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
    ],
)

_ru_1_pdu = TopYoung(addr="10.68.87.36", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru_1 = RU(
    ru_hw_group="AWHQN",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="rfsw", password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4="
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="rfsw", password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4="
    ),
    pdu_port=_ru_1_pdu.pdu_ports[7],
)

_ru_2_pdu = TopYoung(addr="10.68.87.36", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru_2 = RU(
    ru_hw_group="AWHQN",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="rfsw", password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4="
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="rfsw", password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4="
    ),
    pdu_port=_ru_2_pdu.pdu_ports[8],
)

_du_0 = DU(airscale=_airscale_0, rus=[_ru_0, _ru_1, _ru_2], f1_m_ip_addr="10.68.88.77")

_cbts = ClassicalBts(cu=_cu, dus=[_du_0], instance_id="37724", global_bts_id="37724")

#UE-1 NR CPE
_fastmile_appserver_0 = TafUeAppServer(
    app_server_name="APP_SERVER_0",
    address="10.57.191.197",
    user="vrf3_sg4",
    password="vrf3@sg4",
    bind_interface_ip="10.57.191.197",
    expected_prompt="[mmw_sg4@localhost ~]$",
    binary_path="/usr/bin/iperf",
    ports=[46158, 47158],
)
_fastmile_data_transfer_0 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_0,
    interval=2,
    binary_path="iperf",
    version=2,
)

_fastmile_0 = TafUeFastmile(
    phone_number="0",
    com_port="3",
    ue_pc_address="10.68.86.45",
    root_password="HL@AtaLqf4LdsV=g",
    default_user_password="5J8#RTu7qeLmZMsx",
    ue_manage_ip="192.168.0.1",
    serial_number="KLT230800043",
    data_transfer=[_fastmile_data_transfer_0],
    ue_pc_port=9158,
    version="Receiver 5G19-A",
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

#UE-2 NR CPE
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.197",
    user="vrf3_sg4",
    password="vrf3@sg4",
    bind_interface_ip="10.57.191.197",
    expected_prompt="[mmw_sg4@rocky8-KVM-nogui ~]$",
    binary_path="/usr/bin/iperf",
    ports=[46159, 47159],
)
_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=2,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    phone_number="1",
    com_port="11",
    ue_pc_address="10.68.86.46",
    root_password="N6CEKvgK8w8a=PtN",
    default_user_password="4nTnMNgLU=W4kThV",
    ue_manage_ip="192.168.0.1",
    serial_number="KLT23140002F",
    data_transfer=[_fastmile_data_transfer_1],
    ue_pc_port=9158,
    version="Receiver 5G19-A",
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)


_epcsim = EPCSim(
    mme_ip="192.168.4.1",
    mcc=777,
    mnc=44,
    tac=777,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.230", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    dir_path="/opt/wts/latest",
    cfg_filename="TL101_basic_cfg_realLteEnb.cfg",
    edaemon_port="22222",
    egate_port="20021",
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    core=_epcsim,
    ues=[_fastmile_0, _fastmile_1],
)
__all__ = ["tl"]
