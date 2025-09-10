# zones.py - Zone Configuration and Authentication Methods

class ZoneConfig:
    def __init__(self):
        # Authentication symbols
        self.auth_symbols = {
            'C': 'Card Swipe',
            'P': 'PIN Entry', 
            'F': 'Fingerprint',
            'R': 'Retina Scan',
            'V': 'Voice Recognition',
            'Fc': 'Face Recognition',
            'A': 'Admin Override',
            'K': 'Keypad Entry'
        }
        
        # Zone access policies (minimum 4 steps each)
        self.zone_policies = {
            'LOBBY': ['C', 'P', 'F', 'V'],           # Card → PIN → Fingerprint → Voice
            'SERVER_ROOM': ['C', 'P', 'R', 'A'],     # Card → PIN → Retina → Admin
            'LABORATORY': ['C', 'P', 'F', 'Fc'],     # Card → PIN → Fingerprint → Face
            'EXEC_LOUNGE': ['C', 'K', 'R', 'V'],     # Card → Keypad → Retina → Voice
            'RESEARCH_WING': ['C', 'P', 'R', 'Fc'],  # Card → PIN → Retina → Face
            'SECURITY_OFFICE': ['A', 'P', 'F', 'R'], # Admin → PIN → Fingerprint → Retina
            'DATA_CENTER': ['C', 'A', 'R', 'F'],     # Card → Admin → Retina → Fingerprint
            'MEETING_ROOM': ['C', 'P', 'V', 'Fc']    # Card → PIN → Voice → Face
        }
    
    def get_zones(self):
        return list(self.zone_policies.keys())
    
    def get_policy(self, zone):
        return self.zone_policies.get(zone, [])
    
    def get_auth_name(self, symbol):
        return self.auth_symbols.get(symbol, 'Unknown')