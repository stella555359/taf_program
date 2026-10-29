import os
from taf.config.testline import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline import RU, DU
from taf.config.testline.pdu import ATEN
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.airscale import CommonUnit, CapacityUnit, Airscale
from taf.config.testline.ue import Android

__maintainer__ = "CIT"
__team__ = "I_5G_NPS_CIT"
__email__ = "I_5G_NPS_CIT@groups.nokia.com"

_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.28.0.89", username="ute", password="ute"
    )
)

_gnb_pdu = ATEN(addr="TO_UPDATE", port_numbers=[8])
_enb_pdu = ATEN(addr="TO_UPDATE", port_numbers=[8])
_ues_pdu = ATEN(addr="TO_UPDATE", port_numbers=[5])
_ru_pdu = ATEN(addr="TO_UPDATE", port_numbers=[1])

_appserver_ssh = SshServiceDetails(
    addr="10.14.42.195", username="ran5g", password="nokia2018"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.11.70.80",
    iperf_path="/usr/bin/iperf",
)

_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.28.1.178", username="cyg_server", password="Nokia123"
    ),
    # type: SshServiceDetails
    serial_number="37a84a79",  # type: str
    server_dir="C:/pyro_server",  # type: str
    python_path="C:/Python27/python.exe",  # type: str
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",  # type: Optional[str]
    diag_cfg_path="C:/UEManager/ue_manager_files/pyro_server/DIAG.cfg",  # type: Optional[str]
    iperf_details=_iperf,  # type: Optional[IperfDataTransferDetails]
    capabilities=["REAL_UE", "REAL_ANDROID_UE"],  # type: Optional[List[str]]
)

_ru = RU(
    ru_hw_group="hw_group",
    radio_type="AAHF",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.5", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.14.48.248", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
)

_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
)

_du_master_capacity_unit = CapacityUnit(
    addr="fsp1_a", hardware_type="ABIL", hardware_version="A101B1"
)

_du_slave_capacity_unit = CapacityUnit(
    addr="fsp1_b", hardware_type="ABIL", hardware_version="A101B1"
)

_du_fpga_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIL", hardware_version="A101B1"
)

_du_common_unit_0 = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[
        _du_master_capacity_unit,
        _du_slave_capacity_unit,
        _du_fpga_capacity_unit,
    ],
    pdu_port=_gnb_pdu.pdu_ports[8],
    hardware_type="ASIK",
    hardware_version="A101",
)

_airscale = Airscale(common_units=[_du_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru])

_cu = CU(
    backhaul_site_oam_ip="10.14.48.248",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.48.248", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts = ClassicalBts(cu=_cu, dus=[_du])

os.environ["ABSTRACT_LIB_CONFIG"] = "./ue_config_cv361.yml"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    ues=[_android],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIKA101L_ABILA101B1_AAHF",
)

__all__ = ["tl"]
