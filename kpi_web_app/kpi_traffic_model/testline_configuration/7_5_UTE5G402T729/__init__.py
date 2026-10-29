__maintainer__ = "Wu Pengliang"
__team__ = "MN RAN PZ3 SG04"
__email__ = "i_nsb_mn_ran_rd_vrf_haz3_04@internal.nsn.com"
__owner_email__ = "pengliang.wu@nokia-sbell.com"

import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.pdu import FACOM
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.core import EPCSim
from taf.config.testline import DU

# added in taf.meta 5.4
from taf.config.testline.ue import (
    Android,
)
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.radio import (
    RU,
)
from taf.config.testline.pdu import HBTE as hbte
from taf.config.testline.appserver import AppServer
from taf.config.testline import LicenseKeeper

_cfg_dir = os.path.dirname(os.path.abspath(__file__))
_licensekeeper = LicenseKeeper(username="HAZ3_SG4", password="HAZ3_SG4")


# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.50", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_cu = CU(
    backhaul_site_oam_ip="10.71.212.71",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.212.71", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.212.71", username="Nemuadmin", password="nemuuser"
    ),
)

_cu_1 = CU(
    backhaul_site_oam_ip="10.71.212.74",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.212.74", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.212.74", username="Nemuadmin", password="nemuuser"
    ),
)


# DU
_common_unit_pdu = FACOM(addr="10.71.197.130", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_common_unit_pdu1 = FACOM(addr="10.71.197.131", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_lmp_connection_0 = SshServiceDetails(
    addr="10.71.212.71", username="toor4nsn", password="oZPS0POrRieRtu"
)

_lmp_connection_1 = SshServiceDetails(
    addr="10.71.212.74", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.17")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[2],
    test_pc=_test_pc,
)

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_1,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu1.pdu_ports[2],
    test_pc=_test_pc,
)


# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])
_airscale_1 = Airscale(common_units=[_common_unit_1])

# 5G RU
_ru_pdu = hbte(addr="10.101.45.100", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru_pdu2 = hbte(addr="10.101.45.102", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])


_ru = RU(
    ru_hw_group="AQQJ",
    serial_number="1M231703848",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.218.19", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_pdu.pdu_ports[2],
)

_ru2 = RU(
    ru_hw_group="AQQJ",
    serial_number="1M231703853",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.218.18", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_pdu2.pdu_ports[3],
)

_du_0 = DU(airscale=_airscale_0, rus=[_ru], f1_m_ip_addr="10.71.212.71")
_du_1 = DU(airscale=_airscale_1, rus=[_ru2], f1_m_ip_addr="10.71.212.74")


_cbts = ClassicalBts(cu=_cu, dus=[_du_0], global_bts_id="37755", instance_id="37755")
_cbts_1 = ClassicalBts(cu=_cu_1, dus=[_du_1], global_bts_id="37869", instance_id="37869")

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.197", username="vrf3_sg4", password="vrf3@sg4", port="44416"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.197",
    iperf_path="/usr/bin/iperf",
    port="44416",
    ports=[44416, 44417, 44418, 44419, 44420, 44421, 44422, 44423],
)

_appserver = AppServer(_iperf)

_spark_x65_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.162", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="spark_x65_ue1",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Users/nokia5G/AppData/Local/Programs/Python/Python310/python.exe",
    iperf_details=_iperf,
    imsi="262033100024117",
    capabilities=["REAL_ANDROID_UE", "sigspark_multiUE", "sigspark"],
    licensekeeper=_licensekeeper
)

_spark_x65_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.162", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="spark_x65_ue2",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Users/nokia5G/AppData/Local/Programs/Python/Python310/python.exe",
    iperf_details=_iperf,
    imsi="262033100024035",
    capabilities=["REAL_ANDROID_UE", "sigspark_multiUE", "sigspark"],
    licensekeeper=_licensekeeper
)

MTK_UE_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.162", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="MTK_M90_710_001",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung"],
    imsi="460023100024141",
)


_attenuator = TopYoung(
    ip_addr="10.71.205.42",
    port=28888,
    attenuation_port_numbers=[1, 2, 3, 4],
    model="MCS2338A2-64B16-A4",
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts, _cbts_1],
    enbs=[],
    ues=[_spark_x65_0, _spark_x65_1, MTK_UE_0],
    appserver=_appserver,
    attenuator = [_attenuator],
)


__all__ = ["tl"]
