__maintainer__ = "Zhong Mingjuan"
__team__ = "RAN_PZ_NJI_SG01"
__email__ = "mingjuan.zhong@nokia-sbell.com"


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

_gnb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.24.128", username="ute", password="Nokia666@ute!"
    )
)

_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.24.129", username="ute", password="Nokia666@ute!"
    )
)

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.66.30.192",
        vlan_id=30,
        routing=RoutingInformation(gateway="10.66.30.1", ip_prefix_length=24),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.66.30.192", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.66.30.192", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.66.30.192", vlan_id=30),
    x2u=NetworkAddress(v4="10.66.30.192", vlan_id=30),
    s1c=NetworkAddress(v4="10.66.30.192", vlan_id=30),
    s1u=NetworkAddress(v4="10.66.30.192", vlan_id=30),
)

_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=SshServiceDetails(
        addr="10.66.24.128", username="ute", password="Nokia666@ute!"
    ),
)

_capacity_unit0 = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIO", hardware_version="102"
)

_capacity_unit1 = CapacityUnit(
    addr="fsp2_c", hardware_type="ABIO", hardware_version="102"
)

_common_unit = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit0, _capacity_unit1],
    hardware_type="ASIL",
    hardware_version="101",
)

_ru0 = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.24.130", username="ute", password="Nokia666@ute!"
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

_ru1 = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.24.131", username="ute", password="Nokia666@ute!"
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

_du = DU(airscale=_airscale, rus=[_ru0, _ru1])

_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=73276, global_bts_id=73276)

_epcsim = EPCSim(
    mme_ip="10.66.24.128",
    edaemon_port=10000,
    egate_port=20000,
    mcc=460,
    mnc=6,
    tac=1,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.24.128",
        username="ute",
        password="Nokia666@ute!",
    ),
    dir_path="/opt/iphy",
    cfg_filename="epcsim.cfg",
)

_lte_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=SshServiceDetails(
        addr="10.66.24.129", username="ute", password="Nokia666@ute!"
    ),
)

_lte_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIA", hardware_version="A102"
)

_lte_common_unit = CommonUnit(
    lmp_connection=_lte_lmp_connection,
    capacity_units=[_lte_capacity_unit],
    hardware_type="ASIA",
    hardware_version="A102",
)

_airscale_enb = Airscale(common_units=[_lte_common_unit])

_lteenb = RealEnb(system_module=_airscale_enb, oam_ip=NetworkAddress(v4="172.30.1.10"))


def _set_abstract_lib_config_env(ue_config_file):
    ue_config_abs_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ue_config_file
    )
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path
    return ue_config


# ue_config = _set_abstract_lib_config_env("ue_config.yaml")

_epcsim_config = [
    {
        "key": "PGW_ADDR",
        "value": "2001:0db8:0:BBB0::1/60",
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
        "value": "460:06:3100001009",
    },
    {
        "key": "UE_IP_1",
        "value": "2001:db8:0:bbb0:1062:20ff:fe1e:0e4b",
    },
]

tl = TestLine(
    test_pc=_gnb_test_pc,
    # test_pcs=[_gnb_test_pc, _enb_test_pc],
    gnbs=[_cbts],
    enbs=[_lteenb],
    ues=None,
    core=_epcsim,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIR_ASIKL_ABILB1_AWHQJ_COAM",
)
# tl.ue_config = ue_config
tl.epcsim_config = _epcsim_config

__all__ = ["tl"]
