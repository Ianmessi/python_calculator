#!/usr/bin/env python3
"""
PyQt Calculator - A simple calculator using PyQt5 which should be more compatible
with older versions of macOS.
"""

import sys
import math
import re

try:
    # Try to import PyQt5
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                                QGridLayout, QPushButton, QLineEdit, QLabel)
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QFont
except ImportError:
    print("PyQt5 is not installed. Please install it with: pip install PyQt5")
    print("Or run the terminal calculator with: ./macos_compat_calculator.py")
    sys.exit(1)

class PyQtCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Calculator")
        self.setMinimumSize(400, 650)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1C1C1E;
                border-radius: 10px;
            }
        """)
        
        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create a display frame with a border
        self.display_frame = QWidget()
        self.display_frame.setStyleSheet("""
            background-color: #282C34;
            border: 2px solid #3C3C3E;
            border-radius: 8px;
        """)
        self.display_frame.setMinimumHeight(160)
        
        # Layout for the display frame
        self.display_frame_layout = QVBoxLayout(self.display_frame)
        self.display_frame_layout.setContentsMargins(10, 10, 10, 10)
        self.display_frame_layout.setSpacing(0)
        
        # Expression display (shows the full expression)
        self.expression_display = QLabel("")
        self.expression_display.setAlignment(Qt.AlignRight)
        self.expression_display.setFont(QFont("Arial", 16))
        self.expression_display.setStyleSheet("color: #8E8E93;")
        self.expression_display.setMinimumHeight(30)
        self.display_frame_layout.addWidget(self.expression_display)
        
        # Main display
        self.display = QLineEdit("0")
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFont(QFont("Arial", 42, QFont.Bold))
        self.display.setMinimumHeight(80)
        self.display.setStyleSheet("""
            QLineEdit {
                background-color: transparent;
                color: white;
                border: none;
            }
        """)
        self.display_frame_layout.addWidget(self.display)
        
        # Add the display frame to the main layout
        self.main_layout.addWidget(self.display_frame)
        
        # Add some spacing between display and buttons
        self.main_layout.addSpacing(10)
        
        # Current expression
        self.current_expression = ""
        self.function_mode = False
        self.function_name = ""
        self.bracket_count = 0
        
        # Buttons layout
        self.buttons_layout = QGridLayout()
        self.buttons_layout.setSpacing(15)  # Increased spacing between buttons
        self.main_layout.addLayout(self.buttons_layout)
        
        # Define buttons
        self.create_buttons()
        
        # Show the calculator
        self.show()
    
    def create_buttons(self):
        # Button definitions: text, row, column, colspan
        buttons = [
            # Row 0: Clear and basic operations
            ('C', 0, 0, 1), ('⌫', 0, 1, 1), ('(', 0, 2, 1), (')', 0, 3, 1),
            
            # Row 1-3: Scientific functions
            ('sin', 1, 0, 1), ('cos', 1, 1, 1), ('tan', 1, 2, 1), ('log', 1, 3, 1),
            ('ln', 2, 0, 1), ('√', 2, 1, 1), ('x²', 2, 2, 1), ('x³', 2, 3, 1),
            ('π', 3, 0, 1), ('e', 3, 1, 1), ('!', 3, 2, 1), ('∛', 3, 3, 1),
            
            # Row 4-7: Number pad and operations (standard calculator layout)
            ('7', 4, 0, 1), ('8', 4, 1, 1), ('9', 4, 2, 1), ('÷', 4, 3, 1),
            ('4', 5, 0, 1), ('5', 5, 1, 1), ('6', 5, 2, 1), ('×', 5, 3, 1),
            ('1', 6, 0, 1), ('2', 6, 1, 1), ('3', 6, 2, 1), ('-', 6, 3, 1),
            ('0', 7, 0, 2), ('.', 7, 2, 1), ('=', 7, 3, 1), ('+', 7, 3, 1),
        ]
        
        # Create and add buttons with specific styling
        for btn_data in buttons:
            if len(btn_data) == 4:
                btn_text, row, col, colspan = btn_data
                button = QPushButton(btn_text)
                
                # Different styling for different button types
                if btn_text in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
                    # Number buttons
                    button.setStyleSheet("""
                        QPushButton {
                            background-color: #32373B;
                            color: white;
                            font-weight: bold;
                            border-radius: 30px;
                            border: none;
                        }
                        QPushButton:pressed {
                            background-color: #454D54;
                        }
                    """)
                elif btn_text in ['+', '-', '×', '÷']:
                    # Operation buttons
                    button.setStyleSheet("""
                        QPushButton {
                            background-color: #FF9F0A;
                            color: white;
                            font-weight: bold;
                            border-radius: 30px;
                            border: none;
                        }
                        QPushButton:pressed {
                            background-color: #FFB143;
                        }
                    """)
                elif btn_text == '=':
                    # Equals button
                    button.setStyleSheet("""
                        QPushButton {
                            background-color: #FF9F0A;
                            color: white;
                            font-weight: bold;
                            border-radius: 30px;
                            border: none;
                        }
                        QPushButton:pressed {
                            background-color: #FFB143;
                        }
                    """)
                elif btn_text in ['sin', 'cos', 'tan', 'log', 'ln', '√', 'x²', 'x³', 'π', 'e', '!', '∛']:
                    # Scientific function buttons
                    button.setStyleSheet("""
                        QPushButton {
                            background-color: #4E505F;
                            color: white;
                            border-radius: 30px;
                            border: none;
                        }
                        QPushButton:pressed {
                            background-color: #5E6171;
                        }
                    """)
                elif btn_text in ['C', '⌫']:
                    # Clear buttons
                    button.setStyleSheet("""
                        QPushButton {
                            background-color: #A5A5A5;
                            color: black;
                            font-weight: bold;
                            border-radius: 30px;
                            border: none;
                        }
                        QPushButton:pressed {
                            background-color: #C6C6C6;
                        }
                    """)
                elif btn_text in ['(', ')']:
                    # Parentheses
                    button.setStyleSheet("""
                        QPushButton {
                            background-color: #4E505F;
                            color: white;
                            font-weight: bold;
                            border-radius: 30px;
                            border: none;
                        }
                        QPushButton:pressed {
                            background-color: #5E6171;
                        }
                    """)
                
                button.setFont(QFont("Arial", 14))
                button.setMinimumHeight(60)
                
                # Make buttons more square-shaped with padding
                button.setMinimumWidth(70)
                
                # Connect button click
                button.clicked.connect(lambda checked, text=btn_text: self.button_click(text))
                
                # Add to layout
                if colspan > 1:
                    self.buttons_layout.addWidget(button, row, col, 1, colspan)
                else:
                    self.buttons_layout.addWidget(button, row, col)
        
        # Fix the '=' and '+' buttons that had the same position
        equal_button = QPushButton('=')
        equal_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9F0A;
                color: white;
                font-weight: bold;
                border-radius: 30px;
                border: none;
            }
            QPushButton:pressed {
                background-color: #FFB143;
            }
        """)
        equal_button.setFont(QFont("Arial", 14))
        equal_button.setMinimumHeight(60)
        equal_button.setMinimumWidth(70)
        equal_button.clicked.connect(lambda checked: self.button_click('='))
        self.buttons_layout.addWidget(equal_button, 7, 3)
        
        plus_button = QPushButton('+')
        plus_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9F0A;
                color: white;
                font-weight: bold;
                border-radius: 30px;
                border: none;
            }
            QPushButton:pressed {
                background-color: #FFB143;
            }
        """)
        plus_button.setFont(QFont("Arial", 14))
        plus_button.setMinimumHeight(60)
        plus_button.setMinimumWidth(70)
        plus_button.clicked.connect(lambda checked: self.button_click('+'))
        self.buttons_layout.addWidget(plus_button, 6, 3)  # Move + to row 6
    
    def evaluate_expression(self, expression):
        try:
            # Handle empty expression
            if not expression:
                return '0'
            
            # Replace mathematical operators
            expression = expression.replace('×', '*').replace('÷', '/')
            
            # Handle functions
            expression = expression.replace('sin(', 'math.sin(math.radians(')
            expression = expression.replace('cos(', 'math.cos(math.radians(')
            expression = expression.replace('tan(', 'math.tan(math.radians(')
            expression = expression.replace('log(', 'math.log10(')
            expression = expression.replace('ln(', 'math.log(')
            expression = expression.replace('√(', 'math.sqrt(')
            
            # Handle cube root similarly to other functions
            # We need to catch all occurrences of ∛( and replace them with the right expression
            cube_root_pattern = r'∛\((.*?)\)'
            while re.search(cube_root_pattern, expression):
                match = re.search(cube_root_pattern, expression)
                if match:
                    inner_expr = match.group(1)
                    # Replace with inline calculation using ** (1/3)
                    expression = expression.replace(f"∛({inner_expr})", f"({inner_expr})**(1/3)")
            
            # Handle our new function formats
            expression = expression.replace('x²(', '(')
            expression = expression.replace('x³(', '(')
            expression = expression.replace('!(', '(')
            
            # Add closing parentheses if needed
            open_count = expression.count('(')
            close_count = expression.count(')')
            if open_count > close_count:
                expression += ')' * (open_count - close_count)
            
            # Process x², x³, !, operations after closing parentheses 
            if self.function_name == 'x²':
                try:
                    value = eval(expression)
                    return str(value ** 2)
                except:
                    return 'Error'
            elif self.function_name == 'x³':
                try:
                    value = eval(expression)
                    return str(value ** 3)
                except:
                    return 'Error'
            elif self.function_name == '!':
                try:
                    value = eval(expression)
                    # Use the new calculate_factorial method
                    return self.calculate_factorial(str(value))
                except:
                    return 'Error'
            
            # Handle implicit multiplication with brackets
            expression = expression.replace(')(', ')*(')
            
            # Handle percentage
            if '%' in expression:
                parts = expression.split('%')
                if len(parts) == 2:
                    try:
                        value = float(parts[0])
                        expression = str(value / 100)
                    except:
                        return 'Error'
            
            # Simple safety check
            safe_expr = expression
            for term in ['math.sin', 'math.cos', 'math.tan', 'math.log10', 
                         'math.log', 'math.sqrt', 'math.radians', '**']:
                safe_expr = safe_expr.replace(term, '')
            
            safe_chars = '0123456789.+-*/() '
            for char in safe_expr:
                if char not in safe_chars:
                    return 'Error'
            
            # Evaluate the expression
            result = eval(expression)
            
            # Handle division by zero and other errors
            if isinstance(result, float) and (math.isinf(result) or math.isnan(result)):
                return 'Error'
            
            # Format the result
            if isinstance(result, float):
                # Remove trailing zeros after decimal point
                result = f"{result:g}"
            
            return str(result)
        except:
            return 'Error'
    
    def calculate_factorial(self, input_value):
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

    def button_click(self, value):
        current = self.display.text()
        
        # Clear error message if present when pressing any button except C
        if current.startswith('Error') and value != 'C':
            current = '0'
            self.current_expression = ""
            self.expression_display.setText("")
        
        # Clear screen if the current display is a result
        if value != '=' and value != 'C' and not self.function_mode:
            try:
                float(current)  # Check if current is a number
                if value not in '+-×÷':  # Don't clear for operations
                    self.display.setText('0')
                    self.current_expression = ""
                    current = '0'
            except:
                pass
        
        if value == 'C':
            self.display.setText('0')
            self.current_expression = ""
            self.expression_display.setText("")
            self.function_mode = False
            self.function_name = ""
            self.bracket_count = 0
        elif value == '⌫':
            if len(current) > 1:
                self.display.setText(current[:-1])
                self.current_expression = self.current_expression[:-1]
                self.expression_display.setText(self.current_expression)
                if current[-1] == '(':
                    self.bracket_count -= 1
                elif current[-1] == ')':
                    self.bracket_count += 1
            else:
                self.display.setText('0')
                self.current_expression = ""
                self.expression_display.setText("")
                self.bracket_count = 0
        elif value in ['sin', 'cos', 'tan', 'log', 'ln', '√', '∛']:
            self.function_mode = True
            self.function_name = value
            self.current_expression = value + '('
            self.display.setText(value + '(')
            self.expression_display.setText(self.current_expression)
            self.bracket_count += 1
        elif value == '=':
            # Show the full expression in the expression display
            self.expression_display.setText(self.current_expression + " =")
            
            if self.function_mode:
                # Close any open brackets
                while self.bracket_count > 0:
                    self.current_expression += ')'
                    self.bracket_count -= 1
                # Handle function evaluation
                result = self.evaluate_expression(self.current_expression)
                self.display.setText(result)
                self.current_expression = result
                self.function_mode = False
                self.function_name = ""
            else:
                # Handle regular expression evaluation
                result = self.evaluate_expression(self.current_expression)
                self.display.setText(result)
                self.current_expression = result
        elif value == 'x²':
            if current == '0' and self.current_expression == "":
                # Don't calculate for initial zero, treat it as function entry
                self.function_mode = True
                self.function_name = "x²"
                self.current_expression = "x²("
                self.display.setText('x²(')
                self.expression_display.setText(self.current_expression)
                self.bracket_count += 1
            else:
                try:
                    # Get the current displayed number
                    num = float(current)
                    squared = num ** 2
                    
                    # Update the display and expression
                    self.expression_display.setText(f"{current}² =")
                    self.display.setText(str(squared))
                    self.current_expression = str(squared)
                except:
                    self.display.setText('Error')
        elif value == 'x³':
            if current == '0' and self.current_expression == "":
                # Don't calculate for initial zero, treat it as function entry
                self.function_mode = True
                self.function_name = "x³"
                self.current_expression = "x³("
                self.display.setText('x³(')
                self.expression_display.setText(self.current_expression)
                self.bracket_count += 1
            else:
                try:
                    # Get the current displayed number
                    num = float(current)
                    cubed = num ** 3
                    
                    # Update the display and expression
                    self.expression_display.setText(f"{current}³ =")
                    self.display.setText(str(cubed))
                    self.current_expression = str(cubed)
                except:
                    self.display.setText('Error')
        elif value == 'π':
            self.display.setText(str(math.pi))
            self.current_expression = str(math.pi)
            self.expression_display.setText("π")
        elif value == 'e':
            self.display.setText(str(math.e))
            self.current_expression = str(math.e)
            self.expression_display.setText("e")
        elif value == '!':
            if current == '0' and self.current_expression == "":
                # Don't calculate for initial zero, treat it as function entry
                self.function_mode = True
                self.function_name = "!"
                self.current_expression = "!("
                self.display.setText('!(')
                self.expression_display.setText(self.current_expression)
                self.bracket_count += 1
            else:
                # Calculate factorial using the new method
                result = self.calculate_factorial(current)
                
                # Update the display based on result
                if result.startswith('Error'):
                    self.display.setText(result)
                else:
                    # Update the display and expression
                    self.expression_display.setText(f"{current}! =")
                    self.display.setText(result)
                    self.current_expression = result
        elif value == '∛':
            if current == '0' and self.current_expression == "":
                # Don't calculate for initial zero, treat it as function entry
                self.function_mode = True
                self.function_name = "∛"
                self.current_expression = "∛("
                self.display.setText('∛(')
                self.expression_display.setText(self.current_expression)
                self.bracket_count += 1
            else:
                try:
                    # Get the current displayed number and calculate cube root
                    num = float(current)
                    result = num ** (1/3)
                    
                    # Update the display and expression
                    self.expression_display.setText(f"∛{current} =")
                    self.display.setText(str(result))
                    self.current_expression = str(result)
                except:
                    self.display.setText('Error')
        elif value == '(':
            self.current_expression += '('
            self.display.setText(current + '(')
            self.expression_display.setText(self.current_expression)
            self.bracket_count += 1
        elif value == ')':
            if self.bracket_count > 0:
                self.current_expression += ')'
                self.display.setText(current + ')')
                self.expression_display.setText(self.current_expression)
                self.bracket_count -= 1
        else:
            if self.function_mode:
                # Handle function input
                if current == self.function_name + '(':
                    self.display.setText(self.function_name + '(' + value)
                    self.current_expression = self.function_name + '(' + value
                    self.expression_display.setText(self.current_expression)
                else:
                    self.display.setText(current + value)
                    self.current_expression = self.current_expression + value
                    self.expression_display.setText(self.current_expression)
            else:
                # Handle regular input
                if current == '0' and value not in '+-×÷':
                    self.display.setText(value)
                    self.current_expression = value
                    self.expression_display.setText(self.current_expression)
                else:
                    self.display.setText(current + value)
                    self.current_expression = self.current_expression + value
                    self.expression_display.setText(self.current_expression)

def main():
    app = QApplication(sys.argv)
    calculator = PyQtCalculator()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 