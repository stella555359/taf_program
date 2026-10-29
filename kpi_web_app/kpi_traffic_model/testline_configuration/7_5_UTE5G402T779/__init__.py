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
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE, FPFH
from taf.config.testline import TopYoung_PDU
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
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
    LicenseKeeper,
)
from taf.config.testline import (
    Enb,
    SimEnb,
    RealEnb,
    RadioModule,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
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
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.attenuator import HBTE as PA_HBTE
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.appserver import AppServer
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4

__maintainer__ = "Chen Tong"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_2_GMS <I_MN_5G_RAN_IV4_LINE_HZG_2@internal.nsn.com>"
)
__email__ = "tong.chen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))


# Huawei
_appserver_ssh = SshServiceDetails(
    addr="10.71.219.230", username="iperf", password="39nBTScHWRf3weyBMK0=", port="52779"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.230",
    iperf_path="/usr/bin/iperf",
    port=52779,
)

_Xiaomi_host_ssh = SshServiceDetails(
    addr="10.71.218.103", username="MN5GRAN", password="nokia123@"
)

_appserver = AppServer(_iperf)

# CI_Detail_UE_Type='XIAOMI'

_xiaomi = Android(
    ssh_connection_details=_Xiaomi_host_ssh,
    serial_number="70f5029b",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["cell_Mapping: [1]", "Mi12UI13.0.12", "xiaomi"],
)

# #pdn
_pdns = [
    PDN(PDPTypes.IPV4V6.value, "dxdata2"),
]

# #realcore5g  # updated 2020/02/10
_amf_oam_ssh_connection_details = SshServiceDetails(
    addr="10.110.227.5", username="test", password="Nokia456"
)
_n2_address = NetworkAddress(v4="10.0.0.0", v6="100:00::000", vlan_id=1)
_amf = AMF(oam_ssh_connection_details=_amf_oam_ssh_connection_details, n2=_n2_address)
_real_5g_core_details = RealCore5GDetails(amf=_amf)

# #realcore5g
_realcore = RealCore(five_g=_real_5g_core_details, mcc="460", mnc="02", pdns=_pdns)

# 5GRU for classicalBTS
#_ru_0_pdu = TopYoung_PDU(addr="10.56.122.106", port_numbers=[1])

_ru_0_pdu = FPFH(addr="10.56.122.106", port_numbers=[1], login='admin', password='admin')
_ru_0 = RU(
    #'AQHA'
    ru_hw_group="Below6GHz",
    lmp_connection=SshServiceDetails(
        addr="172.22.0.2",
        username="nokia5G",
        password="noki@123",
    ),
    pdu_port=_ru_0_pdu.pdu_ports[1],
    radio_type=RadioTypes.AQHA,
    serial_number="1M231100803",
)

#_ru_1_pdu = TopYoung_PDU(addr="10.56.122.106", port_numbers=[2])
_ru_1_pdu = FPFH(addr="10.56.122.106", port_numbers=[2], login='admin', password='admin')

_ru_1 = RU(
    #'AQHA'
    ru_hw_group="Below6GHz",
    lmp_connection=SshServiceDetails(
        addr="172.22.0.6",
        username="nokia5G",
        password="noki@123",
    ),
    pdu_port=_ru_1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AQHA,
    serial_number="1M222225873",
)

#_ru_2_pdu = TopYoung_PDU(addr="10.56.122.104", port_numbers=[1])
_ru_2_pdu = FPFH(addr="10.56.122.104", port_numbers=[1], login='admin', password='admin')

_ru_2 = RU(
    #'AQHA'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.10",
        port=11,
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.56.122.72",
        username="nokia5G",
        password="noki@123",
    ),
    pdu_port=_ru_2_pdu.pdu_ports[1],
    radio_type=RadioTypes.AQHA,
    serial_number="1M231100801",
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.56.122.105", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru_0, _ru_1, _ru_2],
    f1_m_ip_addr="10.56.122.135",
)

_cu = CU(
    backhaul_site_oam_ip="10.56.122.135",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.56.122.135", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.56.122.135", username="Nemuadmin", password="nemuuser"
    ),
)


# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="10779", global_bts_id="10779"
)

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.78", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[_classical_bts],
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_realcore,
    ues=[
        _xiaomi,
    ],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
    test_pcs=[_host],
)
