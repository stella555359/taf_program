import os
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
from taf.config.testline.core import (
    EPCSim,
    LTEEmuCore,
    PrismaCore,
    RealCore,
    RealCore4GDetails,
    RealCore5GDetails,
    AMF,
    MME,
)
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE
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
)
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.attenuator import AttenuationPort, TopYoung, HBTE, RadioRack
from taf.config.testline.gnb.networkaddress import NetworkAddress
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
from taf.config.testline.pdn import PDN, PDPTypes
import yaml

__maintainer__ = "Xu.2.Liu"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_03@internal.nsn.com"
__email__ = "xu.2.liu@nokia-sbell.com"

__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #pdn
_pdns = [PDN(PDPTypes.IPV4V6.value, "dxdata2")]

_lmp_vm_gnb_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.136", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# #realcore5g  # updated 2023/07/06
_amf_oam_ssh_connection_details = SshServiceDetails(
    addr="10.110.133.68", username="test", password="Nokia456"
)
_n2_address = NetworkAddress(v4="10.0.0.0", v6="100:00::000", vlan_id=1)
_amf = AMF(oam_ssh_connection_details=_amf_oam_ssh_connection_details, n2=_n2_address)
_real_5g_core_details = RealCore5GDetails(amf=_amf)

# #realcore5g
_realcore = RealCore(five_g=_real_5g_core_details, mcc="310", mnc="260", pdns=_pdns)

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.150",
    username="vrf4_sg3",
    password="Haz4_vrf_sg3",
    port="53463",
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.150",
    iperf_path="/cygdrive/c/iperf",
    port="53363",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.150",
    iperf_path="iperf",
    port="53363",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.150",
    iperf_path="/usr/bin/iperf",
    port="53563",
)

_appserver = AppServer(_iperf_details_on_appserver2)

_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.31", username="nokia5G", password="noki@123"
    ),
    serial_number="a7a7fc33",
    sec_key="13100016939",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/python3/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["qct_dx50", "qct_dx50"],
)

_ue_host_ssh = SshServiceDetails(
    addr="10.71.201.22", username="spark", password="spark"
)

_sigspark1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="eeabb98",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.38/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100016932",
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="eeabb98",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.38/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100016933",
)

_sigspark3 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="eeabb98",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.38/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100016934",
)

_sigspark4 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="eeabb98",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.38/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100016935",
)

_sigspark5 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="eeabb98",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.38/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100016936",
)

_sigspark6 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="eeabb98",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.38/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100016937",
)

_sigspark7 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="eeabb98",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.38/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100016938",
)

_sigspark8 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="eeabb98",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.38/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["Huawei", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="310260100016939",
)

_mtk_host_ssh = SshServiceDetails(
    addr="10.71.217.31", username="nokia5G", password="noki@123"
)

_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="",
    iperf_path="/usr/bin/iperf",
    port=53363,
)

_mtk_ue_box = MediaTek(
    ssh_connection_details=_mtk_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="C:/MTK/M90/MDDB_MT6986D_S00_NR17_R2_MP_W25_02_P1_1_unlwtg_n.EDB",
    log_filter='2.Gen99_Default_Standard',
    imei="012345678901234",
    imsi="310260100008790",
    sec_key="13100008790",
    apn_url="dxdata2",
    iperf_details=_iperf_details_on_mtk,
    capabilities=["REAL_MEDIATEK_UE", "mtk"],
    serial_number="0123456789ABCDEF",
)

# #RealEnb1
_real_enb_pdu = FACOM(addr="10.71.196.228", port_numbers=[2])

_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.214.36", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[2],
    test_pc=_lmp_vm_gnb_1,
)

_real_enb = Airscale(common_units=[_common_unit])

_lte_36321 = RealEnb(
    system_module=_real_enb,
    airscale=Airscale(common_units=[_common_unit]),
    oam_ip=NetworkAddress(v4="10.71.214.36"),  # eNB BTS MPLANE
    rms=None,
    x2_link_addr=NetworkAddress(
        v4="10.71.214.36", v6="2a00:8a00:6000:607c::3007", vlan_id=820
    ),
    global_bts_id=36321,
    instance_id=36321,
)

# RealEnb2-mutilrat

_real_enb_pdu = FACOM(addr="10.71.196.227", port_numbers=[8])

_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.214.44", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[8],
    test_pc=_lmp_vm_gnb_1,
)

_real_enb = Airscale(common_units=[_common_unit])

_lte_36312 = RealEnb(
    system_module=_real_enb,
    airscale=Airscale(common_units=[_common_unit]),
    oam_ip=NetworkAddress(v4="10.71.214.44"),  # eNB BTS MPLANE
    rms=None,
    x2_link_addr=NetworkAddress(
        v4="10.71.214.43", v6="2a00:8a00:6000:607c::3007", vlan_id=820
    ),
    global_bts_id=36312,
    instance_id=36312,
)

