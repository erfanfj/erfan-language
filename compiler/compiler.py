from compiler.packer import pack_executable
from compiler.runtime import ensure_runtime


class Compiler:

    def compile(self, source_code, output):
        runtime = ensure_runtime()
        return pack_executable(runtime, source_code, output)
