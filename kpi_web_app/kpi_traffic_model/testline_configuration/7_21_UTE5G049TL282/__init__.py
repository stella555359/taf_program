__maintainer__ = "Jiang Shengmin"
__team__ = "NSB MN RAN Pz NJI 3"
__email__ = "shengmin.jiang@list.nokia.com"

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
from taf.config.testline.attenuator import AttenuationPort, TopYoung, HBTE, RadioRack

_gnb_rf_att = RadioRack(
    ip_addr="10.66.25.205", port="50000", attenuation_port_numbers=[1, 2, 3, 4, 5, 6]
)
_gnb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.24.105", username="ute", password="ute"
    )
)
_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.24.106", username="ute", password="ute"
    )
)

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="172.30.1.11",
        vlan_id=569,
        routing=RoutingInformation(gateway="172.30.1.1", ip_prefix_length=24),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.66.30.168", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="172.30.1.11", vlan_id=119),
    x2u=NetworkAddress(v4="172.30.1.11", vlan_id=119),
    s1c=NetworkAddress(v4="172.30.1.11", vlan_id=119),
    s1u=NetworkAddress(v4="172.30.1.11", vlan_id=119),
)

_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIO", hardware_version="102"
)

_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
        proxy=SshServiceDetails(
            addr="10.66.24.105",
            username="ute",
            password="ute",  # Login information for the VM connected to gNB
        ),
    ),
    capacity_units=[_capacity_unit],
    hardware_type="ASIB",
    hardware_version="102",
)

_ru_1 = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.24.107", username="ute", password="ute"
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

_du = DU(airscale=_airscale, rus=[_ru_1])

_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=49282, global_bts_id=49282)

###################
# eNB definition
###################
_capacity_units_enb = [CapacityUnit(addr="192.168.253.20", hardware_type="ABIA")]

_common_unit_enb = CommonUnit(
    hardware_type="ASIL",
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
        proxy=SshServiceDetails(
            addr="10.66.24.106",
            username="ute",
            password="ute",  # Login information for the VM connected to eNB
        ),
    ),
    capacity_units=_capacity_units_enb,
)

_radio_modules_enb = SC4GRadio(
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.24.107",
                username="ute",
                password="ute",  # Login information for the VM connected to 4G sHUB
            ),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    )
)
_airscale_enb = Airscale(common_units=[_common_unit_enb])

_lteenb = RealEnb(
    x2_link_addr=NetworkAddress(v4="10.66.30.169"),
    system_module=_airscale_enb,
    rms=[_radio_modules_enb],
    instance_id=492821,
    global_bts_id=492821,
    oam_ip=NetworkAddress(v4="10.66.30.169"),
)

_epcsim = EPCSim(
    mme_ip="172.30.1.1",
    edaemon_port=10000,
    egate_port=20000,
    mcc=460,
    mnc=2,
    tac=500,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.24.105", username="ute", password="ute"
    ),
    dir_path="/opt/core",
    cfg_filename="epcsim.cfg",
)

# _lteenb = RealEnb(x2_link_addr=NetworkAddress(v4="172.30.1.10"))


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
    {"key": "IMSI_1", "value": "460:02:3100009700"},
    {"key": "UE_IP_1", "value": "27.168.1.10"},
    {"key": "IMSI_2", "value": "460:02:3100009699"},
    {"key": "UE_IP_2", "value": "27.168.1.11"},
]

tl = TestLine(
    test_pc=_gnb_test_pc,
    test_pcs=[_gnb_test_pc, _enb_test_pc],
    gnbs=[_cbts],
    enbs=[_lteenb],
    ues=None,
    core=_epcsim,
    attenuator=_gnb_rf_att,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIBL_ABIOB1B2_ASILR_ABIOB4_1xAPHG_4xAWHHIQB_RFS",
)
tl.ue_config = ue_config
tl.epcsim_config = epcsim_config

__all__ = ["tl"]
