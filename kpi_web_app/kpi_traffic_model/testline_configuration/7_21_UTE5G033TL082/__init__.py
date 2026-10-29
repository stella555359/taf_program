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
from taf.config.testline import SC5GRadio, SC4GRadio
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import RealEnb
from taf.config.testline.core import EPCSim
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.31.36", username="ute", password="uteUTE!"
    )
)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.66.30.23",
        vlan_id=30,
        routing=RoutingInformation(gateway="10.66.31.0", ip_prefix_length=24),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.66.30.23", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.66.30.23", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="172.30.1.11", vlan_id=169),
    x2u=NetworkAddress(v4="172.30.1.11", vlan_id=169),
    s1c=NetworkAddress(v4="172.30.1.11", vlan_id=169),
    s1u=NetworkAddress(v4="172.30.1.11", vlan_id=169),
)

_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(
    addr="192.168.253.22", hardware_type="ABIL", hardware_version="A102"
)
_common_unit = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    hardware_type="ASIK",
    hardware_version="101",
)


_ru = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.31.38", username="ute", password="Nokia666@ute!"
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
_capacity_units_enb = [CapacityUnit(addr="fsp1_c", hardware_type="ABIA")]

_common_unit_enb = CommonUnit(
    hardware_type="ASIA",
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
        proxy=SshServiceDetails(
            addr="10.66.31.37",
            username="ute",
            password="Nokia666@ute!",  # Login information for the VM connected to eNB
        ),
    ),
    capacity_units=_capacity_units_enb,
)
_airscale = Airscale(common_units=[_common_unit])

_du = DU(airscale=_airscale, rus=[_ru])

_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=3382, global_bts_id=3382)

_epcsim = EPCSim(
    mme_ip="172.30.1.1",
    edaemon_port=10000,
    egate_port=20000,
    mcc=460,
    mnc=6,
    tac=111,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.31.36",
        username="ute",
        password="uteUTE!",
    ),
    dir_path="/opt/core",
    cfg_filename="epcsim.cfg.env",
)

_radio_modules_enb = SC4GRadio(
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.29.38",
                username="ute",
                password="Nokia666@ute!",  # Login information for the VM connected to 4G sHUB
            ),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
)
# _lteenb = RealEnb(x2_link_addr=NetworkAddress(v4="172.30.1.10"))
_airscale_enb = Airscale(common_units=[_common_unit_enb])

_lteenb = RealEnb(
    system_module=_airscale_enb,
    rms=[_radio_modules_enb],
    instance_id=33821,
    global_bts_id=33821,
    oam_ip=NetworkAddress(v4="172.30.1.10"),
    x2_link_addr=NetworkAddress(v4="172.30.1.10"),
)


def _set_abstract_lib_config_env(ue_config_file):
    ue_config_abs_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ue_config_file
    )
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)

    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


ue_config = _set_abstract_lib_config_env("ue_config.yaml")

epcsim_config = [
    {"key": "PGW_ADDR", "value": "27.168.1.200"},
    {"key": "SEC_KEY", "value": "11111111111111111111111111111111"},
    {"key": "OPC_KEY", "value": "11111111111111111111111111111111"},
    # Support up to 10 UEs. from IMSI_1 ~ IMSI_10, UE_IP_1 ~ UE_IP_10
    {"key": "IMSI_1", "value": "460:06:3100000035"},
    {"key": "UE_IP_1", "value": "27.168.1.11"},
    {"key": "IMSI_2", "value": "460:06:4000000011"},
    {"key": "UE_IP_2", "value": "27.168.1.10"},
]

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_lteenb],
    ues=None,
    core=_epcsim,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIR_ASIKR_ABILB4_ASIAL_ABIAB1_APHA_2xAHFHIA_RFS_FDD",
)
tl.ue_config = ue_config
tl.epcsim_config = epcsim_config

__all__ = ["tl"]
