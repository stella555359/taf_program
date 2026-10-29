import os
from collections import OrderedDict
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
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline import Enb, SimEnb, RealEnb, RadioModule, LTEEmuEnb, PrismaEnb
from taf.config.testline.appserver import AppServer
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.dcap import DcapRnD, DcapBasic
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)

__maintainer__ = "He Jingmin"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_07_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_07@internal.nsn.com>"
__email__ = "jingmin.he@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_dcap_1 = DcapBasic(
    connection_details=HttpConnectionDetails(
        addr="10.57.195.82", port="443", username="utfuser", password="utfadmin!"
    )
)
_tce_1778 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.82",
        username="utfuser",
        password="utfadmin!",
        port=49148,
    )
)
_tce_1756 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.82",
        username="utfuser",
        password="utfadmin!",
        port=49148,
    )
)
_tce_pc = DcapBasic(
    connection_details=HttpConnectionDetails(
        addr="10.57.195.82",
        username="utfuser",
        password="utfadmin!",
        port=49148,
    )
)

# CI_Detail_UE_Type='Huawei Mate 20'
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.238", username="vrf3_sg6", password="vrf3@sg6"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.238",
    iperf_path="/usr/bin/iperf",
    port=57802,
)

# UE
_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.170", username="mn5gran", password="nokia123@"
    ),
    serial_number="9EQUT20903003187",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["ANDROID_UE0", "huawei"],
)

_iperf_ul = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.238",
    iperf_path="iperf",
    port="57802",
)
_appserver_ul = AppServer(_iperf_ul)

# #5GRU
_ru_pdu = HBTE(addr="10.57.241.230", port_numbers=[1])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0=",
    ),
    # lmp_connection=SshServiceDetails(
    #    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    # ),
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AVQC.value,
)

# #DU
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)

_capacity_unit = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIP",
    # rus=[_ru],
)

_gnb_pdu = HBTE(addr="10.57.241.233", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
    hardware_type="ASIM",
)

_airscale = Airscale(common_units=[_common_unit_0])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru, label="SFP", port_id=1),
    )
]
_du = DU(
    airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.57.151.226", cablinks=_ru_cablinks
)

_cu = CU(
    backhaul_site_oam_ip="10.57.151.226",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.151.226", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.151.226", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id=1802, global_bts_id=1802, dcap=_tce_pc
)

# #host
_gnb_testpc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.33", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_SA_ASIML_ABIPB1_AEQY_NETACT"

# Real Core
_real_5g_core_details = RealCore5GDetails(
    amf=AMF(
        oam_ssh_connection_details=SshServiceDetails(
            addr="10.110.227.5", username="xxx", password="xxx"
        ),
        n2=NetworkAddress(v4="xxx.xxx.xx.xx", v6="xxx:xx::xxx", vlan_id=1),
    )
)
_realcore = RealCore(five_g=_real_5g_core_details, mcc="460", mnc="2")

tl = TestLine(
    test_pc=_gnb_testpc,
    test_pcs=[_gnb_testpc],
    gnbs=[_classical_bts],
    ues=[_android_0],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver_ul,
    core=_realcore,
)
