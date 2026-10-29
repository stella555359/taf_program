__maintainer__ = "Jiang Hongyu"
__team__ = "I_MN_5G_RAN_IV4_QT_HZG_GMS <I_MN_5G_RAN_IV4_QT_HZG@internal.nsn.com>"
__email__ = "I_MN_5G_RAN_IV4_QT_HZG@internal.nsn.com"
__owner_email__ = "qianyou.zhu@nokia-sbell.com"

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
from taf.config.testline.core import RealCore
from taf.config.testline.testpc import TestPc, Connection
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
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, TopYoung
from taf.config.testline.radio import RadioModule
from taf.config.testline import IperfDataTransferDetails
from taf.config.testline import Mitron
from taf.config.testline.appserver import AppServer
from taf.config.testline import LicenseKeeper
from taf.config.testline.pdu import HBTE as hbte
from taf.config.testline.radio import RadioTypes


_cfg_dir = os.path.dirname(os.path.abspath(__file__))
_licensekeeper = LicenseKeeper(username="HAZ3_SG4", password="HAZ3_SG4")

_attenuator = HBTE(
    ip_addr="10.101.38.229",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)
# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_SA_ASOG_2xAWHQV_AQQY_2xAWHQE_AQQL"

_cu = CU(
    backhaul_site_oam_ip="10.101.49.67",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.49.67", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.49.67", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
_common_unit_pdu = hbte(addr="10.101.45.49", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_lmp_connection_0 = SshServiceDetails(
#    addr="10.101.49.67", username="toor4nsn", password="oZPS0POrRieRtu"
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_gnb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.113", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5G RU
_ru_pdu_1 = hbte(addr="10.101.45.46", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
_ru_pdu_2 = hbte(addr="10.101.45.49", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
_ru_pdu_3 = hbte(addr="10.101.45.51", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
_ru_pdu_4 = hbte(addr="10.101.45.51", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
_ru_pdu_5 = hbte(addr="10.101.45.50", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])


_ru1 = RU(
    ru_hw_group="AWHQV",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.83", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_pdu_1.pdu_ports[1],
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
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
    radio_type=RadioTypes.AWHQV.value,
    serial_number="EB2210R0252",
)

_ru2 = RU(
    ru_hw_group="AWHQV",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.85", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_pdu_2.pdu_ports[3],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
    radio_type=RadioTypes.AWHQV.value,
    serial_number="EB2210R0253",
)

_ru3 = RU(
    ru_hw_group="AWHQE",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.3", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_pdu_3.pdu_ports[3],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
    radio_type=RadioTypes.AWHQE.value,
    serial_number="EB2125R0146",
)

_ru4 = RU(
    ru_hw_group="AWHQE",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.170", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_pdu_4.pdu_ports[1],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
    radio_type=RadioTypes.AWHQE.value,
    serial_number="EB2126R0067",
)

_ru5 = RU(
    ru_hw_group="AQQY",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.39", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_pdu_5.pdu_ports[4],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
    radio_type=RadioTypes.AQQY.value,
    serial_number="1M214010056",
)

_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.17",
    hardware_type="ASOG",
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5],        #UTE cloud required "RU Should Only Be Defined in CapacityUnit( ) Not Directly in DU"
    )

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[5],
    hardware_type="ASOG",
    test_pc=_gnb_test_pc,
)
# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])

_du_0 = DU(
    airscale=_airscale_0,
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5],
    f1_m_ip_addr="10.101.49.67",
)
_cbts = ClassicalBts(cu=_cu, dus=[_du_0], instance_id="37484", global_bts_id="37484")

#Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.217.71", username="ute", password="uteUTE!"
    ),
        connections=[
        Connection(
            interface="eth1",
            device=_cbts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.197", username="vrf3_sg4", password="vrf3@sg4", port="44375"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.197",
    iperf_path="/usr/bin/iperf",
    # iperf_path='/cygdrive/c/iperf',
    port="44375",
    ports=["44375", "44376", "44377", "44378"],
)

# #Qualcomm

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.24",
    iperf_path="iperf",
    port="44375",
)

_appserver = AppServer(_iperf_details_on_appserver)

spark_UE_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.12", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="921aba66",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sigspark_multiUE", "sigspark"],
    imsi="460023100012831",
    licensekeeper=_licensekeeper,
)

spark_UE_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.12", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="921abab6",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sigspark_multiUE", "sigspark"],
    imsi="460023100012831",
    licensekeeper=_licensekeeper,
)


tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    core=RealCore(mcc=460,mnc=2),
    attenuator=_attenuator,
    ues=[spark_UE_0, spark_UE_1],
    appserver=_appserver,
    pdus=[_common_unit_pdu, _ru_pdu_1,_ru_pdu_2,_ru_pdu_3,_ru_pdu_4,_ru_pdu_5],
    tl_cloud_topology=_tl_cloud_topology,
)


__all__ = ["tl"]
