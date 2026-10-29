import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import FACOM, HBTE, TopYoung
from taf.config.testline.ue import Android
from taf.config.testline.core import EPCSim
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer

__maintainer__ = "Liu Tiffany"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG1"
__email__ = "tiffany.liu@nokia-sbell.com"


## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.254", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##epcsim
_epc_sim = EPCSim(
    mme_ip="10.110.227.5",
    mcc="460",
    mnc="02",
    tac="210",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.227.70", username="haijtest", password="Nokia_1234"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)

# 4GRU for RealEnb
#_ru_enb_pdu = HBTE(addr="10.68.87.10", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

#_ru_enb = RadioModule(
#    default_ssh_connection_details=SshServiceDetails(
#        addr="1.1.1.1", username="usr", password="psswd"
#    ),
#    pdu_port=_ru_enb_pdu.pdu_ports[2],
#)

# #RealEnb
#_real_enb_pdu = HBTE(addr="10.68.87.13", port_numbers=[2])

#_common_unit_2 = CommonUnit(
#    lmp_connection=SshServiceDetails(
#        addr="10.68.88.8", username="toor4nsn", password="oZPS0POrRieRtu"
#    ),
#    capacity_units=[],
#    pdu_port=_real_enb_pdu.pdu_ports[2],
#)

#_real_enb = Airscale(common_units=[_common_unit_2])

#_lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)

##5GRU for classicalBTS

_ru_1_pdu = HBTE(addr="10.101.45.52", port_numbers=[2])

_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_1_pdu.pdu_ports[2],
    radio_type="AEQN",
)


_ru_2_pdu = HBTE(addr="10.101.45.52", port_numbers=[1])

_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_2_pdu.pdu_ports[1],
    radio_type="AEQN",
)

_ru_3_pdu = TopYoung(addr="10.101.45.53", port_numbers=[2])

_ru_3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_3_pdu.pdu_ports[2],
    radio_type="AEQN",
)

_ru_4_pdu = HBTE(addr="10.101.45.75", port_numbers=[3])

_ru_4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_4_pdu.pdu_ports[3],
    radio_type="AZQJ",
)

_ru_5_pdu = TopYoung(addr="10.101.45.72", port_numbers=[4])

_ru_5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_5_pdu.pdu_ports[4],
    radio_type="AZQJ",
)


##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="1.1.1.1")

_gnb_pdu = HBTE(addr="10.101.45.86", port_numbers=[6])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[6],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, 
         rus=[_ru_1, _ru_2, _ru_3, _ru_4, _ru_5], 
         f1_m_ip_addr="10.101.49.231",
         )


##CU
_cu = CU(
    backhaul_site_oam_ip="10.101.49.231",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.49.231", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.49.231", username="Nemuadmin", password="nemuuser"
    ),
)


##cloud_topology
_tl_cloud_topology = "CLOUD_5G_INVENTORY"

_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="11106", global_bts_id="11106"
)


# Honor
_ue_host_ssh = SshServiceDetails(
    addr="1.1.1.1", username="nokia5G", password="noki@123"
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.163.34", username="cmw_sg1", password="Noki@123", port="51100"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.34",
    iperf_path="/usr/bin/iperf",
    port="51100",
)

_appserver = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="9EQUT209XXXXXX",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei"],
    imsi="4600280XXXXXXX",
)
# _appserver = AppServer(_iperf)

# CI_Detail_UE_Type='Huawei Honor 30s'
_ue1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="9EQUT2090300XXXX",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei"],
    imsi="46002800100XXXX",
)

# CI_Detail_UE_Type='Nokia FastMile 5G Gateway 3.2'
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.163.34",
    user="cmw_sg1",
    password="Noki_sg1@123!",
    bind_interface_ip="10.57.163.34",
    expected_prompt="[cmw_sg1@smw_sg1 ~]$ ",
    binary_path="/home/cmw_sg1/taf_debug/iperf",
    ports=[53320, 54320],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    com_port="3",
    ue_pc_address="10.57.157.254",
    root_password="d5da66f2833b",
    ue_manage_ip="10.101.39.4",
    serial_number="LPL2214005FA",
    data_transfer=[_fastmile_data_transfer_1],
    ue_pc_port=5555,
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_epc_sim,
 #   enbs=[_lte_real_enb],
    ues=[_fastmile_1],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
)
