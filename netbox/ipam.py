import ipaddress
from netbox import exceptions

class Ipam(object):

    def __init__(self, netbox_con):

        self.netbox_con = netbox_con

    def get_ip_addresses(self, **kwargs):
        """Return all ip addresses"""
        return self.netbox_con.get('/ipam/ip-addresses/', **kwargs)

    def get_ip(self, **kwargs):
        """Return query results"""
        return self.netbox_con.get('/ipam/ip-addresses/', **kwargs)

    def get_ip_by_device(self, device_name):
        """Get IPs which are associated to a device

        :param device_name: Name of the device
        :return: ip address information
        """
        return self.netbox_con.get('/ipam/ip-addresses', device_name=device_name)

    def create_ip_address(self, address, **kwargs):
        """Create a new ip address

        :param address: IP address
        :param kwargs: Optional arguments
        :return: bool True if successful otherwise raise CreateException
        """
        required_fields = {"address": address}
        return self.netbox_con.post('/ipam/ip-addresses/', required_fields, **kwargs)

    def update_ip(self, ip_address, **kwargs):
        """Update ip address

        :param ip_address: ip address with prefix. Format: 1.1.1.1/32
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        ip_id = self.get_ip(q=ip_address)[0]['id']
        return self.netbox_con.patch('/ipam/ip-addresses/', ip_id, **kwargs)

    def delete_ip_address(self, address):
        """Delete IP address

        :param address: IP address to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        ip_address_id = self.get_ip(q=address)[0]['id']
        return self.netbox_con.delete('/ipam/ip-addresses/', ip_address_id)

    def get_ip_prefixes(self, **kwargs):
        """Return all ip prefixes"""
        return self.netbox_con.get('/ipam/prefixes/', **kwargs)

    def get_ip_prefix(self, **kwargs):
        """Get prefix based on filter values

        :param kwargs: filter values
        :return: prefix
        """
        return self.netbox_con.get('/ipam/prefixes/', **kwargs)

    def create_ip_prefix(self, prefix, **kwargs):
        """Create a new ip prefix

        :param prefix: A valid ip prefix format. The syntax will be checked with the ipaddress module
        :param kwargs: Optional arguments
        :return: bool True if successful otherwise raise CreateException
        """
        required_fields = {"prefix": prefix}

        if ipaddress.ip_network(prefix, strict=True):
            return self.netbox_con.post('/ipam/prefixes/', required_fields, **kwargs)

    def delete_ip_prefix(self, **kwargs):
        """Delete IP prefix

        :param kwargs: Delete prefix based on filter values
        :return: bool True if successful otherwise raise DeleteException
        """
        ip_prefix_id = self.get_ip_prefix(**kwargs)[0]['id']
        return self.netbox_con.delete('/ipam/prefixes/', ip_prefix_id)

    def update_ip_prefix(self, ip_prefix, **kwargs):
        """Update ip address

        :param ip_prefix: ip prefix to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        ip_prefix_id = self.get_ip_prefix(q=ip_prefix)[0]['id']
        return self.netbox_con.patch('/ipam/prefixes/', ip_prefix_id, **kwargs)

    def get_next_available_ip(self, **kwargs):
        """Return next available ip in prefix

        :param kwargs: filter for prefix
        :return: next available ip
        """
        prefix_id =  self.get_ip_prefix(**kwargs)[0]['id']
        param = '/ipam/prefixes/{}/available-ips/'.format(prefix_id)
        return self.netbox_con.get(param, limit=1)[0]['address']

    def get_vrfs(self, **kwargs):
        """Get all vrfs"""
        return self.netbox_con.get('/ipam/vrfs/', **kwargs)

    def get_vrf(self, **kwargs):
        """Get vrf based on filter values

        :param kwargs: Filter values
        :return: vrf
        """
        return self.netbox_con.get('/ipam/vrfs/', **kwargs)

    def create_vrf(self, name, rd, **kwargs):
        """Create a new vrf

        :param name: Name of the vrf
        :param rd: Route distinguisher in any format
        :param kwargs: Optional arguments
        :return: bool True if successful otherwise raise CreateException
        """
        required_fields = {"name": name, "rd": rd}
        return self.netbox_con.post('/ipam/vrfs/', required_fields, **kwargs)

    def delete_vrf(self, vrf):
        """Delete vrf

        :param vrf: Name of vrf to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        vrf_id = self.get_vrf(name=vrf)[0]['id']
        return self.netbox_con.delete('/ipam/vrfs/', vrf_id)

    def update_vrf(self, vrf_name, **kwargs):
        """Update vrf

        :param vrf_name: name of the vrf to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        vrf_id = self.get_vrf(name=vrf_name)[0]['id']
        return self.netbox_con.patch('/ipam/vrfs/', vrf_id, **kwargs)

    def get_aggregates(self, **kwargs):
        """Return all aggregates"""
        return self.netbox_con.get('/ipam/aggregates/', **kwargs)

    def get_aggregate(self, **kwargs):
        """Return aggregate

        :param kwargs: arguments
        :return: aggregate
        """

    def create_aggregate(self, prefix, rir, **kwargs):
        """Creates a new aggregate

        :param prefix: IP Prefix
        :param rir: Name of the RIR
        :param kwargs: Optional Arguments
        :return:
        """
        rir_id = self.get_rir(name=rir)[0]['id']
        required_fields = {"prefix": prefix, "rir": rir_id}

        if ipaddress.ip_network(prefix, strict=True):
            return self.netbox_con.post('/ipam/aggregates/', required_fields, **kwargs)

    def update_aggregate(self, prefix, **kwargs):
        """Update aggregate

        :param prefix: Prefix of the aggregate
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        aggregate_id = self.get_aggregate(prefix=prefix)[0]['id']
        return self.netbox_con.patch('/ipam/aggregates/', aggregate_id, **kwargs)

    def get_rirs(self, **kwargs):
        """Return all rirs"""
        return self.netbox_con.get('/ipam/rirs/', **kwargs)

    def get_rir(self, **kwargs):
        """Get rir based on filter values

        :param kwargs: Filter values
        :return: rir
        """
        return self.netbox_con.get('/ipam/rirs', **kwargs)

    def create_rir(self, name, slug):
        """Create new rir

        :param name: Name of the rir
        :param slug: Name of the slug
        :return: bool True if successful otherwise raise CreateException
        """
        required_fields = {"name": name, "slug": slug}
        return self.netbox_con.post('/ipam/rirs/', required_fields)

    def delete_rir(self, rir_name):
        """Delete rir

        :param rir_name: rir name to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        rir_id = self.get_rir(name=rir_name)[0]['id']
        return self.netbox_con.delete('/ipam/rirs/', rir_id)

    def update_rir(self, name, **kwargs):
        """Update rir

        :param name: Name of the rir
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        rir_id = self.get_rir(name=name)[0]['id']
        return self.netbox_con.patch('/ipam/rirs/', rir_id, **kwargs)

    def get_prefix_roles(self, **kwargs):
        """Return all roles"""
        return self.netbox_con.get('/ipam/roles/', **kwargs)

    def get_prefix_role(self, **kwargs):
        """Return prefix role based on filter

        :param kwargs: filter options
        :return: prefix role
        """
        return self.netbox_con.get('/ipam/roles/', **kwargs)

    def create_prefix_role(self, name, slug):
        """Create new prefix role

        :param name: Name of the prefix role
        :param slug: Name of the slug
        :return: bool True if successful otherwise raise CreateException
        """
        required_fields = {"name": name, "slug": slug}
        return self.netbox_con.post('/ipam/roles/', required_fields)

    def delete_prefix_role(self, prefix_role):
        """Delete prefix role

        :param prefix_role: prefix role to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        prefix_role_id = self.get_prefix_role(name=prefix_role)[0]['id']
        return self.netbox_con.delete('/ipam/role/', prefix_role_id)

    def update_prefix_role(self, name, **kwargs):
        """Update prefix role

        :param name: Name of the prefix role
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        prefix_role_id = self.get_prefix_role(name=name)[0]['id']
        return self.netbox_con.patch('/ipam/roles/', prefix_role_id, **kwargs)

    def get_vlans(self, **kwargs):
        """Return all vlans"""
        return self.netbox_con.get('/ipam/vlans/', **kwargs)

    def get_vlan(self, **kwargs):
        """Get vlan by filter

        :param kwargs: Filter values
        :return: vlan
        """
        return self.netbox_con.get('/ipam/vlans/', **kwargs)

    def create_vlan(self, vid, vlan_name):
        """Create new vlan

        :param vid: ID of the new vlan
        :param vlan_name: Name of the vlan
        :return: bool True if successful otherwise raise CreateException
        """
        required_fields = {"vid": vid, "name": vlan_name}
        return self.netbox_con.post('/ipam/vlans/', required_fields)

    def delete_vlan(self, vid):
        """Delete VLAN based on VLAN ID

        :param vid: vlan id to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        vid_id = self.get_vlan(vid=vid)[0]['id']
        return self.netbox_con.delete('/ipam/vlans/', vid_id)

    def update_vlan(self, name, **kwargs):
        """Update vlan

        :param name: Name of the vlan
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        vlan_id = self.get_vlan(name=name)[0]['id']
        return self.netbox_con.patch('/ipam/vlans/', vlan_id, **kwargs)


