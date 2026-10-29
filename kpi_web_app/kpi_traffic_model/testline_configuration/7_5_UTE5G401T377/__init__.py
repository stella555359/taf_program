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
    MediaTek,
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



__maintainer__ = "Jack zeng"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_03_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_03@internal.nsn.com>"
__email__ = "jack.zeng@nokia-sbell"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.119", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.162",
    username="vrf_sg3",
    password="vrf@sg3",
    port="53299",
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.162",
    iperf_path="/usr/bin/iperf",
    port="53399",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.162",
    iperf_path="/usr/bin/iperf",
    port="53499",
)
_appserver = AppServer(_iperf_details_on_appserver2)


# CI_Detail_UE_Type='Huawei_5G_Mate_30_Pro'
_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.41", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="e44b79d9",
    server_dir="/cygdrive/c/pyro_server",
    # python_path="C:/Python27",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["qct_dx50", "REAL_ANDROID_UE", "qct_dx50"],
    imsi="310260100008516",
    sec_key="18001006378",
)

_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.41", username="mn5gran", password="nokia123@"
    ),
    serial_number="RFCX61JGHDV",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["samsung", "samsung"],
    mobile_network_text="172.252.68.19",
)

_android_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.41", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="e44b79d9",
    server_dir="/cygdrive/c/pyro_server",
    # python_path="C:/Python27",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["qct_dx50", "REAL_ANDROID_UE", "qct_dx50"],
    imsi="310260100008516",
    sec_key="18001006378",
)

_android_3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.41", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="e44b79d9",
    server_dir="/cygdrive/c/pyro_server",
    # python_path="C:/Python27",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["qct_dx50", "REAL_ANDROID_UE", "qct_dx50"],
    imsi="310260100008516",
    sec_key="18001006378",
)

_android_4 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.41", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="e44b79d9",
    server_dir="/cygdrive/c/pyro_server",
    # python_path="C:/Python27",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["qct_dx50", "REAL_ANDROID_UE", "qct_dx50"],
    imsi="310260100008516",
    sec_key="18001006378",
)

_android_5 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.41", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="e44b79d9",
    server_dir="/cygdrive/c/pyro_server",
    # python_path="C:/Python27",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["qct_dx50", "REAL_ANDROID_UE", "qct_dx50"],
    imsi="310260100008516",
    sec_key="18001006378",
)

_android_6 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.41", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="e44b79d9",
    server_dir="/cygdrive/c/pyro_server",
    # python_path="C:/Python27",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["qct_dx50", "REAL_ANDROID_UE", "qct_dx50"],
    imsi="310260100008516",
    sec_key="18001006378",
)

_android_7 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.41", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="e44b79d9",
    server_dir="/cygdrive/c/pyro_server",
    # python_path="C:/Python27",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["qct_dx50", "REAL_ANDROID_UE", "qct_dx50"],
    imsi="310260100008516",
    sec_key="18001006378",
)

_android_8 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.41", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="e44b79d9",
    server_dir="/cygdrive/c/pyro_server",
    # python_path="C:/Python27",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["qct_dx50", "REAL_ANDROID_UE", "qct_dx50"],
    imsi="310260100008516",
    sec_key="18001006378",
)

_real_enb_pdu = FACOM(
    addr="10.57.241.212", port_numbers=[1], model="111", version="1.1.1"
)

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.226.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None, instance_id=37721)

# #5GRU for classicalBTS
# attenuator
_hbte_params_1 = {
    "ip_addr": "10.57.230.68",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator1 = HBTE(**_hbte_params_1)


_hbte_params_2 = {
    "ip_addr": "10.57.230.69",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator2 = HBTE(**_hbte_params_2)

_ru1_pdu = FACOM(addr="10.57.176.159", port_numbers=[6])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru1_pdu.pdu_ports[6],
    radio_type=RadioTypes.AVQL,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator2.attenuator_ports[9],
        _attenuator2.attenuator_ports[10],
        _attenuator2.attenuator_ports[11],
        _attenuator2.attenuator_ports[12],
    ],
)

_ru2_pdu = FACOM(addr="10.57.176.159", port_numbers=[1])

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru2_pdu.pdu_ports[1],
    radio_type=RadioTypes.AVQC,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator1.attenuator_ports[13],
        _attenuator1.attenuator_ports[14],
        _attenuator1.attenuator_ports[15],
        _attenuator1.attenuator_ports[16],
    ],
)

_ru3_pdu = FACOM(addr="10.57.176.159", port_numbers=[1])

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru3_pdu.pdu_ports[1],
    radio_type=RadioTypes.AVQC,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator1.attenuator_ports[13],
        _attenuator1.attenuator_ports[14],
        _attenuator1.attenuator_ports[15],
        _attenuator1.attenuator_ports[16],
    ],
)

_ru4_pdu = FACOM(addr="10.57.176.159", port_numbers=[1])

_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru4_pdu.pdu_ports[1],
    radio_type=RadioTypes.AVQC,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator1.attenuator_ports[13],
        _attenuator1.attenuator_ports[14],
        _attenuator1.attenuator_ports[15],
        _attenuator1.attenuator_ports[16],
    ],
)

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.227.144", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.57.176.158", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=_capacity_unit,
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3, _ru4],
    f1_m_ip_addr="10.57.227.144",
    f1_c_ip_addr="10.57.227.144",
    f1_u_ip_addr="10.57.227.144",
)

# #CU
_cu = CU(
    backhaul_site_oam_ip="10.57.227.144",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.227.144", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.227.144", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts0 = ClassicalBts(dus=[_du], cu=_cu, instance_id=37712)

# #DU for classicalBTS2
_lmp_connection1 = SshServiceDetails(
    addr="10.57.227.144", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit1 = CapacityUnit(addr="192.168.253.20")

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts0],
    enbs=[_lte_real_enb],
    ues=[_android, _android_1, _android_2, _android_3, _android_4, _android_5, _android_6, _android_7, _android_8],
    appserver=_appserver,
    attenuator=[_attenuator1, _attenuator2],
    tl_cloud_topology=_tl_cloud_topology,
)
