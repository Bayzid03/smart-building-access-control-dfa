# app.py - Gradio UI for Smart Building Access Control System

import gradio as gr
from dfa import AccessControlDFA
from zones import ZoneConfig

# Initialize the system
dfa = AccessControlDFA()
config = ZoneConfig()

def format_zone_policies():
    """Format zone policies for display"""
    policies_text = "🏢 **ZONE ACCESS POLICIES**\n\n"
    for zone, policy in config.zone_policies.items():
        zone_name = zone.replace('_', ' ')
        policy_names = [config.get_auth_name(symbol) for symbol in policy]
        policies_text += f"**{zone_name}:**\n"
        policies_text += f"  • Sequence: {' → '.join(policy_names)}\n"
        policies_text += f"  • Symbols: {' → '.join(policy)}\n\n"
    return policies_text

def format_auth_methods():
    """Format authentication methods for display"""
    methods_text = "🔐 **AUTHENTICATION METHODS**\n\n"
    for symbol, name in config.auth_symbols.items():
        methods_text += f"**{symbol}** - {name}\n"
    return methods_text

def process_authentication(zone, sequence_input):
    """Process authentication sequence and return results"""
    if not zone:
        return "❌ Please select a zone first!", "", "DENIED"
    
    if not sequence_input.strip():
        return "❌ Please enter an authentication sequence!", "", "DENIED"
    
    # Parse input sequence
    sequence = sequence_input.strip().upper().split()
    
    # Get expected policy for the zone
    zone_key = zone.upper().replace(' ', '_')
    expected_policy = config.get_policy(zone_key)
    
    if not expected_policy:
        return f"❌ Invalid zone: {zone}", "", "DENIED"
    
    # Process the sequence
    results = dfa.process_sequence(sequence, zone_key)
    
    # Format results
    result_text = f"🎯 **AUTHENTICATION FOR {zone}**\n\n"
    result_text += f"**Expected Sequence:** {' → '.join([config.get_auth_name(s) for s in expected_policy])}\n"
    result_text += f"**Your Input:** {' '.join(sequence)}\n\n"
    result_text += "**Processing Steps:**\n"
    
    for result in results:
        status_emoji = "✅" if result['state'] not in ['REJECTED'] else "❌"
        result_text += f"{status_emoji} Step {result['step']}: {result['input']} → {result['state']}\n"
        result_text += f"   {result['message']}\n\n"
    
    # Final result
    if dfa.is_accepted():
        final_result = "✅ **ACCESS GRANTED**"
        status = "GRANTED"
        result_color = "success"
    else:
        final_result = "❌ **ACCESS DENIED**" 
        status = "DENIED"
        result_color = "error"
    
    return result_text, final_result, status

def run_test_cases():
    """Run predefined test cases and return results"""
    test_cases = [
        ("Valid MAIN_ENTRANCE", "MAIN_ENTRANCE", "C P F V", "GRANTED"),
        ("Valid IT_INFRASTRUCTURE", "IT_INFRASTRUCTURE", "P R A F", "GRANTED"),
        ("Valid TECH_LAB", "TECH_LAB", "F C P X", "GRANTED"),
        ("Valid BOARDROOM", "BOARDROOM", "R K V A", "GRANTED"),
        ("Valid INNOVATION_HUB", "INNOVATION_HUB", "V A C K", "GRANTED"),
        ("Valid CONTROL_CENTER", "CONTROL_CENTER", "A X R P", "GRANTED"),
        ("Valid CLOUD_FACILITY", "CLOUD_FACILITY", "K F X R", "GRANTED"),
        ("Valid CONFERENCE_HALL", "CONFERENCE_HALL", "X V P F", "GRANTED"),
        ("Wrong first step", "MAIN_ENTRANCE", "P P F V", "DENIED"),
        ("Out of order", "MAIN_ENTRANCE", "C F P V", "DENIED"),
        ("Invalid symbol", "MAIN_ENTRANCE", "C P X V", "DENIED"),
        ("Extra input after valid", "MAIN_ENTRANCE", "C P F V A", "DENIED"),
        ("Incomplete sequence", "MAIN_ENTRANCE", "C P", "DENIED"),
        
    ]
    
    results_text = "🧪 **TEST CASES RESULTS**\n\n"
    
    for i, (name, zone, sequence, expected) in enumerate(test_cases, 1):
        _, _, actual = process_authentication(zone, sequence)
        pass_fail = "✅ PASS" if actual == expected else "❌ FAIL"
        
        results_text += f"**Test {i}: {name}**\n"
        results_text += f"Zone: {zone} | Sequence: {sequence}\n"
        results_text += f"Expected: {expected} | Actual: {actual} | {pass_fail}\n\n"
    
    return results_text

