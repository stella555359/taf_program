__maintainer__ = "5G SC CRT"
__team__ = "5G SC CRT"
__email__ = "nj-fz-crt@list.nokia.com"

import os
import yaml

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
from taf.config.testline.pdu import PduPort, Pdu
from taf.config.testline import RealEnb
from taf.config.testline.core import EPCSim
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation

_gnb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.26.252", username="ute", password="Nokia666@ute!"
    )
)

_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.26.253", username="ute", password="Nokia666@ute!"
    )
)

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="192.168.255.129",
        vlan_id=689,
        routing=RoutingInformation(gateway="192.168.255.1", ip_prefix_length=24),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="192.168.255.129", vlan_id=689),
    x2u=NetworkAddress(v4="192.168.255.129", vlan_id=689),
    s1c=NetworkAddress(v4="192.168.255.129", vlan_id=689),
    s1u=NetworkAddress(v4="192.168.255.129", vlan_id=689),
)

_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIL", hardware_version="102"
)

_common_unit = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    hardware_type="ASIB",
    hardware_version="102",
)

_ru = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.31.69", username="ute", password="uteUTE!"
            ),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    # pdu_port=PduPort(
    #     pdu=Pdu(addr='1.1.1.1', port_numbers=[1, 2]), port_no=1)
    pdu_port=None,
)

_airscale = Airscale(common_units=[_common_unit])

_du = DU(airscale=_airscale, rus=[_ru])

_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=155, global_bts_id=1)

_epcsim = EPCSim(
    mme_ip="172.30.1.1",
    edaemon_port=10000,
    egate_port=20000,
    mcc="262",
    mnc="03",
    tac=1,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.26.252",
        username="ute",
        password="ute",
    ),
    dir_path="/opt/core",
    cfg_filename="epcsim.cfg",
)

_lteenb = RealEnb(
    x2_link_addr=NetworkAddress(v4="172.30.1.10"),
    oam_ip=NetworkAddress(v4="172.30.1.10"),
)

epcsim_config = [
    {
        "key": "PGW_ADDR",
        "value": "27.168.1.200",
    },
    {
        "key": "SEC_KEY",
        "value": "00112233445566778899aabbccddeeff",
    },
    {
        "key": "OPC_KEY",
        "value": "0ed47545168eafe2c39c075829a7b61f",
    },
    # Support up to 10 UEs. from IMSI_1 ~ IMSI_10, UE_IP_1 ~ UE_IP_10
    {
        "key": "IMSI_1",
        "value": "262:03:3030376346",
    },
    {
        "key": "UE_IP_1",
        "value": "27.168.1.10",
    },
    {
        "key": "IMSI_2",
        "value": "262:03:3030376371",
    },
    {
        "key": "UE_IP_2",
        "value": "27.168.1.11",
    },
]

""" UE Configuration
In order to import UE configuration into the runtime environment of the robot framework,
the variable `ue_config` MUST NOT start with an underscore.
"""


def _set_abstract_lib_config_env(ue_config_file):
    ue_config_abs_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ue_config_file
    )
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)

    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


ue_config = _set_abstract_lib_config_env("ue_config.yaml")


tl = TestLine(
    test_pc=_gnb_test_pc,
    # test_pcs=[_gnb_test_pc, _enb_test_pc],
    gnbs=[_cbts],
    enbs=[_lteenb],
    ues=None,
    core=_epcsim,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_DSS_ASIKL_ABILB1_ASIAR_ABIAB4B5_CDD_4xUAP_FDD",
)
tl.ue_config = ue_config
tl.epcsim_config = epcsim_config

__all__ = ["tl"]
