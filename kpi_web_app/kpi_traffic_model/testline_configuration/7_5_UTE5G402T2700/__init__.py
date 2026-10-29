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
from taf.config.testline.pdu import HBTE, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, FPFH
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import LicenseKeeper
from taf.config.testline import NetAct

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

## Add for CPE3.2
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer


__maintainer__ = "Li xiaojun"
__team__ = "I_MN_RAN_RD_VRF_HAZ_01@internal.nsn.com"
__email__ = "xiaojun.j.li@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.43", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# RealEnb


_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.149.104", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, instance_id="3136")  # 3136 =？ lxj


##5GRU_0 for classicalBTS , connect to all 6 RUs
_ru_pdu = FPFH(addr="10.57.234.16", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

##RU lmp_connection need to be updated in future
_ru1 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="serviceuser", password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc="
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    pdu_port=_ru_pdu.pdu_ports[5],
    radio_type=RadioTypes.AZQJ,
)

_ru2 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.1.10", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    pdu_port=_ru_pdu.pdu_ports[4],
    radio_type=RadioTypes.AVQC,
)

_ru3 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.37.128", username="serviceuser", password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AHFII,
)

_ru4 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.9.46", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    pdu_port=_ru_pdu.pdu_ports[2],
    radio_type=RadioTypes.AVQA,
)

_ru5 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.10.2", username="serviceuser", password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    pdu_port=_ru_pdu.pdu_ports[6],
    radio_type=RadioTypes.AKQJ,
)

_ru6 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.10.26", username="serviceuser", password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc="
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    pdu_port=_ru_pdu.pdu_ports[3],
    radio_type=RadioTypes.AZQS,
)


# #######Netact########

_netact_ssh_2014 = SshServiceDetails('10.107.245.83', 'omc', password='Nokia123!')
_netact_http_2014 = HttpConnectionDetails('qin6lbwas.qin6.srnhz.nsn-rdnet.ne', 'omc', password='Nokia123!')
_netact_2014 = NetAct(_netact_ssh_2014, _netact_http_2014)




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


# inseego: UE Type
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
    network_interface_address="10.57.155.123",
    iperf_path="iperf",
    port="43701",
)

# for FastMile CPE
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.247",
    user="vrf4_sg5",
    password="vrf4@sg5",
    bind_interface_ip="10.57.191.247",
    expected_prompt="[vrf4_sg5@appserver ~]$ ",
    binary_path="/home/vrf4_sg5/taf_debug/iperf",
    ports=[55925, 55926],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    com_port="4",
    ue_pc_address="10.57.150.154",
    root_password="973a2b82d6e3",
    ue_manage_ip="192.168.1.1",
    serial_number="LPL221400619",
    data_transfer=[_fastmile_data_transfer_1],
    version="3.2",
    ue_pc_port=5555,
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)


# spark license
_licensekeeper = LicenseKeeper(
    username="yuanyuan.2.liu@nokia-sbell.com", password="nokia123"
)

_sigspark_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.150", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="921aba50",
    server_dir="C:/Program Files (x86)/Spark1.6.2.0/Bin/Spark.exe",
    python_path="C:/Python38",
    iperf_details=_iperf,
    imsi="262033100026735",
    phone_number="+8613100026735",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    licensekeeper=_licensekeeper,
)
_sigspark_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.150", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="921aba63",
    server_dir="C:/Program Files (x86)/Spark1.6.2.0/Bin/Spark.exe",
    python_path="C:/Python38",
    iperf_details=_iperf,
    imsi="262033100008471",
    phone_number="+8613100008471",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    licensekeeper=_licensekeeper,
)

# #DU_0 for classicalBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.57.149.105", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="1.1.1.1")

_gnb_pdu = HBTE(addr="10.57.243.17", port_numbers=[6])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_gnb_pdu.pdu_ports[6],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6],
    f1_m_ip_addr="10.57.149.105",
)

##CU
_cu = CU(
    backhaul_site_oam_ip="10.57.149.105",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.149.105", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.149.105", username="Nemuadmin", password="nemuuser"
    ),
)

# cloud


# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="2700", global_bts_id="2700"
)


_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.155.123",
    iperf_path="iperf",
    port="43702",
)

_appserver = AppServer(_iperf_details_on_appserver2)

# #cloud_topology
_tl_cloud_topology = "CLASSICAL_DUAL_CORE_ASIB_ASIM_BTS"

tl = TestLine(
    test_pc=_host,
    ues=[_sigspark_1, _sigspark_2,_fastmile_1],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
    nms=_netact_2014,    
)
