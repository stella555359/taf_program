__maintainer__ = "Sun Shuangfeng"
__team__ = "NSB_MN_RAN_RD_VRF_HAZ1_2"
__email__ = "shuangfeng.sun@nokia-sbell.com"

import os
import yaml
from taf.config.testline.testline import TestLine
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, RRB, APC, Gude
from taf.config.testline.core import RealCore
from taf.config.testline.attenuator import HBTE
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Airphone
from taf.config.testline.pdu import FACOM
from taf.config.testline.appserver import AppServer
from taf.config.testline.attenuator import HBTE, JFW, AttenuationPort, TopYoung
from taf.config.testline.core import RealCore
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    Android,
    Qualcomm,
    QualcommUeType,
)
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
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
from taf.config.testline.enb import (
    RealEnb,
)
# common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

## attenuator
_attenuator_5G = TopYoung(
    ip_addr="10.97.65.201",
    port=3000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                              26, 27, 28, 29, 30, 31, 32],
    model="TAS16T16-51-120-1S-DES",
)

# Iperf
_appserver_ssh = SshServiceDetails(
    addr="10.106.243.149", username="ute", password="PZ1RRM3!5t6y7u", port="54015"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.106.243.149",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port="54015",
)

_appserver = AppServer(_iperf)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.97.65.203", username="toor4nsn", password="oZPS0POrRieRtu"
)

# Multi BBMOD
_capacity_unit0 = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIO",
#    serial_number="L1211604246",
)

_capacity_unit1 = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIO",
#    serial_number="DH214543071",
)

_capacity_unit2 = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIP",
#    serial_number="L1233704794",
)

_gnb_pdu = FACOM(addr="10.56.107.8", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit0, _capacity_unit1, _capacity_unit2],
    pdu_port=_gnb_pdu.pdu_ports[1],
    hardware_type="ASIL",
#    serial_number="L1202800702",
)

_airscale = Airscale([_common_unit_0])

# 5GRU for classicalBTS
#PB releated
_ru_0_pdu = FACOM(addr="10.56.107.8", port_numbers=[2])
_ru_1_pdu = FACOM(addr="10.56.107.8", port_numbers=[3])
_ru_2_pdu = FACOM(addr="10.56.107.8", port_numbers=[4])
_ru_3_pdu = FACOM(addr="10.56.107.8", port_numbers=[5])
_ru_4_pdu = FACOM(addr="10.56.107.8", port_numbers=[6])
_ru_5_pdu = FACOM(addr="10.97.65.130", port_numbers=[1])
_ru_6_pdu = FACOM(addr="10.97.65.130", port_numbers=[2])
_ru_7_pdu = FACOM(addr="10.97.65.130", port_numbers=[3])
_ru_8_pdu = FACOM(addr="10.97.65.130", port_numbers=[4])
_ru_9_pdu = FACOM(addr="10.97.65.130", port_numbers=[5])


_ru_0 = RU(
    ru_hw_group="AHFII",
    radio_type="AHFII",
    serial_number="BL2316N44Y3",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[6],
    ],

	    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.9.10", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.9.10", username="root", password="root"
    ),
    pdu_port=_ru_0_pdu.pdu_ports[2],
)

_ru_0_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit2, label="SFP", port_id=1),
        target=Endpoint(unit=_ru_0, label="SFP", port_id=1),
    )
]

_ru_1 = RU(
    ru_hw_group="AHLOB",
    radio_type="AHLOB",
    serial_number="AH243706266",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[26],
        _attenuator_5G.attenuator_ports[30],
    ],
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.9.6", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.9.6", username="root", password="root"
    ),
    pdu_port=_ru_1_pdu.pdu_ports[3],
)

_ru_1_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit2, label="SFP", port_id=2),
        target=Endpoint(unit=_ru_1, label="SFP", port_id=1),
    )
]

