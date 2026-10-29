__maintainer__ = "Zhou Leiming"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05_GMS"
__email__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05@internal.nsn.com"
__owner_email__ = "leiming.zhou@nokia-sbell.com"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline.pdu import Gude, HBTE, TopYoung, PduPort
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline import DU, RU
from taf.config.testline.core import RealCore5G
from taf.config.testline import RealEnb, NetworkAddress, RoutingInformation
from taf.config.testline.ue import Android, Qualcomm
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.ue import MediaTek
from taf.config.testline.dcap import DcapRnD
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.pdn import PDNTafUeAndroidDetails
from taf.config.testline.ue import TafUeAndroid
from taf.config.testline import Connection


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_pdu_1 = HBTE(addr="10.71.195.80", port_numbers=[4])

_pdu_2 = HBTE(addr="10.71.195.80", port_numbers=[5])

_ru_1_pdu = HBTE(addr="10.71.195.82", port_numbers=[2])
_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.56.2", username="serviceuser", password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.77.129", username="serviceuser", password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY="
    ),

    pdu_port=_ru_1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AQQQA.value,

)

_ru_2_pdu = HBTE(addr="10.71.195.83", port_numbers=[4])
_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.56.2", username="rfsw", password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.77.129", username="rfsw", password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc="
    ),

    pdu_port=_ru_2_pdu.pdu_ports[4],
    radio_type=RadioTypes.AHIB.value,

)


_gnb_1_airscale_cu_capacity_unit_left = CapacityUnit(
    addr="1.1.1.1",
    hardware_type="ABIO",
    rus=[_ru1],
)
_gnb_1_airscale_cu_capacity_unit_right = CapacityUnit(
    addr="1.1.1.1",
    hardware_type="ABIO",
    rus=[_ru2],
)

_common_unit_0_pdu_port = PduPort(pdu=_pdu_1, port_no="4")
_common_unit_master = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_gnb_1_airscale_cu_capacity_unit_left],
    pdu_port=_common_unit_0_pdu_port,
    hardware_type="ASIL",
)

_common_unit_1_pdu_port = PduPort(pdu=_pdu_2, port_no="5")
_common_unit_slave = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.119", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_gnb_1_airscale_cu_capacity_unit_right],
    pdu_port=_common_unit_1_pdu_port,
    hardware_type="ASIL",
)


_airscale1 = Airscale([_common_unit_master])

_airscale2 = Airscale([_common_unit_slave])

_test_pc1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.217.57", username="ute", password="ute"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_airscale1.common_units[0],
            interface_type="lmp",
        )
            ],
)

_test_pc2= TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.217.58", username="ute", password="ute"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_airscale2.common_units[0],
            interface_type="lmp",
        )
            ],
)


# #CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.0.83.172",
        v6=None,
        vlan_id=None,
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.0.83.172", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.0.83.172", username="Nemuadmin", password="nemuuser"
    ),
    f1m=None,
    f1c=None,
    f1u=None,
    x2c=NetworkAddress(
        v4="10.0.83.172",
        v6=None,
        vlan_id=None,
    ),
    x2u=NetworkAddress(
        v4="10.0.83.172",
        v6=None,
        vlan_id=None,
    ),
    s1u=NetworkAddress(
        v4="10.0.83.172",
        v6=None,
        vlan_id=None,
    ),
)

_attenuator = AHBTE(
    ip_addr="10.71.203.130",
    port=5000,
    attenuation_port_numbers=[1, 2, 7, 8, 5, 6],
    model="PA-16-16-6-127-0.5-B-S",
)


_du1 = DU(airscale=_airscale1, rus=[_ru1], f1_m_ip_addr="192.168.255.129")

_du2 = DU(airscale=_airscale2, rus=[_ru2])

_dcap = DcapRnD(
    HttpConnectionDetails(
        addr="10.101.60.54", port="443", username="dcapuser", password="dcapadmin!"
    )
)

_classical_bts1 = ClassicalBts(cu=_cu, dus=[_du1], global_bts_id=10960, instance_id=1914, dcap=_dcap)

_classical_bts2 = ClassicalBts(cu=_cu, dus=[_du2], global_bts_id=10960, instance_id=1914, dcap=_dcap)

_core = RealCore5G(mcc=460, mnc=2)

_core_ssh = SshServiceDetails(addr="10.42.61.65", username="5g", password="2019H@slo")


_abia = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIA",)

_asia = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.209.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abia],
    hardware_type="ASIA",
)

_lteenb = RealEnb(
    airscale=Airscale(common_units=[_asia]),
    x2_link_addr=NetworkAddress(
        v4="10.71.209.2",
        routing=RoutingInformation(gateway="10.71.209.1", ip_prefix_length=27),
    ),
    global_bts_id=10081,instance_id=1967
)

_app_server_1 = TafUeAppServer(
    app_server_name="APP_5",
    address="10.71.207.158",
    user="vrf3_sg5",
    password="vrf3@sg5",
    ports=[45814,45914],
)


_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_app_server_1,
    interval=1,
    server_close_delay=50,
)

_pdn1 = PDNTafUeAndroidDetails(
    entryName="dxdata2", apnName="dxdata2", apnType=["DEFAULT"]
)

_android = TafUeAndroid(
    serial_number="be40f1b8", 
    capabilities=['REAL_UE', "qualcomm"],
    ue_pc_address="10.71.218.116",
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.116", username="mn5gran", password="nokia123@"
    ),
    data_transfer=[_data_transfer_iperf],
    pdns=[_pdn1],
    proxy_mngr_port="9955",

)

_ue_pc_ssh = SshServiceDetails(
    addr="10.71.218.116", username="mn5gran", password="nokia123@"
)

tl = TestLine(
    test_pc=_test_pc1,
    test_pcs=[_test_pc1,_test_pc2],
    gnbs=[_classical_bts1,_classical_bts2],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_FULLRACK_QC_ASILL_ABIOB1_AQQQA-ASILR_ABIOB4_AHIB_ENB",
    core=_core,
    enbs=[_lteenb],
    ues=[_android],
    attenuator=_attenuator,
)

__all__ = ["tl"]
