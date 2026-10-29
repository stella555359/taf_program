import os
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
)  # added in taf.meta.5.4
from taf.config.testline.ue import MediaTek
from taf.config.testline.core import EPCSim, RealCore4G
from taf.config.testline.core import RealCore
from taf.config.testline.gnb.du import DU, Cablink, Endpoint
from taf.config.testline.pdu import TopYoung, HBTE
from taf.config.testline.attenuator import AttenuationPort
from taf.config.testline.attenuator import TopYoung as ATOPYOUNG
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.nms import NMS
from taf.config.testline.nom import NOM
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500
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
# from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
from taf.config.testline import NetworkAddress, RoutingInformation, LicenseKeeper
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


__maintainer__ = "meiya.cheng"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02@internal.nsn.com"
__email__ = "meiya.cheng@nokia-sbell.com"


# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Real EPC is used. epcsim is here only as a backup solution.
_epc_sim = EPCSim(
    mme_ip="10.110.66.198",
    mcc="262",
    mnc="2",
    tac="20200",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.70.112.199", username="duqi_test", password="Nokia_4321"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)

# #host
# _host = TestPc(
#     default_ssh_connection_details=SshServiceDetails(
#         addr="10.57.155.210", username="ute", password="iW_K#8.ute%A10h0m0ra"
#     )
# )
_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.71.204.199", username="spark", password="spark"
    )
)

# #5GRU_0 for cloudBTS
_ru_1_pdu = HBTE(addr="10.71.196.84", port_numbers=[3])

_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    pdu_port=_ru_1_pdu.pdu_ports[3],
    radio_type=RadioTypes.AQQJ,
)
# AQQJ_2
_attenuator_0 = ATOPYOUNG(
    ip_addr="10.71.204.198",
    port=23,
    attenuation_port_numbers=[1,2,3,4],
    model="TAS16T16-51-120-1S-DES",
    serial_number="N30018110006"
)

# AHPB_2
_attenuator_1 = ATOPYOUNG(
    ip_addr="10.71.204.198",
    port=23,
    attenuation_port_numbers=[7,8],
    model="TAS16T16-51-120-1S-DES",
    serial_number="N30018110006"
)

# AHPB_1
_attenuator_2 = AHBTE(
    ip_addr="10.71.204.198",
    port=5000,
    attenuation_port_numbers=[9,10],
    model="PA-16-16-6-127-0.5-B-S",
)

_ru_2_pdu = TopYoung(addr="10.71.196.80", port_numbers=[3,4,5])
_ru_4_pdu = TopYoung(addr="10.71.195.234", port_numbers=[1,2])
_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.6",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY="
    ),
    pdu_port=_ru_2_pdu.pdu_ports[4],
    attenuation_ports=[
        _attenuator_0.attenuator_ports[1],
        _attenuator_0.attenuator_ports[2],
        _attenuator_0.attenuator_ports[3],
        _attenuator_0.attenuator_ports[4],
    ],
    radio_type=RadioTypes.AQQJ,
)
_ru_3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.10",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY="
    ),
    pdu_port=_ru_4_pdu.pdu_ports[1],
    radio_type=RadioTypes.AQQJ,
)

_ru_4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.130", username="root", password=""
    ),
    pdu_port=_ru_4_pdu.pdu_ports[2],
    attenuation_ports=[
        _attenuator_2.attenuator_ports[9],
        _attenuator_2.attenuator_ports[10],
    ],
    radio_type=RadioTypes.AHPB,
)

_ru_3_pdu = TopYoung(addr="10.71.196.18", port_numbers=[2])
_ru_5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.129", username="root", password=""
    ),
    pdu_port=_ru_3_pdu.pdu_ports[2],
    attenuation_ports=[
        _attenuator_1.attenuator_ports[7],
        _attenuator_1.attenuator_ports[8],
    ],
    radio_type=RadioTypes.AHPB,
)

# #######Iperf########

_mtk_host_ssh = SshServiceDetails(
    addr="10.71.218.125", username="MN5GRAN", password="nokia123@"
)

