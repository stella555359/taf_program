import os
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.testpc import Connection
from taf.config.testline.core import RealCore
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
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
)  # added in taf.meta 5.4
from taf.config.testline.attenuator import HBTE as att_HBTE
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.appserver import AppServer
# from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android, MediaTek

__maintainer__ = "Liu Jia"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_3_GMS <I_MN_5G_RAN_IV4_LINE_HZG_3@internal.nsn.com>"
)
__email__ = "jia-rebecca.liu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #test PC
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.37", username="ute", password="ute"
       # addr="10.57.167.60", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.173.233",
    username="vrf4_sg3",
    password="Haz4_vrf_sg3",
    port="53162",
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.173.233",
    iperf_path="/cygdrive/c/iperf",
    port="53262",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.173.233",
    iperf_path="iperf",
    port="53362",
)
_appserver = AppServer(_iperf_details_on_appserver2)



_pdns = [
    PDN(pdp_type=PDPTypes.IP.value, apn="dxdata1"),
    PDN(pdp_type=PDPTypes.IP.value, apn="ims"),
    PDN(pdp_type=PDPTypes.IP.value, apn="mdrb.nokia.com")
]

_realcore = RealCore(
    four_g=None, five_g=None, mcc="262", mnc="03", pdns=_pdns,

)
# CI_Detail_UE_Type='Qualcomm'
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.27", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="8d616d37",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["qct_dx50", "REAL_ANDROID_UE"],
)
# CI_Detail_UE_Type='sumsungS24'
_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.27", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCWC0BVNNV",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.5.0.57---08191556\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung", "samsung"],
    imsi="262033100020894",
    sec_key="13100020894",
)
# CI_Detail_UE_Type='sumsungS23'
_android_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.75", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R3CW201W9KX",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.5.0.57---08191556\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung", "samsung"],
    imsi="262033100020893",
    sec_key="13100020893",
)

# CI_Detail_UE_Type='sumsungS21'
_android_3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.75", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R3CR412WBWE",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.5.0.57---08191556\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung", "samsung"],
    imsi="310260100008767",
    sec_key="13100008767",
)
# CI_Detail_UE_Type='MTK M60'
_mtk_host_ssh = SshServiceDetails(
    addr="10.57.150.113", username="MN5GRAN", password="nokia123@"
)

_iperf_details_on_appserver_for_caymus_ul = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address='10.57.150.113',
    iperf_path='/usr/bin/iperf',
    port=53162,
    ports=[53262, 53362, 53462, 53562])

_appserver_for_caymus_ul = AppServer(_iperf_details_on_appserver_for_caymus_ul)

_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="",
    iperf_path="/usr/bin/iperf",
    port=53362,
)

_elt_path = "/cygdrive/c/Users/mn5gran/Downloads/ELT_32"

_mtk_ue_box = MediaTek(
    ssh_connection_details=_mtk_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="C:/Users/mn5gran/Downloads/MDDB_MT6815_S00_NR17R.R1.TC42.SP.W24.44.p2.EDB",
    log_filter='2.Gen99_Default_Standard',
    imei="12345678901234",
    imsi="460023100020794",
    apn_url="dxdata1",
    iperf_details=_iperf_details_on_mtk,
    capabilities=["REAL_MEDIATEK_UE", "mtk"],
    serial_number="0123456789ABCDEF",
)

_mtk_ue_box.elt_path = _elt_path


# #RealEnb
_real_enb_pdu = HBTE(addr="10.57.249.13", port_numbers=[5])

_real_enb2_pdu = FACOM(addr="10.57.249.13", port_numbers=[6])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.226.134", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[5],
)

_common_unit_3 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.226.144", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb2_pdu.pdu_ports[6],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_real_enb_2 = Airscale(common_units=[_common_unit_3])

_lte_real_enb = RealEnb(airscale=_real_enb, instance_id=36221)

_lte_real_enb_2 = RealEnb(airscale=_real_enb_2, rms=None, instance_id=36222)

