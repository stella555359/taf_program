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
from taf.config.testline.core import RealCore
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.enb import RealEnb
from taf.config.testline.ue import TM500, Android
from taf.config.testline import DU, RU
from taf.config.testline.attenuator import AttenuationPort  # added in taf.meta 5.4
from taf.config.testline.attenuator import HBTE as hbte
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import PduPort, Pdu, EPC, HBTE
from taf.config.testline.radio import (
    RadioTypes,
    RadioModule,
)
from taf.config.testline import IperfDataTransferDetails
from taf.config.testline.appserver import AppServer
from taf.config.testline.testpc import Connection
from taf.config.testline import LicenseKeeper


_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_attenuator = hbte(
    ip_addr="10.68.90.54",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
    model="PA-16-16-6-127-0.5-B-S",
)


# Testpctest_pc
# _gnb = ClassicalBts(cu=_cu, dus=[_du_0])

_cu = CU(
    backhaul_site_oam_ip="10.68.90.53",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.90.53", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.90.53", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
_common_unit_pdu = HBTE(addr="10.68.87.248", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.17", hardware_type="ABIP")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[2],
    hardware_type="ASIL",
)

# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])

# 5G RU1
_ru_pdu1 = HBTE(addr="10.68.87.249", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.2", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.48.2", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu1.pdu_ports[1],
    radio_type=RadioTypes.AWHQX,
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
_ru_pdu2 = HBTE(addr="10.68.87.249", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.2", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.48.2", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu2.pdu_ports[2],
    radio_type=RadioTypes.AWHQX,
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
_ru_pdu3 = HBTE(addr="10.68.87.249", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.2", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.48.2", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu3.pdu_ports[3],
    radio_type=RadioTypes.AWHQX,
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
_ru_pdu4 = HBTE(addr="10.68.87.249", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.2", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.48.2", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu3.pdu_ports[4],
    radio_type=RadioTypes.AWHQX,
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
_ru_pdu5 = HBTE(addr="10.68.87.249", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.2", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.48.2", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu3.pdu_ports[5],
    radio_type=RadioTypes.AWHQX,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
    ],
)

# 5G RU6
_ru_pdu6 = HBTE(addr="10.68.87.249", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru6 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.2", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.48.2", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu3.pdu_ports[6],
    radio_type=RadioTypes.AWHQX,
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
    f1_m_ip_addr="10.68.90.53",
)


_appserver_ssh = SshServiceDetails(
    addr="10.57.191.197", username="vrf3_sg4", password="vrf3@sg4", port="44181"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.197",
    iperf_path="/usr/bin/iperf",
    # iperf_path='/cygdrive/c/iperf',
    port="44181",
    ports=[44181, 44182, 44183, 44184, 44185, 44186],
)

_cobham = TM500(
    tma_host=SshServiceDetails(
        addr="10.68.86.40", username="nokia5g", password="noki@123"
    ),
    tma_command_port=5004,
    iperf_details=_iperf,
    tma_path="/cygdrive/c/Program Files (x86)/Aeroflex/TM500/5G NR - NLA latest_version/"
    "Test Mobile Application/TmaApplication.exe",
)

# #Qualcomm

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.197",
    iperf_path="iperf",
    port="44181",
    ports=[44181, 44182, 44183, 44184, 44185, 44186],
)

_appserver = AppServer(_iperf_details_on_appserver)

# UE0
_licensekeeper = LicenseKeeper(username="HAZ3_SG4", password="HAZ3_SG4")
_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.40", username="nokia5g", password="noki@123"
    ),
    serial_number="dc7255fa",
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
    serial_number="d242d476",
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
    serial_number="R3CRB0NH8SV",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.4/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung", "huawei_sigspark"],
    imsi="262033100011512",
    licensekeeper=_licensekeeper,
)

# #Qualcomm

# _epcsim = EPCSim(
#    mme_ip="192.168.4.1",
#    mcc=777,
#    mnc=44,
#    tac=777,
#   default_ssh_connection_details=SshServiceDetails(
#        addr="10.47.199.241", username="ute", password="ute"
#    ),
#    dir_path="/opt/wts/latest",
#    cfg_filename="TL101_basic_cfg_realLteEnb.cfg",
#    edaemon_port="22222",
#    egate_port="20021",
# )
# _eNB_capacity_unit = CapacityUnit(addr="192.168.253.36")
# _real_enb_pdu = HBTE(addr="10.57.241.158", port_numbers=[2])
# _eNB_common_unit = CommonUnit(
#    lmp_connection=SshServiceDetails(
#        addr="10.101.49.89", username="toor4nsn", password="oZPS0POrRieRtu"
#    ),
#    pdu_port=_real_enb_pdu.pdu_ports[2],
#    capacity_units=[_eNB_capacity_unit],
# )
# _enb_airscale = Airscale(common_units=[_eNB_common_unit])
# _enb_0 = RealEnb(airscale=_enb_airscale, instance_id="7012", global_bts_id="7012")
_cbts = ClassicalBts(cu=_cu, dus=[_du_0], instance_id="11547", global_bts_id="11547")

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.69",
        username="ute",
        password="ute",
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_cbts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_ASILL_ABIPB1_6xAWHQX"

tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_cbts],
    core=RealCore(mcc=262, mnc=3),
    #    enbs=[_enb_0],
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
    ues=[_android_0, _android_1, _android_2],
    appserver=_appserver,
)


__all__ = ["tl"]

if __name__ == "__main__":
    print("YYY")
