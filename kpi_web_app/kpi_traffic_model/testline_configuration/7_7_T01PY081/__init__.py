# Generated with TL configuration generator at 2025-09-11_06:49:55

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
from taf.config.testline.lmi import SerialOverTcp, Remote
from taf.config.testline.nms import NMS, NetAct
import os
import yaml

# ------------------------PDU_CONFIGURATION------------------------

_bts_pdu = FPFH(
    port_numbers=[1, 2],
    addr="fpfh-pc04-48-d01.d01-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_bts_ru_pdu_0 = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],
    addr="fpfh-pc03-48-d01.d01-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_bts_ru_pdu_1 = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],
    addr="fpfh-pc03-24-d01.d01-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_bts_ru_pdu_2 = FPFH(
    port_numbers=[1, 2, 3],
    addr="fpfh-pc05-40-d01.d01-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_bts_ru_pdu_3 = FPFH(
    port_numbers=[1, 2, 3],
    addr="fpfh-pc06-40-d01.d01-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_bts_ru_pdu_4 = FPFH(
    port_numbers=[1, 2, 3],
    addr="fpfh-pc07-48-d01.d01-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

# ------------------------RUS_CONFIGURATION------------------------

_radio_unit_ahpmdk_0 = RU(
    ru_hw_group="AHPMDK",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    radio_type="AHPMDK",
    serial_number="L1254007385",
    product_code="476714A",
    pdu_port=PduPort(pdu=_bts_ru_pdu_1, port_no=1),
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(
                addr=NetworkAddress(
                    v4="MUMIN-PC04-04-D01.d01-leg.krk-lab.nsn-rdnet.net"
                ),
                port=2001,
            )
        ]
    ),
)

_radio_unit_ahpmdk_1 = RU(
    ru_hw_group="AHPMDK",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    radio_type="AHPMDK",
    serial_number="L1254504694",
    product_code="476714A",
    pdu_port=PduPort(pdu=_bts_ru_pdu_1, port_no=2),
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(
                addr=NetworkAddress(
                    v4="MUMIN-PC04-14-D01.d01-leg.krk-lab.nsn-rdnet.net"
                ),
                port=2001,
            )
        ]
    ),
)

_radio_unit_ahpmdk_2 = RU(
    ru_hw_group="AHPMDK",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    radio_type="AHPMDK",
    serial_number="L1254503807",
    product_code="476714A",
    pdu_port=PduPort(pdu=_bts_ru_pdu_1, port_no=3),
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(
                addr=NetworkAddress(
                    v4="MUMIN-PC04-13-D01.d01-leg.krk-lab.nsn-rdnet.net"
                ),
                port=2001,
            )
        ]
    ),
)

_radio_unit_ahegha_0 = RU(
    ru_hw_group="AHEGHA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    radio_type="AHEGHA",
    serial_number="K9243720733",
    product_code="475767A",
    pdu_port=PduPort(pdu=_bts_ru_pdu_0, port_no=3),
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(
                addr=NetworkAddress(
                    v4="MUMIN-PC04-07-D01.d01-leg.krk-lab.nsn-rdnet.net"
                ),
                port=2001,
            )
        ]
    ),
)

_radio_unit_ahegha_1 = RU(
    ru_hw_group="AHEGHA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    radio_type="AHEGHA",
    serial_number="K9252708725",
    product_code="475767A",
    pdu_port=PduPort(pdu=_bts_ru_pdu_0, port_no=5),
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(
                addr=NetworkAddress(
                    v4="MUMIN-PC04-08-D01.d01-leg.krk-lab.nsn-rdnet.net"
                ),
                port=2001,
            )
        ]
    ),
)

_radio_unit_ahegha_2 = RU(
    ru_hw_group="AHEGHA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    radio_type="AHEGHA",
    serial_number="K9252708662",
    product_code="475767A",
    pdu_port=PduPort(pdu=_bts_ru_pdu_0, port_no=4),
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(
                addr=NetworkAddress(
                    v4="MUMIN-PC04-09-D01.d01-leg.krk-lab.nsn-rdnet.net"
                ),
                port=2001,
            )
        ]
    ),
)

_radio_unit_ahsb_0 = RU(
    ru_hw_group="AHSB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="",
    ),
    radio_type="AHSB",
    serial_number="RW235000357",
    product_code="476343A",
    pdu_port=PduPort(pdu=_bts_ru_pdu_0, port_no=2),
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(
                addr=NetworkAddress(
                    v4="MUMIN-PC04-06-D01.d01-leg.krk-lab.nsn-rdnet.net"
                ),
                port=2001,
            )
        ]
    ),
)