# #attenuator
_attenuator = TopYoung(
    ip_addr="10.71.201.27",
    port=1000,
    attenuation_port_numbers=[i for i in range(1, 257)],
    model="TAS32B8-51-120-1N-DES",
    version=None,
)

_hbte_params1 = {
    "ip_addr": "10.71.214.40",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_1 = HBTE(**_hbte_params1)

gnb1_ru1_pdu = FACOM(addr="10.71.196.232", port_numbers=[2])
gnb1_ru2_pdu = FACOM(addr="10.71.196.232", port_numbers=[3])
gnb1_ru3_pdu = FACOM(addr="10.71.196.234", port_numbers=[2])
gnb1_ru4_pdu = FACOM(addr="10.71.196.234", port_numbers=[2])
gnb1_ru5_pdu = FACOM(addr="10.71.196.230", port_numbers=[2])
gnb1_ru6_pdu = FACOM(addr="10.71.196.232", port_numbers=[5])
gnb1_ru7_pdu = FACOM(addr="10.71.196.232", port_numbers=[4])
gnb1_ru8_pdu = FACOM(addr="10.71.196.228", port_numbers=[6])
gnb1_ru9_pdu = FACOM(addr="10.71.196.232", port_numbers=[6])
gnb1_ru10_pdu = FACOM(addr="10.71.196.230", port_numbers=[6])

gnb2_ru1_pdu = FACOM(addr="10.71.196.232", port_numbers=[1])
gnb2_ru2_pdu = FACOM(addr="10.71.196.232", port_numbers=[2])

gnb3_ru1_pdu = FACOM(addr="10.71.196.232", port_numbers=[1])
gnb3_ru2_pdu = FACOM(addr="10.71.196.232", port_numbers=[2])

_gnb1_ru1 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.53", username="nokia", password="nokia123"
    ),
    pdu_port=gnb1_ru1_pdu.pdu_ports[2],
    attenuation_ports=[_attenuator.attenuator_ports[1]],
)

_gnb1_ru2 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.53", username="nokia", password="nokia123"
    ),
    pdu_port=gnb1_ru2_pdu.pdu_ports[3],
    attenuation_ports=[_attenuator.attenuator_ports[1]],
)

_gnb1_ru3 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.53", username="nokia", password="nokia123"
    ),
    pdu_port=gnb1_ru3_pdu.pdu_ports[2],
    attenuation_ports=[_attenuator.attenuator_ports[1]],
)

_gnb1_ru4 = RU(
    ru_hw_group="AHFIG",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.53", username="nokia", password="nokia123"
    ),
    pdu_port=gnb1_ru4_pdu.pdu_ports[2],
    attenuation_ports=[_attenuator.attenuator_ports[1]],
)

_gnb1_ru5 = RU(
    ru_hw_group="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.53", username="nokia", password="nokia123"
    ),
    pdu_port=gnb1_ru5_pdu.pdu_ports[2],
    attenuation_ports=[_attenuator.attenuator_ports[1]],
)

_gnb1_ru6 = RU(
    ru_hw_group="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.53", username="nokia", password="nokia123"
    ),
    pdu_port=gnb1_ru6_pdu.pdu_ports[5],
    attenuation_ports=[_attenuator.attenuator_ports[1]],
)

_gnb1_ru7 = RU(
    ru_hw_group="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.53", username="nokia", password="nokia123"
    ),
    pdu_port=gnb1_ru7_pdu.pdu_ports[4],
    attenuation_ports=[_attenuator.attenuator_ports[1]],
)

_gnb1_ru8 = RU(
    ru_hw_group="AEHC",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.53", username="nokia", password="nokia123"
    ),
    pdu_port=gnb1_ru8_pdu.pdu_ports[6],
    attenuation_ports=[_attenuator.attenuator_ports[1]],
)

_gnb1_ru9 = RU(
    ru_hw_group="AEHC",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.53", username="nokia", password="nokia123"
    ),
    pdu_port=gnb1_ru9_pdu.pdu_ports[6],
    attenuation_ports=[_attenuator.attenuator_ports[1]],
)

_gnb1_ru10 = RU(
    ru_hw_group="AEHC",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.53", username="nokia", password="nokia123"
    ),
    pdu_port=gnb1_ru10_pdu.pdu_ports[6],
    attenuation_ports=[_attenuator.attenuator_ports[1]],
)

