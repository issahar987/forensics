import subprocess
import ast
from pathlib import Path
import json

current_folder = Path(__file__).parent
download_folder_path = current_folder / 'downloads'
output_path = download_folder_path / 'deobfuscated_script.py'

def expand_shortcuts(node, script_lines):
    if isinstance(node, ast.Import):
        for alias in node.names:
            script_lines[node.lineno - 1] = script_lines[node.lineno - 1].replace(f"import {alias.name}", f"import {alias.name} as {alias.name}_full")
    elif isinstance(node, ast.ImportFrom):
        for alias in node.names:
            script_lines[node.lineno - 1] = script_lines[node.lineno - 1].replace(f"from {node.module} import {alias.name}", f"from {node.module} import {alias.name} as {alias.name}_full")


def expand_assign_aliases(node, script_lines):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                target_id = target.id
                script_lines[node.lineno - 1] = script_lines[node.lineno - 1].replace(f"{target_id} =", f"{target_id}_full =")


def remove_unused_code(node, script_lines):
    if isinstance(node, ast.Expr):
        script_lines[node.lineno - 1] = "# Removed: " + script_lines[node.lineno - 1]


def expand_function_shortcuts(node, script_lines):
    if isinstance(node, ast.FunctionDef):
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == 'some_decorator':
                node.name = f"{node.name}_full"


def deobfuscate_python_code(script_path, output_path):
    with open(script_path, 'r') as file:
        script_lines = file.readlines()

    tree = ast.parse(''.join(script_lines))

    for node in ast.walk(tree):
        expand_shortcuts(node, script_lines)
        expand_assign_aliases(node, script_lines)
        remove_unused_code(node, script_lines)
        expand_function_shortcuts(node, script_lines)

    with open(output_path, 'w') as output_file:
        output_file.writelines(script_lines)


def analyze_python_code(script_path):
    ast_results = {
        'functions': [],
        'assignments': [],
        'imports': [],
        'imports_from': []
    }
    with open(script_path, 'r') as file:
        source_code = file.read()

    # Analiza składniowa
    tree = ast.parse(source_code)

    # Przeglądanie drzewa składniowego
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            print(f"Znaleziono definicję funkcji: {node.name}")
            print(f"  Linie: {node.lineno}-{node.end_lineno}")

            # Analiza argumentów funkcji
            arguments = [arg.arg for arg in node.args.args]
            print(f"  Argumenty: {', '.join(arguments)}")
            function_info = {
                'name': node.name,
                'lines': f"{node.lineno}-{node.end_lineno}",
                'arguments': [arg.arg for arg in node.args.args]
            }
            ast_results['functions'].append(function_info)

        elif isinstance(node, ast.Assign):
            print("Znaleziono przypisanie wartości:")
            for target in node.targets:
                if isinstance(target, ast.Name):
                    print(f"  Zmienna: {target.id}")
            assignment_info = {
                'targets': [target.id for target in node.targets]
            }
            ast_results['assignments'].append(assignment_info)

        elif isinstance(node, ast.Import):
            print("Znaleziono import:")
            for alias in node.names:
                print(f"  Moduł: {alias.name}")
            import_info = {
                'modules': [alias.name for alias in node.names]
            }
            ast_results['imports'].append(import_info)

        elif isinstance(node, ast.ImportFrom):
            print("Znaleziono import z modułu:")
            print(f"  Moduł: {node.module}")
            for alias in node.names:
                print(f"  Element: {alias.name}")
            import_from_info = {
                'module': node.module,
                'elements': [alias.name for alias in node.names]
            }
            ast_results['imports_from'].append(import_from_info)
    # with open(Path(__file__).parent / 'downloads' / 'result_AST.json', 'w') as ast_json_file:
    #         json.dump(ast_results, ast_json_file, indent=4)
    return ast_results