_radio_unit_ahsb_1 = RU(
    ru_hw_group="AHSB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="",
    ),
    radio_type="AHSB",
    serial_number="RW235000355",
    product_code="476343A",
    pdu_port=PduPort(pdu=_bts_ru_pdu_0, port_no=1),
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(
                addr=NetworkAddress(
                    v4="MUMIN-PC04-05-D01.d01-leg.krk-lab.nsn-rdnet.net"
                ),
                port=2001,
            )
        ]
    ),
)

_radio_unit_ahsb_2 = RU(
    ru_hw_group="AHSB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="",
    ),
    radio_type="AHSB",
    serial_number="LR254505768",
    product_code="476343A",
    pdu_port=PduPort(pdu=_bts_ru_pdu_0, port_no=6),
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(
                addr=NetworkAddress(
                    v4="MUMIN-PC04-18-D01.d01-leg.krk-lab.nsn-rdnet.net"
                ),
                port=2001,
            )
        ]
    ),
)

_radio_unit_avqj_0 = RU(
    ru_hw_group="AVQJ",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    radio_type="AVQJ",
    serial_number="1M253406015",
    product_code="476724A",
    pdu_port=PduPort(pdu=_bts_ru_pdu_3, port_no=1),
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(
                addr=NetworkAddress(
                    v4="MUMIN-PC04-19-D01.d01-leg.krk-lab.nsn-rdnet.net"
                ),
                port=2001,
            )
        ]
    ),
)

_radio_unit_avqj_1 = RU(
    ru_hw_group="AVQJ",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    radio_type="AVQJ",
    serial_number="1M254501645",
    product_code="476724A",
    pdu_port=PduPort(pdu=_bts_ru_pdu_3, port_no=2),
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(
                addr=NetworkAddress(
                    v4="MUMIN-PC04-20-D01.d01-leg.krk-lab.nsn-rdnet.net"
                ),
                port=2001,
            )
        ]
    ),
)

_radio_unit_avqj_2 = RU(
    ru_hw_group="AVQJ",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    radio_type="AVQJ",
    serial_number="1M254501646",
    product_code="476724A",
    pdu_port=PduPort(pdu=_bts_ru_pdu_3, port_no=3),
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(
                addr=NetworkAddress(
                    v4="MUMIN-PC04-21-D01.d01-leg.krk-lab.nsn-rdnet.net"
                ),
                port=2001,
            )
        ]
    ),
)

_radio_unit_avqc_0 = RU(
    ru_hw_group="AVQC",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    radio_type="AVQC",
    serial_number="1M251002394",
    product_code="476401A",
    pdu_port=PduPort(pdu=_bts_ru_pdu_2, port_no=1),
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(
                addr=NetworkAddress(
                    v4="MUMIN-PC04-10-D01.d01-leg.krk-lab.nsn-rdnet.net"
                ),
                port=2001,
            )
        ]
    ),
)

_radio_unit_avqc_1 = RU(
    ru_hw_group="AVQC",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    radio_type="AVQC",
    serial_number="1M252808557",
    product_code="476401A",
    pdu_port=PduPort(pdu=_bts_ru_pdu_2, port_no=2),
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(
                addr=NetworkAddress(
                    v4="MUMIN-PC04-11-D01.d01-leg.krk-lab.nsn-rdnet.net"
                ),
                port=2001,
            )
        ]
    ),
)

_radio_unit_avqc_2 = RU(
    ru_hw_group="AVQC",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    radio_type="AVQC",
    serial_number="1M252808569",
    product_code="476401A",
    pdu_port=PduPort(pdu=_bts_ru_pdu_2, port_no=3),
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(
                addr=NetworkAddress(
                    v4="MUMIN-PC04-12-D01.d01-leg.krk-lab.nsn-rdnet.net"
                ),
                port=2001,
            )
        ]
    ),
)

_radio_unit_azhn_0 = RU(
    ru_hw_group="AZHN",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    radio_type="AZHN",
    serial_number="4H210330025",
    product_code="475547A",
    pdu_port=PduPort(pdu=_bts_ru_pdu_4, port_no=1),
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(
                addr=NetworkAddress(
                    v4="MUMIN-PC04-03-D01.d01-leg.krk-lab.nsn-rdnet.net"
                ),
                port=2001,
            )
        ]
    ),
)

_radio_unit_azhn_1 = RU(
    ru_hw_group="AZHN",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    radio_type="AZHN",
    serial_number="4H210330026",
    product_code="475547A",
    pdu_port=PduPort(pdu=_bts_ru_pdu_4, port_no=2),
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(
                addr=NetworkAddress(
                    v4="MUMIN-PC04-02-D01.d01-leg.krk-lab.nsn-rdnet.net"
                ),
                port=2001,
            )
        ]
    ),
)