_ru_2 = RU(
    ru_hw_group="AEHC",
    radio_type="AEHC",
    serial_number="L1203605096",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[2],
        _attenuator_5G.attenuator_ports[28],
    ],

    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.9.10", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.9.10", username="root", password="root"
    ),
    pdu_port=_ru_2_pdu.pdu_ports[4],
)

_ru_2_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit2, label="SFP", port_id=3),
        target=Endpoint(unit=_ru_2, label="SFP", port_id=1),
    )
]

_ru_3 = RU(
    ru_hw_group="AZQI",
    radio_type="AZQI",
    serial_number="1M214039124",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[8],
        _attenuator_5G.attenuator_ports[10],
    ],

    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.9.10", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.9.10", username="root", password="root"
    ),
    pdu_port=_ru_3_pdu.pdu_ports[5],
)

_ru_3_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit1, label="SFP", port_id=1),
        target=Endpoint(unit=_ru_3, label="SFP", port_id=1),
    )
]

_ru_4 = RU(
    ru_hw_group="AHEGB",
    radio_type="AHEGB",
    serial_number="EA203761488",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[24],
        _attenuator_5G.attenuator_ports[32],
        _attenuator_5G.attenuator_ports[20],
    ],

    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.9.10", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.9.10", username="root", password="root"
    ),
    pdu_port=_ru_4_pdu.pdu_ports[6],
)

_ru_4_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit1, label="SFP", port_id=2),
        target=Endpoint(unit=_ru_4, label="SFP", port_id=1),
    )
]

_ru_5 = RU(
    ru_hw_group="AHFIB",
    radio_type="AHFIB",
    serial_number="BL2236V089P",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[23],
        _attenuator_5G.attenuator_ports[27],
        _attenuator_5G.attenuator_ports[19],
        _attenuator_5G.attenuator_ports[11],
    ],

    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.9.10", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.9.10", username="root", password="root"
    ),
    pdu_port=_ru_5_pdu.pdu_ports[1],
)

_ru_5_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit1, label="SFP", port_id=1),
        target=Endpoint(unit=_ru_5, label="SFP", port_id=1),
    )
]
#37416
_ru_6 = RU(
    ru_hw_group="AZHA",
    radio_type="AZHA",
    serial_number="RW191708325",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[12],
    ],

    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.9.10", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.9.10", username="root", password="root"
    ),
    pdu_port=_ru_6_pdu.pdu_ports[2],
)

_ru_6_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit1, label="SFP", port_id=1),
        target=Endpoint(unit=_ru_6, label="SFP", port_id=1),
    )
]

_ru_7 = RU(
    ru_hw_group="AHFII",
    radio_type="AHFII",
    serial_number="BL2316N44UK",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[3],
        _attenuator_5G.attenuator_ports[31],
    ],

    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.9.10", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.9.10", username="root", password="root"
    ),
    pdu_port=_ru_7_pdu.pdu_ports[3],
)

_ru_7_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit1, label="SFP", port_id=1),
        target=Endpoint(unit=_ru_7, label="SFP", port_id=1),
    )
]

_ru_8 = RU(
    ru_hw_group="AEQE",
    radio_type="AEQE",
    serial_number="1M202413278",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[18],
        _attenuator_5G.attenuator_ports[22],
    ],

    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.9.10", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.9.10", username="root", password="root"
    ),
    pdu_port=_ru_8_pdu.pdu_ports[4],
)

_ru_8_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit1, label="SFP", port_id=1),
        target=Endpoint(unit=_ru_8, label="SFP", port_id=1),
    )
]
#37416
_ru_9 = RU(
    ru_hw_group="AZQJ",
    radio_type="AZQJ",
    serial_number="1M243003806",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[14],

    ],

    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.9.10", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.9.10", username="root", password="root"
    ),
    pdu_port=_ru_9_pdu.pdu_ports[5],
)

