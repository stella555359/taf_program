__maintainer__ = "Li Chun"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05@internal.nsn.com>"
)
__email__ = "chun.li@nokia-sbell.com"

import os
import shutil

from taf.config.testline.appserver import AppServer
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline import DU, RU, RealEnb
from taf.config.testline.fhs import FHS, FhsType
from taf.config.testline.pdu import ATEN, PduPort, HBTE, TopYoung, FPFH
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.core import RealCore, PCF
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.ue import Android, Qualcomm
from taf.config.testline.attenuator import TopYoung as PATopYoung
from taf.config.testline.lmi import SerialOverHost, Local, LMI

from collections import OrderedDict

os.environ["INIT_CONFIG_FILE_PATH"] = os.path.dirname(os.path.abspath(__file__))

__all__ = ["tl"]

os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "ue_config.yaml"
)

_lmi_Pc = TestPc(default_ssh_connection_details=SshServiceDetails(
                    addr="10.71.217.174", username="mn5gran", password="nokia123@", port="22")
)

# Radio Module gNB_2012
_ru_pdu1 = TopYoung(addr="10.71.195.34", port_numbers=[1,3,5,6])
_ru_pdu2 = HBTE(addr="10.71.195.36", port_numbers=[4,6])
_ru_pdu3 = TopYoung(addr="10.71.195.38", port_numbers=[1,2,3,4])
_ru0 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.102.1", username="serviceuser", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.21.1.21", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu1.pdu_ports[5],
    radio_type=RadioTypes.AEHC.value,
    serial_number="L1211609181",
    lmi=SerialOverHost(host=_lmi_Pc, uart_mapping=[Local(port="COM17")]),
)
_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.21.1.21", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu3.pdu_ports[1],
    radio_type=RadioTypes.AEHC.value,
    serial_number="AH242420608",
    lmi=SerialOverHost(host=_lmi_Pc, uart_mapping=[Local(port="COM12")]),
)
_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="serviceuser", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.21.1.21", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu3.pdu_ports[2],
    radio_type=RadioTypes.AEHC.value,
    serial_number="AH242420602",
    lmi=SerialOverHost(host=_lmi_Pc, uart_mapping=[Local(port="COM15")]),
)
_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="172.21.1.21", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu1.pdu_ports[6],
    radio_type=RadioTypes.FHPD.value,
)
_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="172.21.1.21", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu2.pdu_ports[4],
    radio_type=RadioTypes.FHPD.value,
)
_ru5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="172.21.1.21", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu1.pdu_ports[3],
    radio_type=RadioTypes.FHPD.value,
)

_fhs_1 = FHS(
    fhs_type=FhsType.MDEA.value,
    pdu_port=_ru_pdu1.pdu_ports[1],
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.81.128", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.124", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    rus=[_ru3, _ru4, _ru5],
)

_du0_capacity_unit_L_0 = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIO",
    rus=[_ru0, _ru1, _ru2],
)

_du0_capacity_unit_L_1 = CapacityUnit(
    addr="192.168.253.24",
    hardware_type="ABIO",
    rus=[_ru0, _ru1, _ru2],
)

_du0_capacity_unit_L_2 = CapacityUnit(
    addr="192.168.253.28",
    hardware_type="ABIO",
    fhs=[_fhs_1]
)

_gnb_ru_cablinks = [
    Cablink(source=Endpoint(unit=_du0_capacity_unit_L_0, label='SFP', port_id=4),target=Endpoint(unit=_ru0, label='SFP', port_id=3)),
    Cablink(source=Endpoint(unit=_du0_capacity_unit_L_0, label='SFP', port_id=5),target=Endpoint(unit=_ru1, label='SFP', port_id=3)),
    Cablink(source=Endpoint(unit=_du0_capacity_unit_L_0, label='SFP', port_id=6),target=Endpoint(unit=_ru2, label='SFP', port_id=3)),
    Cablink(source=Endpoint(unit=_du0_capacity_unit_L_1, label='SFP', port_id=7),target=Endpoint(unit=_ru0, label='SFP', port_id=4)),
    Cablink(source=Endpoint(unit=_du0_capacity_unit_L_1, label='SFP', port_id=8),target=Endpoint(unit=_ru1, label='SFP', port_id=4)),
    Cablink(source=Endpoint(unit=_du0_capacity_unit_L_1, label='SFP', port_id=9),target=Endpoint(unit=_ru2, label='SFP', port_id=4)),
    Cablink(source=Endpoint(unit=_du0_capacity_unit_L_2, label='SFP', port_id=1),target=Endpoint(unit=_fhs_1, label='SFP', port_id=2)),
    Cablink(source=Endpoint(unit=_fhs_1, label='SFP', port_id=4), target=Endpoint(unit=_ru3, label='SFP', port_id=2)),
    Cablink(source=Endpoint(unit=_fhs_1, label='SFP', port_id=5), target=Endpoint(unit=_ru4, label='SFP', port_id=2)),
    Cablink(source=Endpoint(unit=_fhs_1, label='SFP', port_id=6), target=Endpoint(unit=_ru5, label='SFP', port_id=2)),
]

