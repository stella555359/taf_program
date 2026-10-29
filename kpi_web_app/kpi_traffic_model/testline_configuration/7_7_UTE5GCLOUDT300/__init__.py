# Generated with TL configuration generator at 2024-10-07_11:50:14

# Repository  -> https://wrgitlab.int.net.nokia.com/ran_pz_krk/config_generator
# Jenkins job -> http://krk-pz-jenkins.krk-lab.nsn-rdnet.net:5990/view/Tools/job/Config_Generator/build?delay=0sec

__maintainer__ = "KRKAUTO5GPZ"
__team__ = "I_MN_RAN_PZ_KRK_TAG"
__email__ = "I_MN_RAN_PZ_KRK_TAG@internal.nsn.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import RU, RUExtension
from taf.config.testline.enb import RealEnb
from taf.config.testline.airscale import (
    Airscale,
    CommonUnit,
    CoreUnit,
    CapacityUnit,
    SlotId,
    TRSInterfaces,
)
from taf.config.testline.pdu import PduPort, FPFH, HPE
from taf.config.testline.ue import TafUeAndroid
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
import os
import yaml

# ------------------------PDU_CONFIGURATION------------------------

_bts_pdu_1 = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],  # update port_no
    addr="fpfh-gf07-22-sc5g.sc5g-leg.krk-lab.nsn-rdnet.net",  # update address
    login="admin",
    password="admin",
)
_bts_pdu_2 = FPFH(
    port_numbers=[1, 3, 4, 5],  # update port_no
    addr="fpfh-gf07-46-sc5g.sc5g-leg.krk-lab.nsn-rdnet.net",  # update address
    login="admin",
    password="admin",
)
_hpe_snmp_user = {
    "userName": "user-lab0",
    "authKey": "NokiaBts2003",
    "privKey": "NokiaBts2003",
    "authProtocol": "MD5",
    "privProtocol": "AES",      # HPE v2.0.0.K DES, HPE v2.0.0.Q/v2.0.0.T AES, ATEN should be AES
}

_bts_pdu_3 = HPE(
    port_numbers=[3],  # update port_no
    addr="https://10.89.63.75/#/?_k=mwcfvc",  # update address
    snmp_user=_hpe_snmp_user,
)




# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT300.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_0_instance_id = 75300
_gnb_0_global_bts_id = 75300

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.83.183.50/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.83.183.50/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_0_f1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_f1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_x2c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.83.183.50/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.83.183.50/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_0_xnc_ip = NetworkAddress(
    v4="10.83.183.50/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_0_xnu_ip = NetworkAddress(
    v4="10.83.183.50/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_0_ngc_ip = NetworkAddress(
    v4="10.83.183.50/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_0_ngu_ip = NetworkAddress(
    v4="10.83.183.50/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_0_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_0_oam_ip.v4.split("/")[0],
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

_cu_gnb_0 = CU(
    backhaul_site_oam_ip=_gnb_0_oam_ip,
    oam_ssh_connection_details=_gnb_0_primary_ssh_lmp_connection,
    oam_http_connection_details=_gnb_0_oam_http_connection,
    f1m=_gnb_0_f1m_ip,
    f1c=_gnb_0_f1c_ip,
    f1u=_gnb_0_f1u_ip,
    x2c=_gnb_0_x2c_ip,
    x2u=_gnb_0_x2u_ip,
    s1c=_gnb_0_s1c_ip,
    s1u=_gnb_0_s1u_ip,
    xnc=_gnb_0_xnc_ip,
    xnu=_gnb_0_xnu_ip,
    ngc=_gnb_0_ngc_ip,
    ngu=_gnb_0_ngu_ip,
    instance_id=_gnb_0_instance_id,
    global_bts_id=_gnb_0_global_bts_id,
)

_gnb_0_radio_unit_1 = RU(
    ru_hw_group="AHGF",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHGF",
    serial_number="4H224330002",
    product_code="476301A.X21",
    pdu_port=PduPort(pdu=_bts_pdu_1, port_no=3),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_2 = RU(
    ru_hw_group="AHHA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHHA",
    serial_number="EB233660026",
    product_code="474147A.102",
    pdu_port=PduPort(pdu=_bts_pdu_2, port_no=3),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_3 = RU(
    ru_hw_group="FHEF",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="FHEF",
    serial_number="1M160996665",
    product_code="473043A.101",
    pdu_port=PduPort(pdu=_bts_pdu_2, port_no=5),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_4 = RU(
    ru_hw_group="FHEF",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="FHEF",
    serial_number="1M161075356",
    product_code="473043A.101",
    pdu_port=PduPort(pdu=_bts_pdu_1, port_no=5),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_5 = RU(
    ru_hw_group="FHEF",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="FHEF",
    serial_number="1M161075318",
    product_code="473043A.101",
    pdu_port=PduPort(pdu=_bts_pdu_1, port_no=2),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_6 = RU(
    ru_hw_group="AHGF",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHGF",
    serial_number="4H230230014",
    product_code="476301A.101",
    pdu_port=PduPort(pdu=_bts_pdu_1, port_no=6)  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_7 = RU(
    ru_hw_group="AHHA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHHA",
    serial_number="EB233660117",
    product_code="474147A.102",
    pdu_port=PduPort(pdu=_bts_pdu_2, port_no=4),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_8 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="APHG",
    serial_number="NH222200462",
    product_code="475295A.101",
    pdu_port=PduPort(pdu=_bts_pdu_3, port_no=3)  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[],
    hardware_type="ASOG",
    hardware_version="A.102",
    serial_number="L1243303631",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C1,
    pdu_port=PduPort(pdu=_bts_pdu_2, port_no=1),  # uncomment & update port_no for gNB - for eNB you can delete
)
_gnb_0_radio_unit_9 = RU(
    ru_hw_group="AKQJ",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    radio_type="AKQJ",
    serial_number="1M224640979",
    product_code="475824A.101",
     pdu_port=PduPort(
         pdu=_bts_pdu_1, port_no=4
     ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    #)
)
_gnb_0_radio_unit_10 = RU(
    ru_hw_group="AHEGHA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    radio_type="AHEGHA",
    serial_number="BL2334H60N9",
    product_code="475767A.101",
     pdu_port=PduPort(
         pdu=_bts_pdu_1, port_no=5
     ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)
_gnb_0_airscale = Airscale(
    common_units=[_gnb_0_common_unit_0],
    product_code="N/A",
)

_du_gnb_0 = DU(
    airscale=_gnb_0_airscale,
    oam_ip=_gnb_0_oam_ip,
    f1_m_ip_addr=_gnb_0_f1m_ip,
    f1_c_ip_addr=_gnb_0_f1c_ip,
    f1_u_ip_addr=_gnb_0_f1u_ip,
    f1_m_cu=_gnb_0_f1m_ip,
    f1_c_cu=_gnb_0_f1c_ip,
    f1_u_cu=_gnb_0_f1u_ip,
    instance_id=_gnb_0_instance_id,
    global_bts_id=_gnb_0_global_bts_id,
)

_gnb_0 = ClassicalBts(
    cu=_cu_gnb_0,
    dus=[_du_gnb_0],
    instance_id=_gnb_0_instance_id,
    global_bts_id=_gnb_0_global_bts_id,
)

_test_pc_gnb_0.connections = [
    Connection(
        device=_gnb_0.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

_appserver_ssh = TafUeAppServer(
    app_server_name="APP_1",
    address="10.83.249.131",
    user="5g",
    password="5g",
    bind_interface_ip="10.83.249.161",
    expected_prompt="5g@KRK-SB18s16-App1:.*\$\s+"
)

_samsung_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_appserver_ssh,
    binary_path='/data/data/com.nokia.android.application/'
    # binary_path="/data/local/tmp/"
)

_samsung = TafUeAndroid(
    serial_number="R5CT915CDKB",
    ue_pc_address="10.83.177.27",
    ue_pc_port="80",
    ssh_connection_details=SshServiceDetails(
        addr="PLKR-SG02-200.intra.noklab.net", username="NOKLAB/pzkrk", password="NokiaBts2003"
    ),
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "SAMSUNG"],
    qualcomm_prototype=False,
    data_transfer=[_samsung_iperf]

)

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0],
    test_pcs=[_test_pc_gnb_0],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_SAMSUNG_ASOG_2xAGHF_2xAHHA_3xFHEF_APHG_4xAWHGEQ",
ues = [_samsung]
)
##
__all__ = ["tl"]