_ru_9_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit1, label="SFP", port_id=1),
        target=Endpoint(unit=_ru_9, label="SFP", port_id=1),
    )
]
# Multi_RU
_du = DU(airscale=_airscale,
         rus=[_ru_0, _ru_1, _ru_2, _ru_3, _ru_4, _ru_5, _ru_7, _ru_8],
         f1_m_ip_addr="10.97.65.203",
         cablinks=[_ru_0_cablinks, _ru_1_cablinks, _ru_2_cablinks, _ru_3_cablinks, _ru_4_cablinks,
                   _ru_5_cablinks, _ru_7_cablinks,_ru_8_cablinks],
         )

_cu = CU(
    backhaul_site_oam_ip="10.97.65.203",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.97.65.203", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.97.65.203", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.97.65.203", vlan_id=10),
    x2u=NetworkAddress(v4="10.97.65.203", vlan_id=10),
    s1u=NetworkAddress(v4="10.97.65.203", vlan_id=10),
)

_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=10772, global_bts_id=10772)

_du1 = DU(airscale=_airscale,
          rus=[_ru_6,_ru_9],
          f1_m_ip_addr="10.56.107.70",
          cablinks=[_ru_6_cablinks,_ru_9_cablinks],
          )

_cu1 = CU(
    backhaul_site_oam_ip="10.56.107.70",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.56.107.70", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.56.107.70", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.56.107.70", vlan_id=10),
    x2u=NetworkAddress(v4="10.56.107.70", vlan_id=10),
    s1u=NetworkAddress(v4="10.56.107.70", vlan_id=10),
)

_cbts1 = ClassicalBts(cu=_cu1, dus=[_du1], instance_id=37416, global_bts_id=37416)

# RealEnb--4G
_real_enb_pdu = FACOM(addr="10.97.65.203", port_numbers=[2])

_real_enb = Airscale(common_units=[_common_unit_0])

_lte_real_enb = RealEnb(
    airscale=_real_enb,
    system_module=_common_unit_0,
    rms=[_ru_4],
    oam_ip=NetworkAddress("10.97.65.203"),
    instance_id=10772,
)

# huawei_mate40
Samsung_s22 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.65.202", username="aic", password="Nokia123!"
    ),
    serial_number="R5CTA17R6QH",
    server_dir="/cygdrive/c/pyro_server",
    # python_path="C:/Python27/python.exe",
    python_path="/cygdrive/c/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Commercial", "samsung"],
)

Samsung_s24 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.65.202", username="aic", password="Nokia123!"
    ),
    serial_number="RFCX10ME4QR",
    server_dir="/cygdrive/c/pyro_server",
    # python_path="C:/Python27/python.exe",
    python_path="/cygdrive/c/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Commercial", "samsung"],
)

_M70 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.65.202", username="aic", password="Nokia123!"
    ),
    serial_number="0123456789ABCDEF",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Qualcomm", "REAL_ANDROID_UE"],
)

Qualcomm = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.65.202", username="aic", password="Nokia123!"
    ),
    serial_number="3e5229bd",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "REAL_QUALCOMM_UE"],
)

oppo = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.65.202", username="aic", password="Nokia123!"
    ),
    serial_number="YH49FMYX4PEUNNGQ",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Commercial", "OPPO"],
)

huawei1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.65.202", username="aic", password="Nokia123!"
    ),
    serial_number="7TD5T21415000127",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Commercial", "huawei1"],
)

# ute vm not UE PC
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.56.198.41", username="ute", password="ute"
    ),
    connections=[_cbts.dus[0].airscale.common_units[0]],
)
_realcore = RealCore(five_g=None, mcc="262", mnc="03", pdns=None)

tl = TestLine(
    test_pc=_test_pc,
    ues=[Qualcomm, Samsung_s22, Samsung_s24, _M70],
    gnbs=[_cbts, _cbts1],
    enbs=[_lte_real_enb],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_NSA_SA_1xQC_1xASIL_2xABIO_1xAHLOB_1xAHFII_1xAEQE",
    attenuator=_attenuator_5G,
    appserver=_appserver,
    core=_realcore,
)

__all__ = ["tl"]