_appserver_ssh = SshServiceDetails(
    addr="10.71.219.22", username="mmw_sg2", password="mm@2"
)

_iperf_details_on_MTK = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="",
    iperf_path="/data/local/tmp/iperf",
    port="43166",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.22",
    iperf_path="iperf",
    port="42166",
)
_appserver = AppServer(_iperf_details_on_appserver)

# MTK
#_mtk = MediaTek(
#    ssh_connection_details=_mtk_host_ssh,
#    server_dir="c:/pyro_server",
#    server_port=8080,
#    edb_file_path="C:\MTK\MDDB_MT6879_S00_NR16_R2_MP_W22_29_P4.EDB",
#    imei="35190103100565",
#    imsi="262033100011504",
#    apn_url="dxdata1",
#    iperf_details=_iperf_details_on_MTK,
#    capabilities=["REAL_MEDIATEK_UE"],
#)

# SIGSPARK
# SIGSPARK
_appserver_ip_addr1 = "10.71.219.22"

_spark_appserver_ssh1 = SshServiceDetails(
    addr=_appserver_ip_addr1, username="mmw_sg2", password="mm@2"
)

_iperf_details_on_appserver1 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh1,
    network_interface_address=_appserver_ip_addr1,
    iperf_path="iperf",
    port=42157,
)

_ue_host_ssh = SshServiceDetails(addr="10.71.204.199", username="spark", password="spark")

_licensekeeper = LicenseKeeper(username="HAZ3_SG2", password="HAZ3_SG2")

_IMSI_1="262033100007838"


# C:\Program Files (x86)\Spark1.1.2008.3\Bin\Spark.exe

_spark_server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe"

_sigspark_0 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="051190002139001",
    server_dir=_spark_server_dir,
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_1,
    licensekeeper=_licensekeeper,
)
_sigspark_1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="051190002139001",
    server_dir=_spark_server_dir,
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_1,
    licensekeeper=_licensekeeper,
)

# #DU_0 for cloudlBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.71.211.144", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="10.71.211.144")

_du_pdu = HBTE(addr="10.71.196.85", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_du_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit_0])
_f1_m_ip_addr = "10.71.211.144"
_du = DU(
    airscale=_airscale, rus=[_ru_1,_ru_2,_ru_3,_ru_4,_ru_5], f1_m_ip_addr=_f1_m_ip_addr)

# #CU
_cu_NetworkAddress = NetworkAddress(
    v4=_f1_m_ip_addr,
    vlan_id=None,
    routing=RoutingInformation(gateway="10.71.211.129", ip_prefix_length=27),
)

_cu = CU(
    backhaul_site_oam_ip=_cu_NetworkAddress,
    oam_ssh_connection_details=SshServiceDetails(
        addr=_f1_m_ip_addr, username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr=_f1_m_ip_addr, username="Nemuadmin", password="nemuuser"
    ),
    x2c=_cu_NetworkAddress,
    x2u=_cu_NetworkAddress,
    s1u=_cu_NetworkAddress,
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=157, global_bts_id=157)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASOE_3XAQQJ_2XAHPB"

# netact
_nom_ssh_connection = SshServiceDetails(
    addr="10.107.183.26",
    username="omc"
)

_nom1 = NOM(
    ssh_connections_info=[_nom_ssh_connection],
    https_main_info=HttpConnectionDetails(
        addr="https://han5lbwas.han5.srnhz.nsn-rdnet.net/authentication/Login",
        username="omc",
        password="Nokia126_",
    ),
    neo_endpoints_ip="10.107.183.26",
)
_cnms = NMS(addr="10.107.183.26", nom=_nom1)
tl = TestLine(
    test_pc=_test_pc_gnb,
    test_pcs=[_test_pc_gnb],
    ues=[_sigspark_0, _sigspark_1],
    gnbs=[_classical_bts],
    core=_epc_sim,
    attenuator=[_attenuator_0, _attenuator_1,_attenuator_2],
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
    nms=_cnms,
)

#print (tl.gnbs[0].cu.oam_ssh_connection_details.addr)


