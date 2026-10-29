__maintainer__ = "Xu Yan"
__team__ = "Nanjing ASIR Test Team - LOTUS"
__email__ = "nj-fz-lotus@LIST.NOKIA.COM"
__owner_email__ = "yan.i.xu@nokia-sbell.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import SC5GRadio
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.enb import RealEnb
from taf.config.testline.core import EPCSim
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.pdu import PduPort, ATEN, FACOM, Pdu, EPC , HBTE
from taf.config.testline.appserver import AppServer
import os
import yaml


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path
    return ue_config


_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.31.57", username="ute", password="uteUTE!"
    )
)

_cu = CU(
    backhaul_site_oam_ip="192.168.255.129",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
)

_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_du_capacity_unit = CapacityUnit(
    addr="192.168.253.20", hardware_type="ABIL", hardware_version="A102"
)

_pdu = HBTE(addr="10.66.47.150", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_pdus = [_pdu]

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIK",
    hardware_version="A102",
    #pdu_port=_pdus[0].pdu_ports[3],
)

_ru = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(addr="10.66.31.59", username="ute", password="Nokia666@ute!"),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    # pdu_port=PduPort(pdu=ATEN(addr="1.1.1.1", port_numbers=[1, 2]), port_no=1),
    pdu_port=None,
)

_airscale = Airscale([_du_common_unit])

_du = DU(airscale=_airscale, rus=[_ru])

_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=3487, global_bts_id=3487)

_core_pc_ssh = SshServiceDetails(addr="10.66.31.57", username="ute", password="uteUTE!")
_core_pc = TestPc(default_ssh_connection_details=_core_pc_ssh)
_core = EPCSim(
    mme_ip="172.30.1.1",
    mcc=460,
    mnc=6,
    tac=1,
    default_ssh_connection_details=_core_pc_ssh,
    dir_path="/opt/core",
    cfg_filename="sim_ipv4_nsa.cfg",
    edaemon_port=60002,
    egate_port=60001,
)

# #Qualcomm
_appserver_ssh = SshServiceDetails(
    addr="10.66.31.57", username="ute", password="uteUTE!", port="22"
)


""" UE Configuration
In order to import UE configuration into the runtime environment of the robot framework,
the variable `ue_config` MUST NOT start with an underscore.
"""
_ue_config = _set_abstract_lib_config_env("ue_config.yaml")

_epcsim_config = [
    {
        "key": "PGW_ADDR",
        "value": "27.168.1.200",
    },
    {
        "key": "SEC_KEY",
        "value": "11111111111111111111111111111111",
    },
    {
        "key": "OPC_KEY",
        "value": "11111111111111111111111111111111",
    },
    # Support up to 10 UEs. from IMSI_1 ~ IMSI_10, UE_IP_1 ~ UE_IP_10
    {
        "key": "IMSI_1",
        "value": "460:06:3100000021",
    },
    {
        "key": "UE_IP_1",
        "value": "27.168.1.12",
    },
    {
        "key": "IMSI_2",
        "value": "460:02:8001011057",
    },
    {
        "key": "UE_IP_2",
        "value": "27.168.1.14",
    },
]

_abia = CapacityUnit(addr="192.168.253.20")

_asia = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abia],
)

_lteenb = RealEnb(
    airscale=Airscale(common_units=[_asia]),
    x2_link_addr=NetworkAddress(
        v4="172.30.1.10",
    ),
    global_bts_id=40016,
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_lteenb],
    #pdus=_pdus,
    ues=None,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_SA_ASIR_ASIKR_ABILB4_ASIAL_ABIAB1_APHG_2xAWHHA_RFS",
)
tl.ue_config = _ue_config
# tl.epcsim_config = _epcsim_config

os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "ue_config.yaml"
)

__all__ = ["tl"]
