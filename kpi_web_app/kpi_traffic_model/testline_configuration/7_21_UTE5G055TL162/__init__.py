__maintainer__ = "Xu Yan"
__team__ = "5G SC Syve"
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
from taf.config.testline import RealEnb
from taf.config.testline.core import EPCSim
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.29.133", username="ute", password="ute"
    )
)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="172.30.1.11",
        vlan_id=2762,
        routing=RoutingInformation(gateway="172.30.1.1", ip_prefix_length=24),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="172.30.1.11", vlan_id=3330),
    x2u=NetworkAddress(v4="172.30.1.11", vlan_id=3330),
    s1c=NetworkAddress(v4="172.30.1.11", vlan_id=3330),
    s1u=NetworkAddress(v4="172.30.1.11", vlan_id=3330),
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
    hardware_type="ASIK",
    hardware_version="102",
)


_airscale = Airscale(common_units=[_common_unit])

_du = DU(airscale=_airscale, rus=[])

_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=55162, global_bts_id=55162)

_epcsim = EPCSim(
    mme_ip="172.30.1.1",
    edaemon_port=10000,
    egate_port=20000,
    mcc=460,
    mnc=2,
    tac=1,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.29.133", username="ute", password="ute"
    ),
    dir_path="/opt/core",
    cfg_filename="epcsim.cfg",
)

_lteenb = RealEnb(
    x2_link_addr=NetworkAddress(v4="10.66.29.197"),
    instance_id=551621,
    global_bts_id=551621,
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
    {"key": "SEC_KEY", "value": "00112233445566778899AABBCCDDEEFF"},
    {"key": "OPC_KEY", "value": "0ED47545168EAFE2C39C075829A7B61F"},
    # Support up to 10 UEs. from IMSI_1 ~ IMSI_10, UE_IP_1 ~ UE_IP_10
    {"key": "IMSI_1", "value": "460:02:3100007443"},
    {"key": "UE_IP_1", "value": "27.168.1.11"},
    {"key": "IMSI_2", "value": "460:02:3100007442"},
    {"key": "UE_IP_2", "value": "27.168.1.10"},
]

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_lteenb],
    ues=None,
    core=_epcsim,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_DSS_DAS_ASIKR_ABILB4B5_ASIAL_ABIAB1B2_2xUDFA_3xUDIA_2xUDCA_FDD",
)
tl.ue_config = ue_config
tl.epcsim_config = epcsim_config

__all__ = ["tl"]
