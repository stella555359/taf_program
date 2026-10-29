import os
from taf.config.testline.appserver import AppServer
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)  # added in taf.meta.5.4
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import HBTE, PduPort, Pdu
from taf.config.testline.pdu import HBTE as PDU_HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit

# added in taf.meta 5.4
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.attenuator import (
    AttenuationPort,
    #    TopYoung,
    HBTE,
)  # added in taf.meta 5.4

__maintainer__ = "Helen.1.Chen"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02@internal.nsn.com>"
)
__email__ = "helen.1.chen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #attenuator
_hbte_params = {
    "ip_addr": "10.71.205.50",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator = HBTE(**_hbte_params)

##5GRU_1

_ru1_pdu = PDU_HBTE(addr="10.71.196.84", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.158",
        username="rfsw",
        password="PD6N1DB0lWmwomtNL2qd3ISypbiocdGRy7U+Lipiksk=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="PD6N1DB0lWmwomtNL2qd3ISypbiocdGRy7U+Lipiksk=",
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AQQY,
)

##5GRU_2
_ru2_pdu = PDU_HBTE(addr="10.71.196.84", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru2 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="PD6N1DB0lWmwomtNL2qd3ISypbiocdGRy7U+Lipiksk=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="PD6N1DB0lWmwomtNL2qd3ISypbiocdGRy7U+Lipiksk=",
    ),
    pdu_port=_ru2_pdu.pdu_ports[5],
    radio_type=RadioTypes.AQQY,
)

##5GRU_3
_ru3_pdu = PDU_HBTE(addr="10.71.196.84", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru3 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="PD6N1DB0lWmwomtNL2qd3ISypbiocdGRy7U+Lipiksk=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="PD6N1DB0lWmwomtNL2qd3ISypbiocdGRy7U+Lipiksk=",
    ),
    pdu_port=_ru3_pdu.pdu_ports[5],
    radio_type=RadioTypes.AEQC,
)

##5GRU_4
_ru4_pdu = PDU_HBTE(addr="10.71.196.83", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru4 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="PD6N1DB0lWmwomtNL2qd3ISypbiocdGRy7U+Lipiksk=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="PD6N1DB0lWmwomtNL2qd3ISypbiocdGRy7U+Lipiksk=",
    ),
    pdu_port=_ru4_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEQY,
)

_ru5_pdu = PDU_HBTE(addr="10.71.196.84", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru5 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="PD6N1DB0lWmwomtNL2qd3ISypbiocdGRy7U+Lipiksk=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="PD6N1DB0lWmwomtNL2qd3ISypbiocdGRy7U+Lipiksk=",
    ),
    pdu_port=_ru5_pdu.pdu_ports[1],
    radio_type=RadioTypes.AQQJ,
)


# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.57.162.2", username="mmw_sg2", password="mm@2", port="42132"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.2",
    iperf_path="/system/bin",
    port=42165,
)

# Qualcomm
# CI_Detail_UE_Type='Qualcomm'
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.205.51", username="root", password="123456"
    ),
    serial_number="65J157L210GL000000NA00080",
    imsi="262033100001101",
    server_dir="C:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---05171641/Pioneer.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["dingli_pioneer"],
)

##DU_0 for cloudlBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.71.212.98", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.22")

_du_pdu = PDU_HBTE(addr="10.71.196.85", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_du_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1, _ru2, _ru3, _ru4,], f1_m_ip_addr="10.71.212.105")

_lmp_connection_161 = SshServiceDetails(
    addr="10.71.212.105", username="toor4nsn", password="oZPS0POrRieRtu"
)

_du_pdu_161 = PDU_HBTE(addr="10.71.196.86", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_161 = CommonUnit(
    lmp_connection=_lmp_connection_161,
    capacity_units=[_capacity_unit_0],
    pdu_port=_du_pdu_161.pdu_ports[3],
)

_du_161 = DU(
    airscale=Airscale(common_units=[_common_unit_161]), rus=[_ru5]
)


##CU

_cu = CU(
    backhaul_site_oam_ip="10.71.212.98",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.212.98", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.212.98", username="Nemuadmin", password="nemuuser"
    ),
)

_cu_161 = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.212.105", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.212.105", username="Nemuadmin", password="nemuuser"
    ),
)


##classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=165, global_bts_id=165)

_classical_bts_161 = ClassicalBts(
    dus=[_du_161], cu=_cu_161, instance_id=161, global_bts_id=161)

##host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.66", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_iperf_details = _iperf

_appserver = AppServer(_iperf_details)

##cloud_topology------------------------------------------------
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASOE_AQQY_eCPRI"

tl = TestLine(
    test_pc=_host,
    ues=[_android],
    gnbs=[_classical_bts, _classical_bts_161],
    appserver=_appserver,
    attenuator=[_attenuator],
    tl_cloud_topology=_tl_cloud_topology,
)
