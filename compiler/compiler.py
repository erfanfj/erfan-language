import os
import shutil
import subprocess
import sys
import tempfile

from erfan_ast.nodes import (
    Program,
    Assignment,
    Identifier,
    Number,
    Float,
    String,
    Boolean,
    Null,
    BinaryOperation,
    UnaryOperation,
    FunctionCall,
    Block,
    IfStatement,
    FunctionDef,
    ReturnStatement,
    ClassDef,
    This,
    MemberAccess,
    MethodCall,
)


class CodeGenerator:

    def __init__(self):
        self.lines = []
        self.indent = 0
        self.in_method = False

    def emit(self, line=""):
        self.lines.append(" " * 4 * self.indent + line)

    def visit(self, node):
        method = getattr(self, f"visit_{type(node).__name__}")
        return method(node)

    def visit_Program(self, node):
        for statement in node.statements:
            self.visit(statement)

    def assignment_target(self, target):
        if isinstance(target, Identifier):
            return target.name

        if isinstance(target, MemberAccess):
            return f"{self.visit_expr(target.object)}.{target.member}"

        raise RuntimeError("Invalid assignment target")

    def visit_Assignment(self, node):
        target = self.assignment_target(node.target)
        value = self.visit_expr(node.value)
        self.emit(f"{target} = {value}")

    def visit_Block(self, node):
        for statement in node.statements:
            self.visit(statement)

    def visit_IfStatement(self, node):
        condition = self.visit_expr(node.condition)
        self.emit(f"if {condition}:")
        self.indent += 1
        self.visit(node.then_block)
        self.indent -= 1

        if node.else_block is not None:
            self.emit("else:")
            self.indent += 1
            self.visit(node.else_block)
            self.indent -= 1

    def visit_ClassDef(self, node):
        self.emit(f"class {node.name}:")
        self.indent += 1

        if not node.methods:
            self.emit("pass")
        else:
            for method in node.methods:
                self.visit_class_method(method)

        self.indent -= 1
        self.emit()

    def visit_class_method(self, node):
        params = ["self"] + node.params
        method_name = "__init__" if node.name == "init" else node.name

        self.emit(f"def {method_name}({', '.join(params)}):")
        self.indent += 1
        self.in_method = True
        self.visit(node.body)
        self.in_method = False
        self.indent -= 1

    def visit_FunctionDef(self, node):
        params = ", ".join(node.params)
        self.emit(f"def {node.name}({params}):")
        self.indent += 1
        self.visit(node.body)
        self.indent -= 1
        self.emit()

    def visit_ReturnStatement(self, node):
        value = self.visit_expr(node.value)
        self.emit(f"return {value}")

    def visit_FunctionCall(self, node):
        code = self.function_call_code(node)
        self.emit(code)

    def visit_MethodCall(self, node):
        code = self.method_call_code(node)
        self.emit(code)

    def function_call_code(self, node):
        args = ", ".join(self.visit_expr(arg) for arg in node.arguments)
        if node.name == "chap":
            return f"print({args})"
        return f"{node.name}({args})"

    def method_call_code(self, node):
        obj = self.visit_expr(node.object)
        args = ", ".join(self.visit_expr(arg) for arg in node.arguments)
        return f"{obj}.{node.method}({args})"

    def visit_expr(self, node):
        if isinstance(node, FunctionCall):
            return self.function_call_code(node)

        if isinstance(node, MethodCall):
            return self.method_call_code(node)

        method = getattr(self, f"visit_{type(node).__name__}")
        return method(node)

    def visit_Number(self, node):
        return str(node.value)

    def visit_Float(self, node):
        return str(node.value)

    def visit_String(self, node):
        return repr(node.value)

    def visit_Boolean(self, node):
        return "True" if node.value else "False"

    def visit_Null(self, node):
        return "None"

    def visit_Identifier(self, node):
        return node.name

    def visit_This(self, node):
        return "self"

    def visit_MemberAccess(self, node):
        obj = self.visit_expr(node.object)
        return f"{obj}.{node.member}"

    def visit_UnaryOperation(self, node):
        operand = self.visit_expr(node.operand)
        if node.operator == "!":
            return f"(not {operand})"
        return f"({node.operator}{operand})"

    def visit_BinaryOperation(self, node):
        left = self.visit_expr(node.left)
        right = self.visit_expr(node.right)
        op = node.operator

        if op == "&&":
            op = "and"
        elif op == "||":
            op = "or"

        return f"({left} {op} {right})"

    def generate(self, tree):
        self.visit(tree)
        return "\n".join(self.lines) + "\n"


class Compiler:

    def compile(self, tree, output):
        generator = CodeGenerator()
        source = generator.generate(tree)

        output = os.path.abspath(output)
        output_dir = os.path.dirname(output)
        os.makedirs(output_dir, exist_ok=True)

        with tempfile.TemporaryDirectory() as temp_dir:
            script_path = os.path.join(temp_dir, "program.py")
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(source)

            build_dir = os.path.join(temp_dir, "pyinstaller_out")
            cmd = [
                sys.executable,
                "-m",
                "PyInstaller",
                "--onefile",
                "--noconfirm",
                "--distpath",
                build_dir,
                "--workpath",
                os.path.join(temp_dir, "work"),
                "--specpath",
                temp_dir,
                "--name",
                os.path.splitext(os.path.basename(output))[0],
                script_path,
            ]

            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=False,
                )
            except FileNotFoundError as exc:
                raise RuntimeError(
                    "PyInstaller is required for runbuild. Install it with: pip install pyinstaller"
                ) from exc

            if result.returncode != 0:
                details = (result.stderr or result.stdout or "").strip()
                raise RuntimeError(
                    f"Failed to build executable.\n{details}"
                )

            built_exe = os.path.join(
                build_dir,
                os.path.splitext(os.path.basename(output))[0]
                + (".exe" if sys.platform == "win32" else ""),
            )

            if not os.path.exists(built_exe):
                raise RuntimeError(f"Build finished but executable was not found: {built_exe}")

            if os.path.exists(output):
                os.remove(output)

            shutil.move(built_exe, output)

        return output
