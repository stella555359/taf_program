import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import FACOM
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android, MediaTek
from taf.config.testline.ue import TafUeAndroid
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
from taf.config.testline.radio import RadioTypes
from taf.config.testline.pdu import HBTE as PBHBTE
from taf.config.testline import LicenseKeeper
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.core import RealCore
__maintainer__ = ""
__team__ = "MN 5G RAN I&V 4 Pz HZG SG1"
__email__ = ""

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.20", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##5GRU for classicalBTS
_ru_1_pdu = PBHBTE(addr="10.68.87.20", port_numbers=[8])

_ru_1 = RU(
   ru_hw_group="hw_group",
   default_ssh_connection_details=SshServiceDetails(
       addr="172.22.0.2",
       username="serviceuser",
       password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
   ),
   lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
   pdu_port=_ru_1_pdu.pdu_ports[8],
   radio_type=RadioTypes.AWHQX,
)

_ru_2_pdu = PBHBTE(addr="10.68.87.20", port_numbers=[7])

_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.6",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_2_pdu.pdu_ports[7],
    radio_type="AWPTD",
)

_ru_3_pdu = PBHBTE(addr="10.68.87.18", port_numbers=[3])

_ru_3 = RU(
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.1.2",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    ru_hw_group="hw_group",
    pdu_port=_ru_3_pdu.pdu_ports[3],
    radio_type="AWHQ2",
)

_ru_4_pdu = PBHBTE(addr="10.68.87.22", port_numbers=[4])

_ru_4 = RU(
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.2.2",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    ru_hw_group="hw_group",
    pdu_port=_ru_4_pdu.pdu_ports[4],
    radio_type="AWHQ3",
)

_ru_5_pdu = PBHBTE(addr="10.68.87.24", port_numbers=[1])

_ru_5 = RU(
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.2.6",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    ru_hw_group="hw_group",
    pdu_port=_ru_5_pdu.pdu_ports[1],
    radio_type="AWHNA",
)

_ru_6_pdu = PBHBTE(addr="10.68.87.13", port_numbers=[7])

_ru_6 = RU(
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.2.6",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    ru_hw_group="hw_group",
    pdu_port=_ru_6_pdu.pdu_ports[7],
    radio_type="AWHNB",
)

_ru_7_pdu = PBHBTE(addr="10.68.87.20", port_numbers=[4])

_ru_7 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_7_pdu.pdu_ports[4],
    radio_type="AWPQZ",
)

_ru_8_pdu = PBHBTE(addr="10.68.87.20", port_numbers=[3])

_ru_8 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_8_pdu.pdu_ports[3],
    radio_type="AWPQZ",
)

_ru_9_pdu = PBHBTE(addr="10.68.87.20", port_numbers=[2])

_ru_9 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_9_pdu.pdu_ports[2],
    radio_type="AWPQZ",
)


##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit1 = CapacityUnit(addr="1.1.1.1", hardware_type="ABIN")
_capacity_unit2 = CapacityUnit(addr="1.1.1.1", hardware_type="ABIQ")
_capacity_unit3 = CapacityUnit(addr="1.1.1.1", hardware_type="ABIQ")

_gnb_pdu = PBHBTE(addr="10.68.87.21", port_numbers=[3])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit1, _capacity_unit2, _capacity_unit3],
    pdu_port=_gnb_pdu.pdu_ports[3],
	hardware_type="ASIM",
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru_1, _ru_2, _ru_3, _ru_4, _ru_5, _ru_6, _ru_7, _ru_8, _ru_9],
    f1_m_ip_addr="10.68.88.52",
)


##CU
_cu = CU(
    backhaul_site_oam_ip="10.68.88.52",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.88.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.88.52", username="Nemuadmin", password="nemuuser"
    ),
)


##cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_SA_ASIML_ABINB1_ABIQB2B3_AWHNA_3xAWHQ_AWPTD"
# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="1204", global_bts_id="1204"
)


# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.68.86.13", username="MN5GRAN", password="nokia123@"
)

_spark_appserver_ssh = SshServiceDetails(
    addr="10.71.207.142", username="vrf4_sg1", password="vrf4@sg1"
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.71.207.142",
    iperf_path="/usr/bin/iperf",
    port=51003,
)

_appserver = AppServer(_iperf_details_on_appserver)

_licensekeeper = LicenseKeeper(username="HAZ4_SG1", password="HAZ4_SG1")

_sigspark_1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="FEC5T20407001090",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.52/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="460023100010658",
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    licensekeeper=_licensekeeper,
)

_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.71.207.142",
    user="vrf4_sg1",
    password="vrf4@sg1",
    bind_interface_ip="10.71.207.142",
    expected_prompt="[vrf4_sg1@appserver ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=[51004, 51005],
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
    ue_pc_address="10.57.159.64",
    root_password="ca9aa7b2c75a",
    ue_manage_ip="10.101.36.54",
    serial_number="FSH2112001F4",
    data_transfer=[_fastmile_data_transfer_1],
    ue_pc_port=5555,
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version="3.1",
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

_ue3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.232", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="92f54d86",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.45/Bin/Spark.exe",
    python_path="C:/Python3",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460028001006290",
    licensekeeper=_licensekeeper,
)

x85_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.71.207.142",
    user="vrf4_sg1",
    password="vrf4@sg1",
    bind_interface_ip="10.71.207.142",
    expected_prompt="[vrf4_sg1@appserver ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=[51004, 51005],
)

x85_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=x85_appserver_1,
    interval=1,
    #binary_path="/data/local/tmp/iperf",
    version=2,
)

x85QualComm = TafUeAndroid(
    serial_number='6a263c46',
    capabilities=["qualcomm"],
    ue_pc_address='10.68.86.109',
    data_transfer=[x85_data_transfer_1],
    phone_number='+8613100017438',
    ue_pc_port='8080',
    imei='004403162453833',
    imsi='460023100017438',
    qualcomm_prototype=True,
    service_call_attach='17',
    service_call_detach='17',
    )

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=RealCore(mcc=460, mnc=2),
    ues=[_sigspark_1, _fastmile_1, _ue3, x85QualComm],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
)
