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
        addr="10.57.167.65", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.150",
    username="vrf4_sg3",
    password="Haz4_vrf_sg3",
    port="53376",
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.150",
    iperf_path="/cygdrive/c/iperf",
    port="53376",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.150",
    iperf_path="iperf",
    port="53476",
)
_appserver = AppServer(_iperf_details_on_appserver2)


# CI_Detail_UE_Type='samsung S23'
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.116", username="mn5gran", password="nokia123@"
    ),
    serial_number="R3CW201W9KX",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["samsung", "galaxxys23"],
    pdn=["dxdata2", "mdrb3.nokia.com", "mdrb.nokia.com"],
    dmc_path="10.110.115.132",
    imsi="10.70.112.39",
)

# CI_Detail_UE_Type='Qualcomm X65'
_android1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.131", username="mn5gran", password="nokia123@"
    ),
    serial_number="e1ac059c",
    # serial_number="54f1d86c",
    server_dir="/cygdrive/c/pyro_server/",
    # python_path="C:/Python27/python.exe",
    python_path="C:/Users/mn5gran/AppData/Local/Programs/Python/Python39/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["qct_dx50", "xiaomi"],
    pdn=["dxdata2", "mdrb3.nokia.com", "mdrb.nokia.com"],
)

# #RealEnb
_real_enb_pdu = FACOM(addr="10.71.196.244", port_numbers=[2])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.214.99", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[2],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None, instance_id=31)
_realcore = RealCore(four_g=None, five_g=None, mcc="001", mnc="01", pdns=None)

# #5GRU for classicalBTS
# attenuator
_hbte_params = {
    "ip_addr": "10.71.214.49",
    "port": 5000,
    "attenuation_port_numbers": [13, 14, 15, 16, 9, 10, 11, 12],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator = HBTE(**_hbte_params)

_hbte_params1 = {
    "ip_addr": "10.71.206.30",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator1 = HBTE(**_hbte_params1)

_hbte_params2 = {
    "ip_addr": "10.71.214.50",
    "port": 5000,
    "attenuation_port_numbers": [9, 10],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator2 = HBTE(**_hbte_params2)

_ru1_pdu = FACOM(addr="10.71.196.242", port_numbers=[4])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru1_pdu.pdu_ports[4],
    radio_type=RadioTypes.AEQV,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
)

_ru2_pdu = FACOM(addr="10.71.196.242", port_numbers=[3])

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru2_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEQV,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.71.214.47", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.71.196.228", port_numbers=[4])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=_capacity_unit,
    pdu_port=_gnb_pdu.pdu_ports[4],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru1],
    f1_m_ip_addr="10.71.214.47",
    f1_c_ip_addr="10.71.214.47",
    f1_u_ip_addr="10.71.214.47",
)

# #CU
_cu = CU(
    backhaul_site_oam_ip="10.71.214.47",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.214.47", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.214.47", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts0 = ClassicalBts(dus=[_du], cu=_cu, instance_id=37611, global_bts_id=3761199999)

# #DU for classicalBTS2
_lmp_connection1 = SshServiceDetails(
    addr="10.71.214.57", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit1 = CapacityUnit(addr="192.168.253.20")

_gnb_pdu1 = FACOM(addr="10.71.196.227", port_numbers=[4])

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection1,
    capacity_units=_capacity_unit1,
    pdu_port=_gnb_pdu1.pdu_ports[4],
)

_airscale2 = Airscale(common_units=[_common_unit_1])

_du1 = DU(
    airscale=_airscale2,
    rus=[_ru2],
    f1_m_ip_addr="10.71.214.57",
    f1_c_ip_addr="10.71.214.57",
    f1_u_ip_addr="10.71.214.57",
)

# #CU
_cu1 = CU(
    backhaul_site_oam_ip="10.71.214.57",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.214.57", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.214.57", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts1 = ClassicalBts(dus=[_du1], cu=_cu1, instance_id=37612, global_bts_id=37612)
_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts0, _classical_bts1],
    enbs=[_lte_real_enb],
    ues=[_android, _android1],
    appserver=_appserver,
    core=_realcore,
    attenuator=[_attenuator, _attenuator1, _attenuator2],
    tl_cloud_topology=_tl_cloud_topology,
)