# #5GRU for classicalBTS
# attenuator
_attenuator = TopYoung(
    ip_addr="10.57.226.135",
    port=28888,
    attenuation_port_numbers=[1, 2, 3, 4],
    model="MCS2338A2-64B16-A4",
)

hbte_attenuator = att_HBTE(ip_addr="10.57.239.211",
                       port=5000,
                       attenuation_port_numbers=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
                       model='PA-16-16-6-127-0.5-B-S')


_ru1_pdu = HBTE(addr="10.57.176.66", port_numbers=[3])
_ru2_pdu = HBTE(addr="10.57.176.66", port_numbers=[4])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="serviceuser", password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.2", username="serviceuser", password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4="
    ),
    pdu_port=_ru1_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEHC.value,
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.128", username="serviceuser", password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.33.128", username="serviceuser", password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="
    ),
    pdu_port=_ru2_pdu.pdu_ports[4],
    radio_type=RadioTypes.AHFII.value,
)

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIO",
#    rus=[_ru1,_ru2],
)

_gnb_pdu = HBTE(addr="10.57.249.13", port_numbers=[2])

_ru_cablinks = [Cablink(source=Endpoint(unit=_capacity_unit, label='SFP', port_id=1), target=Endpoint(unit=_ru1, label='SFP', port_id=2)),
                Cablink(source=Endpoint(unit=_capacity_unit, label='SFP', port_id=7), target=Endpoint(unit=_ru1, label='SFP', port_id=3)),
                Cablink(source=Endpoint(unit=_capacity_unit, label='SFP', port_id=1), target=Endpoint(unit=_ru2, label='SFP', port_id=1)),
                # Cablink(source=Endpoint(unit=_capacity_unit, label='SFP', port_id=2), target=Endpoint(unit=_ru2, label='SFP', port_id=2))
                ]

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
    hardware_type="ASIL",
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru1,_ru2],
    f1_m_ip_addr="10.57.226.133",
    f1_c_ip_addr="10.57.226.133",
    f1_u_ip_addr="10.57.226.133",
#    cablinks=_ru_cablinks,
)


# #CU

_cu = CU(backhaul_site_oam_ip=NetworkAddress(v4='10.57.226.133', vlan_id=None,
                                             routing=RoutingInformation(gateway='10.57.226.129', ip_prefix_length=27)),
    oam_ssh_connection_details=SshServiceDetails(addr='10.57.226.133', username='toor4nsn', password='oZPS0POrRieRtu'),
    oam_http_connection_details=HttpConnectionDetails(addr='10.57.226.133', username='Nemuadmin', password='nemuuser'),
    x2c=NetworkAddress(v4='10.57.226.133', vlan_id=None,
                       routing=RoutingInformation(gateway='10.57.226.129', ip_prefix_length=27)),
    x2u=NetworkAddress(v4='10.57.226.133', vlan_id=None,
                       routing=RoutingInformation(gateway='10.57.226.129', ip_prefix_length=27)),
    s1u=NetworkAddress(v4='10.57.226.133', vlan_id=None,
                       routing=RoutingInformation(gateway='10.57.226.129', ip_prefix_length=27)))


_classical_bts0 = ClassicalBts(dus=[_du], cu=_cu, instance_id=10318, global_bts_id=3621199999)

# #host
_gnb_testpc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.37", username="ute", password="ute"
       # addr="10.57.167.60", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts0.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

_enb_testpc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.37", username="ute", password="ute"
    ),
    connections=[],
)

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_QC_ASIML_ABIOB1B2_AEQV_AZQO"

tl = TestLine(
    test_pc=_gnb_testpc,
    test_pcs=[_gnb_testpc],
    gnbs=[_classical_bts0],
    enbs=[_lte_real_enb,_lte_real_enb_2],
    core=_realcore,
    ues=[_android,_android_1,_android_2,_android_3,_mtk_ue_box],
    appserver=_appserver,
    attenuator=[_attenuator,hbte_attenuator],
    tl_cloud_topology=_tl_cloud_topology,
)
