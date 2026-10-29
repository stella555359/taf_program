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
from taf.config.testline.pdu import FACOM, HBTE, TopYoung
from taf.config.testline.radio import RU, RadioTypes
from taf.config.testline.ran import BSC, RNC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.testpc import TestPc
from taf.config.testline.appserver import AppServer
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
    MediaTek,
)
from taf.config.testline.pdn import PDN, PDPTypes

__maintainer__ = "jiayi tang"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_03_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_03@internal.nsn.com>"  # TL owner's team
__email__ = "jiayi.tang@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.204", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_pdu_1 = TopYoung(addr="10.71.196.21", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_fsp_1 = CapacityUnit(
    addr="192.168.253.21",
    hardware_type="ABIO",
    hardware_version="475266A.101",
    serial_number="L1204104720",
)

_fct_1 = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_fsp_1],
    pdu_port=_pdu_1.pdu_ports[4],
    hardware_type="ASIL",
    hardware_version="474767A.101",
    serial_number="L1212006760",
)

_ru_pdu = TopYoung(addr="10.71.196.22", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_rmod_1 = RU(
    ru_hw_group="hw_group",
    radio_type=RadioTypes.AQHC,
    serial_number="1M220306243",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.22", username="rfsw", password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc="
    ),
    pdu_port=_ru_pdu.pdu_ports[2],
)

_enb_sbts_1 = RealEnb(
    system_module=[_fct_1],
    rms=[_rmod_1],
    oam_ip=NetworkAddress("10.71.211.138"),
    instance_id=163,
    global_bts_id=163,
)

# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.57.178.20", username="mmw_sg2_3", password="mm@2@3"
)

_mtk_host_ssh = SshServiceDetails(
    addr="10.71.218.46", username="nokia5G", password="noki@123"
)

_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="",
    iperf_path="C:/Tool/iperf-2.0.9-win64/iperf",
    port="47163",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.20",
    iperf_path="/usr/bin/iperf",
    port="46163",
)
_appserver = AppServer(_iperf_details_on_appserver)

#UE
_mtk_lte = MediaTek(
    ssh_connection_details=_mtk_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="C:\MTK\Item.3_NR16.R2.MP.W22.18.p1_MT6298_DONGLE(NLWCG_SAP_R16)_bin\MDDB_MT6298_S00_NR16_R2_MP_W22_18_P1.EDB",
    imei="12345678901234",
    imsi="262033032995919",
    apn_url="dxdata4",
    iperf_details=_iperf_details_on_mtk,
    capabilities=["REAL_MEDIATEK_UE","mtk_lte"],
)


tl = TestLine(
    test_pc=_host,
    enbs=[_enb_sbts_1],
    ues=[_mtk_lte],
    tl_cloud_topology="CLOUD_SRAN_L_1ASIL_1ABIO_1AQHC",
    appserver=_appserver,
)


#print (tl.enbs[0].rms[0].pdu_port.pdu.vendor)
#print (tl.enbs[0].system_module[0].pdu_port.pdu.vendor)
#print (tl.enbs[0].system_module[0].pdu_port.pdu.addr)
#print (tl.enbs[0].system_module[0].pdu_port.port_no)

