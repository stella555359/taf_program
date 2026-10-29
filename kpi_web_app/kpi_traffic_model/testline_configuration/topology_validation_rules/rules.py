class RequiredParam(object):
    """ Class for instances defining rules with required parameters"""

    def __init__(self, parameters):
        self.parameters = parameters


airphone_mandatory_params = RequiredParam(
    parameters=[
        "tl.test_pc.default_ssh_connection_details.password",
        "tl.gnbs[0].cu.x2c",
        "tl.gnbs[0].cu.oam_ssh_connection_details.password",
        "tl.gnbs[0].cu.oam_http_connection_details.password",
        "tl.gnbs[0].cu.oam_http_connection_details.username",
        "tl.gnbs[0].du.airscale.common_units[0].lmp_connection.password",
        "tl.ues[0].l1.common_units[0].lmp_connection.password",
        "tl.gnbs[0].du.airscale.common_units[0].pdu_port",
        "tl.ues[0].l1.common_units[0].pdu_port",
    ]
)

rpi_mandatory_params = RequiredParam(
    parameters=[
        "tl.hardware_controllers[0].default_ssh_connection_details.addr",
        "tl.hardware_controllers[0].default_ssh_connection_details.username",
        "tl.hardware_controllers[0].default_ssh_connection_details.password",
    ]
)

prisma_mandatory_params = RequiredParam(
    parameters=[
        "tl.ues[0].airmosaic_ssh_connection_details.addr",
        "tl.ues[0].airmosaic_ssh_connection_details.username",
        "tl.ues[0].airmosaic_ssh_connection_details.password",
        "tl.ues[0].airmosaic_harness_connection_details.addr",
        "tl.ues[0].airmosaic_harness_connection_details.port",
        "tl.ues[0].lsu_uu_ssh_connection_details.addr",
        "tl.ues[0].lsu_uu_ssh_connection_details.username",
        "tl.ues[0].lsu_uu_ssh_connection_details.password",
        "tl.ues[0].lsu_uu_ssh_connection_details.proxy",
        "tl.ues[0].tstm_uu_ssh_connection_details.addr",
        "tl.ues[0].tstm_uu_ssh_connection_details.username",
        "tl.ues[0].tstm_uu_ssh_connection_details.password",
        "tl.ues[0].tstm_uu_ssh_connection_details.proxy",
        "tl.ues[0].prisma_config_file",
        "tl.ues[0].default_sid_file",
        "tl.ues[0].iperf_details.ssh_connection_details",
        "tl.ues[0].iperf_details.network_interface_address",
        "tl.ues[0].iperf_details.iperf_path",
        "tl.ues[0].iperf_details.port",
        "tl.ues[0].imsi",
        "tl.ues[0].sec_key",
        "tl.ues[0].gnb_common_unit_for_throughput_check.capacity_units",
    ]
)

appserver_mandatory_params = RequiredParam(
    parameters=[
        "tl.appserver.iperf_details.ssh_connection_details",
        "tl.appserver.iperf_details.network_interface_address",
        "tl.appserver.iperf_details.iperf_path",
        "tl.appserver.iperf_details.port",
    ]
)

gnbs_mandatory_params = RequiredParam(
    parameters=[
        "tl.gnbs[0].cu.backhaul_site_oam_ip.v4",
        "tl.gnbs[0].cu.backhaul_site_oam_ip.routing.gateway",
        "tl.gnbs[0].cu.backhaul_site_oam_ip.routing.ip_prefix_length",
        "tl.gnbs[0].cu.x2c.v4",
        "tl.gnbs[0].cu.x2c.routing.gateway",
        "tl.gnbs[0].cu.x2c.routing.ip_prefix_length",
        "tl.gnbs[0].cu.x2u.v4",
        "tl.gnbs[0].cu.x2u.routing.gateway",
        "tl.gnbs[0].cu.x2u.routing.ip_prefix_length",
        "tl.gnbs[0].cu.s1u.v4",
        "tl.gnbs[0].cu.s1u.routing.gateway",
        "tl.gnbs[0].cu.s1u.routing.ip_prefix_length",
        "tl.gnbs[0].instance_id",
        "tl.gnbs[0].global_bts_id",
        "tl.gnbs[0].dus[0].airscale.common_units[0].lmp_connection.addr",
        "tl.gnbs[0].dus[0].airscale.common_units[0].lmp_connection.username",
        "tl.gnbs[0].dus[0].airscale.common_units[0].lmp_connection.password",
        "tl.gnbs[0].dus[0].airscale.common_units[0].capacity_units[0].addr",
        "tl.gnbs[0].dus[0].airscale.common_units[0].capacity_units[0].hardware_type",
        "tl.gnbs[0].dus[0].airscale.common_units[0].capacity_units[0].hardware_version",
        "tl.gnbs[0].dus[0].airscale.common_units[0].hardware_type",
    ]
)
