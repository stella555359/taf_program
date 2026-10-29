__maintainer__ = "Kong xiangli"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG1"
__email__ = "Shuhui.lou@nokia-sbell.com"

import os
import yaml
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import Android
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.core import EPCSim
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline import DU, RU
from taf.config.testline.core import RealCore5G
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline.pdu import TopYoung, FACOM
from taf.config.testline.pdu import HBTE as PBHBTE
from taf.config.testline.attenuator import HBTE
from taf.config.testline.radio import RadioTypes
from taf.config.testline import LicenseKeeper


_ru_1_pdu = PBHBTE(addr="10.68.87.10", port_numbers=[4])
_ru1 = RU(
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(addr="", username=""),
    pdu_port=_ru_1_pdu.pdu_ports[4],
    ru_hw_group="",
    serial_number="BL2243D50WF",
    radio_type=RadioTypes.AHLOB,
)

_ru_2_pdu = PBHBTE(addr="10.57.246.212", port_numbers=[4])
_ru2 = RU(
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(addr="", username=""),
    pdu_port=_ru_2_pdu.pdu_ports[4],
    ru_hw_group="",
    serial_number="BL2223G1B97",
    radio_type=RadioTypes.AHLOA,
)

_ru_3_pdu = PBHBTE(addr="10.57.246.212", port_numbers=[1])
_ru3 = RU(
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(addr="", username=""),
    pdu_port=_ru_3_pdu.pdu_ports[1],
    ru_hw_group="",
    serial_number="BL2223G1B96",
    radio_type=RadioTypes.AHLOA,
)
_gnb_pdu1 = PBHBTE(addr="10.68.87.29", port_numbers=[2])

_gnb_1_airscale_cu_capacity_unit_left = CapacityUnit(addr="1.1.1.1", rus=[_ru1, _ru2, _ru3])

_common_unit1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_gnb_1_airscale_cu_capacity_unit_left],
    pdu_port=_gnb_pdu1.pdu_ports[2],
)


_airscale1 = Airscale(common_units=[_common_unit1])


_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="192.168.255.129",
        v6=None,
        vlan_id=None,
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.88.27", username="Nemuadmin", password="nemuuser"
    ),
    f1m=None,
    f1c=None,
    f1u=None,
    x2c=NetworkAddress(
        v4="10.68.88.27",
        v6=None,
        vlan_id=None,
    ),
    x2u=NetworkAddress(
        v4="10.68.88.27",
        v6=None,
        vlan_id=None,
    ),
    s1u=NetworkAddress(
        v4="10.68.88.27",
        v6=None,
        vlan_id=None,
    ),
)


# _du1 = DU(_airscale1, rus=[_ru1])
_du1 = DU(
    airscale=_airscale1,
    rus=[_ru1, _ru2, _ru3],
    f1_m_ip_addr="192.168.255.129",
)




_cbts1 = ClassicalBts(cu=_cu, dus=[_du1], instance_id=616, global_bts_id=616)

##epcsim
_epc_sim = EPCSim(
    mme_ip="10.110.227.5",
    mcc="460",
    mnc="02",
    tac="210",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.227.70", username="haijtest", password="Nokia_1234"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)

# 4GRU for RealEnb
_ru_enb_pdu = TopYoung(addr="10.101.45.85", port_numbers=[4])

_ru_enb = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="usr", password="psswd"
    ),
    pdu_port=_ru_enb_pdu.pdu_ports[4],
)

# #RealEnb
_real_enb_pdu = TopYoung(addr="10.101.45.86", port_numbers=[4])


_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.49.235", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[4],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)

_attenuator = HBTE(
    ip_addr="10.101.36.238",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
    model="PA-16-16-6-127-0.5-B-S",
)

_test_pc1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.35", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[_cbts1],
)


_ue_pc_ssh = SshServiceDetails(
    addr="10.101.47.13", username="nokia5G", password="noki@123"
)

_2_ue_pc_ssh = SshServiceDetails(
    addr="10.101.47.218", username="mn5gran", password="nokia123@"
)

_iperf_ue = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.219.233", username="cmw_sg1", password="cm@1"
    ),
    network_interface_address="10.71.219.233",
    iperf_path="/usr/bin/iperf",
    port="51100",
)

_licensekeeper = LicenseKeeper(username="HAZ4_SG1", password="HAZ4_SG1")
_android_ue1 = Android(
    ssh_connection_details=_ue_pc_ssh,
    serial_number="9YS0220414000564",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_ue,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "Guanghetong", "huawei_sigspark"],
    imsi="262032001000310",
    licensekeeper=_licensekeeper,
)


_android_ue2 = Android(
    ssh_connection_details=_2_ue_pc_ssh,
    serial_number="9YS0220414000564",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_ue,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "Guanghetong", "huawei_sigspark"],
    imsi="262032001000310",
    licensekeeper=_licensekeeper,
)


tl = TestLine(
    test_pc=_test_pc1,
    gnbs=[_cbts1],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_FULLRACK_QC_SA_ASIBL_ABIOB1_AWHQN-ASIBR_ABINB4_AWHQX",
    core=_epc_sim,
    enbs=[_lte_real_enb],
    # pdus=_pdus,
    ues=[_android_ue1, _android_ue2],
    attenuator=_attenuator,
    # attenuators=[_attenuator1, _attenuator2],
)

__all__ = ["tl"]
