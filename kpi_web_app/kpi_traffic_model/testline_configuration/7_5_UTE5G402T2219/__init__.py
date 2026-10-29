import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.radio import RadioTypes
from taf.config.testline.pdu import HBTE as PBHBTE

__maintainer__ = ""
__team__ = "MN 5G RAN I&V 4 Pz HZG SG1"
__email__ = ""

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.87", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##5GRU for classical BTS
_ru1_pdu = PBHBTE(addr="10.68.87.8", port_numbers=[1])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="user", password="pass"
    ),
    pdu_port=_ru1_pdu.pdu_ports[1],
    radio_type=RadioTypes.AWHQ2,
)

_ru2_pdu = PBHBTE(addr="10.68.87.8", port_numbers=[5])

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="user", password="pass"
    ),
    pdu_port=_ru2_pdu.pdu_ports[5],
    radio_type=RadioTypes.AWHQN,
)


##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit1 = CapacityUnit(addr="1.1.1.1", hardware_type="ABIQ")
_capacity_unit2 = CapacityUnit(addr="1.1.1.1", hardware_type="ABIP")
_capacity_unit3 = CapacityUnit(addr="1.1.1.1", hardware_type="ABIL")


_gnb_pdu = PBHBTE(addr="10.68.87.13", port_numbers=[3])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit1, _capacity_unit2, _capacity_unit3],
    pdu_port=_gnb_pdu.pdu_ports[3],
	hardware_type="ASIM",
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2],
    f1_m_ip_addr="10.68.88.58",
)

##CU
_cu = CU(
    backhaul_site_oam_ip="10.68.88.58",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.88.58", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.88.58", username="Nemuadmin", password="nemuuser"
    ),
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"
# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="36970", global_bts_id="36970"
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
)