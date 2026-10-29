__maintainer__ = ""
__email__ = ""

from ute_testline_configuration.ute_config import UTE_CONFIG, Host, Pdu, FSMr3, IPHY

host = [Host(), Host("10.92.11.12")]
fsm3 = [
    FSMr3(
        pdu=Pdu("10.92.11.17", 2, "ATEN"),
        bbmod1_pdu=Pdu("10.92.11.17", 3, "ATEN"),
        bbmod2_pdu=Pdu("10.92.11.17", 4, "ATEN"),
        top_ip="10.8.17.250",
    ),
    FSMr3(
        pdu=Pdu("10.92.11.17", 6, "ATEN"),
        bbmod1_pdu=Pdu("10.92.11.17", 7, "ATEN"),
        bbmod2_pdu=Pdu("10.92.11.17", 8, "ATEN"),
        trs_ip="10.0.1.4",
        top_ip="10.8.17.250",
    ),
]
iphy = [
    IPHY(pdu=Pdu("10.92.11.17", 1, "ATEN")),
    IPHY(pdu=Pdu("10.92.11.17", 5, "ATEN"), trs_ip="10.0.2.4"),
]

tl = UTE_CONFIG(host=host, fsm=fsm3, iphy=iphy)
node1 = tl[1]
node2 = tl[2]

__all__ = ["tl"]
