import streamlit as st
import math
import re
import copy
import ast

# Set page configuration
st.set_page_config(
    page_title="Python Calculator",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for better styling - improved colors and layout
st.markdown("""
<style>
    .calculator-container {
        max-width: 320px;
        margin: 0 auto;
        background-color: #202020;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .display-area {
        background-color: #1C1C1E;
        color: white;
        border-radius: 5px;
        margin-bottom: 15px;
        padding: 10px;
        text-align: right;
        font-family: Arial, sans-serif;
        min-height: 80px;
        border: 1px solid #333;
    }
    .expression-display {
        min-height: 20px;
        color: #8a8a8a;
        font-size: 16px;
        margin-bottom: 5px;
        overflow-wrap: break-word;
    }
    .result-display {
        min-height: 40px;
        font-size: 32px;
        font-weight: bold;
        overflow-wrap: break-word;
    }
    button {
        width: 100% !important;
        height: 50px !important;
        font-size: 18px !important;
        border-radius: 5px !important;
        border: none !important;
        margin: 3px 0 !important;
        transition: all 0.1s ease !important;
    }
    .stButton > button:active {
        transform: scale(0.95);
        opacity: 0.8;
    }
    .function-btn > button {
        background-color: #4A4A4A !important;
        color: white !important;
    }
    .number-btn > button {
        background-color: #666666 !important;
        color: white !important;
        font-weight: bold !important;
    }
    .clear-btn > button {
        background-color: #b3b3b3 !important;
        color: black !important;
        font-weight: bold !important;
    }
    .operator-btn > button {
        background-color: #FF9500 !important;
        color: white !important;
        font-weight: bold !important;
    }
    .equals-btn > button {
        background-color: #FF9500 !important;
        color: white !important;
        font-weight: bold !important;
    }
    /* Fix button spacing issues */
    div[data-testid="column"] {
        padding: 0 3px !important;
    }
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    /* Fix expander styling */
    .streamlit-expanderHeader {
        font-size: 14px;
        font-weight: normal;
    }
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state if not already initialized
if 'display' not in st.session_state:
    st.session_state.display = '0'
if 'expression' not in st.session_state:
    st.session_state.expression = ''
if 'function_mode' not in st.session_state:
    st.session_state.function_mode = False
if 'function_name' not in st.session_state:
    st.session_state.function_name = ''
if 'awaiting_second_operand' not in st.session_state:
    st.session_state.awaiting_second_operand = False
if 'last_button' not in st.session_state:
    st.session_state.last_button = ''

def calculate_factorial(input_value):
    try:
        # Convert input to integer
        num = int(float(input_value))
        
        # Factorial is only defined for non-negative integers
        if num < 0:
            return "Error: Negative number"
        
        # Calculate factorial
        return str(math.factorial(num))
    
    except ValueError:
        return "Error: Invalid Input"
    except OverflowError:
        return "Error: Number too large"

def safe_eval(expr):
    """Safely evaluate an expression"""
    try:
        # Use ast.literal_eval for safety
        return eval(expr)
    except Exception as e:
        raise ValueError(f"Invalid expression: {expr}")

def evaluate_expression(expression):
    if not expression:
        return "0"
    
    try:
        # Replace all instances of 'π' with 'math.pi'
        expression = expression.replace('π', 'math.pi')
        # Replace all instances of 'e' with 'math.e'
        expression = expression.replace('e', 'math.e')
        
        # Handle square root expressions
        sqrt_pattern = r'√\((.*?)\)'
        while re.search(sqrt_pattern, expression):
            match = re.search(sqrt_pattern, expression)
            if match:
                inner_expr = match.group(1)
                inner_value = eval(inner_expr)
                if inner_value < 0:
                    return "Error: Cannot find square root of negative number"
                expression = expression.replace(f"√({inner_expr})", f"math.sqrt({inner_expr})")
        
        # Handle cube root expressions
        cube_root_pattern = r'∛\((.*?)\)'
        while re.search(cube_root_pattern, expression):
            match = re.search(cube_root_pattern, expression)
            if match:
                inner_expr = match.group(1)
                expression = expression.replace(f"∛({inner_expr})", f"({inner_expr})**(1/3)")
        
        # Handle sin function
        sin_pattern = r'sin\((.*?)\)'
        while re.search(sin_pattern, expression):
            match = re.search(sin_pattern, expression)
            if match:
                inner_expr = match.group(1)
                expression = expression.replace(f"sin({inner_expr})", f"math.sin(math.radians({inner_expr}))")
        
        # Handle cos function
        cos_pattern = r'cos\((.*?)\)'
        while re.search(cos_pattern, expression):
            match = re.search(cos_pattern, expression)
            if match:
                inner_expr = match.group(1)
                expression = expression.replace(f"cos({inner_expr})", f"math.cos(math.radians({inner_expr}))")
        
        # Handle tan function
        tan_pattern = r'tan\((.*?)\)'
        while re.search(tan_pattern, expression):
            match = re.search(tan_pattern, expression)
            if match:
                inner_expr = match.group(1)
                angle_rad = math.radians(eval(inner_expr))
                if abs(math.cos(angle_rad)) < 1e-10:
                    return "Error: Tangent undefined at this angle"
                expression = expression.replace(f"tan({inner_expr})", f"math.tan(math.radians({inner_expr}))")
        
        # Handle log function (base 10)
        log_pattern = r'log\((.*?)\)'
        while re.search(log_pattern, expression):
            match = re.search(log_pattern, expression)
            if match:
                inner_expr = match.group(1)
                inner_value = eval(inner_expr)
                if inner_value <= 0:
                    return "Error: Cannot find log of zero or negative number"
                expression = expression.replace(f"log({inner_expr})", f"math.log10({inner_expr})")
        
        # Handle ln function (natural log)
        ln_pattern = r'ln\((.*?)\)'
        while re.search(ln_pattern, expression):
            match = re.search(ln_pattern, expression)
            if match:
                inner_expr = match.group(1)
                inner_value = eval(inner_expr)
                if inner_value <= 0:
                    return "Error: Cannot find natural log of zero or negative number"
                expression = expression.replace(f"ln({inner_expr})", f"math.log({inner_expr})")
        
        # Handle x² expressions
        squared_pattern = r'x²\((.*?)\)'
        while re.search(squared_pattern, expression):
            match = re.search(squared_pattern, expression)
            if match:
                inner_expr = match.group(1)
                expression = expression.replace(f"x²({inner_expr})", f"({inner_expr})**2")
        
        # Handle x³ expressions
        cubed_pattern = r'x³\((.*?)\)'
        while re.search(cubed_pattern, expression):
            match = re.search(cubed_pattern, expression)
            if match:
                inner_expr = match.group(1)
                expression = expression.replace(f"x³({inner_expr})", f"({inner_expr})**3")
                
        # Handle factorial expressions
        factorial_pattern = r'!\((.*?)\)'
        while re.search(factorial_pattern, expression):
            match = re.search(factorial_pattern, expression)
            if match:
                inner_expr = match.group(1)
                inner_value = eval(inner_expr)
                fact_result = calculate_factorial(inner_value)
                if fact_result.startswith("Error"):
                    return fact_result
                expression = expression.replace(f"!({inner_expr})", f"{fact_result}")
        
        # Handle percentage calculation
        expression = expression.replace('%', '/100')
        
        # Replace × with *
        expression = expression.replace('×', '*')
        # Replace ÷ with /
        expression = expression.replace('÷', '/')
        
        # Check for division by zero
        if '/0' in expression.replace('/0.', '').replace('/0e', ''):
            return "Error: Division by zero"
            
        # Evaluate the expression and get the result
        result = eval(expression)
        
        # Handle special cases
        if math.isnan(result):
            return "Error: Not a number"
        if math.isinf(result):
            return "Error: Infinite result"
        
        # Format the result to remove trailing zeros if it's a float
        if isinstance(result, float):
            # If the result is very small or very large, use scientific notation
            if abs(result) < 0.0001 or abs(result) > 10000000:
                return f"{result:.10e}"
            else:
                # Remove trailing zeros
                result_str = f"{result:.10f}"
                result_str = result_str.rstrip('0').rstrip('.')
                return result_str
        else:
            return str(result)
    
    except Exception as e:
        return f"Error: {str(e)}"

def button_click(value):
    # If awaiting second operand and a number is pressed, start a new expression
    if st.session_state.awaiting_second_operand and value.isdigit():
        st.session_state.display = value
        st.session_state.expression = value
        st.session_state.awaiting_second_operand = False
        return
    
    # If the current display is a result and we're not in function mode, clear it when a new button is pressed
    current = st.session_state.display
    
    # Don't clear the screen when pressing equals, backspace, or in function mode
    if (not current.startswith('Error') and 
        value != '=' and 
        not st.session_state.function_mode and
        len(current) > 0):
        try:
            # Try to convert to float to verify it's a number
            float(current)
            
            # If the last button was '=', and this is a new digit or operation, clear the screen
            if st.session_state.last_button == '=' and (value.isdigit() or value in ['+', '-', '×', '÷']):
                st.session_state.display = value
                st.session_state.expression = value
                st.session_state.last_button = value
                return
        except ValueError:
            # Not a number, so don't clear
            pass
    
    # Update the last button pressed
    st.session_state.last_button = value
    
    # Handle the Clear button
    if value == 'C':
        st.session_state.display = '0'
        st.session_state.expression = ''
        st.session_state.function_mode = False
        st.session_state.function_name = ''
        st.session_state.awaiting_second_operand = False
        return
    
    # Handle the Backspace button
    if value == '⌫':
        if len(current) > 1:
            st.session_state.display = current[:-1]
            if len(st.session_state.expression) > 0:
                st.session_state.expression = st.session_state.expression[:-1]
        else:
            st.session_state.display = '0'
            if len(st.session_state.expression) <= 1:
                st.session_state.expression = ''
        return
    
    # Handle the Equals button
    if value == '=':
        try:
            if st.session_state.function_mode:
                # If we're in function mode, evaluate the function with the current expression
                function_expr = f"{st.session_state.function_name}({current})"
                st.session_state.expression = function_expr
                result = evaluate_expression(function_expr)
                st.session_state.display = result
                st.session_state.function_mode = False
                st.session_state.function_name = ''
            else:
                # Otherwise, evaluate the full expression
                if current.startswith('Error'):
                    return
                
                expr_to_evaluate = copy.copy(st.session_state.expression)
                if not expr_to_evaluate:
                    expr_to_evaluate = current
                
                result = evaluate_expression(expr_to_evaluate)
                st.session_state.display = result
            
            st.session_state.awaiting_second_operand = True
            
        except Exception as e:
            st.session_state.display = f"Error: {str(e)}"
        return
    
    # Handle functions (sin, cos, tan, log, ln, √, x², x³, !, ∛)
    if value in ['sin', 'cos', 'tan', 'log', 'ln', '√', 'x²', 'x³', '!', '∛']:
        if current.startswith('Error'):
            return
        
        st.session_state.function_mode = True
        st.session_state.function_name = value
        st.session_state.display = ''
        return
    
    # Handle special constants (pi, e)
    if value in ['π', 'e']:
        if current == '0' or st.session_state.awaiting_second_operand:
            st.session_state.display = value
            st.session_state.expression = value
        else:
            st.session_state.display += value
            st.session_state.expression += value
        
        st.session_state.awaiting_second_operand = False
        return
    
    # Handle other buttons (numbers, operators, parentheses)
    if current == '0' and value.isdigit():
        # Replace the initial 0 with the digit
        st.session_state.display = value
        st.session_state.expression = value
    elif current.startswith('Error'):
        # If there's an error, start fresh with the new input
        if value.isdigit() or value == '.':
            st.session_state.display = value
            st.session_state.expression = value
        elif value in ['+', '-', '×', '÷']:
            st.session_state.display = '0' + value
            st.session_state.expression = '0' + value
    elif st.session_state.function_mode:
        # If in function mode, build the function argument
        if st.session_state.display == '':
            # Start the function argument
            if value.isdigit() or value == '.' or value == '-':
                st.session_state.display = value
            elif value == '(':
                st.session_state.display = value
            # If operator is pressed directly, use 0 as the first operand
            elif value in ['+', '-', '×', '÷'] and st.session_state.display == '':
                st.session_state.display = '0' + value
        else:
            # Continue building the function argument
            st.session_state.display += value
    else:
        # Normal operation - update the display and expression
        if value in ['+', '-', '×', '÷', '.', '(', ')', '%']:
            # For operators, update expression directly
            st.session_state.display += value
            st.session_state.expression += value
        else:
            # For numbers, update both
            st.session_state.display += value
            st.session_state.expression += value
    
    st.session_state.awaiting_second_operand = False

# Create the calculator UI with a smaller, more compact design
st.markdown('<h2 style="text-align: center; margin-bottom: 0.5rem;">Python Calculator</h2>', unsafe_allow_html=True)

# Calculator container
st.markdown('<div class="calculator-container">', unsafe_allow_html=True)

# Display area
st.markdown(f"""
<div class="display-area">
    <div class="expression-display">{st.session_state.expression}</div>
    <div class="result-display">{st.session_state.display}</div>
</div>
""", unsafe_allow_html=True)

# First row - Special Functions (Clear, Backspace, Parentheses, Division)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
    if st.button("C"):
        button_click("C")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
    if st.button("⌫"):
        button_click("⌫")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="function-btn">', unsafe_allow_html=True)
    if st.button("()"):
        # Toggle between opening and closing parenthesis
        if '(' in st.session_state.display and st.session_state.display.count('(') > st.session_state.display.count(')'):
            button_click(")")
        else:
            button_click("(")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="operator-btn">', unsafe_allow_html=True)
    if st.button("÷"):
        button_click("÷")
    st.markdown('</div>', unsafe_allow_html=True)

# Second row - Numbers 7-9 and Multiplication
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="number-btn">', unsafe_allow_html=True)
    if st.button("7"):
        button_click("7")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="number-btn">', unsafe_allow_html=True)
    if st.button("8"):
        button_click("8")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="number-btn">', unsafe_allow_html=True)
    if st.button("9"):
        button_click("9")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="operator-btn">', unsafe_allow_html=True)
    if st.button("×"):
        button_click("×")
    st.markdown('</div>', unsafe_allow_html=True)

# Third row - Numbers 4-6 and Subtraction
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="number-btn">', unsafe_allow_html=True)
    if st.button("4"):
        button_click("4")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="number-btn">', unsafe_allow_html=True)
    if st.button("5"):
        button_click("5")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="number-btn">', unsafe_allow_html=True)
    if st.button("6"):
        button_click("6")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="operator-btn">', unsafe_allow_html=True)
    if st.button("-"):
        button_click("-")
    st.markdown('</div>', unsafe_allow_html=True)

# Fourth row - Numbers 1-3 and Addition
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="number-btn">', unsafe_allow_html=True)
    if st.button("1"):
        button_click("1")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="number-btn">', unsafe_allow_html=True)
    if st.button("2"):
        button_click("2")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="number-btn">', unsafe_allow_html=True)
    if st.button("3"):
        button_click("3")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="operator-btn">', unsafe_allow_html=True)
    if st.button("+"):
        button_click("+")
    st.markdown('</div>', unsafe_allow_html=True)

# Fifth row - Zero, Decimal Point, and Equals
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="number-btn">', unsafe_allow_html=True)
    if st.button("0"):
        button_click("0")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="number-btn">', unsafe_allow_html=True)
    if st.button("."):
        button_click(".")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="function-btn">', unsafe_allow_html=True)
    if st.button("%"):
        button_click("%")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="equals-btn">', unsafe_allow_html=True)
    if st.button("="):
        button_click("=")
    st.markdown('</div>', unsafe_allow_html=True)

# Scientific Functions section - use an expander for less frequently used functions
with st.expander("Scientific Functions"):
    # Row 1 - Trigonometric functions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="function-btn">', unsafe_allow_html=True)
        if st.button("sin"):
            button_click("sin")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="function-btn">', unsafe_allow_html=True)
        if st.button("cos"):
            button_click("cos")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="function-btn">', unsafe_allow_html=True)
        if st.button("tan"):
            button_click("tan")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 2 - Logarithmic functions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="function-btn">', unsafe_allow_html=True)
        if st.button("log"):
            button_click("log")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="function-btn">', unsafe_allow_html=True)
        if st.button("ln"):
            button_click("ln")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="function-btn">', unsafe_allow_html=True)
        if st.button("√"):
            button_click("√")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 3 - Powers and roots
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="function-btn">', unsafe_allow_html=True)
        if st.button("x²"):
            button_click("x²")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="function-btn">', unsafe_allow_html=True)
        if st.button("x³"):
            button_click("x³")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="function-btn">', unsafe_allow_html=True)
        if st.button("∛"):
            button_click("∛")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 4 - Constants and factorial
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="function-btn">', unsafe_allow_html=True)
        if st.button("π"):
            button_click("π")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="function-btn">', unsafe_allow_html=True)
        if st.button("e"):
            button_click("e")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="function-btn">', unsafe_allow_html=True)
        if st.button("!"):
            button_click("!")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close calculator-container

# Footer with GitHub link
st.markdown("""
<div style="text-align: center; margin-top: 20px; color: gray; font-size: 12px;">
    Python Calculator | <a href="https://github.com/yourusername/python-calculator" target="_blank">GitHub Repository</a>
</div>
""", unsafe_allow_html=True) 