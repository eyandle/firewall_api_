from pydantic import BaseModel, validator
from typing import List, Optional
import re
from ipaddress import IPv4Network, IPv4Address
from IPClassifier import IPClassifier
from random import randint

CIDR_REG_EX = '^([0-9]{1,3}.){3}[0-9]{1,3}($|/(16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31|32))$'
PORT_REG_EX = '^(TCP|UDP|ICMP)/[0-9]{1,5}$'
ip_classifier = IPClassifier()


class FirewallRule(BaseModel):
    source: str
    destination: str
    port: str
    application: str

    @validator('source')
    def validate_source(cls, value):
        if not re.match(CIDR_REG_EX, value):
            raise ValueError('Invalid Source CIDR Address')

        return value

    @validator('destination')
    def validate_destination(cls, value):
        if not re.match(CIDR_REG_EX, value):
            raise ValueError('Invalid Destination CIDR Address')

        return value

    @validator('port')
    def validate_port(cls, value):
        if not re.match(PORT_REG_EX, value):
            raise ValueError('Invalid Port Combination')

        return value

    @validator('application')
    def validate_application(cls, value):
        return value

    @property
    def source_netmask(self):
        return IPv4Network(self.source, strict=False).netmask

    @property
    def destination_netmask(self):
        return IPv4Network(self.destination, strict=False).netmask

    @property
    def protocol(self):
        return self.port.split('/')[0]

    @property
    def port_number(self):
        return self.port.split('/')[1]

    @property
    def source_zone(self):
        return ip_classifier.find_zone(self.source)

    @property
    def destination_zone(self):
        return ip_classifier.find_zone(self.destination)

    @property
    def source_network_address(self):
        return IPv4Network(self.source, strict=False).network_address

    @property
    def destination_network_address(self):
        return IPv4Network(self.destination, strict=False).network_address


class FirewallRequestModel(BaseModel):
    businessCase: str
    firewallRules: List[FirewallRule]
    ticket: Optional[int]

    def __init__(self, **kwargs):

        BaseModel.__init__(self, **kwargs)
        self.ticket = randint(100000, 9999999)



