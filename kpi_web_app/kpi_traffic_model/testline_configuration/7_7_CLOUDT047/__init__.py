__maintainer__ = "5G SC QT"
__team__ = "5G QT"
__email__ = "I_SC_5G_QT_KRK@internal.nsn.com"


import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    OpenStackConnectionDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
)
from taf.config.testline.cloud_hosting import (
    NCIR,
    ControlNode,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    ComputeNode,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.core import EPCSim
from taf.config.testline.ue import Airphone
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import PduPort, ATEN
from taf.compatibility.configuration import TestlineWrapper


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7_7_CLOUDT047.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
    )
)

_cu = CU(
    backhaul_site_oam_ip="10.83.182.47",
    oam_ssh_connection_details=SshServiceDetails(
        addr="sc5g-enb-047.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
)

_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_du_capacity_unit = CapacityUnit(addr="fsp1_c")

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection, capacity_units=[_du_capacity_unit]
)

_airscale = Airscale(common_units=[_du_common_unit])

_du = DU(airscale=_airscale)

_cbts = ClassicalBts(cu=_cu, dus=[_du])


tl = TestLine(test_pc=_test_pc, gnbs=[_cbts], tl_cloud_topology="class04")
tl = TestlineWrapper(tl)

__all__ = ["tl"]
