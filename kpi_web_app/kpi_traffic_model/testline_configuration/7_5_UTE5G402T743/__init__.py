__maintainer__ = "Long Zengqiang"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04@internal.nsn.com>"
)
__email__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04@internal.nsn.com"
__owner_email__ = "zengqiang.long@nokia-sbell.com"

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
from taf.config.testline.pdu import HBTE as hbte
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

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_attenuator = HBTE(
    ip_addr="10.101.46.10",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    model="PA-16-16-6-127-0.5-B-S",
)


# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.43", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_cu = CU(
    backhaul_site_oam_ip="10.101.52.35",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.52.35", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.52.35", username="Nemuadmin", password="nemuuser"
    ),
)
_cu1 = CU(
    backhaul_site_oam_ip="10.71.209.248",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.209.248", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.209.248", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
_common_unit_pdu = FACOM(addr="10.101.46.10", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_lmp_connection_0 = SshServiceDetails(
    addr="10.101.52.35", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.17")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[3],
)

# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])

# 5G RU1
_ru_pdu1 = hbte(addr="10.101.46.11", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.10.10.136", username="serviceuser", password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
    ),
      lmp_connection=SshServiceDetails(
        addr="10.10.10.136", username="serviceuser", password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
      ),
    pdu_port=_ru_pdu1.pdu_ports[4],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
    ],
)

# 5G RU2
_ru_pdu2 = hbte(addr="10.10.10.136", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.10.10.136", username="serviceuser", password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.10.10.136", username="serviceuser", password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
    ),
    pdu_port=_ru_pdu1.pdu_ports[1],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
    ],
)


_du_0 = DU(airscale=_airscale_0, rus=[_ru1, _ru2], f1_m_ip_addr="10.101.52.35")

_cbts = ClassicalBts(cu=_cu, dus=[_du_0], instance_id="37725", global_bts_id="37725")

# DU2
# _common_unit_pdu = FACOM(addr="10.71.195.150", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
# _lmp_connection_1 = SshServiceDetails(
    # addr="10.71.209.248", username="toor4nsn", password="oZPS0POrRieRtu"
# )

# _capacity_unit_1 = CapacityUnit(addr="192.168.253.17")

# _common_unit_1 = CommonUnit(
    # lmp_connection=_lmp_connection_1,
    # capacity_units=[_capacity_unit_1],
    # pdu_port=_common_unit_pdu.pdu_ports[2],
# )

# airscale
_airscale_1 = Airscale(common_units=[_common_unit_0])

# 5G RU3
_ru_pdu3 = hbte(addr="10.71.195.148", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.10.10.136", username="serviceuser", password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.10.10.136", username="serviceuser", password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
    ),
    pdu_port=_ru_pdu3.pdu_ports[3],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
    ],
)

# 5G RU4
_ru_pdu4 = hbte(addr="10.68.87.88", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
       addr="10.10.10.131", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.10.10.131", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    pdu_port=_ru_pdu3.pdu_ports[3],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
    ],
)
# 5G RU5
_ru_pdu4 = hbte(addr="10.68.87.88", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
       addr="10.10.10.131", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    lmp_connection=SshServiceDetails(
        addr="110.10.10.131", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    pdu_port=_ru_pdu3.pdu_ports[4],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
    ],
)

_du_1 = DU(airscale=_airscale_1, rus=[_ru3, _ru4], f1_m_ip_addr="10.71.209.248")

_cbts1 = ClassicalBts(cu=_cu1, dus=[_du_1], instance_id="37725", global_bts_id="37725")

_appserver_ssh = SshServiceDetails(
    addr="10.101.38.228", username="mmw_sg4", password="mm@4", port="44048"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.197",
    iperf_path="/usr/bin/iperf",
    # iperf_path='/cygdrive/c/iperf',
    port="44191",
    ports=[44191, 44192],
)

# _cobham = TM500(
    # tma_host=SshServiceDetails(
        # addr="10.57.130.139", username="nokia5G", password="noki@123"
    # ),
    # tma_command_port=5004,
    # iperf_details=_iperf,
    # tma_path="/cygdrive/c/Program Files (x86)/Aeroflex/TM500/5G NR - NLA latest_version/"
    # "Test Mobile Application/TmaApplication.exe",
# )

# #Qualcomm

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.197",
    iperf_path="iperf",
    port="44001",
    ports=[44001, 44002,44003,44004,44005,44006,44007],
)

_appserver = AppServer(_iperf_details_on_appserver)

# UE0
_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.6", username="nokia5G", password="noki@123"
    ),
    serial_number="RFCNC0TDASX",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.4/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung"],
    imsi="310260100010206",
)

# #Qualcomm

_epcsim = EPCSim(
    mme_ip="192.168.4.1",
    mcc=777,
    mnc=44,
    tac=777,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.47.199.241", username="ute", password="ute"
    ),
    dir_path="/opt/wts/latest",
    cfg_filename="TL101_basic_cfg_realLteEnb.cfg",
    edaemon_port="22222",
    egate_port="20021",
)
_eNB_capacity_unit = CapacityUnit(addr="192.168.253.36")
_real_enb_pdu = FACOM(addr="10.57.241.158", port_numbers=[2])
_eNB_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.209.231", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_real_enb_pdu.pdu_ports[2],
    capacity_units=[_eNB_capacity_unit],
)
_enb_airscale = Airscale(common_units=[_eNB_common_unit])
_enb_0 = RealEnb(airscale=_enb_airscale, instance_id="10432", global_bts_id="10432")

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts, _cbts1],
    core=_epcsim,
    enbs=[_enb_0],
    attenuator=_attenuator,
    ues=[_android_0],
    appserver=_appserver,
)


__all__ = ["tl"]
