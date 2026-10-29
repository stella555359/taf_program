import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.gnb.gnb import ClassicalBts, CU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.ue import TafUeAndroid
from taf.config.testline.enb import RealEnb
from taf.config.testline.appserver import AppServer
from taf.config.testline.radio import RadioTypes, RU
from taf.config.testline.dcap import DcapBasic
from taf.config.testline.appserver import AppServer, TafUeAppServer

__maintainer__ = "Zhang Lusha"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02@internal.nsn.com"
__email__ = "lusha.zhang@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.122", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# dcap
_host_dcap = DcapBasic(
    connection_details=HttpConnectionDetails(
        addr="10.101.60.49", username="utfuser", password="utfadmin!"
    )
)

# RealEnb
_real_enb_pdu = HBTE(addr="10.101.45.208", port_numbers=[1])

_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.51.68", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_1])

_lte_real_enb = RealEnb(airscale=_real_enb)

# 4GRU for RealEnb
_ru_enb_pdu = HBTE(addr="10.101.45.210", port_numbers=[1])


# gNB

# CU
_f1m = NetworkAddress(v4="9.9.1.1", v6="xxxx", vlan_id=1)
_f1c = NetworkAddress(v4="9.9.1.2", v6="xxxx", vlan_id=2)
_f1u = NetworkAddress(v4="9.9.1.3", v6="xxxx", vlan_id=3)
_x2c = NetworkAddress(v4="9.9.2.1", v6="xxxx", vlan_id=1)
_x2u = NetworkAddress(v4="9.9.2.2", v6="xxxx", vlan_id=2)
_s1c = NetworkAddress(v4="9.9.3.1", v6="xxxx", vlan_id=1)
_s1u = NetworkAddress(v4="9.9.3.2", v6="xxxx", vlan_id=2)
_tracing = NetworkAddress(v4="9.9.1.2", v6="xxxx", vlan_id=1)

_cu = CU(
    backhaul_site_oam_ip="10.101.51.66",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.51.66", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.51.66", username="Nemuadmin", password="nemuuser"
    ),
    f1m=_f1m,
    f1c=_f1c,
    f1u=_f1u,
    x2c=_x2c,
    x2u=_x2u,
    s1c=_s1c,
    s1u=_s1u,
    tracing=_tracing,
)


# 5GRU for classicalBTS
_ru_1_pdu = HBTE(addr="10.101.45.211", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.6",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    pdu_port=_ru_1_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEQP,
)

_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.10",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    pdu_port=_ru_1_pdu.pdu_ports[6],
    radio_type=RadioTypes.AQQK,
)

_ru_3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.22",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    pdu_port=_ru_1_pdu.pdu_ports[5],
    radio_type=RadioTypes.AQQJ,
)

_ru_4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.1.10",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    pdu_port=_ru_1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AVHA,
)

_ru_5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.1.2",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    pdu_port=_ru_1_pdu.pdu_ports[4],
    radio_type=RadioTypes.AVQQA,
)

# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.71.219.22", username="mmw_sg2", password="mm@2", port="44162"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.22",
    iperf_path="iperf",
    port="42162",
)
_appserver = AppServer(_iperf_details_on_appserver)

# Qualcomm
_appserver_taf_ue = TafUeAppServer(
    app_server_name="APP_TAF_UE",
    address="10.42.61.65",
    user="qt5g",
    password="5Gqtmoth!",
    bind_interface_ip="10.42.197.170",
    expected_prompt="qt5g@wl-srn-server-1-idf3_4",
)

_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf", app_server=_appserver_taf_ue, interval=1
)

_android = TafUeAndroid(
    serial_number="RFCX720ESLY",
    capabilities=["REAL_UE", "samsung_ue"],
    ue_pc_address="10.68.86.250",
    data_transfer=_data_transfer_iperf,
    ueproxy_force_release=False,
    ue_pc_port=5000,
    imsi="android",
    qualcomm_prototype=False,
    voice_call_dialing_timeout="30",
    network_mode_switch_method="ADB",
)


# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.101.51.66", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_pdu = HBTE(addr="10.101.45.208", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru_1, _ru_2, _ru_3, _ru_4, _ru_5],
    f1_m_ip_addr="10.101.51.66",
)

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id="339", global_bts_id="1")

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIB_ABIO_AEQP_eCPRI"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
    enbs=[_lte_real_enb],
    test_pcs=[_host_dcap],
)
