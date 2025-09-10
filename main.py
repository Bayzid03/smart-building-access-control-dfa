# main.py - Main Access Control System

from dfa import AccessControlDFA
from zones import ZoneConfig

def display_menu():
    """Display main menu"""
    print("\n" + "="*50)
    print("SMART BUILDING ACCESS CONTROL SYSTEM")
    print("="*50)
    print("1. View Available Zones")
    print("2. View Authentication Methods") 
    print("3. Test Authentication Sequence")
    print("4. Run Predefined Test Cases")
    print("5. Show Zone Policies")
    print("6. Exit")
    print("-"*50)

def display_zones(config):
    """Display all available zones"""
    print("\nAvailable Zones:")
    zones = config.get_zones()
    for i, zone in enumerate(zones, 1):
        print(f"{i}. {zone.replace('_', ' ')}")

def display_auth_methods(config):
    """Display authentication methods"""
    print("\nAuthentication Methods:")
    for symbol, name in config.auth_symbols.items():
        print(f"  {symbol} - {name}")

def display_zone_policies(config):
    """Display access policies for all zones"""
    print("\nZone Access Policies:")
    print("-" * 60)
    for zone, policy in config.zone_policies.items():
        policy_names = [config.get_auth_name(symbol) for symbol in policy]
        print(f"{zone.replace('_', ' '):<15}: {' → '.join(policy_names)}")
        print(f"{'Sequence':<15}: {' → '.join(policy)}")
        print()

def test_authentication():
    """Interactive authentication testing"""
    dfa = AccessControlDFA()
    config = ZoneConfig()
    
    print("\nInteractive Authentication Test")
    print("-" * 40)
    
    # Show available zones
    display_zones(config)
    
    try:
        zone_choice = int(input("\nSelect zone (enter number): ")) - 1
        zones = config.get_zones()
        
        if 0 <= zone_choice < len(zones):
            selected_zone = zones[zone_choice]
            policy = config.get_policy(selected_zone)
            
            print(f"\nSelected Zone: {selected_zone.replace('_', ' ')}")
            print(f"Required Sequence: {' → '.join([config.get_auth_name(s) for s in policy])}")
            print(f"Symbol Sequence: {' → '.join(policy)}")
            
            # Get authentication sequence from user
            print(f"\nEnter authentication sequence (space-separated symbols):")
            print("Available symbols:", ', '.join(config.auth_symbols.keys()))
            
            sequence_input = input("Authentication sequence: ").strip().split()
            
            # Process the sequence
            print(f"\nProcessing authentication for {selected_zone}...")
            print("-" * 40)
            
            results = dfa.process_sequence(sequence_input, selected_zone)
            
            for result in results:
                print(f"Step {result['step']}: {result['input']} → {result['state']}")
                print(f"  Message: {result['message']}")
            
            # Final result
            if dfa.is_accepted():
                print(f"\n✅ FINAL RESULT: ACCESS GRANTED TO {selected_zone}")
            else:
                print(f"\n❌ FINAL RESULT: ACCESS DENIED")
                
        else:
            print("Invalid zone selection!")
            
    except (ValueError, IndexError):
        print("Invalid input!")

def run_test_cases():
    """Run predefined test cases"""
    dfa = AccessControlDFA()
    config = ZoneConfig()
    
    # Test cases: (description, sequence, zone, expected_result)
    test_cases = [
        ("Correct LOBBY sequence", ['C', 'P', 'F', 'V'], 'LOBBY', 'ACCEPTED'),
        ("Correct SERVER_ROOM sequence", ['C', 'P', 'R', 'A'], 'SERVER_ROOM', 'ACCEPTED'),
        ("Wrong first symbol", ['P', 'P', 'F', 'V'], 'LOBBY', 'REJECTED'),
        ("Partially correct then wrong", ['C', 'P', 'R', 'V'], 'LOBBY', 'REJECTED'),
        ("Too many symbols", ['C', 'P', 'F', 'V', 'A'], 'LOBBY', 'REJECTED'),
        ("Invalid symbol", ['C', 'P', 'X', 'V'], 'LOBBY', 'REJECTED'),
        ("Too short sequence", ['C', 'P', 'F'], 'LOBBY', 'REJECTED'),
        ("Wrong zone sequence", ['C', 'P', 'R', 'A'], 'LOBBY', 'REJECTED'),
    ]
    
    print("\nRunning Test Cases...")
    print("="*80)
    print(f"{'Test Case':<30} {'Expected':<12} {'Actual':<12} {'Pass/Fail':<10}")
    print("-"*80)
    
    for i, (description, sequence, zone, expected) in enumerate(test_cases, 1):
        results = dfa.process_sequence(sequence, zone)
        actual = 'ACCEPTED' if dfa.is_accepted() else 'REJECTED'
        pass_fail = 'PASS' if actual == expected else 'FAIL'
        
        print(f"{description:<30} {expected:<12} {actual:<12} {pass_fail:<10}")
        
        # Show details for failed tests
        if pass_fail == 'FAIL':
            print(f"  Sequence: {sequence}")
            print(f"  Zone: {zone}")
            print(f"  Last message: {results[-1]['message'] if results else 'No results'}")
    
    print("-"*80)

def main():
    """Main program loop"""
    config = ZoneConfig()
    
    while True:
        display_menu()
        
        try:
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                display_zones(config)
            elif choice == '2':
                display_auth_methods(config)
            elif choice == '3':
                test_authentication()
            elif choice == '4':
                run_test_cases()
            elif choice == '5':
                display_zone_policies(config)
            elif choice == '6':
                print("\nThank you for using Smart Building Access Control System!")
                break
            else:
                print("Invalid choice! Please select 1-6.")
                
        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()