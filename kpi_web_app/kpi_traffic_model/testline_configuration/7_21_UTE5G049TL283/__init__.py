import os
import yaml  # <----------
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, DU, ClassicalBts
from taf.config.testline import SC5GRadio, SC4GRadio
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation

__maintainer__ = "5G SC CRT"
__team__ = "5G SC CRT"
__email__ = "nj-fz-crt@list.nokia.com"

###########################################
# Test PC - server running the Robot tests
###########################################
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.24.112",
        username="ute",
        password="ute"
        # Login information for the VM where the test cases will be run  #<------
    )
)

_epcsim = EPCSim(  #  <---------
    mme_ip="172.30.1.1",
    edaemon_port=10000,
    egate_port=20000,
    mcc=460,
    mnc=2,
    tac=1,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.24.111",
        username="ute",
        password="ute",
    ),
    dir_path="/opt/iphy/WTS_825328.3_4.0.5730/",
    cfg_filename="sim_ipv4.cfg",
)


def _set_abstract_lib_config_env(ue_config_file):  # <----------
    ue_config_abs_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ue_config_file
    )
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)

    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


ue_config = _set_abstract_lib_config_env("ue_config.yaml")  # <----------

epcsim_config = [  # <----------
    {
        "key": "PGW_ADDR",
        "value": "27.168.1.200",
    },
    {
        "key": "SEC_KEY",
        "value": "00112233445566778899AABBCCDDEEFF",
    },
    {
        "key": "OPC_KEY",
        "value": "0ED47545168EAFE2C39C075829A7B61F",
    },
    # Support up to 10 UEs. from IMSI_1 ~ IMSI_10, UE_IP_1 ~ UE_IP_10
    {
        "key": "IMSI_1",
        "value": "460:02:3100010833",
    },
    {
        "key": "UE_IP_1",
        "value": "27.168.1.70",
    },
]
###################
# gNB definition
###################

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.66.30.12",  # <----
        vlan_id=30,
        routing=RoutingInformation(gateway="10.66.30.1", ip_prefix_length=24),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.66.30.12", username="toor4nsn", password="oZPS0POrRieRtu"  # <----
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.66.30.12", username="Nemuadmin", password="nemuuser"  # <----
    ),
    x2c=NetworkAddress(v4="172.30.1.11", vlan_id=159),  # <----
    x2u=NetworkAddress(v4="172.30.1.11", vlan_id=159),  # <----
    s1c=NetworkAddress(v4="172.30.1.11", vlan_id=159),  # <----
    s1u=NetworkAddress(v4="172.30.1.11", vlan_id=159),  # <----
)

_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIO", hardware_version="101"
)

_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129",  # <----
        username="toor4nsn",
        password="oZPS0POrRieRtu",
        proxy=SshServiceDetails(
            addr="10.66.24.112",
            username="ute",
            password="ute",  # Login information for the VM connected to gNB  #<----
        ),
    ),
    capacity_units=[_capacity_unit],
    hardware_type="ASIB",
    hardware_version="102",
)

_ru = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="10.66.24.80",  # <----
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.24.80",
                username="ute",
                password="ute",  # Login information for the VM connected to 5G sHUB   #<----
            ),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=None,
)

_airscale = Airscale(common_units=[_common_unit])
_du = DU(airscale=_airscale, rus=[_ru])
_cbts = ClassicalBts(
    cu=_cu,
    dus=[_du],
    instance_id=4007,  # ID of MRBTS object   #<----
    global_bts_id=4007,  # ID of NRBTS object   #<----
)

###################
# eNB definition
###################
_capacity_units_enb = [CapacityUnit(addr="192.168.253.20", hardware_type="ABIA")]

_common_unit_enb = CommonUnit(
    hardware_type="ASIB",
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
        proxy=SshServiceDetails(
            addr="10.66.24.112",
            username="ute",
            password="ute",  # Login information for the VM connected to eNB   #<----
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
                addr="10.66.24.80",
                username="ute",
                password="ute",  # Login information for the VM connected to 4G sHUB   #<----
            ),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
)
_airscale_enb = Airscale(common_units=[_common_unit_enb])

_lteenb = RealEnb(
    system_module=_airscale_enb,
    rms=[_radio_modules_enb],
    instance_id=492831,  # ID of MRBTS object   #<----
    global_bts_id=492831,  # ID of LNBTS object   #<----
    oam_ip=(
        NetworkAddress(
            v4="192.168.255.129",  # <------Mplan IP of Primary Core
            v6="2a00:8a00:8001:2::aa",
        ),
        NetworkAddress(
            v4="172.30.1.10",  # <----- Mplan IP of Secondary Core
            v6="2a00:8a00:8001:2::aa",
        ),
    ),
    x2_link_addr=NetworkAddress(
        v4="192.168.255.129"
    ),  # <---- Be used to get eNB scf:SC_UE_keywords.Get asir enb scf ${enb_x2ip}, ${OUTPUT DIR}/, Enb_SCF.xml
)


_netact = Netact("10.32.215.128")


####################################################################################################
# Example of testline definition consists of both 5G and 4G.
# Add other definitions, such as "ues", "core", etc. according to actual test line configurations.
####################################################################################################
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_lteenb],
    ues=None,
    core=_epcsim,
    tl_cloud_topology="CLOUD_4G_CLASSICAL_ASIBR_ABIOB4_ABINB5_APHG_2xAWHHIQB_3xAHENB",
)
tl.ue_config = ue_config
tl.epcsim_config = epcsim_config

__all__ = ["tl"]
