import os
import re
import yaml
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    DeploymentSecurityGroupStack,
    ComputeNode,
    OSP,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import RealCore, EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline.gnb.du import DU, Cablink, Endpoint
from taf.config.testline.pdu import HBTE, FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import Android
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import RU, DU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)  # added in taf.meta.5.4
from taf.config.testline import RealEnb
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
    HBTE,
)  # added in taf.meta 5.4
from taf.config.testline.gnb.networkaddress import (
    NetworkAddress,
    RoutingInformation,
)  # add in taf.meta 5.4
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.hardware_controller import (
    AmiaFanHardwareController,
    GPSPowerHardwareController,
)
from taf.config.testline.signal_analyzer import KeysightN9935A
from taf.config.testline.nms import Netact
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.optical_switch import Leoni
from taf.config.testline.appserver import AppServer
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android, MediaTek

__maintainer__ = "lijun.j.xu"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_03_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_03@internal.nsn.com>"
)
__email__ = "lijun.j.xu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))


# test pc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.78", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# DCAP server
_dcap_1 = TestPc(
    # default_ssh_connection_details=HttpConnectionDetails(
    # addr="10.57.150.41", username="dcapuser", password="dcapadmin!", port=443
    # ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.150.41", username="lab5g", password="Noki@pdz123!", port=49148
    )
)

_dcap_2 = TestPc(
    # default_ssh_connection_details=HttpConnectionDetails(
    # addr="10.101.60.50", username="dcapuser", password="dcapadmin!", port=443
    # ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.101.60.50", username="dcapuser", password="dcapadmin!", port=49148
    )
)

_dcap_3 = TestPc(
    # default_ssh_connection_details=HttpConnectionDetails(
    # addr="10.101.60.51", username="dcapuser", password="dcapadmin!", port=443
    # ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.101.60.51", username="dcapuser", password="dcapadmin!", port=49148
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.167.78",
    username="ute",
    password="iW_K#8.ute%A10h0m0ra",
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.167.78",
    iperf_path="/cygdrive/c/iperf",
    port="43026",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.167.78",
    iperf_path="iperf",
    port="43026",
)
_appserver = AppServer(_iperf_details_on_appserver2)


# inseego
_ue_config_path = os.path.join(_cfg_dir, "TestData/inseego.yml")
if os.path.isfile(_ue_config_path):
    with open(_ue_config_path) as f:
        _ue_inseego = f.read()
        qci_port = re.findall("(_iperf.*?port)", _ue_inseego)
        for item in qci_port:
            _ue_inseego = _ue_inseego.replace(item, str(eval(item)))
        _ue_config = yaml.safe_load(_ue_inseego)
else:
    _ue_config = ""

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.101.51.164", username="toor4nsn", password="oZPS0POrRieRtu"
)
# _enb_pdu = HBTE(addr="10.101.45.234", port_numbers=[1])
_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.51.164", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    # pdu_port=_real_enb_pdu.pdu_ports[1],
)
_real_enb = Airscale(common_units=[_common_unit_2])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None, instance_id=3096)

# 5GRU for classicalBTS RU PB


# attenuator
# _hbte_params = {
#    "ip_addr": "10.101.51.173",
#    "port": 5000,
#    "attenuation_port_numbers": [16, 9, 10, 11, 12, 13, 14, 15, 16],
#    "model": "PA-16-16-6-127-0.5-B-S",
#    "version": None,
# }
# _attenuator = HBTE(**_hbte_params)

_attenuator = HBTE(
    ip_addr="10.101.41.66",
    port=5000,
    attenuation_port_numbers=[5, 6, 7, 8, 9, 10, 11, 12],
    model="PA-16-16-6-127-0.5-B-S",
    version=None,
)

# _ru_pdu = HBTE(addr="10.101.45.236", port_numbers=[1])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.48.2", username="root", password="umniedziala"
    ),
    # pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEQN,
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
    signal_analyzer=None,
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.101.51.170", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
# _gnb_pdu = HBTE(addr="10.101.45.234", port_numbers=[1])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    # pdu_port=_gnb_pdu.pdu_ports[1],
)
_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=2),
        target=Endpoint(unit=_ru, label="SFP", port_id=2),
    ),
]
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale,
    rus=[_ru],
    f1_m_ip_addr="10.101.51.170",
    f1_c_ip_addr="10.101.51.170",
    f1_u_ip_addr="10.101.51.170",
)

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.101.51.170",
        vlan_id=None,
        routing=RoutingInformation(
            gateway="10.101.51.161",
            ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.51.170", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.51.170", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.101.51.170",
        vlan_id=None,
        routing=RoutingInformation(
            gateway="10.101.51.161",
            ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.101.51.170",
        vlan_id=None,
        routing=RoutingInformation(
            gateway="10.101.51.161",
            ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.101.51.170",
        vlan_id=None,
        routing=RoutingInformation(
            gateway="10.101.51.161",
            ip_prefix_length=27),
    ),
)

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du],
    cu=_cu,
    instance_id=10207,
    global_bts_id=10207)

# UE
_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.137", username="nokia5G", password="noki@123"
    ),
    # serial_number="6e256d7",
    serial_number="RFCT32A4KYJ",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python38/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    # capabilities=["REAL_UE", "qct_dx50"],
    capabilities=["REAL_UE", "samsung"],
)

# CI_Detail_UE_Type='Huawei Mate 30'
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.137", username="nokia5G", password="noki@123"
    ),
    serial_number="d98acb45",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    clear_server_files="yes",
    clear_logs="yes",
    # capabilities=["REAL_UE", "huawei"],
    capabilities=["REAL_UE", "qct_dx50"],
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIKR_ABILR_AZQL"

tl = TestLine(
    test_pc=[_test_pc, _dcap_1, _dcap_2, _dcap_3],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    # ues=[_ue_config],
    ues=[_android],
    appserver=_appserver,
    attenuator=[_attenuator],
    tl_cloud_topology=_tl_cloud_topology,
)
