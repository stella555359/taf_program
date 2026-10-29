__maintainer__ = "Miao Huibo / Wang Teana"
__team__ = (
    "I_NSB_MN_RAN_RD_VRF_HAZ3_07_GMS <I_NSB_MN_RAN_RD_VRF_HAZ3_07@internal.nsn.com>"
)
__email__ = "huibo.miao@nokia-sbell.com"

import os
import yaml

from taf.config.testline.appserver import AppServer
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline import DU, RU, RealEnb
from taf.config.testline.pdu import ATEN, PduPort
from taf.config.testline.pdu import TopYoung, FACOM, HBTE
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.core import RealCore5G, PCF
from taf.config.testline.testline import TestLine
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.ue import Android, Qualcomm
from taf.config.testline.attenuator import HBTE as AHBTE

from taf.config.testline.attenuator import TopYoung

from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.ue import TafUeAt,TafUeAndroid
from taf.config.testline.pdn import PDNTafUeAndroidDetails


os.environ["INIT_CONFIG_FILE_PATH"] = os.path.dirname(os.path.abspath(__file__))

__all__ = ["tl"]


os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "ue_config.yaml"
)

_appserver_ssh = SshServiceDetails(
    addr="10.71.187.33", username="ute", password="Ut3pa5s#ff97", port="47200"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.187.33",
    iperf_path="/cygdrive/c",
    port="47201",
)

_app_server_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.71.187.33",
    user="ute",
    password="Ut3pa5s#ff97",
    bind_interface_ip="10.71.187.33",
    expected_prompt="\[ute.*\$ ",
    ports=[47000, 47001]
)

_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_app_server_1,
    interval=1,
    binary_path="/system/bin/",
    #interface_name="stdata1",
    server_close_delay=50,
   # bind_ue_ip="10.69.5.68",
    version=2,
    #dt_from_uepc=False,
)

_data_transfer_ping = TafUeDataTransferProtocol(
    protocol_name="ping", app_server=_app_server_1, interval=1
)

_data_transfer_ftp = TafUeDataTransferProtocol(
    protocol_name="ftp", app_server=_app_server_1, interval=1
)


_pdn1 = PDNTafUeAndroidDetails(
    entryName='default',  # MANDATORY / use this entry point as KW argument (pdn)
    apnName='stdata1',  # MANDATORY
    apnType=['DEFAULT', 'MMS', 'XCAP'],  # MANDATORY
    carrierEnabled=True,  # OPTIONAL
    operatorNumeric='55520',  # OPTIONAL
    protocol='IPV4V6',  # OPTIONAL
    roamingProtocol='IPV4V6',  # OPTIONAL
    proxyAddress='192.168.1.55',  # OPTIONAL
    proxyPort=1234,  # OPTIONAL
    mmsc='uri1',  # OPTIONAL
    mmsProxyAddress='192.168.1.66',  # OPTIONAL
    mmsProxyPort=4567,  # OPTIONAL
    user='tafue',  # OPTIONAL
    password='tafue',  # OPTIONAL
    mvnoType='GID',  # OPTIONAL
    networkType='NR',  # OPTIONAL
    authType='PAP')  # OPTIONAL

_pdn2 = PDNTafUeAndroidDetails(
    entryName='emergency',  # use this entry point as KW argument  (pdn)
    apnName='apn2',
    apnType=['SUPL', 'FOTA'])

_ue_host_ssh_dingli = SshServiceDetails(
    addr="10.71.180.106", username="tester5g", password="Nokia123!"
)

_sigspark = Android(
    ssh_connection_details=_ue_host_ssh_dingli,
    serial_number="a3aa0f43",
    server_dir="C:\Program Files (x86)\DingLi\Pilot PioneerX11.0.9.0---03081033/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["pioneer", "huawei_sigspark"],
    imsi="262033100016791",
)