_radio_unit_azhn_2 = RU(
    ru_hw_group="AZHN",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    radio_type="AZHN",
    serial_number="4H210930084",
    product_code="475547A",
    pdu_port=PduPort(pdu=_bts_ru_pdu_4, port_no=3),
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(
                addr=NetworkAddress(
                    v4="MUMIN-PC04-01-D01.d01-leg.krk-lab.nsn-rdnet.net"
                ),
                port=2001,
            )
        ]
    ),
)

_radio_unit_akna_0 = RU(
    ru_hw_group="AKNA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    radio_type="AKNA",
    serial_number="1M252902908",
    product_code="475945A",
    pdu_port=PduPort(pdu=_bts_ru_pdu_1, port_no=4),
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(
                addr=NetworkAddress(
                    v4="MUMIN-PC04-15-D01.d01-leg.krk-lab.nsn-rdnet.net"
                ),
                port=2001,
            )
        ]
    ),
)

_radio_unit_akna_1 = RU(
    ru_hw_group="AKNA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    radio_type="AKNA",
    serial_number="1M223420933",
    product_code="475945A",
    pdu_port=PduPort(pdu=_bts_ru_pdu_1, port_no=6),
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(
                addr=NetworkAddress(
                    v4="MUMIN-PC04-16-D01.d01-leg.krk-lab.nsn-rdnet.net"
                ),
                port=2001,
            )
        ]
    ),
)

_radio_unit_akna_2 = RU(
    ru_hw_group="AKNA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    radio_type="AKNA",
    serial_number="1M223420924",
    product_code="475945A",
    pdu_port=PduPort(pdu=_bts_ru_pdu_1, port_no=5),
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(
                addr=NetworkAddress(
                    v4="MUMIN-PC04-17-D01.d01-leg.krk-lab.nsn-rdnet.net"
                ),
                port=2001,
            )
        ]
    ),
)

# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T01PY081-1.d01.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_0_instance_id = 85081
_gnb_0_global_bts_id = 85081

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.89.3.81/24",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.89.3.81/24",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
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
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_xnc_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_xnu_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_ngc_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_ngu_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
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

_gnb_0_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIA",
    hardware_version="A.103",
    serial_number="K9181626380",
    product_code="473096A.103",
    slot_id=SlotId.B3,
    rus=[
        _radio_unit_ahpmdk_0,
        _radio_unit_ahpmdk_1,
        _radio_unit_ahpmdk_2,
    ],
)

_gnb_0_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.26",
    hardware_type="ABIP",
    hardware_version="A.102",
    serial_number="L1233802874",
    product_code="475792A.102",
    slot_id=SlotId.B1,
    rus=[
        _radio_unit_ahpmdk_0,
        _radio_unit_ahpmdk_1,
        _radio_unit_ahpmdk_2,
        _radio_unit_ahsb_0,
        _radio_unit_ahsb_1,
        _radio_unit_ahsb_2,
        _radio_unit_ahegha_0,
        _radio_unit_ahegha_1,
        _radio_unit_ahegha_2,
    ],
)

_gnb_0_capacity_unit_2 = CapacityUnit(
    addr="192.168.253.30",
    hardware_type="ABIQ",
    hardware_version="A.102",
    serial_number="L1241505051",
    product_code="476397A.102",
    slot_id=SlotId.B2,
    rus=[
        _radio_unit_ahegha_0,
        _radio_unit_ahegha_1,
        _radio_unit_ahegha_2,
        _radio_unit_avqj_0,
        _radio_unit_avqj_1,
        _radio_unit_avqj_2,
    ],
)

_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[
        _gnb_0_capacity_unit_0,
        _gnb_0_capacity_unit_1,
        _gnb_0_capacity_unit_2,
    ],
    hardware_type="ASIM",
    hardware_version="A.104",
    serial_number="L1233406239",
    mac_addr="28:74:f5:0b:62:9",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
    pdu_port=PduPort(pdu=_bts_pdu, port_no=1),
)

_gnb_0_airscale = Airscale(
    common_units=[_gnb_0_common_unit_0],
    product_code="475773A",
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

# ------------------------GNB1_CONFIGURATION------------------------

_test_pc_gnb_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T01PY081-2.d01.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_1_instance_id = 85082
_gnb_1_global_bts_id = 85082

_gnb_1_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_1.default_ssh_connection_details,
)

