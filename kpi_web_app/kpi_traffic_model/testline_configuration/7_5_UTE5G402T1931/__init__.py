__maintainer__ = "Liqin Yang"  # TL owner name
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05@internal.nsn.com>"  # TL owner's team
__email__ = "liqin.yang@nokia-sbell.com"  # TL owner's email


import os
import shutil
import yaml
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import RealCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import HBTE
from taf.config.testline.pdu import ATEN, PduPort
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import Android, TafUeFastmile
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
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
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline import NetworkAddress, RoutingInformation, Netact, NOM
from taf.config.testline.appserver import AppServer, TafUeAppServer
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# 5GRU for classicalBTS
_ru_pdu = HBTE(addr="10.106.223.70", port_numbers=[5])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[5],
    radio_type=RadioTypes.AQQQA,
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.106.223.228", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru, label="SFP", port_id=3),
    )
]

_du0_pdu = HBTE(addr="10.106.223.72", port_numbers=[3])

_common_unit_0_pdu_port = PduPort(pdu=_du0_pdu, port_no="3")

_du0_capacity_unit_L_0 = CapacityUnit(addr="192.168.253.20")

_du0_master_capacity_unit_L_0 = CapacityUnit(addr="fsp1_a")

_du0_slave_capacity_unit_L_0 = CapacityUnit(addr="fsp1_b")

_du0_fpga_capacity_unit_L_0 = CapacityUnit(addr="fsp1_c")

_du0_capacity_unit_L_1 = CapacityUnit(addr="192.168.253.24")

_du0_master_capacity_unit_L_1 = CapacityUnit(addr="fsp2_a")

_du0_slave_capacity_unit_L_1 = CapacityUnit(addr="fsp2_b")

_du0_fpga_capacity_unit_L_1 = CapacityUnit(addr="fsp2_c")

_du0_capacity_unit_L_2 = CapacityUnit(addr="192.168.253.28")

_du0_master_capacity_unit_L_2 = CapacityUnit(addr="fsp3_a")

_du0_slave_capacity_unit_L_2 = CapacityUnit(addr="fsp3_b")

_du0_fpga_capacity_unit_L_2 = CapacityUnit(addr="fsp3_c")

_common_unit_0_L = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[
        _du0_capacity_unit_L_0,
        _du0_master_capacity_unit_L_0,
        _du0_slave_capacity_unit_L_0,
        _du0_fpga_capacity_unit_L_0,
        _du0_capacity_unit_L_1,
        _du0_master_capacity_unit_L_1,
        _du0_slave_capacity_unit_L_1,
        _du0_fpga_capacity_unit_L_1,
        _du0_capacity_unit_L_2,
        _du0_master_capacity_unit_L_2,
        _du0_slave_capacity_unit_L_2,
        _du0_fpga_capacity_unit_L_2,
    ],
    pdu_port=_common_unit_0_pdu_port,
)

_airscale = Airscale(common_units=[_common_unit_0_L])

_du = DU(
    airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.106.223.228", cablinks=_ru_cablinks
)

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.106.223.228",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.106.223.225", ip_prefix_length=24),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.106.223.228", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.106.223.228", username="Nemuadmin", password="nemuuser", port=443
    ),
    x2c=NetworkAddress(
        v4="10.106.223.228",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.106.223.225", ip_prefix_length=28),
    ),
    x2u=NetworkAddress(
        v4="10.106.223.228",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.106.223.225", ip_prefix_length=28),
    ),
    s1u=NetworkAddress(
        v4="10.106.223.228",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.106.223.225", ip_prefix_length=28),
    ),
)


_lmp_connection_enb = SshServiceDetails(
    addr="10.106.223.228", username="toor4nsn", password="oZPS0POrRieRtu"
)

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
)
_real_enb = Airscale(common_units=[_common_unit_1])

# RealEnb
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None,
                        x2_link_addr=NetworkAddress(
                            v4="10.106.223.228",
                            routing=RoutingInformation(gateway="10.106.223.225", ip_prefix_length=27),
                        ),
                        global_bts_id=10516, instance_id=1931
                        )

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_ASIMR_ABIP_AQQQA_NETACT"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=1931, global_bts_id=11541)

# test pc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.56", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="x.x.x.x", username="ute", password="ute"
    ),
    connections=[_lte_real_enb],
)

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.139", username="vrf3_sg5", password="vrf3@sg5", port="45831"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.139",
    iperf_path="/data/data/com.nokia.android.application/",
    port=45931,
)
_appserver = AppServer(_iperf)


_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.106.223.67", username="SDT2", password="Nokia@123"
    ),
    serial_number="a1fdd103",  # a1fdd103
    server_dir="C:/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE"],
)

_ue2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.106.223.67", username="SDT2", password="Nokia@123"
    ),
    serial_number="R5CT32189CK",
    server_dir="C:/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE"],
)

_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.71.207.139",
    user="vrf3_sg5",
    password="vrf3@sg5",
    bind_interface_ip="10.71.207.139",
    expected_prompt="[mmw_sg5@appserver ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=[45831, 45931],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    ue_pc_address="10.57.195.56",
    root_password='NTgyA@xD?Z%F93Vs',
    default_user_password='rFiBt6GJqXUnQ2#Z',
    ue_manage_ip="10.106.223.90",
    data_transfer=[_fastmile_data_transfer_1],
    serial_number='KLT231600267',
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version='receiver 5g19a',
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

_fastmile_2 = TafUeFastmile(
    ue_pc_address="10.57.195.56",
    root_password='y4d9nxbAma6tfjL=',
    default_user_password='gWi6MnTLCMe:Dn7e',
    ue_manage_ip="10.106.223.91",
    data_transfer=[_fastmile_data_transfer_1],
    serial_number='KLT232200C87',
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version='receiver 5g19a',
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

_attenuator = TopYoung(ip_addr="x.x.x.x", port=23, attenuation_port_numbers=[7, 8])

_netact = Netact(
    addr="10.110.144.154",
    nom=NOM(
        ssh_connections_info=SshServiceDetails(
            addr="10.110.144.154", username="omc", password="Nokia126_"
        ),
        https_user_mgmt_info=HttpConnectionDetails(
            addr="10.110.144.154", username="omc", password="Nokia126_"
        ),
    ),
)

tl = TestLine(
    test_pc=_test_pc,
    test_pcs=[_test_pc, _test_pc_enb],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    core=RealCore(mcc=1, mnc=1),
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_ue1, _ue2, _fastmile_1, _fastmile_2],
    nms=_netact,
    attenuator=_attenuator,
    appserver=_appserver,
)
