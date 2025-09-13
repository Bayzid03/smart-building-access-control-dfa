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
            'X': 'Face Recognition',
            'A': 'Admin Override',
            'K': 'Keypad Entry'
        }
        
        # Zone access policies - Each starts with UNIQUE symbol
        self.zone_policies = {
            'MAIN_ENTRANCE': ['C', 'P', 'F', 'V'],      # Card → PIN → Fingerprint → Voice
            'IT_INFRASTRUCTURE': ['P', 'R', 'A', 'F'],  # PIN → Retina → Admin → Fingerprint
            'TECH_LAB': ['F', 'C', 'P', 'X'],           # Fingerprint → Card → PIN → Face
            'BOARDROOM': ['R', 'K', 'V', 'A'],          # Retina → Keypad → Voice → Admin
            'INNOVATION_HUB': ['V', 'A', 'C', 'K'],     # Voice → Admin → Card → Keypad
            'CONTROL_CENTER': ['A', 'X', 'R', 'P'],     # Admin → Face → Retina → PIN
            'CLOUD_FACILITY': ['K', 'F', 'X', 'R'],     # Keypad → Fingerprint → Face → Retina
            'CONFERENCE_HALL': ['X', 'V', 'P', 'F']     # Face → Voice → PIN → Fingerprint
        }
    
    def get_zones(self):
        return list(self.zone_policies.keys())
    
    def get_policy(self, zone):
        return self.zone_policies.get(zone, [])
    
    def get_auth_name(self, symbol):
        return self.auth_symbols.get(symbol, 'Unknown')