_gnb2_ru1 = RU(
    ru_hw_group="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.53", username="nokia", password="nokia123"
    ),
    pdu_port=gnb2_ru1_pdu.pdu_ports[1],
    attenuation_ports=[_attenuator.attenuator_ports[1]],
)

_gnb2_ru2 = RU(
    ru_hw_group="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.53", username="nokia", password="nokia123"
    ),
    pdu_port=gnb2_ru2_pdu.pdu_ports[2],
    attenuation_ports=[_attenuator.attenuator_ports[1]],
)

_gnb3_ru1 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.53", username="nokia", password="nokia123"
    ),
    pdu_port=gnb3_ru1_pdu.pdu_ports[1],
    attenuation_ports=[_attenuator.attenuator_ports[1]],
)

_gnb3_ru2 = RU(
    ru_hw_group="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.53", username="nokia", password="nokia123"
    ),
    pdu_port=gnb3_ru2_pdu.pdu_ports[2],
    attenuation_ports=[_attenuator.attenuator_ports[1]],
)

_lmp_connection = SshServiceDetails(
    addr="10.71.214.38", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.71.196.229", port_numbers=[8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[8],
    test_pc=_lmp_vm_gnb_1,
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[
        _gnb1_ru1,
        _gnb1_ru2,
        _gnb1_ru3,
        _gnb1_ru4,
        _gnb1_ru5,
        _gnb1_ru6,
        _gnb1_ru7,
        _gnb1_ru8,
        _gnb1_ru9,
        _gnb1_ru10,
    ],
    f1_m_ip_addr="10.71.214.38",
    f1_c_ip_addr="10.71.214.38",
    f1_u_ip_addr="10.71.214.38",
)

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.214.38", v6="2a00:8a00:6000:607c::2a07", vlan_id=915  # 5G BTS MPLANE
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.214.38", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.214.38", username="Nemuadmin", password="nemuuser"
    ),
)

_lmp_connection2 = SshServiceDetails(
    addr="10.71.214.44", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit2 = CapacityUnit(addr="192.168.253.20")

_gnb2_pdu = FACOM(addr="10.71.196.227", port_numbers=[8])

_common_unit_2 = CommonUnit(
    lmp_connection=_lmp_connection2,
    capacity_units=[_capacity_unit2],
    pdu_port=_gnb2_pdu.pdu_ports[8],
    test_pc=_lmp_vm_gnb_1,
)

_airscale2 = Airscale(common_units=[_common_unit_2])

_du2 = DU(
    airscale=_airscale2,
    rus=[_gnb2_ru1, _gnb2_ru2],
    f1_m_ip_addr="10.71.214.44",
    f1_c_ip_addr="10.71.214.44",
    f1_u_ip_addr="10.71.214.44",
)

_cu2 = CU(
    backhaul_site_oam_ip="10.71.214.44",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.214.44", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.214.44", username="Nemuadmin", password="nemuuser"
    ),
)

_lmp_connection3 = SshServiceDetails(
    addr="10.71.214.43", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit3 = CapacityUnit(addr="192.168.253.20")

_gnb3_pdu = FACOM(addr="10.71.196.229", port_numbers=[8])

_common_unit_3 = CommonUnit(
    lmp_connection=_lmp_connection3,
    capacity_units=[_capacity_unit3],
    pdu_port=_gnb3_pdu.pdu_ports[8],
    test_pc=_lmp_vm_gnb_1,
)

_airscale3 = Airscale(common_units=[_common_unit_3])

_du3 = DU(
    airscale=_airscale3,
    rus=[_gnb3_ru1, _gnb3_ru2],
    f1_m_ip_addr="10.71.214.43",
    f1_c_ip_addr="10.71.214.43",
    f1_u_ip_addr="10.71.214.43",
)

_cu3 = CU(
    backhaul_site_oam_ip="10.71.214.43",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.214.43", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.214.43", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=36311, global_bts_id=3631199999)

_classical_bts2 = ClassicalBts(
    dus=[_du2], cu=_cu2, instance_id=36312, global_bts_id=36312
)

_classical_bts3 = ClassicalBts(
    dus=[_du3], cu=_cu3, instance_id=36313, global_bts_id=36313
)

_lmp_vm_gnb_2 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.136", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[_classical_bts],  # ClassicalBts Object in list format
)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_lmp_vm_gnb_1,
    gnbs=[_classical_bts, _classical_bts2],
    core=_realcore,
    enbs=[_lte_36321, _lte_36312],
    ues=[_android, _sigspark1, _sigspark2, _sigspark3, _sigspark4, _sigspark5, _sigspark6, _sigspark7, _sigspark8,
         _mtk_ue_box],
    appserver=_appserver,
    attenuator=[_attenuator, _attenuator_1],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_lmp_vm_gnb_2],
)
