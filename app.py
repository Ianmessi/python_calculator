import streamlit as st
import math
import re
import copy

# Set page configuration
st.set_page_config(
    page_title="Python Calculator",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for better styling
st.markdown("""
<style>
    .calculator-container {
        max-width: 400px;
        margin: 0 auto;
        background-color: #1C1C1E;
        border-radius: 15px;
        padding: 15px;
    }
    .display-area {
        background-color: #1C1C1E;
        color: white;
        border-radius: 10px;
        margin-bottom: 15px;
        padding: 10px;
        text-align: right;
        font-family: Arial, sans-serif;
    }
    .expression-display {
        min-height: 25px;
        color: #8a8a8a;
        font-size: 16px;
        margin-bottom: 5px;
    }
    .result-display {
        min-height: 50px;
        font-size: 32px;
        font-weight: bold;
    }
    .btn-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
    }
    .stButton > button {
        width: 100%;
        height: 60px;
        font-size: 20px;
        border-radius: 30px;
        border: none;
    }
    .function-btn > button {
        background-color: #4E505F;
        color: white;
    }
    .number-btn > button {
        background-color: #32373B;
        color: white;
    }
    .clear-btn > button {
        background-color: #A5A5A5;
        color: black;
    }
    .operator-btn > button {
        background-color: #FF9F0A;
        color: white;
    }
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
        num = int(input_value)
        
        # Factorial is only defined for non-negative integers
        if num < 0:
            return "Error: Negative number"
        
        # Calculate factorial
        return str(math.factorial(num))
    
    except ValueError:
        return "Error: Invalid Input"

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
                expression = expression.replace(f"√({inner_expr})", f"math.sqrt({inner_expr})")
        
        # Handle cube root expressions
        cube_root_pattern = r'∛\((.*?)\)'
        while re.search(cube_root_pattern, expression):
            match = re.search(cube_root_pattern, expression)
            if match:
                inner_expr = match.group(1)
                expression = expression.replace(f"∛({inner_expr})", f"({inner_expr})**(1/3)")
        
        # Handle other functions
        sin_pattern = r'sin\((.*?)\)'
        while re.search(sin_pattern, expression):
            match = re.search(sin_pattern, expression)
            if match:
                inner_expr = match.group(1)
                expression = expression.replace(f"sin({inner_expr})", f"math.sin(math.radians({inner_expr}))")
        
        cos_pattern = r'cos\((.*?)\)'
        while re.search(cos_pattern, expression):
            match = re.search(cos_pattern, expression)
            if match:
                inner_expr = match.group(1)
                expression = expression.replace(f"cos({inner_expr})", f"math.cos(math.radians({inner_expr}))")
        
        tan_pattern = r'tan\((.*?)\)'
        while re.search(tan_pattern, expression):
            match = re.search(tan_pattern, expression)
            if match:
                inner_expr = match.group(1)
                expression = expression.replace(f"tan({inner_expr})", f"math.tan(math.radians({inner_expr}))")
        
        log_pattern = r'log\((.*?)\)'
        while re.search(log_pattern, expression):
            match = re.search(log_pattern, expression)
            if match:
                inner_expr = match.group(1)
                expression = expression.replace(f"log({inner_expr})", f"math.log10({inner_expr})")
        
        ln_pattern = r'ln\((.*?)\)'
        while re.search(ln_pattern, expression):
            match = re.search(ln_pattern, expression)
            if match:
                inner_expr = match.group(1)
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
                fact_result = calculate_factorial(eval(inner_expr))
                expression = expression.replace(f"!({inner_expr})", f"{fact_result}")
        
        # Handle percentage calculation
        expression = expression.replace('%', '/100')
        
        # Replace × with *
        expression = expression.replace('×', '*')
        # Replace ÷ with /
        expression = expression.replace('÷', '/')
        
        # Evaluate the expression and get the result
        result = eval(expression)
        
        # Handle division by zero
        if result == float('inf') or result == float('-inf'):
            return "Error: Division by zero"
        
        # Format the result to remove trailing zeros if it's a float
        if isinstance(result, float):
            # If the result is very small or very large, use scientific notation
            if abs(result) < 0.0001 or abs(result) > 10000000:
                return f"{result:.10e}"
            else:
                # Remove trailing zeros
                result_str = str(result)
                if '.' in result_str:
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

# Create the calculator UI
st.title("Python Calculator")

# Calculator container
st.markdown('<div class="calculator-container">', unsafe_allow_html=True)

# Display area
st.markdown(f"""
<div class="display-area">
    <div class="expression-display">{st.session_state.expression}</div>
    <div class="result-display">{st.session_state.display}</div>
</div>
""", unsafe_allow_html=True)

# Create calculator buttons
# Row 1 - Clear, Backspace, Parentheses, Division
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

# Row 2 - Scientific functions
col1, col2, col3, col4 = st.columns(4)
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

with col4:
    st.markdown('<div class="operator-btn">', unsafe_allow_html=True)
    if st.button("×"):
        button_click("×")
    st.markdown('</div>', unsafe_allow_html=True)

# Row 3 - More functions
col1, col2, col3, col4 = st.columns(4)
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

with col4:
    st.markdown('<div class="operator-btn">', unsafe_allow_html=True)
    if st.button("-"):
        button_click("-")
    st.markdown('</div>', unsafe_allow_html=True)

# Row 4 - Special functions
col1, col2, col3, col4 = st.columns(4)
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
    if st.button("!"):
        button_click("!")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="operator-btn">', unsafe_allow_html=True)
    if st.button("+"):
        button_click("+")
    st.markdown('</div>', unsafe_allow_html=True)

# Row 5 - Constants and cube root
col1, col2, col3, col4 = st.columns(4)
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
    if st.button("∛"):
        button_click("∛")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="function-btn">', unsafe_allow_html=True)
    if st.button("%"):
        button_click("%")
    st.markdown('</div>', unsafe_allow_html=True)

# Row 6 - Numbers 7-9
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
    if st.button("="):
        button_click("=")
    st.markdown('</div>', unsafe_allow_html=True)

# Row 7 - Numbers 4-6
col1, col2, col3 = st.columns(3)
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

# Row 8 - Numbers 1-3
col1, col2, col3 = st.columns(3)
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

# Row 9 - Zero and decimal point
col1, col2 = st.columns(2)
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

st.markdown('</div>', unsafe_allow_html=True)  # Close calculator-container

# Footer with GitHub link
st.markdown("""
<div style="text-align: center; margin-top: 20px; color: gray; font-size: 12px;">
    Python Calculator | <a href="https://github.com/yourusername/python-calculator" target="_blank">GitHub Repository</a>
</div>
""", unsafe_allow_html=True) 