# dfa.py - Deterministic Finite Automaton Implementation

from zones import ZoneConfig

class AccessControlDFA:
    def __init__(self):
        self.config = ZoneConfig()
        self.current_state = 'START'
        self.current_sequence = []
        self.target_zone = None
        
        # States: START, STEP_1, STEP_2, STEP_3, ACCEPTED, REJECTED
        self.states = ['START', 'STEP_1', 'STEP_2', 'STEP_3', 'ACCEPTED', 'REJECTED']
        self.final_states = ['ACCEPTED']
        self.reject_state = 'REJECTED'
    
    def reset(self):
        """Reset DFA to initial state"""
        self.current_state = 'START'
        self.current_sequence = []
        self.target_zone = None
    
    def transition(self, input_symbol, zone=None):
        """
        Process input symbol and transition to next state
        Returns: (new_state, message)
        """
        # Set target zone if provided at START
        if zone and self.current_state == 'START':
            if zone not in self.config.get_zones():
                return self._reject("Invalid zone specified")
            self.target_zone = zone
        
        # If no zone specified at start, reject immediately
        if not self.target_zone and self.current_state == 'START':
            return self._reject("No target zone specified")
        
        # If already accepted or rejected, ignore further inputs
        if self.current_state in ['REJECTED', 'ACCEPTED']:
            return self.current_state, "Process already completed. Reset required."
        
        # Validate input symbol against the 8-symbol alphabet
        if input_symbol not in self.config.auth_symbols:
            return self._reject(f"Invalid authentication symbol: {input_symbol}")
        
        # Get expected sequence for target zone
        expected_sequence = self.config.get_policy(self.target_zone)
        current_step = len(self.current_sequence)
        
        # Sequence too long? Reject.
        if current_step >= len(expected_sequence):
            return self._reject("Authentication sequence too long")
        
        # Check if current input matches expected symbol at this step
        expected_symbol = expected_sequence[current_step]
        if input_symbol != expected_symbol:
            expected_name = self.config.get_auth_name(expected_symbol)
            actual_name = self.config.get_auth_name(input_symbol)
            return self._reject(f"Wrong authentication method. Expected: {expected_name}, Got: {actual_name}")
        
        # Valid transition: record input and advance
        self.current_sequence.append(input_symbol)
        new_step = len(self.current_sequence)
        
        # If complete sequence → accept
        if new_step == len(expected_sequence):
            self.current_state = 'ACCEPTED'
            return 'ACCEPTED', f"Access GRANTED to {self.target_zone}"
        else:
            # Move to next step state
            self.current_state = f'STEP_{new_step}'
            next_expected = self.config.get_auth_name(expected_sequence[new_step])
            return self.current_state, f"Step {new_step} completed. Next: {next_expected}"
    
    def _reject(self, reason):
        """Helper method to reject and return error message"""
        self.current_state = 'REJECTED'
        return 'REJECTED', f"Access DENIED: {reason}"
    
    def is_accepted(self):
        """Check if current state is accepting"""
        return self.current_state == 'ACCEPTED'
    
    def is_rejected(self):
        """Check if current state is rejected"""
        return self.current_state == 'REJECTED'
    
    def get_current_state(self):
        """Get current state information"""
        return {
            'state': self.current_state,
            'sequence': self.current_sequence.copy(),
            'target_zone': self.target_zone
        }
    
    def process_sequence(self, sequence, zone):
        """Process complete authentication sequence"""
        self.reset()
        results = []
        
        for i, symbol in enumerate(sequence):
            if i == 0:
                state, message = self.transition(symbol, zone)
            else:
                state, message = self.transition(symbol)
            
            results.append({
                'step': i + 1,
                'input': symbol,
                'state': state,
                'message': message
            })
            
            # Stop processing if reached final state
            if state in ['REJECTED', 'ACCEPTED']:
                break
        
        return results
