### How to using heat templates

### Create 5G CU VNFCs Step by Step

### Admin user create Flavors

$openstack stack create -t 5gbts_flavor.yaml <flavors-stack-name> --wait

### Admin user create image

before creating the image, you should upload VNFCs qcow2 file

$openstack image create --disk-format=qcow2 --container-format=bare --project <tenant_id> --file=<qcow2-name> <image-name>

### Admin user create oam network

before creating the oam network, you should edit the parameters in 5gbts_oam_net.env.

$openstack stack create -t 5gbts_oam_net.yaml -e 5gbts_oam_net.env <oam-net-stack-name> --wait

### Admin user create external networks based on flat provider net

before creating the external networks, you should edit the parameters in 5gbts_ext_net.env.

$openstack stack create -t 5gbts_ext_net.yaml -e 5gbts_ext_net.env <ext-net-stack-name>

### Admin user create internal networks based on tenant network

before creating the internal networks, you should edit the parameters in 5gbts_int_net.env.

$openstack stack create -t 5gbts_int_net.yaml -e 5gbts_int_net.env <ext-net-stack-name>

### _member_ user create keypair

$openstack keypair create <keypair-name> > <keypair-file>

### _member_ create VNFCs for 5G CU

before creating the VNFCs, you should edit the parameters in 5gbts_heat.env

$openstack stack create -t 5gbts_heat.yaml -e 5gbts_heat.env <vnfcs-stack-name>


### Parameters

### Parameters for 5gbts_oam_net.env
* network_opts:                          the whole json parameter for creating oam network.
* network_opts.vnf_name:                 the vnf name, currently it just using as a name prefix for the created network.
* network_opts.number_of_networks:       the number of external networks to create.
* network_opts.networks:                 the array of the external networks' parameters.
* network_opts.networks[n].name:         the name of the created network.
* network_opts.networks[n].cidr:         the cidr address of the created sub-net in the network.
* network_opts.networks[n].gateway:      the gateway address of the created sub-net in the network, 'null' needs disable gateway.
* network_opts.networks[n].start:        the start address of the ip-pool in created sub-net.
* network_opts.networks[n].end:          the end address of the ip-pool in created sub-net.
* network_opts.networks[n].net_type:     the net type for the created network, currently, according the site solution the value is vlan, please do not modify the type.
* network_opts.networks[n].sid:          the segment id of the tenant network.
* network_opts.networks[n].ip_ver:       the network's IP version, 4 or 6.
* network_opts.networks[n].provider:     the provider name where the network will create on.
* network_opts.networks[n].tenant_id:    the tenant id of the _member_ user.


### Parameters for 5gbts_ext_net.env

* network_opts:                          the whole json parameter for creating external networks.
* network_opts.vnf_name:                 the vnf name, currently it just using as a name prefix for the created network.
* network_opts.number_of_networks:       the number of external networks to create.
* network_opts.networks:                 the array of the external networks' parameters.
* network_opts.networks[n].name:         the name of the created network.
* network_opts.networks[n].cidr:         the cidr address of the created sub-net in the network.
* network_opts.networks[n].gateway:      the gateway address of the created sub-net in the network.
* network_opts.networks[n].start:        the start address of the ip-pool in created sub-net.
* network_opts.networks[n].end:          the end address of the ip-pool in created sub-net.
* network_opts.networks[n].net_type:     the net type for the created network, currently, according the site solution the value is flat, please do not modify the type.
* network_opts.networks[n].ip_ver:       the network's IP version, 4 or 6.
* network_opts.networks[n].provider:     the provider name where the network will create on.
* network_opts.networks[n].tenant_id:    the tenant id of the _member_ user.


### Parameters for 5gbts_int_net.env

* network_opts:                          the whole json parameter for creating internal networks.
* network_opts.vnf_name:                 the vnf name, currently it just using as a name prefix for the created network.
* network_opts.number_of_networks:       the number of internal networks to create.
* network_opts.networks:                 the array of the internal networks' parameters.
* network_opts.networks[n].name:         the name of the created network.
* network_opts.networks[n].ip_ver:       the network's IP version, 4 or 6.
* network_opts.networks[n].tenant_id:    the tenant id of the _member_ user.

### Parameters for 5gbts_heat.env

