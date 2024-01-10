import subprocess
import ast

def deobfuscate_pyarmor(obfuscated_file, deobfuscated_file):
    # Ścieżka do narzędzia PyArmorDeobfuscator.py
    pyarmor_deobfuscator_path = 'path/to/PyArmorDeobfuscator.py'

    # Uruchomienie narzędzia PyArmorDeobfuscator.py
    command = [
        'python', pyarmor_deobfuscator_path,
        '-f', obfuscated_file,
        '-o', deobfuscated_file
    ]

    try:
        result = subprocess.run(command, capture_output=True, check=True, text=True)
        print(result.stdout)
        print(f"[+] Deobfuscation successful. Deobfuscated code saved to {deobfuscated_file} [+]")
    except subprocess.CalledProcessError as e:
        print(f"[-] Deobfuscation failed. Error: {e.stderr} [-")



def analyze_python_code(script_path):
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

        elif isinstance(node, ast.Assign):
            print("Znaleziono przypisanie wartości:")
            for target in node.targets:
                if isinstance(target, ast.Name):
                    print(f"  Zmienna: {target.id}")

        elif isinstance(node, ast.Import):
            print("Znaleziono import:")
            for alias in node.names:
                print(f"  Moduł: {alias.name}")

        elif isinstance(node, ast.ImportFrom):
            print("Znaleziono import z modułu:")
            print(f"  Moduł: {node.module}")
            for alias in node.names:
                print(f"  Element: {alias.name}")

