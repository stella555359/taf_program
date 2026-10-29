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
from taf.config.testline.pdu import HBTE
from taf.config.testline.radio import RU, RadioTypes
from taf.config.testline.ran import BSC, RNC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.testpc import TestPc
from taf.config.testline.appserver import AppServer
# added in taf.meta 5.4
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
    LicenseKeeper,
)

__maintainer__ = "Tong Chen"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_02_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_02@internal.nsn.com>"  # TL owner's team
__email__ = "tong.chen@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.131.165", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_pdu_1 = HBTE(addr="10.71.197.14", port_numbers=[1])

_fsp_1 = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIO",
    hardware_version="475266A.104",
    serial_number="L1213010357",
)

_fct_1 = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_fsp_1],
    pdu_port=_pdu_1.pdu_ports[1],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="DH212975800",
)

_ru_pdu = HBTE(addr="10.71.197.12", port_numbers=[1])

_rmod_1 = RU(
    ru_hw_group="hw_group",
    radio_type=RadioTypes.AQHA,
    serial_number="1M222225874",
    default_telnet_connection_details=TelnetConnectionDetails(
        addr="192.168.253.", port=2323
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
)

_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.214.201", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_pdu_1.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_1])

_enb_sbts_1 = RealEnb(
    airscale=_real_enb,
    system_module=[_fct_1],
    rms=[_rmod_1],
    oam_ip=NetworkAddress("10.71.214.201"),
    instance_id=10755,
    global_bts_id=10755,
)

_appserver_ssh_1 = SshServiceDetails(
    addr="10.57.162.12", username="cmw_sg2", password="cm@2"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_1,
    network_interface_address="10.57.162.12",
    iperf_path="iperf",
    port=52554,
)

_appserver = AppServer(_iperf)

# CI_Detail_UE_Type='Huawei Mate 20X'

_Huawei_host_ssh = SshServiceDetails(
    addr="10.71.218.13", username="nokia5G", password="noki@123"
)

_Huawei = Android(
    ssh_connection_details=_Huawei_host_ssh,
    serial_number="L8K5T19919001465",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["cell_Mapping: [1]", "huawei"],

)



tl = TestLine(
    test_pc=_host,
    enbs=[_enb_sbts_1],
    ues=[_Huawei],
    tl_cloud_topology="CLOUD_SRAN_L_1ASIB_1ABIC_1AEQP",
)
