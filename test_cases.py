# test_cases.py - Comprehensive Test Cases for DFA Access Control

from dfa import AccessControlDFA
from zones import ZoneConfig

def run_comprehensive_tests():
    """Run comprehensive test suite"""
    dfa = AccessControlDFA()
    config = ZoneConfig()
    
    # Comprehensive test cases
    test_cases = [
        # Valid sequences for each zone
        {
            'name': 'MAIN_ENTRANCE - Valid Sequence',
            'sequence': ['C', 'P', 'F', 'V'],
            'zone': 'MAIN_ENTRANCE',
            'expected': 'ACCEPTED',
            'description': 'Correct sequence for MAIN_ENTRANCE access'
        },
        {
            'name': 'IT_INFRASTRUCTURE - Valid Sequence', 
            'sequence': ['P', 'R', 'A', 'F'],
            'zone': 'IT_INFRASTRUCTURE',
            'expected': 'ACCEPTED',
            'description': 'Correct sequence for IT_INFRASTRUCTURE access'
        },
        {
            'name': 'TECH_LAB - Valid Sequence',
            'sequence': ['F', 'C', 'P', 'X'],
            'zone': 'TECH_LAB', 
            'expected': 'ACCEPTED',
            'description': 'Correct sequence for TECH_LAB access'
        },
        
        # Invalid sequences
        {
            'name': 'Wrong First Symbol',
            'sequence': ['P', 'P', 'R', 'A'],
            'zone': 'MAIN_ENTRANCE',
            'expected': 'REJECTED',
            'description': 'Starting with wrong authentication method'
        },
        {
            'name': 'Out of Order Sequence',
            'sequence': ['P', 'R', 'A', 'F'],
            'zone': 'MAIN_ENTRANCE',
            'expected': 'REJECTED',
            'description': 'Correct symbols but wrong order'
        },
        {
            'name': 'Partially Correct Then Wrong',
            'sequence': ['F', 'C', 'P', 'R', 'A'],
            'zone': 'MAIN_ENTRANCE',
            'expected': 'REJECTED',
            'description': 'First two steps correct, then wrong symbol'
        },
        {
            'name': 'Extra Input After Valid',
            'sequence': ['F', 'C', 'P', 'R', 'A', 'F'],
            'zone': 'MAIN_ENTRANCE',
            'expected': 'REJECTED',
            'description': 'Valid sequence with extra symbol'
        },
        {
            'name': 'Invalid Symbol',
            'sequence': ['F', 'C', 'P', 'X'],
            'zone': 'MAIN_ENTRANCE',
            'expected': 'REJECTED',
            'description': 'Contains invalid authentication symbol'
        },
        {
            'name': 'Incomplete Sequence',
            'sequence': ['F', 'C', 'P'],
            'zone': 'MAIN_ENTRANCE',
            'expected': 'REJECTED',
            'description': 'Sequence too short - missing final step'
        },
        {
            'name': 'Wrong Zone Policy',
            'sequence': ['P', 'R', 'A', 'F'],
            'zone': 'MAIN_ENTRANCE',
            'expected': 'REJECTED',
            'description': 'Using IT_INFRASTRUCTURE sequence for MAIN_ENTRANCE'
        },
        
        # Edge cases
        {
            'name': 'Empty Sequence',
            'sequence': [],
            'zone': 'MAIN_ENTRANCE',
            'expected': 'REJECTED',
            'description': 'No authentication attempts'
        },
        {
            'name': 'Single Symbol',
            'sequence': ['F'],
            'zone': 'MAIN_ENTRANCE',
            'expected': 'REJECTED',
            'description': 'Only first authentication step'
        }
    ]
    
    print("COMPREHENSIVE DFA ACCESS CONTROL TEST SUITE")
    print("="*70)
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['name']}")
        print("-" * 50)
        print(f"Description: {test['description']}")
        print(f"Zone: {test['zone']}")
        print(f"Sequence: {test['sequence']}")
        print(f"Expected: {test['expected']}")
        
        # Run the test
        results = dfa.process_sequence(test['sequence'], test['zone'])
        actual = 'ACCEPTED' if dfa.is_accepted() else 'REJECTED'
        
        print(f"Actual: {actual}")
        
        # Show processing steps
        if results:
            print("Processing Steps:")
            for result in results:
                print(f"  Step {result['step']}: {result['input']} → {result['state']}")
                print(f"    {result['message']}")
        
        # Determine pass/fail
        if actual == test['expected']:
            print("✅ PASS")
            passed += 1
        else:
            print("❌ FAIL")
            failed += 1
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("-" * 20)
    print(f"Total Tests: {len(test_cases)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/len(test_cases)*100):.1f}%")
    
    return passed, failed

def generate_test_table():
    """Generate test results table for documentation"""
    dfa = AccessControlDFA()
    
    test_cases = [
        ("Valid MAIN_ENTRANCE sequence", ['C', 'P', 'F', 'V'], 'MAIN_ENTRANCE', 'ACCEPTED'),
        ("Valid IT_INFRASTRUCTURE sequence", ['P', 'R', 'A', 'F'], 'IT_INFRASTRUCTURE', 'ACCEPTED'), 
        ("Wrong first symbol", ['P', 'P', 'R', 'A'], 'MAIN_ENTRANCE', 'REJECTED'),
        ("Out of order sequence", ['P', 'R', 'A', 'F'], 'MAIN_ENTRANCE', 'REJECTED'),
        ("Invalid symbol in sequence", ['C', 'P', 'X', 'V'], 'MAIN_ENTRANCE', 'REJECTED')
    ]
    
    print("\nTEST RESULTS TABLE FOR DOCUMENTATION")
    print("="*90)
    print(f"{'Test Case':<35} {'Expected':<12} {'Actual':<12} {'Pass/Fail':<12}")
    print("-"*90)
    
    for description, sequence, zone, expected in test_cases:
        results = dfa.process_sequence(sequence, zone)
        actual = 'ACCEPTED' if dfa.is_accepted() else 'REJECTED'
        pass_fail = 'PASS' if actual == expected else 'FAIL'
        
        print(f"{description:<35} {expected:<12} {actual:<12} {pass_fail:<12}")
    
    print("-"*90)

if __name__ == "__main__":
    # Run comprehensive tests
    run_comprehensive_tests()
    
    # Generate documentation table
    generate_test_table()
