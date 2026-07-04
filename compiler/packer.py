import os

MAGIC = b"ERFAN\x00"


def pack_executable(stub_path, source_code, output_path):
    with open(stub_path, "rb") as handle:
        stub_bytes = handle.read()

    source_bytes = source_code.encode("utf-8")
    payload = MAGIC + len(source_bytes).to_bytes(4, "little") + source_bytes

    output_dir = os.path.dirname(os.path.abspath(output_path))
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "wb") as handle:
        handle.write(stub_bytes + payload)

    return output_path
