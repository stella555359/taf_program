import os
import yaml
import re
import sys
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
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
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
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
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
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
from taf.config.testline.appserver import AppServer
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android, MediaTek
from taf.config.testline.core import RealCore


__maintainer__ = "zhang yayun"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_03_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_03@internal.nsn.com>"
__email__ = "yayun.zhang@nokia-sbell"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.18", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.150",
    username="vrf4_sg3",
    password="Haz4_vrf_sg3",
    port="53388",
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.150",
    iperf_path="/cygdrive/c/iperf",
    port="53388",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.150",
    iperf_path="iperf",
    port="43388",
)
_appserver = AppServer(_iperf_details_on_appserver2)


# CI_Detail_UE_Type='Huawei_5G_Mate_30_Pro'
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.117", username="mn5gran", password="nokia123@"
    ),
    serial_number="R5CT402BXAR",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["samsung", "samsung22"],
    pdn=["dxdata2", "mdrb3.nokia.com", "mdrb.nokia.com"]
)

_android1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.236", username="mn5gran", password="nokia123@"
    ),
    serial_number="RFCW20HQAHJ",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["samsung", "samsung23"],
    pdn=["dxdata2", "mdrb3.nokia.com", "mdrb.nokia.com"]
)

_android2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.236", username="mn5gran", password="nokia123@"
    ),
    serial_number="RFCX61M63DA",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["samsung", "samsung24"],
    pdn=["dxdata2", "mdrb3.nokia.com", "mdrb.nokia.com"]
)


# #RealEnb
_real_enb_pdu = FACOM(addr="10.71.196.245", port_numbers=[1])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.214.101", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None, instance_id=38821)
_realcore = RealCore(four_g=None, five_g=None, mcc="262", mnc="03", pdns=None)


# #5GRU for classicalBTS
# attenuator
_hbte_params = {
    "ip_addr": "10.71.214.50",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 11],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator = HBTE(**_hbte_params)

_hbte_params_ru3 = {
    "ip_addr": "10.71.206.34",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_ru3 = HBTE(**_hbte_params_ru3)

_ru1_pdu = FACOM(addr="10.71.196.244", port_numbers=[3])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru1_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEQV,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru2_pdu = FACOM(addr="10.71.196.244", port_numbers=[4])

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru2_pdu.pdu_ports[4],
    radio_type=RadioTypes.AEQV,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_ru3_pdu = FACOM(addr="10.71.196.238", port_numbers=[1])

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru3_pdu.pdu_ports[1],
    radio_type=RadioTypes.AWHHI,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)
# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.71.214.98", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.71.196.244", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=_capacity_unit,
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru3],
    f1_m_ip_addr="10.71.214.98",
    f1_c_ip_addr="10.71.214.98",
    f1_u_ip_addr="10.71.214.98",
)

# #CU
_cu = CU(
    backhaul_site_oam_ip="10.71.214.98",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.214.98", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.214.98", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts0 = ClassicalBts(dus=[_du], cu=_cu, instance_id=38811, global_bts_id=3881199999)

# #DU for classicalBTS2
_lmp_connection1 = SshServiceDetails(
    addr="10.71.214.55", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit1 = CapacityUnit(addr="192.168.253.20")

_gnb_pdu1 = FACOM(addr="10.71.196.227", port_numbers=[6])

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection1,
    capacity_units=_capacity_unit1,
    pdu_port=_gnb_pdu1.pdu_ports[6],
)

_airscale2 = Airscale(common_units=[_common_unit_1])

_du1 = DU(
    airscale=_airscale2,
    rus=[_ru2],
    f1_m_ip_addr="10.71.214.55",
    f1_c_ip_addr="10.71.214.55",
    f1_u_ip_addr="10.71.214.55",
)

# #CU
_cu1 = CU(
    backhaul_site_oam_ip="10.71.214.55",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.214.55", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.214.55", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts1 = ClassicalBts(dus=[_du1], cu=_cu1, instance_id=38812, global_bts_id=38812)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts0, _classical_bts1],
    enbs=[_lte_real_enb],
    ues=[_android, _android1, _android2],
    appserver=_appserver,
    core=_realcore,
    attenuator=[_attenuator, _attenuator_ru3],
    tl_cloud_topology=_tl_cloud_topology,
)
