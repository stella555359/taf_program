__maintainer__ = "Chen Zheyuan"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04@internal.nsn.com>"
)
__email__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04@internal.nsn.com"
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
from taf.config.testline.radio import RadioTypes, RU
from taf.config.testline.pdu import HBTE as HBTE_pb
from taf.config.testline import LicenseKeeper
from taf.config.testline.gnb.networkaddress import NetworkAddress

_cfg_dir = os.path.dirname(os.path.abspath(__file__))
_licensekeeper = LicenseKeeper(username="HAZ3_SG4", password="HAZ3_SG4")

_attenuator = HBTE(
    ip_addr="10.101.48.87",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
)

_attenuator_1 = HBTE(
    ip_addr="10.101.37.232",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
    model="PA-16-16-6-127-0.5-B-S",
)

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.75", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_cu = CU(
    backhaul_site_oam_ip="10.101.49.53",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.49.53", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.49.53", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
_common_unit_pdu = HBTE_pb(addr="10.101.45.42", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_lmp_connection_0 = SshServiceDetails(
    addr="10.101.49.53", username="toor4nsn", password="oZPS0POrRieRtu"
)

# _capacity_unit_0 = CapacityUnit(addr="192.168.253.17", rus=[_ru1],)

# _common_unit_0 = CommonUnit(
#     lmp_connection=_lmp_connection_0,
#     capacity_units=[_capacity_unit_0],
#     pdu_port=_common_unit_pdu.pdu_ports[7],
# )

# airscale
# _airscale_0 = Airscale(common_units=[_common_unit_0])

# 5G RU1
_ru_pdu1 = FACOM(addr="10.71.195.144", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="AWHQX",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.42", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_pdu1.pdu_ports[1],
    radio_type=RadioTypes.AWHQX.value,
    serial_number="EB2232R0689",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
    ],
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.17", rus=[_ru1],)

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[7],
    test_pc=_test_pc,
)

_airscale_0 = Airscale(common_units=[_common_unit_0])

# 5G RU2
_ru_pdu2 = FACOM(addr="10.71.195.152", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru2 = RU(
    ru_hw_group="AWHQX",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.43", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_pdu2.pdu_ports[2],
    radio_type=RadioTypes.AWHQX.value,
    serial_number="EB2232R0703",
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
_ru_pdu3 = FACOM(addr="10.71.195.144", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru3 = RU(
    ru_hw_group="AWHQX",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.41", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_pdu3.pdu_ports[2],
    radio_type=RadioTypes.AWHQX.value,
    serial_number="EB2232R0707",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
    ],
)

_du_0 = DU(airscale=_airscale_0, rus=[_ru1, _ru2, _ru3], f1_m_ip_addr="10.101.49.53")

_cbts = ClassicalBts(cu=_cu, dus=[_du_0], instance_id="11448", global_bts_id="11448")

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.197", username="vrf3_sg4", password="vrf3@sg4", port="44015"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.197",
    iperf_path="/usr/bin/iperf",
    # iperf_path='/cygdrive/c/iperf',
    port="44181",
    ports=[44181, 44182, 44183, 44184, 44185, 44186, 44187, 44188],
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
    network_interface_address="10.101.49.49",
    iperf_path="iperf",
    port="44015",
    ports=[44015, 44016],
)

_appserver = AppServer(_iperf_details_on_appserver)


# UE0
_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.46", username="nokia5G", password="noki@123"
    ),
    serial_number="RFCR10S5TDE",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.4/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung"],
    imsi="262033100010082",
)

#TL717_UE_INFO
# UE0
_android_3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.40", username="nokia5g", password="noki@123"
    ),
    serial_number="90c99bee",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.4/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "xiaomi", "huawei_sigspark"],
    imsi="262033100010748",
    licensekeeper=_licensekeeper,
)

# UE1
_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.40", username="nokia5g", password="noki@123"
    ),
    serial_number="90c99bee",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.4/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "xiaomi", "huawei_sigspark"],
    imsi="262033100010067",
    licensekeeper=_licensekeeper,
)

# UE2
_android_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.40", username="nokia5g", password="noki@123"
    ),
    serial_number="RFCX720DHJK",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.4/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung", "huawei_sigspark"],
    imsi="262033100011512",
    licensekeeper=_licensekeeper,
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
        addr="10.101.49.89", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_real_enb_pdu.pdu_ports[2],
    capacity_units=[_eNB_capacity_unit],


)
_enb_airscale = Airscale(common_units=[_eNB_common_unit])
_enb_0 = RealEnb(airscale=_enb_airscale, instance_id="7012", global_bts_id="7012",
                 system_module=_enb_airscale,
                 oam_ip=NetworkAddress(v4="10.101.49.89"),
                 )

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    core=_epcsim,
    enbs=[_enb_0],
    # attenuator=_common_unit_pdu,
    attenuator=[_common_unit_pdu, _attenuator_1],
    ues=[_android_0, _android_1, _android_2, _android_3],
    appserver=_appserver,
)


__all__ = ["tl"]