_gnb_1_oam_ip = NetworkAddress(
    v4="10.89.3.82/24",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_1_f1m_ip = NetworkAddress(
    v4="10.89.3.82/24",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_1_f1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_f1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_x2c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_x2u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_s1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_xnc_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_xnu_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_ngc_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_ngu_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_1_oam_ip.v4.split("/")[0],
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

_cu_gnb_1 = CU(
    backhaul_site_oam_ip=_gnb_1_oam_ip,
    oam_ssh_connection_details=_gnb_1_primary_ssh_lmp_connection,
    oam_http_connection_details=_gnb_1_oam_http_connection,
    f1m=_gnb_1_f1m_ip,
    f1c=_gnb_1_f1c_ip,
    f1u=_gnb_1_f1u_ip,
    x2c=_gnb_1_x2c_ip,
    x2u=_gnb_1_x2u_ip,
    s1c=_gnb_1_s1c_ip,
    s1u=_gnb_1_s1u_ip,
    xnc=_gnb_1_xnc_ip,
    xnu=_gnb_1_xnu_ip,
    ngc=_gnb_1_ngc_ip,
    ngu=_gnb_1_ngu_ip,
    instance_id=_gnb_1_instance_id,
    global_bts_id=_gnb_1_global_bts_id,
)

_gnb_1_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIP",
    hardware_version="A.101",
    serial_number="L1231800027",
    product_code="475792A.101",
    slot_id=SlotId.B2,
    rus=[
        _radio_unit_ahpmdk_0,
        _radio_unit_ahpmdk_1,
        _radio_unit_ahpmdk_2,
        _radio_unit_ahsb_0,
        _radio_unit_ahsb_1,
        _radio_unit_ahsb_2,
    ],
)

_gnb_1_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.26",
    hardware_type="ABIP",
    hardware_version="A.101",
    serial_number="L1231505847",
    product_code="475792A.101",
    slot_id=SlotId.B3,
    rus=[
        _radio_unit_ahegha_0,
        _radio_unit_ahegha_1,
        _radio_unit_ahegha_2,
        _radio_unit_avqc_0,
        _radio_unit_avqc_1,
        _radio_unit_avqc_2,
    ],
)

_gnb_1_capacity_unit_2 = CapacityUnit(
    addr="192.168.253.30",
    hardware_type="ABIO",
    hardware_version="A.105",
    serial_number="L1230613326",
    product_code="475266A.105",
    slot_id=SlotId.B1,
    rus=[
        _radio_unit_azhn_0,
        _radio_unit_azhn_1,
        _radio_unit_azhn_2,
        _radio_unit_akna_0,
        _radio_unit_akna_1,
        _radio_unit_akna_2,
    ],
)

_gnb_1_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_1_primary_ssh_lmp_connection,
    capacity_units=[
        _gnb_1_capacity_unit_0,
        _gnb_1_capacity_unit_1,
        _gnb_1_capacity_unit_2,
    ],
    hardware_type="ASIM",
    hardware_version="A.104",
    serial_number="L1233406321",
    mac_addr="28:74:f5:0b:74:87",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
    pdu_port=PduPort(pdu=_bts_pdu, port_no=2),
)

_gnb_1_airscale = Airscale(
    common_units=[_gnb_1_common_unit_0],
    product_code="475773A",
)

_du_gnb_1 = DU(
    airscale=_gnb_1_airscale,
    oam_ip=_gnb_1_oam_ip,
    f1_m_ip_addr=_gnb_1_f1m_ip,
    f1_c_ip_addr=_gnb_1_f1c_ip,
    f1_u_ip_addr=_gnb_1_f1u_ip,
    f1_m_cu=_gnb_1_f1m_ip,
    f1_c_cu=_gnb_1_f1c_ip,
    f1_u_cu=_gnb_1_f1u_ip,
    instance_id=_gnb_1_instance_id,
    global_bts_id=_gnb_1_global_bts_id,
)

_gnb_1 = ClassicalBts(
    cu=_cu_gnb_1,
    dus=[_du_gnb_1],
    instance_id=_gnb_1_instance_id,
    global_bts_id=_gnb_1_global_bts_id,
)

_test_pc_gnb_1.connections = [
    Connection(
        device=_gnb_1.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

# --------------------------MantaRay netact------------------------

_nms = NMS(
    netact=NetAct(
        ssh_connections_info=SshServiceDetails(
            addr="10.43.48.76",
            username="omc",
            password="Medsql!_1893",
        ),
        https_main_info=HttpConnectionDetails(
            addr="srnclab1044lbwas.srnblr.nsn-rdnet.net",
        ),
    ),
)

# ------------------------UE_CONFIGURATION------------------------

def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path
    return ue_config


_set_abstract_lib_config_env("ue.yaml")

# ------------------------TL_CONFIGURATION------------------------

tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0, _gnb_1],
    test_pcs=[_test_pc_gnb_0, _test_pc_gnb_1],
    tl_cloud_topology="CLOUD_7_7_T01PY081",
    nms=_nms,
)

tl.netact_dn = 'PLMN-PLMN/MRBTS-85081'

__all__ = ["tl"]
