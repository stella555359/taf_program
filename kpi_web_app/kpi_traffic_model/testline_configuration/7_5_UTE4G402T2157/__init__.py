import os
import re
import yaml
from taf.config.testline.connection_details import (
    SshServiceDetails,
    TelnetConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.airscale import Airscale, CapacityUnit, CommonUnit
from taf.config.testline.enb import RealEnb
from taf.config.testline.flexi import Flexi
from taf.config.testline.pdu import HBTE, TopYoung
from taf.config.testline.radio import RU, RadioTypes
from taf.config.testline.ran import BSC, RNC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
    MediaTek,
)  # added in taf.meta.5.4
from taf.config.testline.testpc import TestPc
from taf.config.testline.appserver import AppServer, TafUeAppServer

__maintainer__ = "linghui kong"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_04_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_04@internal.nsn.com>"  # TL owner's team
__email__ = "linghui.kong@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.20", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_pdu_1 = HBTE(addr="10.68.87.114", port_numbers=[1])

_fsp_1 = CapacityUnit(
    addr="192.168.253.38",
    hardware_type="ABIO",
    hardware_version="A.103",
    serial_number="DH214941790",
)

_fct_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_fsp_1],
    pdu_port=_pdu_1.pdu_ports[1],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="DH214543979",
)

_ru_pdu = HBTE(addr="10.68.87.116", port_numbers=[6])

_rmod_1 = RU(
    ru_hw_group="hw_group",
    radio_type=RadioTypes.AQQA,
    serial_number="1M221311529",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.49",
        username="rfsw",
        password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc=",
    ),
    pdu_port=_ru_pdu.pdu_ports[6],
)

_enb_sbts_1 = RealEnb(
    system_module=[_fct_1],
    rms=[_rmod_1],
    oam_ip=NetworkAddress("10.101.51.21"),
    instance_id=2157,
    global_bts_id=2157,
)

_appserver_ssh = SshServiceDetails(
    addr="10.71.219.237",
    username="cmw_sg8",
    password="cm@8",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.237",
    iperf_path="iperf",
    port=58042,
)

_appserver = AppServer(_iperf_details_on_appserver)


_mtk_host_ssh_197 = SshServiceDetails(
    addr="10.68.86.197", username="MN5GRAN", password="nokia123@"
)

_iperf_details_on_mtk_197 = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh_197,
    network_interface_address="",
    iperf_path="/data/local/tmp/iperf",
    port=58302,
)

_mtk_197 = MediaTek(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.197", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="0123456789ABCDEF",
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    imei="432187658765873",
    imsi="262033100010055",
    apn_url="wap1.nokia.com",
    iperf_details=_iperf_details_on_mtk_197,
    capabilities=["REAL_MTK_UEPC_197", "NSA", 'mkt_lte'],
)



tl = TestLine(
    test_pc=_host,
    enbs=[_enb_sbts_1],
    appserver=_appserver,
    ues=[_mtk_197],
    tl_cloud_topology="CLOUD_SRAN_L_1ASIB_1ABIO_1AQQA",
)

