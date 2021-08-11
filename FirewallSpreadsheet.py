from openpyxl import load_workbook
from DataModels import FirewallRequestModel
from IPClassifier import IPClassifier
from random import choice
from datetime import datetime



class FirewallSpreadsheet:
    def __init__(self):
        self.workbook = load_workbook('bby_fw_change_template.xlsx')
        self.ip_classifier = IPClassifier()

    def parse_firewall_change(self, firewall_request: FirewallRequestModel):
        worksheet = self.workbook.get_sheet_by_name('Change Request')
        cisco_worksheet = self.workbook.get_sheet_by_name('Configuration - Cisco')
        juniper_worksheet = self.workbook.get_sheet_by_name('Configuration - Juniper')

        self._parse_in_ticket_details(firewall_request, worksheet)
        self._parse_in_firewall_rules(firewall_request, worksheet)
        self._parse_in_cisco_asa_config(firewall_request, cisco_worksheet)
        self._parse_in_juniper_config(firewall_request, juniper_worksheet)

        self.workbook.save('temp_fw_req.xlsx')

    def _parse_in_ticket_details(self, firewall_request: FirewallRequestModel, worksheet):
        worksheet['E4'].value = firewall_request.businessCase
        worksheet['B4'].value = firewall_request.ticket
        worksheet['B5'].value = datetime.now()
        worksheet['B6'].value = choice(['Approved', 'Pending', 'Rejected'])

    def _parse_in_firewall_rules(self, firewall_request: FirewallRequestModel, worksheet):
        row = 10

        for rule in firewall_request.firewallRules:
            worksheet[f'B{row}'].value = 'edge-fw-01'
            worksheet[f'C{row}'].value = f'{rule.source_zone}-inbound'
            worksheet[f'D{row}'].value = rule.source
            worksheet[f'E{row}'].value = rule.destination
            worksheet[f'F{row}'].value = rule.port
            worksheet[f'G{row}'].value = rule.application
            row += 1

    def _parse_in_cisco_asa_config(self, firewall_request, worksheet):
        row = 1
        for rule in firewall_request.firewallRules:
            worksheet[f'A{row}'].value = \
                f'access-list {self.ip_classifier.find_zone(rule.source)}-inbound ' \
                f'permit {rule.protocol} {rule.source_network_address} {rule.source_netmask}' \
                f' {rule.destination_network_address} {rule.destination_netmask} eq {rule.port_number}'

            row += 1
            worksheet[f'A{row}'].value = f'access-list {self.ip_classifier.find_zone(rule.source)}-inbound remark - See Ticket {firewall_request.ticket}'
            row += 1

    def _parse_in_juniper_config(self, firewall_request, worksheet):
        row = 1
        rule_count = 1
        for rule in firewall_request.firewallRules:
            prefix = f'set firewall filter {self.ip_classifier.find_zone(rule.source)}-inbound term {firewall_request.ticket}-{rule_count}'
            worksheet[f'A{row}'].value = f'{prefix} from source-address {rule.source}'
            row += 1
            worksheet[f'A{row}'].value = f'{prefix} from destination-address {rule.destination}'
            row += 1
            worksheet[f'A{row}'].value = f'{prefix} from destination-port {rule.protocol}'
            row += 1
            worksheet[f'A{row}'].value = f'{prefix} from destination-port {rule.port_number}'
            row += 1
            worksheet[f'A{row}'].value = f'{prefix} then accept'
            row += 1