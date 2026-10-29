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
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
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
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import HBTE, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.pdu import HBTE, FACOM
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit

# from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch

# added in taf.meta 5.4
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
from taf.config.testline.appserver import AppServer
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.attenuator import HBTE as AHBTE

__maintainer__ = "Wang Xiaocui"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_03@internal.nsn.com"
__email__ = "jianwu.qian@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# attenuator
_attenuator = AHBTE(
    ip_addr="10.71.203.147",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)


# 5GRU for classicalBTS
_ru_pdu = FACOM(addr="10.101.45.226", port_numbers=[6])

_ru1 = RU(
    ru_hw_group="AZQG",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru_pdu.pdu_ports[6],
    radio_type=RadioTypes.AZQG,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.68", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# DCAP server
_dcap_1 = TestPc(
    # default_ssh_connection_details=HttpConnectionDetails(
    # addr="10.57.150.41", username="dcapuser", password="dcapadmin!", port=443
    # ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.150.41", username="lab5g", password="Noki@pdz123!", port=443
    )
)

_dcap_2 = TestPc(
    # default_ssh_connection_details=HttpConnectionDetails(
    # addr="10.101.60.50", username="dcapuser", password="dcapadmin!", port=443
    # ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.101.60.50", username="dcapuser", password="dcapadmin!", port=443
    )
)

_dcap_3 = TestPc(
    # default_ssh_connection_details=HttpConnectionDetails(
    # addr="10.101.60.51", username="dcapuser", password="dcapadmin!", port=443
    # ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.101.60.51", username="dcapuser", password="dcapadmin!", port=443
    )
)

# RealEnb


_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.209.36", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, instance_id="3136")


##5GRU_0 for classicalBTS
_ru_pdu = HBTE(addr="10.71.195.99", port_numbers=[8])

##need change
_ru = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.162", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    pdu_port=_ru_pdu.pdu_ports[8],
    radio_type=RadioTypes.AZQG,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)


# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.57.195.68", username="ute", password="iW_K#8.ute%A10h0m0ra", port="43703"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.195.68",
    iperf_path="/usr/bin/iperf",
    port=43701,
)

# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.101.36.230", username="spark", password="spark"
)

_sigspark1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="2a2c44fa",
    server_dir="C:\Program Files (x86)\Spark1.1.1996.15\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033100008426",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="4a2f1af1",
    server_dir="C:\Program Files (x86)\Spark1.1.1997.1\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033033320301",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark3 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="4e129e50",
    server_dir="C:\Program Files (x86)\Spark1.1.1997.1\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033100008475",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark4 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="826c1d32",
    server_dir="C:\Program Files (x86)\Spark1.1.1997.1\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033100008471",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark5 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="8ae6d1ff",
    server_dir="C:\Program Files (x86)\Spark1.1.1997.1\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033100008472",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark6 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="8f95cbc0",
    server_dir="C:\Program Files (x86)\Spark1.1.1997.1\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033032993568",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark7 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="97f904a8",
    server_dir="C:\Program Files (x86)\Spark1.1.1997.1\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033032996934",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark8 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="e402a77d",
    server_dir="C:\Program Files (x86)\Spark1.1.1997.1\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033032996901",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

# Qualcomm
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.105", username="nokia5G", password="noki@123"
    ),
    serial_number="XPL5T19A24026737",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python38/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei"],
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

_mtk_host_ssh = SshServiceDetails(
    addr="10.101.47.90", username="nokia5G", password="noki@123"
)

_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="10.57.195.68",
    iperf_path="iperf",
    port="43701",
)

_mtk = MediaTek(
    ssh_connection_details=_mtk_host_ssh,
    #                serial_number='2867e6fc',
    server_dir="C:/pyro_server",
    server_port=8080,
    edb_file_path=r"C:\MTK\sw\w19.41_1400/MDDB_MT6297_S00_VMOLY_W19_43_P3.EDB",
    #                python_path='C:/Python27/python.exe',
    imei="352569090028547",
    apn_url="wap2.nokia.com",
    #                qcat_path='C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe',
    #                diag_cfg_path='C:/pyro_server/DIAG.cfg',
    iperf_details=_iperf,
    capabilities=["REAL_MEDIATEK_UE"],
)
_mtk.inject_file = r"C:\MTK\ELT\nsa_tl923.tcl"

# #DU_0 for classicalBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.71.209.40", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="1.1.1.1")

_gnb_pdu = HBTE(addr="10.71.195.101", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.71.209.40")

##CU
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.209.40", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.209.40", username="Nemuadmin", password="nemuuser"
    ),
)

# cloud


# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="10459", global_bts_id="10459"
)


_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.70.222.51",
    iperf_path="iperf",
    port="43702",
)

_appserver = AppServer(_iperf_details_on_appserver2)
# Qualcomm UE as Android
_samsung0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.146", username="nokia5G", password="noki@123"
    ),
    # serial_number='R5CN20LYX0Y',
    serial_number="R5CT324PXGB",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=IperfDataTransferDetails(
        ssh_connection_details=_appserver_ssh,
        network_interface_address="10.70.222.51",
        iperf_path="/usr/bin/iperf",
        port="43777",
    ),
    capabilities=["samsungS21"],
)
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.146", username="nokia5G", password="noki@123"
    ),
    serial_number="be0c151c",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python38/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    clear_server_files="yes",
    clear_logs="yes",
    # capabilities=["REAL_UE", "huawei"],
    capabilities=["REAL_UE", "qct_dx50"],
)


# #cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=[_host, _dcap_1, _dcap_2, _dcap_3],
    ues=[_android],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
    appserver=_appserver,
)
