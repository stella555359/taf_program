import os
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)  # added in taf.meta.5.4
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)

# added in taf.meta 5.4
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline import Mitron
from taf.config.testline import RU
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer

__maintainer__ = "Chen Yin"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_2_GMS <I_MN_5G_RAN_IV4_LINE_HZG_2@internal.nsn.com>"
)
__email__ = "yin.1.chen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.111", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CI_Detail_UE_Type=''


# #5GRU for classicalBTS
_ru1_pdu = HBTE(addr="10.57.172.78", port_numbers=[2])

_ru1 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHQK,
)

_ru2_pdu = HBTE(addr="10.57.172.78", port_numbers=[4])

_ru2 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.6", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.6", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru2_pdu.pdu_ports[4],
    radio_type=RadioTypes.AHQK,
)

_ru3_pdu = HBTE(addr="10.57.172.78", port_numbers=[1])

_ru3 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.10", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.10", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru3_pdu.pdu_ports[1],
    radio_type=RadioTypes.AHQK,
)

_ru4_pdu = FACOM(addr="10.57.172.79", port_numbers=[3])

_ru4 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.14", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.14", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru4_pdu.pdu_ports[3],
    radio_type=RadioTypes.AHQK,
)

_ru5_pdu = HBTE(addr="10.57.131.137", port_numbers=[3])

_ru5 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.18", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.18", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru5_pdu.pdu_ports[3],
    radio_type=RadioTypes.AHQK,
)

_ru6_pdu = FACOM(addr="10.57.172.79", port_numbers=[5])

_ru6 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.22", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.22", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru6_pdu.pdu_ports[5],
    radio_type=RadioTypes.AHQK,
)
###UE-fastmile

# for FastMile CPE
_fastmile_appserver = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.244",
    user="vrf4_sg2",
    password="Vrf4@sg2_123456",
    bind_interface_ip="10.57.191.244",
    expected_prompt="[vrf4_sg2@appserver ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=[54000, 54006, 54007, 54008, 54009],
)

_fastmile_data_transfer = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile = TafUeFastmile(
    com_port="22",
    ue_pc_address="10.57.130.217",
    root_password="bb6abee2c4cc",
    ue_manage_ip="192.168.1.1",
    serial_number="LPL22140061A",
    data_transfer=[_fastmile_data_transfer],
    ue_pc_port=5555,
#    proxy_mngr_port=5555,
    ueproxy_force_release=True,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

_Huawei = Android(
    ssh_connection_details=SshServiceDetails(
    addr="10.57.130.217", username="mn5gran", password="nokia123@"
),
    serial_number="1111111",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    capabilities=["REAL_ANDROID_UE", "Huawei"],
)


# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.57.242.45", port_numbers=[5])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6],
    f1_m_ip_addr="10.57.223.234",
)

# #CU
_cu = CU(
    backhaul_site_oam_ip="10.57.223.234",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.223.234", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.223.234", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, global_bts_id="226", instance_id="226")

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    ues=[_fastmile,_Huawei],
    tl_cloud_topology=_tl_cloud_topology,
)