_du_pdu = HBTE(addr="10.71.195.37", port_numbers=[1,4])

_common_unit_0_L = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[
        _du0_capacity_unit_L_0,
        _du0_capacity_unit_L_1,
        _du0_capacity_unit_L_2,
    ],
    pdu_port=_du_pdu.pdu_ports[1],
    hardware_type="ASIB",
)

_airscale = Airscale(common_units=[_common_unit_0_L])

_du = DU(airscale=_airscale, rus=[_ru0, _ru1, _ru2], f1_m_ip_addr="10.71.208.104", cablinks=_gnb_ru_cablinks)

_cu = CU(
    backhaul_site_oam_ip="10.71.208.104",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.208.104", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.208.104", username="Nemuadmin", password="nemuuser", port=443
    ),
)

_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=2012, global_bts_id=11114)


# Enb_2011
_ru6 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="rfsw", password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.21.1.21", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu3.pdu_ports[4],
    radio_type=RadioTypes.AHEGC.value,
)
_ru7 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="rfsw", password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.21.1.21", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu2.pdu_ports[6],
    radio_type=RadioTypes.AHEGC.value,
)
_ru8 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="rfsw", password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.21.1.21", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu3.pdu_ports[3],
    radio_type=RadioTypes.AHEGC.value,
)

_enb_capacity_unit_L_0 = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIA",
    rus=[_ru3, _ru4, _ru5],
)

_enb_capacity_unit_L_1 = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIA",
    rus=[_ru6, _ru7, _ru8],
)

_enb_ru_cablinks = [
    Cablink(source=Endpoint(unit=_enb_capacity_unit_L_0, label='SFP', port_id=1),target=Endpoint(unit=_ru3, label='SFP', port_id=1)),
    Cablink(source=Endpoint(unit=_enb_capacity_unit_L_0, label='SFP', port_id=2),target=Endpoint(unit=_ru4, label='SFP', port_id=1)),
    Cablink(source=Endpoint(unit=_enb_capacity_unit_L_0, label='SFP', port_id=3),target=Endpoint(unit=_ru5, label='SFP', port_id=1)),
    Cablink(source=Endpoint(unit=_enb_capacity_unit_L_0, label='SFP', port_id=1),target=Endpoint(unit=_ru3, label='SFP', port_id=1)),
    Cablink(source=Endpoint(unit=_enb_capacity_unit_L_0, label='SFP', port_id=2),target=Endpoint(unit=_ru4, label='SFP', port_id=1)),
    Cablink(source=Endpoint(unit=_enb_capacity_unit_L_0, label='SFP', port_id=3),target=Endpoint(unit=_ru5, label='SFP', port_id=1)),
]

_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[
        _enb_capacity_unit_L_0,
        _enb_capacity_unit_L_1,
    ],
    pdu_port=_du_pdu.pdu_ports[4],
    hardware_type="ASIB",
)

_real_enb = Airscale(common_units=[_common_unit_1])

_lte_2011 = RealEnb(
    system_module=_real_enb,
    rms=[_ru3, _ru4, _ru5, _ru6, _ru7, _ru8],
    cablinks=_enb_ru_cablinks,
    oam_ip=NetworkAddress(
        v4="10.71.208.103"),
    instance_id=2011,
    global_bts_id=10670,
)

_lte_real_enb2 = RealEnb(
    system_module=_airscale, rms=None, oam_ip=NetworkAddress(v4="10.71.208.104"), instance_id=2012, global_bts_id=4793
)

# Test VM
_lmp_vm_gnb_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.217.74", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_cbts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

_lmp_vm_enb_2011 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.217.75", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_lte_2011.system_module.common_units[0],
            interface_type="lmp",
        )
    ],
)

# APP server and UEs:
_appserver_ssh = SshServiceDetails(
    addr="10.71.207.149", username="vrf3_sg5", password="vrf3@sg5"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.149",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/iperf",
    port="45014",
)

_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.174", username="mn5gran", password="nokia123@"
    ),
    serial_number="R3CR50N50JW",  # R5CN20LYP5R R5CN20HRWLM R5CN212N3RX  RFCR11BREQR  RFCR40NZG0V
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "samsung"],
)

_appserver = AppServer(iperf_details=_iperf)

_attenuator = PATopYoung(
    ip_addr="10.71.208.101",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4],
    model="TAS32B8-51-120-0.25S-DES",
)

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_ASIBL_ABIOB1-B3_3xAEHC_FHS_3xFHPD_RFS_ENB"

tl = TestLine(
    test_pc=_lmp_vm_gnb_1,
    test_pcs=[_lmp_vm_enb_2011, _lmp_vm_gnb_1],
    gnbs=[_cbts],
    enbs=[_lte_2011,_lte_real_enb2],
    core=RealCore(mcc=262, mnc=3),
    ues=[_android],
    appserver=_appserver,
    attenuator=_attenuator,
    tl_cloud_topology=_tl_cloud_topology,
)
