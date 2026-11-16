import sys
from pathlib import Path

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker

from BabyDuckLexer import BabyDuckLexer
from BabyDuckParser import BabyDuckParser
from SemanticAnalyzer import SemanticAnalyzer
from FunctionCollector import FunctionCollector
from QuadrupleGenerator import QuadrupleGenerator


def main():

    # Obtener el archivo de entrada
    if len(sys.argv) > 1:
        archivo = Path(sys.argv[1])
    else:
        archivo = Path(__file__).parent / "prueba.txt"

    # Leer el código fuente
    try:
        codigo = archivo.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo {archivo}")
        return

    # 1. Lexer: convierte el código en tokens
    input_stream = InputStream(codigo)
    lexer = BabyDuckLexer(input_stream)

    # 2. Parser: construye el árbol sintáctico
    tokens = CommonTokenStream(lexer)
    parser = BabyDuckParser(tokens)
    tree = parser.programa()

    # 3. Análisis semántico
        
    if parser.getNumberOfSyntaxErrors() == 0:

        print("Programa analizado correctamente.")

        walker = ParseTreeWalker()

        # Primer recorrido: registrar todas las funciones
        collector = FunctionCollector()
        walker.walk(collector, tree)

        # Segundo recorrido: realizar el análisis semántico
        analyzer = SemanticAnalyzer(
            collector.directory,
            collector.valid_function_contexts
        )
        walker.walk(analyzer, tree)

        # Combinar errores de ambos recorridos
        analyzer.errors = collector.errors + analyzer.errors

        # Mostrar variables y funciones
        print("\nVariables globales:")
        print(analyzer.directory.global_table.symbols)

        print("\nFunciones:")
        print(analyzer.directory.functions.keys())

        for nombre, info in analyzer.directory.functions.items():
            print(f"\nVariables locales de {nombre}:")
            print(info["local_table"].symbols)

        # Mostrar errores semánticos
        print("\nErrores semánticos:")

        if analyzer.errors:
            for error in analyzer.errors:
                print(error)

        else:
            print("No se encontraron errores semánticos.")

            # Tercer recorrido: generar cuádruplos
            generator = QuadrupleGenerator(analyzer.directory)
            walker.walk(generator, tree)

            print("\nCuádruplos generados:")

            for i, quad in enumerate(generator.Quad.get_all(), start=1):
                print(f"{i}. {quad}")

            if generator.errors:
                print("\nErrores durante la generación:")
                for error in generator.errors:
                    print(error)

    else:
        print("El programa contiene errores de sintaxis.")

if __name__ == "__main__":
    main()