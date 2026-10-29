import os
import re
import yaml
from taf.config.testline.connection_details import (
    SshServiceDetails,
    TelnetConnectionDetails,
    IperfDataTransferDetails,
    OpenStackConnectionDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
)
from taf.config.testline.core import (
    EPCSim,
    RealCore4G,
    RealCore,
    RealCore5GDetails,
    AMF,
)
from taf.config.testline.airscale import Airscale, CapacityUnit, CommonUnit
from taf.config.testline.enb import RealEnb
from taf.config.testline.flexi import Flexi
from taf.config.testline.pdu import FACOM, HBTE, TopYoung
from taf.config.testline.radio import RU, RadioTypes
from taf.config.testline.ran import BSC, RNC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.testpc import TestPc
from taf.config.testline.appserver import AppServer, TafUeAppServer
from taf.config.testline.ue import TafUeFastmile
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
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline.gnb.du import DU
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol


__maintainer__ = "Qingqing Deng"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_03_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_03@internal.nsn.com>"  # TL owner's team
__email__ = "qingqing.deng@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.34", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_pdu_1 = TopYoung(addr="10.101.45.208", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_fsp_1 = CapacityUnit(
    addr="192.168.253.21",
    hardware_type="ABIO",
    hardware_version="475266A.M01",
    serial_number="L1204201498",
)

_fct_1 = CommonUnit(
    SshServiceDetails(
        addr="10.101.40.230", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_fsp_1],
    pdu_port=_pdu_1.pdu_ports[3],
    hardware_type="ASIB",
    hardware_version="473764A.M02",
    serial_number="L1202403064",
)

_ru_pdu = TopYoung(addr="10.101.45.214", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_rmod_1 = RU(
    ru_hw_group="hw_group",
    radio_type=RadioTypes.AEQP,
    serial_number="1M221126973",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.22",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    pdu_port=_ru_pdu.pdu_ports[4],
)

_enb_sbts_1 = RealEnb(
    system_module=[_fct_1],
    rms=[_rmod_1],
    oam_ip=NetworkAddress("10.101.40.230"),
    instance_id=1148,
    global_bts_id=1148,
)


# #5GRU_0 for cloudBTS
_ru_pdu = TopYoung(addr="10.101.45.214", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.22",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_ru_pdu.pdu_ports[4],
    radio_type=RadioTypes.AEQP,
)


# #DU_0 for cloudlBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.101.40.230", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.21")

_du_pdu = TopYoung(addr="10.101.45.208", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit],
    pdu_port=_du_pdu.pdu_ports[4],
)

_airscale = Airscale(common_units=[_common_unit_0])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru, label="SFP", port_id=1),
    )
]

_du = DU(
    airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.101.40.230", cablinks=_ru_cablinks
)


# #CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.101.40.230",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.40.225", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.40.230", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.40.230", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.101.40.230",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.40.225", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.101.40.230",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.40.225", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.101.40.230",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.40.225", ip_prefix_length=27),
    ),
)


# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=1148, global_bts_id=1148)

# #######################Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.198", username="vrf3_sg2", password="vrf3@sg2"
)

_mtk_host_ssh = SshServiceDetails(
    addr="10.68.86.188", username="nokia5G", password="noki@123"
)

_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="",
    iperf_path="C:/Tool/UE-iperf-tool/iperf",
    port="42148",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.198",
    iperf_path="/usr/bin/iperf",
    port="42148",
)
_appserver = AppServer(_iperf_details_on_appserver)

# for FastMile CPE
# _fastmile_tl148_appserver = TafUeAppServer(
#    app_server_name='APP_SERVER_1',
#    address='10.57.178.20',
#    user='mmw_sg2_3',
#    password='mm@2@3',
#    bind_interface_ip='10.57.178.20',
#    expected_prompt='[mmw_sg2_3@WA19-APPServer-5 ~]$ ',
#    binary_path='/usr/bin/iperf',
#    ports=[42148, 43148])

_fastmile_tl148_appserver = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.195",
    user="vrf3_sg2",
    password="vrf3@sg2",
    bind_interface_ip="10.57.191.195",
    expected_prompt="[vrf3_sg2@appserver ~]$",
    binary_path="/usr/bin/iperf",
    ports=[42148, 42248],
)


_fastmile_tl148_data_transfer = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_tl148_appserver,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile = TafUeFastmile(
    com_port="19",
    ue_pc_address="10.68.86.188",
    root_password="595aaa22b757",
    ue_manage_ip="192.168.1.1",
    serial_number="LPL2214005F2",
    data_transfer=[
        _fastmile_tl148_data_transfer,
    ],
    ue_pc_port=2148,
    version="3.2",
    capabilities=["REAL_UE", "nokia_fastmile"],
)

_pdns = [
    PDN(pdp_type=PDPTypes.IP.value, apn="dxdata1"),
    PDN(pdp_type=PDPTypes.IP.value, apn="dxdata1"),
]
_core = RealCore(pdns=_pdns)


tl = TestLine(
    test_pc=_host,
    enbs=[_enb_sbts_1],
    ues=[_fastmile],
    gnbs=[_classical_bts],
    core=_core,
    tl_cloud_topology="_1ASIL_1ABIO_1AEQP",
)
