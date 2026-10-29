__maintainer__ = "Tian chun"
__team__ = "I_MN_5G_RAN_IV4_QT_HZG_GMS <I_MN_5G_RAN_IV4_QT_HZG@internal.nsn.com>"
__email__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04@internal.nsn.com"
__owner_email__ = "chun.tian@nokia-sbell.com"

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
from taf.config.testline.testpc import Connection
from taf.config.testline.core import EPCSim, RealCore
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.enb import RealEnb
from taf.config.testline.ue import TM500, Android
from taf.config.testline import DU, RU
from taf.config.testline.radio import (
    RadioTypes,
    RadioModule,
)
from taf.config.testline.attenuator import (
    AttenuationPort,
    HBTE,
)  # added in taf.meta 5.4
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.radio import RadioModule
from taf.config.testline import IperfDataTransferDetails
from taf.config.testline import Mitron, HBTE_PDU
from taf.config.testline.appserver import AppServer

_cfg_dir = os.path.dirname(os.path.abspath(__file__))
_optical_switch = Mitron(addr="10.101.36.198", model="OXC1000-32X32-SM-1356-DD-50-LP")
_attenuator = HBTE(
    ip_addr="10.101.52.41",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
)

# Testpc

_cu = CU(
    backhaul_site_oam_ip="10.68.90.68",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.90.68", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.90.68", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
_common_unit_pdu = HBTE_PDU(addr="10.68.90.91", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.17", hardware_type="ASIB",)

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[6],
    hardware_type="ASIB",
)

# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])

# 5G RU
_ru_pdu = HBTE_PDU(addr="10.68.87.246", port_numbers=[1, 2, 3, 4, 5, 6, 9, 10])


_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.87.246", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[2],
    radio_type=RadioTypes.AWEUA.value,
    optical_switch_channels=[
        _optical_switch.modules[8].channels[8],
        _optical_switch.modules[11].channels[11],
        _optical_switch.modules[12].channels[12],
    ],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_du_0 = DU(airscale=_airscale_0, rus=[_ru], f1_m_ip_addr="192.168.255.129")

_cbts = ClassicalBts(cu=_cu, dus=[_du_0], instance_id="7422", global_bts_id="1")

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.248", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ), connections=[Connection(interface="eth1", device=_cbts.dus[0].airscale.common_units[0], interface_type="lmp")],
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.178.18", username="mmw_sg4", password="mm@4", port="44141"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.18",
    iperf_path="/usr/bin/iperf",
    # iperf_path='/cygdrive/c/iperf',
    port="44141",
    ports=[
        "44141",
        "44142",
        "44143",
        "44144",
        "44145",
        "44146",
        "44147",
        "44148",
        "44149",
        "44150",
    ],
)

_cobham = TM500(
    tma_host=SshServiceDetails(
        addr="10.101.47.44", username="nokia5G", password="noki@123"
    ),
    tma_command_port=5004,
    iperf_details=_iperf,
    tma_path="",
)

# #Qualcomm

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.18",
    iperf_path="iperf",
    port="44141",
)

_appserver = AppServer(_iperf_details_on_appserver)

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.44", username="nokia5G", password="noki@123"
    ),
    serial_number="3e4c0cde",
    server_dir="C:/Program Files (x86)/Spark1.1.2003.15/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    # qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    # diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "askey_sigspark"],
    imsi="262033032996922",
)

_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.44", username="nokia5G", password="noki@123"
    ),
    serial_number="RFCT30V6JCX",
    server_dir="C:/Program Files (x86)/Spark1.1.2003.15/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    # qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    # diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "askey_sigspark", "samsung"],
    imsi="262033100010723",
)

# inseego
_ue_config_path = os.path.join(_cfg_dir, "TestData/inseego.yml")
if os.path.isfile(_ue_config_path):
    with open(_ue_config_path) as f:
        _ue_inseego = f.read()
        qci_port = re.findall("(_iperf.*?port)", _ue_inseego)
        for item in qci_port:
            _ue_inseego = _ue_inseego.replace(item, str(eval(item)))
        _ue_config = yaml.load(_ue_inseego)
else:
    _ue_config = ""
# inseego


_epcsim = EPCSim(
    mme_ip="192.168.4.1",
    mcc=777,
    mnc=44,
    tac=777,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.248", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    dir_path="/opt/wts/latest",
    cfg_filename="TL101_basic_cfg_realLteEnb.cfg",
    edaemon_port="22222",
    egate_port="20021",
)
_eNB_capacity_unit = CapacityUnit(addr="192.168.253.36")
_real_enb_pdu = HBTE_PDU(addr="10.68.87.90", port_numbers=[2])
_eNB_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.48.71", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_eNB_capacity_unit],
)
_enb_airscale = Airscale(common_units=[_eNB_common_unit])
_enb_0 = RealEnb(airscale=_enb_airscale, instance_id="706", global_bts_id="706")

_eNB_capacity_unit = CapacityUnit(addr="192.168.253.36")
_real_enb_pdu = HBTE_PDU(addr="10.68.87.90", port_numbers=[2])

_eNB_capacity_unit = CapacityUnit(addr="192.168.253.36")
_real_enb_pdu = FACOM(addr="10.57.241.158", port_numbers=[2])
_eNB_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.48.71", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_real_enb_pdu.pdu_ports[2],
    capacity_units=[_eNB_capacity_unit],
)
_enb_airscale_1 = Airscale(common_units=[_eNB_common_unit_1])
_enb_1 = RealEnb(airscale=_enb_airscale_1, instance_id="706", global_bts_id="706")

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_ASIBL_ABIOB1-B3_2xAWEUA_AEUD_ENB"

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_enb_0, _enb_1],
    core=RealCore(mcc=262, mnc=3),
    attenuator=_attenuator,
    ues=[_android_0, _ue_config, _android_1],
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
)


__all__ = ["tl"]
