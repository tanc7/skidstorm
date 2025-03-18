import random
import textwrap
import re

# Generates random attack campaign key
import secrets

def generate_char_array(input_str, var_name="data"):
    length = len(input_str) + 1  # +1 for null terminator
    c_array = f'char {var_name}[{length}] = "{input_str}";'
    return c_array
def generate_random_hex(length=64):
    return secrets.token_hex(length // 2)  # token_hex gives 2 chars per byte

random_str = generate_random_hex()
CAMPAIGN_KEY = generate_char_array(random_str)


# MSVC Intrinsics Compatible Headers
INCLUDE_HEADERS = textwrap.dedent("""
#include <intrin.h>
#include <immintrin.h>
#include <cstdlib>
""")

# MSVC-Compatible 64-bit ROP Gadgets
ROP_GADGETS = [
    "__nop(); _mm_pause();",
    "__m128i t{0} = _mm_set1_epi32(0x42); _mm_storeu_si128(reinterpret_cast<__m128i*>(&t{0}), _mm_xor_si128(t{0}, t{0}));",
    "__m128i t{0} = _mm_setzero_si128(); _mm_aesimc_si128(t{0});",
    "_mm_prefetch(reinterpret_cast<const char*>(0xBEEF), _MM_HINT_T0);",
    "__nop(); __nop(); _mm_pause();",
    "__m128i t{0} = _mm_set1_epi16(0x1234); _mm_stream_si128(reinterpret_cast<__m128i*>(&t{0}), t{0});"
]

# Complex Control Flow Flattening Loops
#CFF_FUNCTIONS = [
 #   "int x{0} = rand() % 20; switch (x{0}) { case 0: x{0} += 2; break; case 1: x{0} -= 1; break; case 2: x{0} *= 2; break; case 3: x{0} /= 2; break; case 4: x{0} += 3; break; case 5: x{0} -= 2; break; case 6: x{0} *= 3; break; case 7: x{0} /= 3; break; case 8: x{0} += 4; break; case 9: x{0} -= 3; break; case 10: x{0} *= 4; break; case 11: x{0} /= 4; break; case 12: x{0} += 5; break; case 13: x{0} -= 4; break; case 14: x{0} *= 5; break; case 15: x{0} /= 5; break; case 16: x{0} += 6; break; case 17: x{0} -= 5; break; case 18: x{0} *= 6; break; case 19: x{0} /= 6; break; default: x{0} += 7; break; }",
 #   "int x{0} = rand() % 20; switch (x{0}) { case 0: x{0} += 3; break; case 1: x{0} -= 2; break; case 2: x{0} *= 3; break; case 3: x{0} /= 3; break; case 4: x{0} += 4; break; case 5: x{0} -= 3; break; case 6: x{0} *= 4; break; case 7: x{0} /= 4; break; case 8: x{0} += 5; break; case 9: x{0} -= 4; break; case 10: x{0} *= 5; break; case 11: x{0} /= 5; break; case 12: x{0} += 6; break; case 13: x{0} -= 5; break; case 14: x{0} *= 6; break; case 15: x{0} /= 6; break; case 16: x{0} += 7; break; case 17: x{0} -= 6; break; case 18: x{0} *= 7; break; case 19: x{0} /= 7; break; default: x{0} += 8; break; }",
 #   "int x{0} = rand() % 20; switch (x{0}) { case 0: x{0} += 4; break; case 1: x{0} -= 3; break; case 2: x{0} *= 4; break; case 3: x{0} /= 4; break; case 4: x{0} += 5; break; case 5: x{0} -= 4; break; case 6: x{0} *= 5; break; case 7: x{0} /= 5; break; case 8: x{0} += 6; break; case 9: x{0} -= 5; break; case 10: x{0} *= 6; break; case 11: x{0} /= 6; break; case 12: x{0} += 7; break; case 13: x{0} -= 6; break; case 14: x{0} *= 7; break; case 15: x{0} /= 7; break; case 16: x{0} += 8; break; case 17: x{0} -= 7; break; case 18: x{0} *= 8; break; case 19: x{0} /= 8; break; default: x{0} += 9; break; }",
 #   "int x{0} = rand() % 20; switch (x{0}) { case 0: x{0} += 5; break; case 1: x{0} -= 4; break; case 2: x{0} *= 5; break; case 3: x{0} /= 5; break; case 4: x{0} += 6; break; case 5: x{0} -= 5; break; case 6: x{0} *= 6; break; case 7: x{0} /= 6; break; case 8: x{0} += 7; break; case 9: x{0} -= 6; break; case 10: x{0} *= 7; break; case 11: x{0} /= 7; break; case 12: x{0} += 8; break; case 13: x{0} -= 7; break; case 14: x{0} *= 8; break; case 15: x{0} /= 8; break; case 16: x{0} += 9; break; case 17: x{0} -= 8; break; case 18: x{0} *= 9; break; case 19: x{0} /= 9; break; default: x{0} += 10; break; }",
 #   "int x{0} = rand() % 20; switch (x{0}) { case 0: x{0} += 6; break; case 1: x{0} -= 5; break; case 2: x{0} *= 6; break; case 3: x{0} /= 6; break; case 4: x{0} += 7; break; case 5: x{0} -= 6; break; case 6: x{0} *= 7; break; case 7: x{0} /= 7; break; case 8: x{0} += 8; break; case 9: x{0} -= 7; break; case 10: x{0} *= 8; break; case 11: x{0} /= 8; break; case 12: x{0} += 9; break; case 13: x{0} -= 8; break; case 14: x{0} *= 9; break; case 15: x{0} /= 9; break; case 16: x{0} += 10; break; case 17: x{0} -= 9; break; case 18: x{0} *= 10; break; case 19: x{0} /= 10; break; default: x{0} += 11; break; }",
#]
#CFF_FUNCTIONS = [
#    "int x{{0}} = rand() % 20; switch (x{{0}}) {{ case 0: x{{0}} += 2; break; case 1: x{{0}} -= 1; break; case 2: x{{0}} *= 2; break; case 3: x{{0}} /= 2; break; case 4: x{{0}} += 3; break; case 5: x{{0}} -= 2; break; case 6: x{{0}} *= 3; break; case 7: x{{0}} /= 3; break; case 8: x{{0}} += 4; break; case 9: x{{0}} -= 3; break; case 10: x{{0}} *= 4; break; case 11: x{{0}} /= 4; break; case 12: x{{0}} += 5; break; case 13: x{{0}} -= 4; break; case 14: x{{0}} *= 5; break; case 15: x{{0}} /= 5; break; case 16: x{{0}} += 6; break; case 17: x{{0}} -= 5; break; case 18: x{{0}} *= 6; break; case 19: x{{0}} /= 6; break; default: x{{0}} += 7; break; }}",
#    "int x{{0}} = rand() % 20; switch (x{{0}}) {{ case 0: x{{0}} += 3; break; case 1: x{{0}} -= 2; break; case 2: x{{0}} *= 3; break; case 3: x{{0}} /= 3; break; case 4: x{{0}} += 4; break; case 5: x{{0}} -= 3; break; case 6: x{{0}} *= 4; break; case 7: x{{0}} /= 4; break; case 8: x{{0}} += 5; break; case 9: x{{0}} -= 4; break; case 10: x{{0}} *= 5; break; case 11: x{{0}} /= 5; break; case 12: x{{0}} += 6; break; case 13: x{{0}} -= 5; break; case 14: x{{0}} *= 6; break; case 15: x{{0}} /= 6; break; case 16: x{{0}} += 7; break; case 17: x{{0}} -= 6; break; case 18: x{{0}} *= 7; break; case 19: x{{0}} /= 7; break; default: x{{0}} += 8; break; }}",
#    "int x{{0}} = rand() % 20; switch (x{{0}}) {{ case 0: x{{0}} += 4; break; case 1: x{{0}} -= 3; break; case 2: x{{0}} *= 4; break; case 3: x{{0}} /= 4; break; case 4: x{{0}} += 5; break; case 5: x{{0}} -= 4; break; case 6: x{{0}} *= 5; break; case 7: x{{0}} /= 5; break; case 8: x{{0}} += 6; break; case 9: x{{0}} -= 5; break; case 10: x{{0}} *= 6; break; case 11: x{{0}} /= 6; break; case 12: x{{0}} += 7; break; case 13: x{{0}} -= 6; break; case 14: x{{0}} *= 7; break; case 15: x{{0}} /= 7; break; case 16: x{{0}} += 8; break; case 17: x{{0}} -= 7; break; case 18: x{{0}} *= 8; break; case 19: x{{0}} /= 8; break; default: x{{0}} += 9; break; }}",
#    "int x{{0}} = rand() % 20; switch (x{{0}}) {{ case 0: x{{0}} += 5; break; case 1: x{{0}} -= 4; break; case 2: x{{0}} *= 5; break; case 3: x{{0}} /= 5; break; case 4: x{{0}} += 6; break; case 5: x{{0}} -= 5; break; case 6: x{{0}} *= 6; break; case 7: x{{0}} /= 6; break; case 8: x{{0}} += 7; break; case 9: x{{0}} -= 6; break; case 10: x{{0}} *= 7; break; case 11: x{{0}} /= 7; break; case 12: x{{0}} += 8; break; case 13: x{{0}} -= 7; break; case 14: x{{0}} *= 8; break; case 15: x{{0}} /= 8; break; case 16: x{{0}} += 9; break; case 17: x{{0}} -= 8; break; case 18: x{{0}} *= 9; break; case 19: x{{0}} /= 9; break; default: x{{0}} += 10; break; }}",
#    "int x{{0}} = rand() % 20; switch (x{{0}}) {{ case 0: x{{0}} += 6; break; case 1: x{{0}} -= 5; break; case 2: x{{0}} *= 6; break; case 3: x{{0}} /= 6; break; case 4: x{{0}} += 7; break; case 5: x{{0}} -= 6; break; case 6: x{{0}} *= 7; break; case 7: x{{0}} /= 7; break; case 8: x{{0}} += 8; break; case 9: x{{0}} -= 7; break; case 10: x{{0}} *= 8; break; case 11: x{{0}} /= 8; break; case 12: x{{0}} += 9; break; case 13: x{{0}} -= 8; break; case 14: x{{0}} *= 9; break; case 15: x{{0}} /= 9; break; case 16: x{{0}} += 10; break; case 17: x{{0}} -= 9; break; case 18: x{{0}} *= 10; break; case 19: x{{0}} /= 10; break; default: x{{0}} += 11; break; }}",
#]
CFF_FUNCTIONS = [
    "int x{0} = rand() % 20; switch (x{0}) {{ case 0: x{0} += 2; break; case 1: x{0} -= 1; break; case 2: x{0} *= 2; break; case 3: x{0} /= 2; break; case 4: x{0} += 3; break; case 5: x{0} -= 2; break; case 6: x{0} *= 3; break; case 7: x{0} /= 3; break; case 8: x{0} += 4; break; case 9: x{0} -= 3; break; case 10: x{0} *= 4; break; case 11: x{0} /= 4; break; case 12: x{0} += 5; break; case 13: x{0} -= 4; break; case 14: x{0} *= 5; break; case 15: x{0} /= 5; break; case 16: x{0} += 6; break; case 17: x{0} -= 5; break; case 18: x{0} *= 6; break; case 19: x{0} /= 6; break; default: x{0} += 7; break; }}",
    "int x{0} = rand() % 20; switch (x{0}) {{ case 0: x{0} += 3; break; case 1: x{0} -= 2; break; case 2: x{0} *= 3; break; case 3: x{0} /= 3; break; case 4: x{0} += 4; break; case 5: x{0} -= 3; break; case 6: x{0} *= 4; break; case 7: x{0} /= 4; break; case 8: x{0} += 5; break; case 9: x{0} -= 4; break; case 10: x{0} *= 5; break; case 11: x{0} /= 5; break; case 12: x{0} += 6; break; case 13: x{0} -= 5; break; case 14: x{0} *= 6; break; case 15: x{0} /= 6; break; case 16: x{0} += 7; break; case 17: x{0} -= 6; break; case 18: x{0} *= 7; break; case 19: x{0} /= 7; break; default: x{0} += 8; break; }}",
    "int x{0} = rand() % 20; switch (x{0}) {{ case 0: x{0} += 4; break; case 1: x{0} -= 3; break; case 2: x{0} *= 4; break; case 3: x{0} /= 4; break; case 4: x{0} += 5; break; case 5: x{0} -= 4; break; case 6: x{0} *= 5; break; case 7: x{0} /= 5; break; case 8: x{0} += 6; break; case 9: x{0} -= 5; break; case 10: x{0} *= 6; break; case 11: x{0} /= 6; break; case 12: x{0} += 7; break; case 13: x{0} -= 6; break; case 14: x{0} *= 7; break; case 15: x{0} /= 7; break; case 16: x{0} += 8; break; case 17: x{0} -= 7; break; case 18: x{0} *= 8; break; case 19: x{0} /= 8; break; default: x{0} += 9; break; }}",
    "int x{0} = rand() % 20; switch (x{0}) {{ case 0: x{0} += 5; break; case 1: x{0} -= 4; break; case 2: x{0} *= 5; break; case 3: x{0} /= 5; break; case 4: x{0} += 6; break; case 5: x{0} -= 5; break; case 6: x{0} *= 6; break; case 7: x{0} /= 6; break; case 8: x{0} += 7; break; case 9: x{0} -= 6; break; case 10: x{0} *= 7; break; case 11: x{0} /= 7; break; case 12: x{0} += 8; break; case 13: x{0} -= 7; break; case 14: x{0} *= 8; break; case 15: x{0} /= 8; break; case 16: x{0} += 9; break; case 17: x{0} -= 8; break; case 18: x{0} *= 9; break; case 19: x{0} /= 9; break; default: x{0} += 10; break; }}",
    "int x{0} = rand() % 20; switch (x{0}) {{ case 0: x{0} += 6; break; case 1: x{0} -= 5; break; case 2: x{0} *= 6; break; case 3: x{0} /= 6; break; case 4: x{0} += 7; break; case 5: x{0} -= 6; break; case 6: x{0} *= 7; break; case 7: x{0} /= 7; break; case 8: x{0} += 8; break; case 9: x{0} -= 7; break; case 10: x{0} *= 8; break; case 11: x{0} /= 8; break; case 12: x{0} += 9; break; case 13: x{0} -= 8; break; case 14: x{0} *= 9; break; case 15: x{0} /= 9; break; case 16: x{0} += 10; break; case 17: x{0} -= 9; break; case 18: x{0} *= 10; break; case 19: x{0} /= 10; break; default: x{0} += 11; break; }}",
]

# Generate a unique six-digit number
get_unique_id = lambda: random.randint(100000, 999999)

# Replace Placeholders for ROP and CFF with Unique Variable Names
def insert_rop_and_cff(line):
    if "//ROP64" in line:
        unique_id = get_unique_id()
        rop_gadget = random.choice(ROP_GADGETS).format(*([unique_id] * 6))
        return line.replace("//ROP64", rop_gadget)
    elif "//CFF" in line:
        unique_id = get_unique_id()
        cff_code = random.choice(CFF_FUNCTIONS).format(*([unique_id] * 5))
        return line.replace("//CFF", cff_code)
    return line

# Ensure variable renaming for existing 'x' and 't'
def rename_variables(line):
    line = re.sub(r'\b(x|t)\b', lambda m: f"{m.group(1)}{get_unique_id()}", line)
    return line

# Process Input C++ File
def process_cpp_file(input_file, output_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
    
    with open(output_file, 'w') as outfile:
        outfile.write(INCLUDE_HEADERS + '\n' + CAMPAIGN_KEY + '\n')
        for line in lines:
            line = rename_variables(line)  # Ensure all 'x' and 't' have unique names
            line = insert_rop_and_cff(line)  # Replace ROP and CFF placeholders
            outfile.write(line + '\n')

if __name__ == "__main__":
    process_cpp_file("xorshellcoderunner.c", "obfuscated_shellcoderunner.c")
    print("Obfuscation complete: obfuscated_shellcoderunner.c")
    print("Compile with: cl.exe /nologo /Od /Ob0 /Oy- /MT /W0 /GS- /Tp obfuscated_shellcoderunner.c /link /OUT:obfuscated_implant.exe /SUBSYSTEM:CONSOLE")

