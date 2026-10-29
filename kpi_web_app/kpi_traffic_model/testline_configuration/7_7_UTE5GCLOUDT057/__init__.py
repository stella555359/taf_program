__maintainer__ = "Marcin Wachacki"
__team__ = "5G_PZ_MMW_KRK_6_SG"
__email__ = "marcin.wachacki@nokia.com"


from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline import NetworkAddress, RU
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import PduPort, ATEN
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import MediaTek
from taf.config.testline.connection_details import IperfDataTransferDetails
from taf.config.testline.attenuator import RadioRack


_attenuator = RadioRack(
    ip_addr="10.83.185.240",
    port="50000",
    attenuation_port_numbers=[13, 14, 15, 16],
)


# Test PCs configuration (VMs)
_test_pc_gnb_1_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT057.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
)

_test_pc_gnb_2_default_ssh_connection_details = SshServiceDetails(
    addr="SC5G-eNB-288.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
)

_test_pc_gnb_1 = TestPc(
    default_ssh_connection_details=_test_pc_gnb_1_default_ssh_connection_details
)

_test_pc_gnb_2 = TestPc(
    default_ssh_connection_details=_test_pc_gnb_2_default_ssh_connection_details
)


# gNBs configuration
_gnb_1_bc_ip = NetworkAddress(v4="10.83.182.57")  # ? 10.83.178.245
_gnb_2_bc_ip = NetworkAddress(v4="10.83.183.38")  # ? 10.83.179.48

_default_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)

_default_gnb_1_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_1_bc_ip.v4,
    username="Nemuadmin",
    password="nemuuser",
)

_default_gnb_2_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_2_bc_ip.v4,
    username="Nemuadmin",
    password="nemuuser",
)

# CUs
_cu_gnb_1 = CU(
    backhaul_site_oam_ip=_gnb_1_bc_ip,
    oam_ssh_connection_details=_default_ssh_lmp_connection,
    oam_http_connection_details=_default_gnb_1_oam_http_connection,
)

_cu_gnb_2 = CU(
    backhaul_site_oam_ip=_gnb_2_bc_ip,
    oam_ssh_connection_details=_default_ssh_lmp_connection,
    oam_http_connection_details=_default_gnb_2_oam_http_connection,
)

# DUs
_du_lmp_connection_gnb_1 = _default_ssh_lmp_connection
_du_lmp_connection_gnb_1.proxy = _test_pc_gnb_1_default_ssh_connection_details
_du_lmp_connection_gnb_2 = _default_ssh_lmp_connection
_du_lmp_connection_gnb_2.proxy = _test_pc_gnb_2_default_ssh_connection_details

_abil_master_gnb = CapacityUnit(addr="fsp1_c")  # or: 192.168.253.20

_du_common_unit_gnb_1 = CommonUnit(
    lmp_connection=_du_lmp_connection_gnb_1,
    capacity_units=[_abil_master_gnb],
    hardware_type="ASIK",
    hardware_version="102",
)

_du_common_unit_gnb_2 = CommonUnit(
    lmp_connection=_du_lmp_connection_gnb_2,
    capacity_units=[_abil_master_gnb],
    hardware_type="ASIK",
    hardware_version="102",
)

_ru_gnb_1 = RU(
    ru_hw_group="RF5.1",
    default_ssh_connection_details=SshServiceDetails(
        addr=NetworkAddress(v4="172.16.19.33").v4,
        username="root",
        password="asmr",
    ),
    pdu_port=PduPort(
        pdu=ATEN(addr="1.1.1.1", port_numbers=[1, 2]), port_no=1
    ),  # to check it
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
    ],
)

_ru_gnb_2 = RU(
    ru_hw_group="RF5.1",
    default_ssh_connection_details=SshServiceDetails(
        addr=NetworkAddress(v4="172.16.19.33").v4,
        username="root",
        password="asmr",
    ),
    pdu_port=PduPort(
        pdu=ATEN(addr="1.1.1.1", port_numbers=[1, 2]), port_no=1
    ),  # to check it
    attenuation_ports=[
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)

_airscale_gnb_1 = Airscale(common_units=[_du_common_unit_gnb_1])
_airscale_gnb_2 = Airscale(common_units=[_du_common_unit_gnb_2])

_du_gnb_1 = DU(airscale=_airscale_gnb_1, rus=[_ru_gnb_1])
_du_gnb_2 = DU(airscale=_airscale_gnb_2, rus=[_ru_gnb_2])


# gNBs configuration
_gnb_1 = ClassicalBts(
    cu=_cu_gnb_1,
    dus=[_du_gnb_1],
    instance_id="75057",
    global_bts_id="57",
)

_gnb_2 = ClassicalBts(
    cu=_cu_gnb_2,
    dus=[_du_gnb_2],
    instance_id="75288",
    global_bts_id="288",
)


# UE configuration
_ue_pc_ssh = SshServiceDetails("10.83.185.21", "user-lab0", password="Bts2003")
_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_ue_pc_ssh,
    network_interface_address="",
    iperf_path="",
    port=52029,
)
_elt_path = "/cygdrive/c/ELT_v3.2048.0/"

_mtk_ue_1 = MediaTek(
    ssh_connection_details=_ue_pc_ssh,
    server_dir="c:/pyro_server",
    server_port=9090,
    edb_file_path="auto",
    imei="",
    imsi="",
    apn_url="5gsakrk",
    iperf_details=_iperf_details_on_mtk,
    capabilities=["REAL_MEDIATEK_UE"],
)

_mtk_ue_1.elt_path = _elt_path


# TL configuration
tl = TestLine(
    test_pc=_test_pc_gnb_1,
    gnbs=[_gnb_1, _gnb_2],
    test_pcs=[_test_pc_gnb_1, _test_pc_gnb_2],
    ues=[_mtk_ue_1],
    attenuator=_attenuator,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ABIL_ASIK_AEQA",
)


__all__ = ["tl"]
