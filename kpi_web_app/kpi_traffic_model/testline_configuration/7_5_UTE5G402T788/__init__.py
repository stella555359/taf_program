import os
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.ue import Android
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Enb, SimEnb, RealEnb, RadioModule, LTEEmuEnb
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.mcs import HBTE
from taf.config.testline.core import RealCore
from taf.config.testline.pdu import HBTE, TopYoung
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer

__maintainer__ = "Chen Xiaodong"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG2"
__email__ = "xiaodong.d.chen@nokia-sbell.com"

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.66", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# Real 5G Core is used in real world.  here use EPCsim as the 5GC class is not implemented in tl config lib yet.
_epc_sim = EPCSim(
    mme_ip="10.110.227.5",
    mcc="460",
    mnc="2",
    tac="0",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.227.70", username="haijtest", password="Nokia_1234"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)

##5GRU for classical BTS
_ru1_pdu = FACOM(addr="10.57.172.99", port_numbers=[2])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="serviceuser", password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g="
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="user", password="pass"
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
)

_ru2_pdu = FACOM(addr="10.57.172.99", port_numbers=[4])

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="serviceuser", password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g="
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="user", password="pass"
    ),
    pdu_port=_ru2_pdu.pdu_ports[4],
)

_ru3_pdu = FACOM(addr="10.57.172.86", port_numbers=[6])

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="serviceuser", password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g="
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="user", password="pass"
    ),
    pdu_port=_ru3_pdu.pdu_ports[6],
)


##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_pdu = FACOM(addr="10.57.242.45", port_numbers=[8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[8],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1, _ru2, _ru3], f1_m_ip_addr="10.57.223.248")

##CU
_cu = CU(
    backhaul_site_oam_ip="10.57.223.248",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.223.248", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.223.248", username="Nemuadmin", password="nemuuser"
    ),
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id="788", global_bts_id="788")

##TOPYOUNG_MCS

# CI_Detail_UE_Type='Nokia FastMile 5G Gateway 3.2'
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.244",
    user="vrf4_sg2",
    password="Vrf4@sg2_123456",
    bind_interface_ip="10.57.191.244",
    expected_prompt="[vrf4_sg2@appserver ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=[52228, 52229],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="/usr/bin/iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    ue_pc_address="10.57.159.66",
    root_password="ecea46b2bc75",
    ue_manage_ip="10.57.156.153",
    serial_number="LPL2214005EA",
    data_transfer=[_fastmile_data_transfer_1],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

_fastmile_2 = TafUeFastmile(
    ue_pc_address="10.57.159.66",
    root_password="8adaeea29b3c",
    ue_manage_ip="10.57.156.154",
    serial_number="LPL2214005E4",
    data_transfer=[_fastmile_data_transfer_1],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

_fastmile_3 = TafUeFastmile(
    ue_pc_address="10.57.159.66",
    root_password="U.r=cR:iEZrhrX:F",
    ue_manage_ip="10.57.231.135",
    serial_number="KLT241000AF5",
    data_transfer=[_fastmile_data_transfer_1],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

# switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="0.0.0.0", port="1", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

# switch Mtor
_dell_s4048ton_ssh = SshServiceDetails(
    addr="0.0.0.0", port="1", username="5gran", password="nokia123"
)
_dell_s4048ton_switch = DellS4048TONSwitch(_dell_s4048ton_ssh)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_epc_sim,
    ues=[_fastmile_1, _fastmile_2, _fastmile_3],
    tl_cloud_topology=_tl_cloud_topology,
)
