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
from taf.config.testline.appserver import AppServer

from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline import LicenseKeeper

_cfg_dir = os.path.dirname(os.path.abspath(__file__))
_licensekeeper = LicenseKeeper(username="HAZ3_SG4", password="HAZ3_SG4")

_attenuator = hbte(
    ip_addr="10.10.10.10",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
)

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.247", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_cu = CU(
    backhaul_site_oam_ip="10.71.203.229",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.203.229", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.203.229", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
_common_unit_pdu = HBTE(addr="10.71.197.102", port_numbers=[4])
_lmp_connection_0 = SshServiceDetails(
    addr="10.71.203.229", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.17")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[4],
)

# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])

# 5G RU1
_ru_pdu1 = HBTE(addr="10.10.10.10", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.2", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.48.2", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu1.pdu_ports[3],
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
_ru_pdu2 = HBTE(addr="10.10.10.10", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.2", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.48.2", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu2.pdu_ports[2],
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
    rus=[_ru1, _ru2],
    f1_m_ip_addr="10.71.203.229",
)

_cbts = ClassicalBts(cu=_cu, dus=[_du_0], instance_id="11234", global_bts_id="11234")

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.148", username="vrf3_sg4", password="vrf3@sg4", port="44200"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.148",
    iperf_path="/usr/bin/iperf",
    # iperf_path='/cygdrive/c/iperf',
    port="44200",
    ports=[44200, 44201, 44202, 44203, 44204, 44205, 44206, 44207, 44208, 44209],
)

_appserver = AppServer(_iperf)

# UE0
UE_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.120", username="mn5gran", password="nokia123@"
    ),
    serial_number="330b40af",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["X80", "sigspark_multiUE", "sigspark"],
    imsi="262033100004109",
    licensekeeper=_licensekeeper,
)

UE_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.120", username="mn5gran", password="nokia123@"
    ),
    serial_number="R3CW10X11XP",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung", "sigspark_multiUE", "sigspark"],
    imsi="262033100009207",
    licensekeeper=_licensekeeper,
)

UE_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.120", username="mn5gran", password="nokia123@"
    ),
    serial_number="ee5a4d5c",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["X80", "sigspark_multiUE", "sigspark"],
    imsi="262033031393688",
    licensekeeper=_licensekeeper,
)

UE_3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.120", username="mn5gran", password="nokia123@"
    ),
    serial_number="15be99f6",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["X80", "sigspark_multiUE", "sigspark"],
    imsi="262033100007839",
    licensekeeper=_licensekeeper,
)

readcap_UE_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.137", username="mn5gran", password="nokia123@"
    ),
    serial_number="c8c73561",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["X80", "sigspark_multiUE", "sigspark"],
    imsi="262033100020844",
    licensekeeper=_licensekeeper,
)

readcap_UE_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.137", username="mn5gran", password="nokia123@"
    ),
    serial_number="132997f5",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung", "sigspark_multiUE", "sigspark"],
    imsi="262033100020842",
    licensekeeper=_licensekeeper,
)

readcap_UE_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.137", username="mn5gran", password="nokia123@"
    ),
    serial_number="5d542C28",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["X80", "sigspark_multiUE", "sigspark"],
    imsi="262033100020843",
    licensekeeper=_licensekeeper,
)

readcap_UE_3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.137", username="mn5gran", password="nokia123@"
    ),
    serial_number="b34d3490",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["X80", "sigspark_multiUE", "sigspark"],
    imsi="262033100020845",
    licensekeeper=_licensekeeper,
)
## Real 4G

_eNB_capacity_unit = CapacityUnit(addr="192.168.253.36")
_real_enb_pdu = HBTE(addr="10.57.241.158", port_numbers=[2])
_eNB_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.49.89", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_real_enb_pdu.pdu_ports[2],
    capacity_units=[_eNB_capacity_unit],
)


tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    attenuator=_attenuator,
    ues=[
        readcap_UE_0,
        readcap_UE_1,
        readcap_UE_2,
        readcap_UE_3,
        UE_0,
        UE_1,
        UE_2,
        UE_3,
    ],
    appserver=_appserver,
)

__all__ = ["tl"]
