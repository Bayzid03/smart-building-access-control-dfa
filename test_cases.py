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
            'name': 'LOBBY - Valid Sequence',
            'sequence': ['C', 'P', 'F', 'V'],
            'zone': 'LOBBY',
            'expected': 'ACCEPTED',
            'description': 'Correct sequence for LOBBY access'
        },
        {
            'name': 'SERVER_ROOM - Valid Sequence', 
            'sequence': ['C', 'P', 'R', 'A'],
            'zone': 'SERVER_ROOM',
            'expected': 'ACCEPTED',
            'description': 'Correct sequence for SERVER_ROOM access'
        },
        {
            'name': 'LABORATORY - Valid Sequence',
            'sequence': ['C', 'P', 'F', 'Fc'],
            'zone': 'LABORATORY', 
            'expected': 'ACCEPTED',
            'description': 'Correct sequence for LABORATORY access'
        },
        
        # Invalid sequences
        {
            'name': 'Wrong First Symbol',
            'sequence': ['P', 'P', 'F', 'V'],
            'zone': 'LOBBY',
            'expected': 'REJECTED',
            'description': 'Starting with wrong authentication method'
        },
        {
            'name': 'Out of Order Sequence',
            'sequence': ['C', 'F', 'P', 'V'],
            'zone': 'LOBBY',
            'expected': 'REJECTED',
            'description': 'Correct symbols but wrong order'
        },
        {
            'name': 'Partially Correct Then Wrong',
            'sequence': ['C', 'P', 'R', 'V'],
            'zone': 'LOBBY',
            'expected': 'REJECTED',
            'description': 'First two steps correct, then wrong symbol'
        },
        {
            'name': 'Extra Input After Valid',
            'sequence': ['C', 'P', 'F', 'V', 'A'],
            'zone': 'LOBBY',
            'expected': 'REJECTED',
            'description': 'Valid sequence with extra symbol'
        },
        {
            'name': 'Invalid Symbol',
            'sequence': ['C', 'P', 'X', 'V'],
            'zone': 'LOBBY',
            'expected': 'REJECTED',
            'description': 'Contains invalid authentication symbol'
        },
        {
            'name': 'Incomplete Sequence',
            'sequence': ['C', 'P', 'F'],
            'zone': 'LOBBY',
            'expected': 'REJECTED',
            'description': 'Sequence too short - missing final step'
        },
        {
            'name': 'Wrong Zone Policy',
            'sequence': ['C', 'P', 'R', 'A'],
            'zone': 'LOBBY',
            'expected': 'REJECTED',
            'description': 'Using SERVER_ROOM sequence for LOBBY'
        },
        
        # Edge cases
        {
            'name': 'Empty Sequence',
            'sequence': [],
            'zone': 'LOBBY',
            'expected': 'REJECTED',
            'description': 'No authentication attempts'
        },
        {
            'name': 'Single Symbol',
            'sequence': ['C'],
            'zone': 'LABORATORY',
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
