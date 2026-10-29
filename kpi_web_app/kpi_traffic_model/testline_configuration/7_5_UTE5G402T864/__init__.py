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
from taf.config.testline.attenuator import (
    AttenuationPort,
    HBTE,
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
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.dcap import DcapRnD, DcapBasic


__maintainer__ = "Hong Liping"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_07_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_07@internal.nsn.com>"
__email__ = "liping.hong@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# testPc(taf)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.152", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_docker_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.163",
        username="dcapuser",
        password="iW_K#8.ute%A10h0m0ra",
        port=49151,
    )
)
_tce_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.163",
        username="dcapuser",
        password="iW_K#8.ute%A10h0m0ra",
        port=49151,
    )
)

_dcapbasic = DcapBasic(
    connection_details=HttpConnectionDetails(
        addr="10.57.195.83",
        port=49148,
        username="utfuser",
        password="utfadmin!",
    )
)

_attenuator = HBTE(
    ip_addr="10.71.204.212",
    port="5000",
    model="PA-16-16-6-127-0.5-B-S",
    attenuation_port_numbers=[r for r in range(1, 17)],
)

_PB_2IG01_1 = FACOM(addr="10.71.196.34", port_numbers=[r for r in range(1, 9)])

_PB_2IG02_1 = FACOM(addr="10.71.196.36", port_numbers=[r for r in range(1, 9)])

_PB_2IG02_2 = FACOM(addr="10.71.196.37", port_numbers=[r for r in range(1, 9)])

_PB_2IG03_1 = FACOM(addr="10.71.196.38", port_numbers=[r for r in range(1, 9)])

_PB_2IG05_1 = FACOM(addr="10.71.196.42", port_numbers=[r for r in range(1, 9)])

# ----------------------------------------------------
# ----------------5G TestLine TL864-------------------
# ----------------------------------------------------

# 5G RU
_ru_pdu = FACOM(addr="10.71.196.34", port_numbers=[3])
_ru1 = RU(
    ru_hw_group="AZQJ",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.0.176.212", username="ute", password="3edc4rfv%TGB"
    ),
    # lmp_connection=SshServiceDetails(addr='10.68.86.50', username='root', password='nokia123'),
    pdu_port=_ru_pdu.pdu_ports[3],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_ru2_pdu = FACOM(addr="10.71.196.34", port_numbers=[4])
_ru2 = RU(
    ru_hw_group="AZQJ",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.0.176.211", username="ute", password="3edc4rfv%TGB"
    ),
    # lmp_connection=SshServiceDetails(addr='10.68.86.50', username='root', password='nokia123'),
    pdu_port=_ru2_pdu.pdu_ports[4],
    attenuation_ports=[
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

# DU
# _lmp_connection = SshServiceDetails(
#     addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
# )
# _capacity_unit = CapacityUnit(addr="192.168.253.20")
# _gnb_pdu = FACOM(addr="10.71.196.37", port_numbers=[4])
_tl864_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[CapacityUnit(addr="192.168.253.20")],
    pdu_port=_PB_2IG02_2.pdu_ports[4],
)
# _airscale = Airscale(common_units=[_common_unit_0])
_tl864_du = DU(
    airscale=Airscale(common_units=[_tl864_common_unit]),
    rus=[_ru1, _ru2],
    f1_m_ip_addr="10.71.211.162",
)

# CU
_tl864_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.211.162", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.211.162", username="Nemuadmin", password="nemuuser"
    ),
)

# GNB
_tl864_classical_bts = ClassicalBts(
    # dus=[_tl864_du],cu=_tl864_cu, instance_id=10843, global_bts_id=10843, dcap=_dcapbasic,
    dus=[_tl864_du],
    cu=_tl864_cu,
    instance_id=864,
    global_bts_id=864,
    dcap=_dcapbasic,
)

# ----------------5G TestLine TL865-------------------
_tl865_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_PB_2IG02_1.pdu_ports[2],
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[12],
    ],
)
# DU
_tl865_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[CapacityUnit(addr="192.168.253.20")],
    pdu_port=_PB_2IG02_2.pdu_ports[5],
)
_tl865_du = DU(
    airscale=Airscale(common_units=[_tl865_common_unit]),
    rus=[_tl865_ru1],
    f1_m_ip_addr="10.71.211.163",
)
# CU
_tl865_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.211.163", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.211.163", username="Nemuadmin", password="nemuuser"
    ),
)
# GNB
_tl865_classical_bts = ClassicalBts(
    dus=[_tl865_du], cu=_tl865_cu, instance_id=10844, global_bts_id=10844
)


# RealEnb
_enb_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.211.165", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_PB_2IG02_2.pdu_ports[7],
)

_lte_real_enb = RealEnb(
    # airscale=Airscale(common_units=[_enb_common_unit]),global_bts_id=10447,instance_id=10447,
    airscale=Airscale(common_units=[_enb_common_unit]),
    global_bts_id=865,
    instance_id=865,
)

_enb_common_unit2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.211.202", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_PB_2IG05_1.pdu_ports[3],
)
_lte_real_enb2 = RealEnb(
    airscale=Airscale(common_units=[_enb_common_unit2]),
    global_bts_id=10702,
    instance_id=10702,
)

# Real Core
_real_5g_core_details = RealCore5GDetails(
    amf=AMF(
        oam_ssh_connection_details=SshServiceDetails(
            addr="10.110.66.198", username="xxx", password="xxx"
        ),
        n2=NetworkAddress(v4="xxx.xxx.xx.xx", v6="xxx:xx::xxx", vlan_id=1),
    )
)
_realcore = RealCore(five_g=_real_5g_core_details, mcc="262", mnc="3")

# UE
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.238", username="vrf3_sg6", password="vrf3@sg6"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.238",
    iperf_path="/usr/bin/iperf",
    port=57864,
)
_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.154", username="mn5gran", password="nokia123@"
    ),
    serial_number="9EQUT20903003352",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "honor"],
)
_android_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.154", username="mn5gran", password="nokia123@"
    ),
    # serial_number="L8K5T19925008493",
    serial_number="L8K5T19910016408",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei"],
)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    test_pcs=[_docker_pc, _tce_pc],
    gnbs=[_tl864_classical_bts],
    enbs=[_lte_real_enb],
    core=_realcore,
    ues=[_android_2, _android_1],
    attenuator=_attenuator,
    tl_cloud_topology=_tl_cloud_topology,
)
