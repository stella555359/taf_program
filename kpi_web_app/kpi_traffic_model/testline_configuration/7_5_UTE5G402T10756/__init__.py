import os
import yaml
import re
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import RealCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE, FPFH, TopYoung
from taf.config.testline.radio import RU, RadioTypes
from taf.config.testline.ran import BSC, RNC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)

# added in taf.meta.5.4
from taf.config.testline import RealEnb
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.ue import TafUeAndroid
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.pdn import PDNTafUeAndroidDetails

__maintainer__ = "Xiaodong Chen"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_02_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_02@internal.nsn.com>"

# TL owner's team
__email__ = "xiaodong.d.chen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_attenuator = AHBTE(
    ip_addr="10.71.206.115",
    port=5000,
    attenuation_port_numbers=[5, 6, 7, 8],
    model="PA-16-16-6-127-0.5-B-S",
)

# CI_Detail_UE_Type='Samsung Galaxy S20'
_app_server_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.71.207.143",
    user="vrf4_sg2",
    password="Vrf4@sg2_123456",
    expected_prompt="[vrf4_sg2@appserver ~]$ ",
    ports=[52011, 52126],
)

_data_transfer_iperf_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_app_server_1,
    interval=1,
)

_ue1 = TafUeAndroid(
    serial_number="R5CN103KSWY",
    ue_pc_address="10.0.176.232",
    data_transfer=[_data_transfer_iperf_1],
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.232", username="mn5gran", password="nokia123@"
    ),
    ue_pc_port="8080",
    imei="354144110031455",
    imsi="262033100011519",
    qualcomm_prototype=False,
    voice_call_dialing_timeout="30",
    network_mode_switch_method="ADB",
    airplane_mode_switcher_text="Off|On",
    capabilities=["REAL_UE", "samsung_ue"],
)

_ru1_pdu = HBTE(addr="10.71.197.12", port_numbers=[2])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", 
        username="serviceuser", 
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.2", 
        username="serviceuser", 
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY="
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AQHA,
    serial_number="1M194713981",
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_ru2_pdu = FPFH(addr="10.71.197.12", port_numbers=[3], login='admin', password='admin')
_ru2 = RU(
    #'AQHA'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.6", 
        username="serviceuser", 
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.6",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    pdu_port=_ru2_pdu.pdu_ports[3],
    radio_type=RadioTypes.AQHA,
    serial_number="1M231100803",
)

_ru3_pdu = FPFH(addr="10.71.197.12", port_numbers=[4], login='admin', password='admin')
_ru3 = RU(
    #'AQHA'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.10", 
        username="serviceuser", 
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.10",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    pdu_port=_ru3_pdu.pdu_ports[4],
    radio_type=RadioTypes.AQHA,
    serial_number="1M231100801",
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = TopYoung(addr="10.101.46.36", port_numbers=[1])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru1, _ru2, _ru3], f1_m_ip_addr="10.71.214.202")

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.214.202",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.214.129", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.214.202", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.214.202", username="Nemuadmin", password="nemuuser"
    ),
)

# RealEnb  enb&enb_HBTE ip_addr
_lmp_connection_enb = SshServiceDetails(
    addr="10.71.214.202", username="toor4nsn", password="oZPS0POrRieRtu"
)

_enb_pdu = HBTE(addr="10.71.197.14", port_numbers=[1])

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb)

# cloud_topology
_tl_cloud_topology = "CLOUD_SRAN_L_1ASIB_1ABIO_1AQHA"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=10756, global_bts_id=10756)

# host
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.6", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[_classical_bts],
)

_test_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.6", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[_lte_real_enb],
)

tl = TestLine(
    test_pc=_test_pc,
    test_pcs=[_test_pc, _test_pc_1],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    ues=[_ue1],
    # ues=[_ue_config],
    core=RealCore(mcc=262, mnc=3),
    attenuator=_attenuator,
    tl_cloud_topology=_tl_cloud_topology,
)
