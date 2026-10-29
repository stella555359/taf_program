__maintainer__ = "Yin 4. Chen"
__team__ = "NSB MN RAN RD VRF HAZ3 6"
__email__ = "yin.4.chen@nokia-sbell.com"

import os

from taf.config.testline import (
    CloudDeployment,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    MasterNode,
    K8S,
)
from taf.config.testline import (
    SshServiceDetails,
    HttpConnectionDetails,
    K8SConnectionDetails,
)
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline import RealEnb, Airscale, CommonUnit
from taf.config.testline import HBTE_PDU as HBTE
from taf.config.testline import RU, RadioTypes
from taf.config.testline import CloudBts, CU
from taf.config.testline import VDU, FHGW
from taf.config.testline import PxeServer
from taf.config.testline import TestLine
from taf.config.testline import RealEnb
from taf.config.testline import TestPc
from taf.config.testline.dcap import DcapRnD, DcapBasic
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile


_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.28", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_dcap = DcapBasic(
    connection_details=HttpConnectionDetails(
        addr="10.57.195.83", port="443", username="utfuser", password="utfadmin!"
    )
)


# CU
_cu = CU(
    instance_id=877,
    global_bts_id=877,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.187.145"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.187.2", username="cranuser877", password="systeM!23"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.187.145", username="Nemuadmin", password="Nokia@123", port=443
    ),
)

# cloud_deployment for vCU
_vcu_cnf_1 = DeploymentVnfStack(
    name="cran877vcu",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_cnf_values-override.yaml"),
)
_vcu_intnet_1 = DeploymentNetworkStack(
    name=_vcu_cnf_1.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_pvc_values-override.yaml"),
)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.57.187.2", username="cranuser877", password=""
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.187.2", username="cranuser877", password="", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran877", master_node=_vcu_master_node)

_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_cnf_1],
    cloud_hosting=_vcu_k8s,
)


# 5G RU
_ru_pdu = HBTE(addr="10.71.196.52", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu.pdu_ports[6],
    radio_type=RadioTypes.AEQE,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.45",
        username="root",
        password="a2%FgSz3$fHmdusap354xujw7a",
    ),
)

# vDU
_ssh_connection_details_0 = SshServiceDetails(
    addr="10.64.161.34", username="core", password="system123"
)
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.64.161.34", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_k8s_0 = K8S(namespace="cran877", master_node=_master_node_0)
_vdu_cnf_0 = DeploymentVnfStack(
    name="vdu877",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_0/DU_cnf_values-override.yaml"),
)
_vdu_intnet_0 = DeploymentNetworkStack(
    name=_vdu_cnf_0.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_0/DU_pvc_values-override.yaml"),
)

_vdu_k8s_cloud_deployment_0 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_k8s_0,
    networks=[_vdu_intnet_0],
    vnfs=[_vdu_cnf_0],
)


_du_0 = VDU(
    cloud_deployment=_vdu_k8s_cloud_deployment_0,
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.64.161.254", username="Nemuadmin", password="nemuuser"
    ),
    instance_id=877,
    global_bts_id=877,
)

# for FastMile CPE
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.238",
    user="vrf3_sg6",
    password="vrf3@sg6",
    bind_interface_ip="10.57.191.238",
    expected_prompt="[vrf3_sg6@appserver ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=[57877, 57877],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    com_port="25",
    # ue_pc_address="10.57.130.11",
    ue_pc_address="10.71.218.195",
    root_password="AQU_,t+:Z3jHzgWH",
    default_user_password="kafYG3iK!=..pMqn",
    ue_manage_ip="192.168.0.1",
    serial_number="KLT234301908",
    data_transfer=[_fastmile_data_transfer_1],
    version="Receiver 5G19-A",
    ue_pc_port=5555,
    capabilities=["REAL_FASTMILE_UE", "nokia_fastmile"],
)


# BTS
_cbts = CloudBts(
    dus=[_du_0],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
    dcap=_dcap
)

# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    ues=[_fastmile_1],
    tl_cloud_topology="CLOUD_5G_AIC_RM17_OCP_AEQE",
)

_misc = {
    # 1-Use NOM config in __init__.py, 0-Use NOM config in global_variable.py.
    # If this key is not given, default value is 1
    "nom_config_source_from_init_py": "1",
    # 1-Use Netact config in __init__.py, 0-Use Netact config in global_variable.py.
    # If this key is not given, default value is 1
    "netact_config_source_from_init_py": "1",
}
tl._misc = _misc

__all__ = ["tl"]
