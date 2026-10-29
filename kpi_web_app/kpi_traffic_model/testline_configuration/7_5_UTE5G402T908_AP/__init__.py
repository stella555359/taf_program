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

__maintainer__ = "Wang Xiaocui"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_03@internal.nsn.com"
__email__ = "jianwu.qian@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.17", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# RealEnb


_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.68.88.232", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, instance_id="3136")


##5GRU_0 for classicalBTS
_ru_pdu = HBTE(addr="10.68.87.66", port_numbers=[6])

##need change
_ru = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.48.2", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[6],
    radio_type=RadioTypes.AZQG,
)


# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.235", username="vrf3_sg3", password="vrf3@sg3", port="43703"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.235",
    iperf_path="/usr/bin/iperf",
    port=50227,
)

# Qualcomm
# _android = Android(
    # ssh_connection_details=SshServiceDetails(
        # addr="10.101.47.90", username="nokia5G", password="noki@123"
    # ),
    # serial_number="bc94206e",
    # server_dir="/cygdrive/c/pyro_server",
    # python_path="C:/Python27/python.exe",
    # qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    # diag_cfg_path="C:/pyro_server/DIAG.cfg",
    # iperf_details=_iperf,
    # capabilities=["REAL_UE", "inseego"],
# )

# inseego
_ue_config_path = os.path.join(_cfg_dir, "TestData/inseego.yml")
if os.path.isfile(_ue_config_path):
    with open(_ue_config_path) as f:
        _ue_inseego = f.read()
        qci_port = re.findall("(_iperf.*?port)", _ue_inseego)
        for item in qci_port:
            _ue_inseego = _ue_inseego.replace(item, str(eval(item)))
        _ue_config = yaml.load(_ue_inseego, Loader=yaml.FullLoader)
else:
    _ue_config = ""

_mtk_host_ssh = SshServiceDetails(
    addr="10.101.47.90", username="nokia5G", password="noki@123"
)

_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="10.57.177.17",
    iperf_path="iperf",
    port="43701",
)


# _android = Android(
    # ssh_connection_details=SshServiceDetails(
        # addr="10.68.86.171", username="nokia5G", password="noki@123"
    # ),
    # serial_number="41e97418",
    # server_dir="/cygdrive/c/pyro_server",
    # python_path="C:/Python27/python.exe",
    # qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    # diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    # iperf_details=_iperf,
    # capabilities=["REAL_ANDROID_UE", "xiaomi"],
# )
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.171", username="nokia5G", password="noki@123"
    ),
    serial_number="RFCR11CL9DH",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["samsung", "samsung"],
)
_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.171", username="nokia5G", password="noki@123"
    ),
    serial_number="R3CR40S2CMM",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["samsung", "samsung"],
)

# #DU_0 for classicalBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.71.209.51", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="1.1.1.1")

_gnb_pdu = HBTE(addr="10.68.87.98", port_numbers=[4])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_gnb_pdu.pdu_ports[4],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.71.209.51")

##CU
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.209.51", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.209.51", username="Nemuadmin", password="nemuuser"
    ),
)

# cloud


# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id="1", global_bts_id="1")


_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.235",
    iperf_path="iperf",
    port="43107",
)

_appserver = AppServer(_iperf_details_on_appserver2)

# #cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    ues=[_android,_android_1],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
)

