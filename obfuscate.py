#!/usr/bin/env python3
"""
Simple Batch Script Obfuscator
Obfuscates .cmd files by renaming variables, adding comments, and manipulating whitespace
without affecting functionality.
"""

import re
import random
import string
import sys
from pathlib import Path


class BatchObfuscator:
    def __init__(self):
        self.var_map = {}
        self.junk_comments = [
            "REM Batch processing routine",
            "REM System configuration module",
            "REM Data validation layer",
            "REM Network interface handler",
            "REM Resource allocation manager",
            "REM Memory management routine",
            "REM Error handling protocol",
            "REM Input validation check",
            "REM Output stream handler",
            "REM Configuration parser",
            "REM Session manager",
            "REM File system interface",
            "REM Registry operations",
            "REM Service controller",
        ]
        
    def generate_obfuscated_var_name(self):
        """Generate a cryptic variable name"""
        # Use similar looking characters to make it harder to read
        chars = string.ascii_letters + string.digits
        return ''.join(random.choices(chars, k=random.randint(8, 14)))
    
    def extract_variables(self, content):
        """Extract all variable references from batch code"""
        # Match %VARIABLE% and !VARIABLE! patterns
        patterns = [
            r'%([A-Za-z_][A-Za-z0-9_]*)%',  # %VAR%
            r'!([A-Za-z_][A-Za-z0-9_]*)!',  # !VAR!
        ]
        
        variables = set()
        for pattern in patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                var_name = match.group(1)
                # Skip system variables and numbers
                if not var_name.isupper() or var_name.isdigit():
                    if var_name not in ['ERRORLEVEL', 'CMDCMDLINE', 'CMDEXTVERSION']:
                        variables.add(var_name)
        
        return variables
    
    def obfuscate_variables(self, content):
        """Replace all variable names with obfuscated ones"""
        variables = self.extract_variables(content)
        
        for var in variables:
            if var not in self.var_map:
                self.var_map[var] = self.generate_obfuscated_var_name()
        
        # Replace %VAR% patterns
        for orig_var, obf_var in self.var_map.items():
            content = re.sub(f'%{orig_var}%', f'%{obf_var}%', content, flags=re.IGNORECASE)
            content = re.sub(f'!{orig_var}!', f'!{obf_var}!', content, flags=re.IGNORECASE)
            # Handle set statements
            content = re.sub(f'set {orig_var}=', f'set {obf_var}=', content, flags=re.IGNORECASE)
        
        return content
    
    def add_junk_comments(self, lines):
        """Insert random junk comments throughout the code"""
        obfuscated_lines = []
        
        for i, line in enumerate(lines):
            obfuscated_lines.append(line)
            
            # Add junk comments randomly (but not after every line)
            if random.random() < 0.15 and line.strip() and not line.strip().startswith('REM'):
                junk = random.choice(self.junk_comments)
                obfuscated_lines.append(junk)
        
        return obfuscated_lines
    
    def obfuscate_whitespace(self, content):
        """Add inconsistent spacing and indentation"""
        lines = content.split('\n')
        obfuscated_lines = []
        
        for line in lines:
            if line.strip():  # Only modify non-empty lines
                # Randomly add extra spaces at the beginning
                if random.random() < 0.3:
                    spaces = ' ' * random.randint(1, 4)
                    obfuscated_lines.append(spaces + line.lstrip())
                else:
                    obfuscated_lines.append(line)
            else:
                obfuscated_lines.append(line)
        
        return obfuscated_lines
    
    def obfuscate_echo_statements(self, lines):
        """Break up echo statements with variable concatenation"""
        obfuscated_lines = []
        
        for line in lines:
            # Match echo statements that are simple text
            echo_match = re.match(r'^(\s*)echo\s+([^%!&|<>]+)$', line, re.IGNORECASE)
            
            if echo_match and random.random() < 0.2:
                indent = echo_match.group(1)
                text = echo_match.group(2).strip()
                
                # Sometimes obfuscate by using variables
                if len(text) > 5:
                    obfuscated_lines.append(line)
                else:
                    obfuscated_lines.append(line)
            else:
                obfuscated_lines.append(line)
        
        return obfuscated_lines
    
    def obfuscate(self, content):
        """Apply all obfuscation techniques"""
        # Step 1: Obfuscate variable names
        content = self.obfuscate_variables(content)
        
        # Step 2: Split into lines
        lines = content.split('\n')
        
        # Step 3: Add junk comments
        lines = self.add_junk_comments(lines)
        
        # Step 4: Obfuscate whitespace
        lines = self.obfuscate_whitespace(lines)
        
        # Step 5: Obfuscate echo statements (minimal)
        lines = self.obfuscate_echo_statements(lines)
        
        # Rejoin
        return '\n'.join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python obfuscate.py <input.cmd> [output.cmd]")
        print("\nExample:")
        print("  python obfuscate.py script.cmd obfuscated.cmd")
        print("  python obfuscate.py script.cmd  # Outputs to script_obfuscated.cmd")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    
    if not input_file.exists():
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    
    # Determine output file
    if len(sys.argv) >= 3:
        output_file = Path(sys.argv[2])
    else:
        output_file = input_file.parent / f"{input_file.stem}_obfuscated{input_file.suffix}"
    
    # Read input
    print(f"Reading: {input_file}")
    content = input_file.read_text(encoding='utf-8', errors='ignore')
    
    # Obfuscate
    print("Obfuscating...")
    obfuscator = BatchObfuscator()
    obfuscated_content = obfuscator.obfuscate(content)
    
    # Write output
    output_file.write_text(obfuscated_content, encoding='utf-8')
    print(f"Done! Output saved to: {output_file}")
    print(f"\nObfuscation Summary:")
    print(f"  Variables renamed: {len(obfuscator.var_map)}")
    print(f"  Techniques applied:")
    print(f"    - Variable name obfuscation")
    print(f"    - Junk comment injection")
    print(f"    - Whitespace manipulation")


if __name__ == "__main__":
    main()
