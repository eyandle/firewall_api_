

class IPClassifier:

    def find_zone(self, ip):
        if self.is_ip_trusted(ip):
            return 'inside'
        elif self.is_ip_dmz(ip):
            return 'dmz'
        else:
            return 'outside'

    @staticmethod
    def is_ip_trusted(ip):
        return str(ip).startswith('192.168.0.')

    @staticmethod
    def is_ip_dmz(ip):
        return str(ip).startswith('192.168.1.')