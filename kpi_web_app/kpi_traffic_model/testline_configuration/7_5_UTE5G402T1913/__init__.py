__maintainer__ = "Sebastian Mikos"
__team__ = "MN 5G&SC 5G Pz 2 WRO 5 SG"
__email__ = "I_5GSC_5G_PZ2_WRO_5@internal.nsn.com"
__owner_email__ = "sebastian.mikos@nokia.com"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc
from taf.config.testline.pdu import Gude
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline import DU, RU
from taf.config.testline.core import RealCore5G
from taf.config.testline import RealEnb, NetworkAddress, RoutingInformation
from taf.config.testline.ue import Android, Qualcomm
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline.pdu import Gude, HBTE, TopYoung
from taf.config.testline.dcap import DcapRnD
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.pdn import PDNTafUeAndroidDetails
from taf.config.testline.ue import TafUeAndroid
from taf.config.testline import Connection


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_abil_master = CapacityUnit(addr="192.168.253.20")
_abil_slave = CapacityUnit(addr="192.168.253.21")
_abil_loner = CapacityUnit(addr="192.168.253.22")

_pdu_1 = Gude("10.44.206.32", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "EPC", "8221-1")

_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.208.231", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil_master, _abil_slave, _abil_loner],
    pdu_port=_pdu_1.pdu_ports[8],
)

_airscale = Airscale(common_units=[_common_unit])


# #CU
_cu = CU(
    backhaul_site_oam_ip="10.71.208.231",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.208.231", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.208.231", username="Nemuadmin", password="nemuuser"
    ),
)

_ru_pdu = TopYoung(addr="10.71.195.72", port_numbers=[2])

_ru0 = RU(
    ru_hw_group='hw_group',
    default_ssh_connection_details=SshServiceDetails(
        addr='172.22.8.6',
        username='rfsw',
        password='3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc='),
    lmp_connection=SshServiceDetails(
        addr='172.16.77.128',
        username='toor4nsn',
        password='oZPS0POrRieRtu'),
    pdu_port=_ru_pdu.pdu_ports[2],
)

_attenuator = AHBTE(
    ip_addr="10.71.208.204",
    port=5000,
    attenuation_port_numbers=[3, 4, 5, 6],
    model="PA-16-16-6-127-0.5-B-S",
)

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_common_unit,label="SFP", port_id=1),
        target=Endpoint(unit=_ru0 ,label="SFP", port_id=1),
    )
]



_du = DU(airscale=_airscale, rus=[_ru0],f1_m_ip_addr="10.71.208.231",cablinks=_ru_cablinks)

_dcap = DcapRnD(
    HttpConnectionDetails(
        addr="10.101.60.54", port="443", username="dcapuser", password="dcapadmin!"
    )
)

_classical_bts = ClassicalBts(cu=_cu, dus=[_du], global_bts_id=10298, instance_id=1913, dcap=_dcap)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.24", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_airscale.common_units[0],
            interface_type="lmp",
        )
            ],
)

_core = RealCore5G(mcc=460, mnc=2)

_core_ssh = SshServiceDetails(addr="10.42.61.65", username="5g", password="2019H@slo")

_common_unit_lte_ssh = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_common_unit_lte = CommonUnit(
    _common_unit_lte_ssh, capacity_units=[_capacity_unit], pdu_port=None
)

_abia = CapacityUnit(addr="192.168.253.20")

_asia = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.208.205", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abia],
)

_lteenb = RealEnb(
    airscale=Airscale(common_units=[_asia]),
    x2_link_addr=NetworkAddress(
        v4="10.71.208.205",
        routing=RoutingInformation(gateway="10.71.208.1", ip_prefix_length=24),
    ),
    global_bts_id=10082,instance_id=1964
)

#_appserver_ssh = SshServiceDetails(
#    addr="10.71.219.229", username="mmw_sg5", password="mm@5", port="45813"
#)

#_iperf = IperfDataTransferDetails(
#    ssh_connection_details=_appserver_ssh,
#    network_interface_address="10.71.219.229",
#    port="45913",
#)


_app_server_1 = TafUeAppServer(
    app_server_name="APP_5",
    address="10.71.207.149",
    user="vrf3_sg5",
    password="vrf3@sg5",
    ports=[45813,45913],
)



_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_app_server_1,
    interval=1,
    server_close_delay=50,
)

_pdn1 = PDNTafUeAndroidDetails(
    entryName="dxdata2", apnName="dxdata2", apnType=["DEFAULT"]
)

_android = TafUeAndroid(
    serial_number="7b0bf687", 
    capabilities=['REAL_UE', "qualcomm"],
    ue_pc_address="10.71.217.57",
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.57", username="mn5gran", password="nokia123@"
    ),
    data_transfer=[_data_transfer_iperf],
    pdns=[_pdn1],
    proxy_mngr_port="9955",
#    server_dir="/cygdrive/c/pyro_server",
#    python_path="C:/Python27/python.exe",
#    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
#    diag_cfg_path="C:/pyro_server/DIAG.cfg",
#    iperf_details=_iperf,
#    capabilities=["qct_dx50"],

)

#_appserver = AppServer(iperf_details=_iperf)

tl = TestLine(
    test_pc=_test_pc,
    test_pcs=[_test_pc],
    gnbs=[_classical_bts],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_QC_ASILR_ABIO1_AQQQA_ENB",
    core=_core,
    enbs=[_lteenb],
    ues=[_android],
#   appserver=_appserver,
    attenuator=_attenuator,

)

__all__ = ["tl"]