_at_1 = TafUeAt(
    com_port="5",
    serial_number="d98acb45",
    capabilities=["qualcomm"],
    ue_pc_address="10.71.180.106",
    ue_pc_login="tester5g",
    ue_pc_password="Nokia123!",
    ue_pc_expected_prompt=".*$",
    data_transfer=[_data_transfer_iperf, _data_transfer_ping, _data_transfer_ftp],
    phone_number="+8613100016789",
    ue_pc_port="8080",
    imei="864766050006767",
    imsi="262033100016791",
)
###miaohuibo:ue_pc_address / imei / imsi

# RealEnb---------------------------------------------------------
# 5GRU------------------------------------
# add 2 more 5g ru info
# ru_hw_group: Above6GHZ or Below6GHZ

_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.106.174.67", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)
###miaohuibo:addr
_real_enb = Airscale(common_units=[_common_unit_1])



_ru0_pdu = HBTE(addr="10.71.180.112", port_numbers=[3])
###miaohuibo:port_numbers

_ru0 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.3",
        username="rfsw",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.33.128", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type=RadioTypes.AHLOA,
)


_du0_pdu = HBTE(addr="10.71.180.113", port_numbers=[8])

_common_unit_0_pdu_port = PduPort(pdu=_du0_pdu, port_no="8")
###miaohuibo:port_numbers / port_no
_du0_capacity_unit_L_0 = CapacityUnit(addr="192.168.253.20", hardware_type="ABIP")

_du0_master_capacity_unit_L_0 = CapacityUnit(addr="fsp-1-1a", hardware_type="ABIP")

_du0_slave_capacity_unit_L_0 = CapacityUnit(addr="fsp-1-1b", hardware_type="ABIP")

_du0_fpga_capacity_unit_L_0 = CapacityUnit(addr="fsp-1-1c", hardware_type="ABIP")
###miaohuibo:hardware_type
_ru_cablinks = [
    Cablink(source=Endpoint(unit=_du0_capacity_unit_L_0, label='SFP', port_id=1), target=Endpoint(unit=_ru0, label='SFP', port_id=1)),
    Cablink(source=Endpoint(unit=_du0_capacity_unit_L_0, label='SFP', port_id=2), target=Endpoint(unit=_ru0, label='SFP', port_id=2)),
    ]

_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.180.106", username="tester5g", password="Nokia123!"
    ),
    serial_number="d98acb45",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python3/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "qct_dx50"],
)
###miaohuibo:addr
_common_unit_0_L = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[
        _du0_capacity_unit_L_0,
        _du0_master_capacity_unit_L_0,
        _du0_slave_capacity_unit_L_0,
        _du0_fpga_capacity_unit_L_0,
    ],
    pdu_port=_common_unit_0_pdu_port,
    hardware_type="ASIM",
)
###miaohuibo:hardware_type
_airscale = Airscale(common_units=[_common_unit_0_L])

_du = DU(airscale=_airscale, rus=[_ru0], f1_m_ip_addr="10.106.174.67", cablinks=_ru_cablinks)

_cu = CU(
    backhaul_site_oam_ip="10.106.174.67",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.106.174.67", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.106.174.67", username="Nemuadmin", password="nemuuser", port=443
    ),
)
###miaohuibo:addr
_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=37311, global_bts_id=37311)


_realcore = RealCore5G(mcc=262, mnc=3)

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_QC_ASILL_ABIOB1B2_AHFIB_AEUD"




_appserver = AppServer(iperf_details=_iperf)

"""
_attenuator = AHBTE(
    ip_addr="10.71.180.78",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4],
    model="PA-16-16-6-127-0.5-B-S",
)
"""
_attenuator = TopYoung(
    ip_addr="10.71.180.78",
    port=3000,
    attenuation_port_numbers=[9, 10, 11, 12],
    model="TAS16T16-51-120-1S-DES",
)
###miaohuibo:attenuation_port_numbers
# Test VM
_test_vm = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.71.187.132", username="ute", password="ute"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_cbts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.71.187.132", username="ute", password="ute"
    )
)
###miaohuibo:addr/password (for UTE)
tl = TestLine(
    test_pc=_host,
    gnbs=[_cbts],
    tl_cloud_topology=_tl_cloud_topology,
    core=_realcore,
    ues=[_sigspark],
    test_pcs=[_test_vm],
    appserver=_appserver,
    attenuator=_attenuator,
)