* image:                                 the image name for creating the VNFCs, check it by command "openstack image list".
* ssh_public_key:                        the public key for generate key-pair, check it by command "openstack keypair show <keypair-name> --public-key".
* vnf_name:                              the vnf name, currently it just using as a name prefix for the created VNFCs.
* cluster_id:                            the cluster id for identify the different VNFs with the same vnf_name.
* vnfc_type_name_case:                   the case of vnfc type, allowed values are upper and lower.
* flavors:                               A json dictionary for identify the flavor name for each VNFC, you could check them by command "openstack flavor list".
* timezone:                              the default timezone for all created VNFC vm.
* oam_network:                           the uuid of the oam network, check it by command "openstack network list".
* oam_ip:                                the OAM ip address for the OAM VNFC in oam network.
* ntp_servers:                           the ntp server value.
* dns_forwarders:                        the dns forwarders.
* internal_network:                      the uuid of the internal network, check it by command "openstack network list".
* internal_srv_network:                  the uuid of the internal_srv network, check it by command "openstack network list".
* internal_networks.internal:            the cidr address and ip-pool of the created internal subnet.
* internal_networks.internal_srv:        the cidr address and ip-pool of the created internal_srv subnet.
* external_networks.extnet_*:            the uuids of the external networks, check it by command "openstack network list".
* ext_port_vlans.f1om_sid_*:             the vlan of the created f1om port.
* ext_port_vlans.fronthaul_sid_*:        the vlan of the created fronthaul port.
* ext_port_vlans.backhaul_sid_*:         the vlan of the created backhaul port.
* oam_port_type:                         the port type of oam interface, for 296-D, only virtio is supported.
* int_port_type:                         the port type of internal and internal_srv interface, for 296-D, only virtio is supported.
* ext_port_type:                         the port type of fronthaul, backhaul and f1om interface, for 296-D, only sriov is supported.
* int_port_mtu:                          the mtu of internal and internal_srv interface
* ext_port_mtu:                          the mtu of fronthaul, backhaul and f1om interface
* oam_port_mtu:                          the mtu of oam interface
* int_pmtu:                              the max mtu value supported by internal and internal_srv interface
* ext_pmtu:                              the max mtu value supported by fronthaul, backhaul and f1om interface
* oam_pmtu:                              the max mtu value supported by oam interface
* availability_zone:                     availability zone region
* number_of_upue_nodes:                  the number of UPUE VMs, for 296-D only 1 is supported.
* number_of_cpue_nodes:                  the number of CPUE VMs, for 296-D only 1 is supported.
* number_of_uvm_nodes:                   the number of UVM VMs, for 296-D and 296-A, set number_of_uvm_nodes to 0.
* cloudplatform                          the openstack platform, osp for 296.
* vnf_layout                             value should be (vnf_layout: basic) or (vnf_layout: redundant), however, value as redundant should be used for feautre 300 feature and not be released now. please consider the risk if you insist on use value as redundant
*f1om_ip_cpcl_a: [ ]                     should not be used in layout as basic
*f1om_ip_cpnb_a: [ ]                     should not be used in layout as basic
*f1om_ip_cpif_a: [ ]                     should not be used in layout as basic
*f1om_ip_upue_a: [ ]                     should not be used in layout as basic
*f1om_ip_cpue_a: [ ]                     should not be used in layout as basic
*fronthaul_ip_cpif_a: [ ]                should not be used in layout as basic
*fronthaul_ip_upue_a: [ ]                should not be used in layout as basic
*fronthaul_ip_oam_a: [ ]                 should not be used in layout as basic
*backhaul_ip_cpif_a: [ ]                 should not be used in layout as basic
*backhaul_ip_upue_a: [ ]                 should not be used in layout as basic
*f1om_ip_cpcl_b: []                      should not be used in layout as basic
*f1om_ip_cpnb_b: []                      should not be used in layout as basic
*f1om_ip_cpif_b: []                      should not be used in layout as basic
*f1om_ip_upue_b: []                      should not be used in layout as basic
*f1om_ip_cpue_b: []                      should not be used in layout as basic
*fronthaul_ip_cpif_b: []                 should not be used in layout as basic
*fronthaul_ip_upue_b: []                 should not be used in layout as basic
*fronthaul_ip_oam_b: []                  should not be used in layout as basic
*backhaul_ip_cpif_b: []                  should not be used in layout as basic
*backhaul_ip_upue_b: []                  should not be used in layout as basic

### login to oam
chmod 0600 <keypair-file>
ssh -i <keypair-file> _nokrcpautoremoteuser@oam_ip

### Internal functionality (no official support)
### robot account
The robot account is not created by default. If you still want to using this account, please using the parameter extra_cloud_config_data.
Add below content in your 5gbts_heat.env file, then create the heat with this env file will create the testing robot account with the specified password.

parameters:
  extra_cloud_config_data:
    system_info:
      default_user:
        name: robot
    users:
    - default
    - name: robot
      gecos: Robot user for test automation purposes
      primary-group: root
      lock_passwd: false
      plain_text_passwd: 'rastre1'
      home: /home/robot
      shell: /bin/bash
      sudo:
      - ALL=(ALL) NOPASSWD:ALL
    write_files:
    - content: |
        robot
      path: /etc/opt/nokia/setupsshkey.d/testusers
      permissions: '0644'