def create_demo():
    """Create Gradio interface"""
    
    # Custom CSS for better styling
    custom_css = """
    .gradio-container {
        max-width: 1200px !important;
    }
    .status-granted {
        background-color: #d4edda !important;
        color: #155724 !important;
        border: 1px solid #c3e6cb !important;
        padding: 10px !important;
        border-radius: 5px !important;
        font-weight: bold !important;
    }
    .status-denied {
        background-color: #f8d7da !important;
        color: #721c24 !important;
        border: 1px solid #f5c6cb !important;
        padding: 10px !important;
        border-radius: 5px !important;
        font-weight: bold !important;
    }
    """
    
    with gr.Blocks(css=custom_css, title="Smart Building Access Control") as demo:
        
        gr.Markdown("""
        # 🏢 Smart Building Access Control System
        ### DFA-Based Authentication System
        
        This system uses **Deterministic Finite Automaton (DFA)** to control access to different zones in a smart building.
        Each zone requires a specific sequence of authentication methods.
        """)
        
        with gr.Tabs():
            
            # Main Authentication Tab
            with gr.TabItem("🔐 Authentication"):
                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### Select Zone and Enter Sequence")
                        
                        zone_dropdown = gr.Dropdown(
                            choices=[zone.replace('_', ' ') for zone in config.get_zones()],
                            label="🏢 Select Zone"
                        )
                        
                        sequence_input = gr.Textbox(
                            label="🔑 Authentication Sequence",
                            placeholder="Enter symbols separated by spaces (e.g., C P F V)",
                            info="Use symbols like C (Card), P (PIN), F (Fingerprint), etc."
                        )
                        
                        with gr.Row():
                            auth_button = gr.Button("🚀 Authenticate", variant="primary")
                            clear_button = gr.Button("🗑️ Clear", variant="secondary")
                    
                    with gr.Column(scale=2):
                        result_display = gr.Markdown(label="📋 Authentication Results")
                        status_display = gr.Markdown(label="🎯 Final Status")
                
                # Hidden output for status
                status_output = gr.Textbox(visible=False)
                
                # Event handlers
                auth_button.click(
                    fn=process_authentication,
                    inputs=[zone_dropdown, sequence_input],
                    outputs=[result_display, status_display, status_output]
                )
                
                clear_button.click(
                    fn=lambda: ("", "", "", ""),
                    outputs=[sequence_input, result_display, status_display, status_output]
                )
            
            # Zone Policies Tab
            with gr.TabItem("📋 Zone Policies"):
                gr.Markdown(format_zone_policies())
            
            # Authentication Methods Tab  
            with gr.TabItem("🔐 Authentication Methods"):
                gr.Markdown(format_auth_methods())
            
            # Test Cases Tab
            with gr.TabItem("🧪 Test Cases"):
                gr.Markdown("### Run Predefined Test Cases")
                gr.Markdown("Click the button below to run comprehensive test cases and see the results.")
                
                test_button = gr.Button("▶️ Run All Tests", variant="primary")
                test_results = gr.Markdown()
                
                test_button.click(
                    fn=run_test_cases,
                    outputs=test_results
                )
            
            # Help & Instructions Tab
            with gr.TabItem("❓ Help"):
                gr.Markdown("""
                ## How to Use This System
                
                ### 🏢 **Zone Selection**
                1. Choose a zone from the dropdown menu
                2. Each zone has a unique 4-step authentication sequence
                
                ### 🔑 **Authentication Sequence**
                1. Enter symbols separated by spaces
                2. Symbols must be entered in the exact order
                3. Available symbols:
                   - **C** = Card Swipe
                   - **P** = PIN Entry  
                   - **F** = Fingerprint
                   - **R** = Retina Scan
                   - **V** = Voice Recognition
                   - **X** = Face Recognition
                   - **A** = Admin Override
                   - **K** = Keypad Entry
                
                ### ✅ **Example Usage**
                - **Zone:** MAIN_ENTRANCE
                - **Sequence:** C P F V
                - **Result:** Access Granted ✅
                
                ### ❌ **Common Errors**
                - Wrong symbol order → Access Denied
                - Invalid symbols → Access Denied  
                - Incomplete sequence → Access Denied
                - Extra symbols → Access Denied
                
                ### 🔧 **Technical Details**
                This system implements a **Deterministic Finite Automaton (DFA)** where:
                - Each input symbol leads to exactly one next state
                - Invalid transitions immediately lead to rejection
                - Only complete, correct sequences grant access
                """)
        
        gr.Markdown("""
        ---
        **Theory of Computation Project** | **DFA-Based Access Control System**  
        *Built with Python & Gradio*
        """)
    
    return demo

def find_available_port(start_port=7860, max_attempts=10):
    import socket
    port = start_port
    for _ in range(max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            port += 1
    return None

def main():
    """Launch the Gradio app"""
    demo = create_demo()
    port = find_available_port(7860)
    if port is None:
        print("Error: Could not find an available port. Please close other applications using ports 7860-7870 and try again.")
        return
        
    print(f"\nApplication starting on http://localhost:{port}")
    demo.launch(
        share=False,  # Disable public link
        server_name="localhost",  # Use localhost for local development
        server_port=port,
        show_error=True
    )

if __name__ == "__main__":
    main()
