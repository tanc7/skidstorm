import random
import textwrap
import re

# MSVC Intrinsics Compatible Headers
INCLUDE_HEADERS = textwrap.dedent("""
#include <intrin.h>
#include <immintrin.h>
#include <cstdlib>
#define _INTERLOCKED_INTRINSICS_SUPPORTED
#define _AMD64_  // Force expose 64-bit intrinsic prototypes if needed
char data[64] = "592ea92cef33d0206701e0d5bb2f8880eea5653a71e0e8aaa0bd8ed90763c91";

""")

# MSVC-Compatible 64-bit ROP Gadgets
ROP_GADGETS = [
    "volatile __int64 t{0} = 0;_InterlockedOr64(&t{0}, 0xDEADBEEF); _InterlockedAnd64(&t{0}, 0xFF); __writegsqword(0x8, __readgsqword(0x8)); _mm_clflush(&data); _mm_sfence();",
    "volatile __int64 t{0} = 0;_mm_pause(); _mm_clflush(&data); _mm_sfence(); __writegsqword(0x8, __readgsqword(0x8));",
    "volatile __int64 t{0} = 0;_InterlockedAnd64(&t{0}, 0xFF); _InterlockedOr64(&t{0}, 0xDEADBEEF); _InterlockedCompareExchange64(&t{0}, 1, 0); _ReadWriteBarrier();",
    "volatile __int64 t{0} = 0;_mm_mfence(); _InterlockedCompareExchange64(&t{0}, 1, 0); _mm_clflush(&data); _mm_sfence(); _mm_pause();",
    "volatile __int64 t{0} = 0;_InterlockedXor64(&t{0}, 0xAA); _InterlockedCompareExchange64(&t{0}, 1, 0); _mm_mfence(); _ReadWriteBarrier(); _mm_clflush(&data); _InterlockedAnd64(&t{0}, 0xFF);",
    "volatile __int64 t{0} = 0;_InterlockedOr64(&t{0}, 0xDEADBEEF); _mm_sfence(); _mm_clflush(&data); _InterlockedCompareExchange64(&t{0}, 1, 0); __writegsqword(0x8, __readgsqword(0x8));",
    "volatile __int64 t{0} = 0;_InterlockedCompareExchange64(&t{0}, 1, 0); _InterlockedXor64(&t{0}, 0xAA); _mm_lfence(); _mm_sfence(); __writegsqword(0x8, __readgsqword(0x8));",
    "volatile __int64 t{0} = 0;_ReadWriteBarrier(); _mm_sfence(); _InterlockedCompareExchange64(&t{0}, 1, 0); _InterlockedExchange64(&t{0}, 1); _InterlockedIncrement64(&t{0}); _mm_lfence();",
    "volatile __int64 t{0} = 0;_mm_pause(); _mm_lfence(); _ReadWriteBarrier(); _InterlockedIncrement64(&t{0});",
    "volatile __int64 t{0} = 0;_InterlockedAnd64(&t{0}, 0xFF); _mm_lfence(); _InterlockedOr64(&t{0}, 0xDEADBEEF); _mm_mfence(); _ReadWriteBarrier(); _InterlockedIncrement64(&t{0});",
    "volatile __int64 t{0} = 0;_mm_pause(); _mm_sfence(); __writegsqword(0x8, __readgsqword(0x8)); _InterlockedIncrement64(&t{0}); _InterlockedAnd64(&t{0}, 0xFF);",
    "volatile __int64 t{0} = 0;_InterlockedAnd64(&t{0}, 0xFF); _mm_pause(); _ReadWriteBarrier(); __writegsqword(0x8, __readgsqword(0x8)); _mm_sfence();",
    "volatile __int64 t{0} = 0;_mm_sfence(); _InterlockedOr64(&t{0}, 0xDEADBEEF); _ReadWriteBarrier(); _InterlockedCompareExchange64(&t{0}, 1, 0); _mm_mfence(); _InterlockedXor64(&t{0}, 0xAA);",
    "volatile __int64 t{0} = 0;_ReadWriteBarrier(); __writegsqword(0x8, __readgsqword(0x8)); _mm_sfence(); _InterlockedXor64(&t{0}, 0xAA); _mm_clflush(&data);",
    "volatile __int64 t{0} = 0;_mm_clflush(&data); _mm_mfence(); _ReadWriteBarrier(); _InterlockedXor64(&t{0}, 0xAA); _mm_pause(); _InterlockedExchange64(&t{0}, 1);",
    "volatile __int64 t{0} = 0;_mm_sfence(); _mm_lfence(); _InterlockedIncrement64(&t{0}); _InterlockedOr64(&t{0}, 0xDEADBEEF); _mm_mfence();",
    "volatile __int64 t{0} = 0;_mm_lfence(); _InterlockedXor64(&t{0}, 0xAA); _InterlockedCompareExchange64(&t{0}, 1, 0); _mm_mfence(); _mm_pause();",
    "volatile __int64 t{0} = 0;_InterlockedIncrement64(&t{0}); _ReadWriteBarrier(); __writegsqword(0x8, __readgsqword(0x8)); _mm_clflush(&data);",
    "volatile __int64 t{0} = 0;_InterlockedAnd64(&t{0}, 0xFF); _InterlockedXor64(&t{0}, 0xAA); _InterlockedExchange64(&t{0}, 1); _mm_sfence(); _InterlockedCompareExchange64(&t{0}, 1, 0);",
    "volatile __int64 t{0} = 0;__writegsqword(0x8, __readgsqword(0x8)); _InterlockedAnd64(&t{0}, 0xFF); _mm_mfence(); _InterlockedCompareExchange64(&t{0}, 1, 0);",
    "volatile __int64 t{0} = 0;_mm_lfence(); _InterlockedIncrement64(&t{0}); _InterlockedOr64(&t{0}, 0xDEADBEEF); _mm_pause(); _InterlockedExchange64(&t{0}, 1); _mm_sfence();",
    "volatile __int64 t{0} = 0;_ReadWriteBarrier(); _InterlockedCompareExchange64(&t{0}, 1, 0); _mm_sfence(); _mm_clflush(&data);",
    "volatile __int64 t{0} = 0;_InterlockedAnd64(&t{0}, 0xFF); _ReadWriteBarrier(); _InterlockedCompareExchange64(&t{0}, 1, 0); _mm_lfence(); _InterlockedXor64(&t{0}, 0xAA);",
    "volatile __int64 t{0} = 0;_mm_pause(); _InterlockedCompareExchange64(&t{0}, 1, 0); _InterlockedIncrement64(&t{0}); _mm_sfence(); _ReadWriteBarrier(); _InterlockedExchange64(&t{0}, 1);",
    "volatile __int64 t{0} = 0;_ReadWriteBarrier(); _InterlockedOr64(&t{0}, 0xDEADBEEF); _InterlockedExchange64(&t{0}, 1); _mm_lfence(); _InterlockedCompareExchange64(&t{0}, 1, 0);",
    "volatile __int64 t{0} = 0;__writegsqword(0x8, __readgsqword(0x8)); _InterlockedExchange64(&t{0}, 1); _ReadWriteBarrier(); _mm_pause(); _InterlockedXor64(&t{0}, 0xAA);",
    "volatile __int64 t{0} = 0;_InterlockedCompareExchange64(&t{0}, 1, 0); _ReadWriteBarrier(); _mm_clflush(&data); _InterlockedExchange64(&t{0}, 1); __writegsqword(0x8, __readgsqword(0x8));",
    "volatile __int64 t{0} = 0;__writegsqword(0x8, __readgsqword(0x8)); _mm_sfence(); _InterlockedAnd64(&t{0}, 0xFF); _mm_clflush(&data); _InterlockedExchange64(&t{0}, 1); _ReadWriteBarrier();",
    "volatile __int64 t{0} = 0;_mm_sfence(); _InterlockedIncrement64(&t{0}); _InterlockedCompareExchange64(&t{0}, 1, 0); __writegsqword(0x8, __readgsqword(0x8));",
    "volatile __int64 t{0} = 0;_InterlockedAnd64(&t{0}, 0xFF); _mm_mfence(); _InterlockedOr64(&t{0}, 0xDEADBEEF); _mm_pause();",
    "volatile __int64 t{0} = 0;_InterlockedXor64(&t{0}, 0xAA); _InterlockedExchange64(&t{0}, 1); _InterlockedCompareExchange64(&t{0}, 1, 0); _mm_sfence();",
    "volatile __int64 t{0} = 0;_mm_mfence(); _mm_sfence(); _mm_pause(); _InterlockedCompareExchange64(&t{0}, 1, 0);",
    "volatile __int64 t{0} = 0;_InterlockedAnd64(&t{0}, 0xFF); _InterlockedOr64(&t{0}, 0xDEADBEEF); _mm_mfence(); _mm_sfence(); _mm_lfence();",
    "volatile __int64 t{0} = 0;_mm_pause(); _mm_sfence(); _InterlockedOr64(&t{0}, 0xDEADBEEF); _InterlockedCompareExchange64(&t{0}, 1, 0); _InterlockedIncrement64(&t{0});",
    "volatile __int64 t{0} = 0;_mm_mfence(); _InterlockedXor64(&t{0}, 0xAA); _mm_sfence(); _ReadWriteBarrier(); _InterlockedAnd64(&t{0}, 0xFF); _InterlockedIncrement64(&t{0});",
    "volatile __int64 t{0} = 0;_InterlockedCompareExchange64(&t{0}, 1, 0); _mm_clflush(&data); _mm_pause(); _mm_mfence(); _InterlockedXor64(&t{0}, 0xAA);",
    "volatile __int64 t{0} = 0;_InterlockedOr64(&t{0}, 0xDEADBEEF); _InterlockedAnd64(&t{0}, 0xFF); _mm_lfence(); _InterlockedExchange64(&t{0}, 1); _mm_sfence(); _InterlockedCompareExchange64(&t{0}, 1, 0);",
    "volatile __int64 t{0} = 0;_ReadWriteBarrier(); _InterlockedIncrement64(&t{0}); _InterlockedOr64(&t{0}, 0xDEADBEEF); _InterlockedXor64(&t{0}, 0xAA); _mm_mfence();",
    "volatile __int64 t{0} = 0;_mm_lfence(); _InterlockedCompareExchange64(&t{0}, 1, 0); _InterlockedXor64(&t{0}, 0xAA); _InterlockedExchange64(&t{0}, 1); _InterlockedIncrement64(&t{0}); _InterlockedOr64(&t{0}, 0xDEADBEEF);",
    "volatile __int64 t{0} = 0;_mm_lfence(); _InterlockedAnd64(&t{0}, 0xFF); _mm_mfence(); _mm_pause();",
    "volatile __int64 t{0} = 0;_mm_pause(); _InterlockedIncrement64(&t{0}); __writegsqword(0x8, __readgsqword(0x8)); _mm_clflush(&data); _InterlockedOr64(&t{0}, 0xDEADBEEF);",
    "volatile __int64 t{0} = 0;_InterlockedAnd64(&t{0}, 0xFF); _mm_sfence(); _InterlockedXor64(&t{0}, 0xAA); _InterlockedIncrement64(&t{0}); _InterlockedCompareExchange64(&t{0}, 1, 0); _mm_lfence();",
    "volatile __int64 t{0} = 0;_mm_pause(); __writegsqword(0x8, __readgsqword(0x8)); _InterlockedIncrement64(&t{0}); _InterlockedXor64(&t{0}, 0xAA); _InterlockedExchange64(&t{0}, 1);",
    "volatile __int64 t{0} = 0;_InterlockedExchange64(&t{0}, 1); _InterlockedOr64(&t{0}, 0xDEADBEEF); _ReadWriteBarrier(); _InterlockedXor64(&t{0}, 0xAA); _mm_mfence();",
    "volatile __int64 t{0} = 0;_InterlockedOr64(&t{0}, 0xDEADBEEF); _InterlockedExchange64(&t{0}, 1); _mm_pause(); _InterlockedAnd64(&t{0}, 0xFF); _InterlockedCompareExchange64(&t{0}, 1, 0);",
    "volatile __int64 t{0} = 0;_InterlockedIncrement64(&t{0}); __writegsqword(0x8, __readgsqword(0x8)); _mm_lfence(); _mm_sfence(); _InterlockedAnd64(&t{0}, 0xFF);",
    "volatile __int64 t{0} = 0;_InterlockedXor64(&t{0}, 0xAA); __writegsqword(0x8, __readgsqword(0x8)); _InterlockedOr64(&t{0}, 0xDEADBEEF); _InterlockedCompareExchange64(&t{0}, 1, 0); _mm_mfence();",
    "volatile __int64 t{0} = 0;_mm_clflush(&data); _ReadWriteBarrier(); _mm_sfence(); _InterlockedAnd64(&t{0}, 0xFF); __writegsqword(0x8, __readgsqword(0x8));",
    "volatile __int64 t{0} = 0;_mm_clflush(&data); __writegsqword(0x8, __readgsqword(0x8)); _InterlockedOr64(&t{0}, 0xDEADBEEF); _InterlockedIncrement64(&t{0}); _mm_mfence(); _InterlockedCompareExchange64(&t{0}, 1, 0);",
    "volatile __int64 t{0} = 0;_InterlockedAnd64(&t{0}, 0xFF); _mm_pause(); __writegsqword(0x8, __readgsqword(0x8)); _mm_clflush(&data); _mm_mfence(); _InterlockedXor64(&t{0}, 0xAA);",
    "volatile __int64 t{0} = 0;_InterlockedExchange64(&t{0}, 1); _InterlockedAnd64(&t{0}, 0xFF); _mm_mfence(); _InterlockedXor64(&t{0}, 0xAA); _ReadWriteBarrier();",
    "volatile __int64 t{0} = 0;_mm_clflush(&data); _InterlockedOr64(&t{0}, 0xDEADBEEF); _mm_mfence(); __writegsqword(0x8, __readgsqword(0x8)); _mm_lfence(); _ReadWriteBarrier();",
    "volatile __int64 t{0} = 0;_InterlockedExchange64(&t{0}, 1); _InterlockedOr64(&t{0}, 0xDEADBEEF); _InterlockedAnd64(&t{0}, 0xFF); _InterlockedCompareExchange64(&t{0}, 1, 0);",
    "volatile __int64 t{0} = 0;_InterlockedExchange64(&t{0}, 1); _InterlockedIncrement64(&t{0}); _InterlockedOr64(&t{0}, 0xDEADBEEF); _ReadWriteBarrier(); __writegsqword(0x8, __readgsqword(0x8));",
    "volatile __int64 t{0} = 0;_InterlockedAnd64(&t{0}, 0xFF); _mm_lfence(); _InterlockedXor64(&t{0}, 0xAA); _InterlockedCompareExchange64(&t{0}, 1, 0);",
    "volatile __int64 t{0} = 0;_InterlockedIncrement64(&t{0}); _mm_sfence(); __writegsqword(0x8, __readgsqword(0x8)); _InterlockedCompareExchange64(&t{0}, 1, 0);",
    "volatile __int64 t{0} = 0;__writegsqword(0x8, __readgsqword(0x8)); _InterlockedAnd64(&t{0}, 0xFF); _InterlockedExchange64(&t{0}, 1); _mm_pause(); _InterlockedXor64(&t{0}, 0xAA);",
    "volatile __int64 t{0} = 0;_mm_lfence(); _InterlockedIncrement64(&t{0}); _InterlockedCompareExchange64(&t{0}, 1, 0); _mm_sfence(); _InterlockedExchange64(&t{0}, 1); _mm_mfence();",
    "volatile __int64 t{0} = 0;_InterlockedOr64(&t{0}, 0xDEADBEEF); _mm_clflush(&data); _InterlockedCompareExchange64(&t{0}, 1, 0); _InterlockedIncrement64(&t{0}); _mm_lfence(); _mm_mfence();",
    "volatile __int64 t{0} = 0;_mm_pause(); _InterlockedIncrement64(&t{0}); _InterlockedAnd64(&t{0}, 0xFF); _mm_clflush(&data); _ReadWriteBarrier(); _mm_sfence();",
    "volatile __int64 t{0} = 0;_InterlockedXor64(&t{0}, 0xAA); _mm_sfence(); __writegsqword(0x8, __readgsqword(0x8)); _InterlockedAnd64(&t{0}, 0xFF); _InterlockedCompareExchange64(&t{0}, 1, 0);",
    "volatile __int64 t{0} = 0;_mm_clflush(&data); __writegsqword(0x8, __readgsqword(0x8)); _mm_mfence(); _InterlockedXor64(&t{0}, 0xAA); _InterlockedCompareExchange64(&t{0}, 1, 0);",
    "volatile __int64 t{0} = 0;_mm_sfence(); _InterlockedIncrement64(&t{0}); _ReadWriteBarrier(); _mm_clflush(&data);",
    "volatile __int64 t{0} = 0;_InterlockedXor64(&t{0}, 0xAA); _ReadWriteBarrier(); _mm_sfence(); _InterlockedAnd64(&t{0}, 0xFF);",
    "volatile __int64 t{0} = 0;_InterlockedAnd64(&t{0}, 0xFF); _InterlockedXor64(&t{0}, 0xAA); _InterlockedExchange64(&t{0}, 1); _mm_pause(); _InterlockedOr64(&t{0}, 0xDEADBEEF);",
    "volatile __int64 t{0} = 0;_mm_sfence(); _InterlockedXor64(&t{0}, 0xAA); _InterlockedExchange64(&t{0}, 1); _ReadWriteBarrier(); _mm_clflush(&data); _mm_lfence();",
    "volatile __int64 t{0} = 0;_ReadWriteBarrier(); _mm_pause(); _InterlockedExchange64(&t{0}, 1); _mm_clflush(&data);",
    "volatile __int64 t{0} = 0;_InterlockedXor64(&t{0}, 0xAA); _InterlockedExchange64(&t{0}, 1); _InterlockedCompareExchange64(&t{0}, 1, 0); _InterlockedAnd64(&t{0}, 0xFF);",
    "volatile __int64 t{0} = 0;_mm_pause(); _mm_lfence(); _InterlockedExchange64(&t{0}, 1); _InterlockedXor64(&t{0}, 0xAA);",
    "volatile __int64 t{0} = 0;_InterlockedExchange64(&t{0}, 1); _InterlockedXor64(&t{0}, 0xAA); _InterlockedOr64(&t{0}, 0xDEADBEEF); _mm_lfence(); _InterlockedCompareExchange64(&t{0}, 1, 0);",
    "volatile __int64 t{0} = 0;_mm_pause(); _InterlockedOr64(&t{0}, 0xDEADBEEF); _InterlockedIncrement64(&t{0}); _mm_sfence();",
    "volatile __int64 t{0} = 0;_InterlockedCompareExchange64(&t{0}, 1, 0); _mm_sfence(); __writegsqword(0x8, __readgsqword(0x8)); _InterlockedExchange64(&t{0}, 1);",
    "volatile __int64 t{0} = 0;_InterlockedIncrement64(&t{0}); _ReadWriteBarrier(); _mm_clflush(&data); __writegsqword(0x8, __readgsqword(0x8));",
    "volatile __int64 t{0} = 0;_InterlockedAnd64(&t{0}, 0xFF); _mm_clflush(&data); _ReadWriteBarrier(); _mm_pause(); _InterlockedExchange64(&t{0}, 1); _InterlockedCompareExchange64(&t{0}, 1, 0);",
    "volatile __int64 t{0} = 0;__writegsqword(0x8, __readgsqword(0x8)); _mm_pause(); _InterlockedXor64(&t{0}, 0xAA); _InterlockedCompareExchange64(&t{0}, 1, 0);",
    "volatile __int64 t{0} = 0;_InterlockedOr64(&t{0}, 0xDEADBEEF); _mm_clflush(&data); _mm_pause(); _mm_mfence(); _InterlockedXor64(&t{0}, 0xAA);",
    "volatile __int64 t{0} = 0;_InterlockedXor64(&t{0}, 0xAA); _mm_mfence(); __writegsqword(0x8, __readgsqword(0x8)); _mm_clflush(&data);",
    "volatile __int64 t{0} = 0;_InterlockedCompareExchange64(&t{0}, 1, 0); _mm_pause(); _mm_clflush(&data); _InterlockedIncrement64(&t{0});",
    "volatile __int64 t{0} = 0;__writegsqword(0x8, __readgsqword(0x8)); _InterlockedOr64(&t{0}, 0xDEADBEEF); _mm_pause(); _InterlockedCompareExchange64(&t{0}, 1, 0); _mm_mfence();",
    "volatile __int64 t{0} = 0;_ReadWriteBarrier(); _mm_lfence(); _InterlockedIncrement64(&t{0}); _InterlockedCompareExchange64(&t{0}, 1, 0); _InterlockedOr64(&t{0}, 0xDEADBEEF); _InterlockedXor64(&t{0}, 0xAA);",
    "volatile __int64 t{0} = 0;_InterlockedXor64(&t{0}, 0xAA); _InterlockedExchange64(&t{0}, 1); _InterlockedOr64(&t{0}, 0xDEADBEEF); _mm_lfence(); _InterlockedIncrement64(&t{0});",
    "volatile __int64 t{0} = 0;_InterlockedExchange64(&t{0}, 1); _InterlockedAnd64(&t{0}, 0xFF); _InterlockedOr64(&t{0}, 0xDEADBEEF); _mm_mfence();",
    "volatile __int64 t{0} = 0;_InterlockedOr64(&t{0}, 0xDEADBEEF); __writegsqword(0x8, __readgsqword(0x8)); _InterlockedCompareExchange64(&t{0}, 1, 0); _InterlockedIncrement64(&t{0});",
    "volatile __int64 t{0} = 0;_InterlockedCompareExchange64(&t{0}, 1, 0); _InterlockedIncrement64(&t{0}); _InterlockedAnd64(&t{0}, 0xFF); _InterlockedExchange64(&t{0}, 1); _ReadWriteBarrier(); _InterlockedXor64(&t{0}, 0xAA);",
    "volatile __int64 t{0} = 0;_mm_clflush(&data); __writegsqword(0x8, __readgsqword(0x8)); _ReadWriteBarrier(); _mm_mfence(); _InterlockedXor64(&t{0}, 0xAA);",
    "volatile __int64 t{0} = 0;_ReadWriteBarrier(); _InterlockedAnd64(&t{0}, 0xFF); _mm_mfence(); _InterlockedXor64(&t{0}, 0xAA); _InterlockedExchange64(&t{0}, 1);",
    "volatile __int64 t{0} = 0;_InterlockedCompareExchange64(&t{0}, 1, 0); __writegsqword(0x8, __readgsqword(0x8)); _InterlockedExchange64(&t{0}, 1); _mm_pause(); _mm_clflush(&data); _InterlockedOr64(&t{0}, 0xDEADBEEF);",
    "volatile __int64 t{0} = 0;_mm_mfence(); _InterlockedXor64(&t{0}, 0xAA); _InterlockedOr64(&t{0}, 0xDEADBEEF); _mm_clflush(&data);",
    "volatile __int64 t{0} = 0;_InterlockedOr64(&t{0}, 0xDEADBEEF); _mm_pause(); _InterlockedXor64(&t{0}, 0xAA); _mm_lfence(); _mm_sfence(); _ReadWriteBarrier();",
    "volatile __int64 t{0} = 0;_ReadWriteBarrier(); _InterlockedXor64(&t{0}, 0xAA); _InterlockedAnd64(&t{0}, 0xFF); _mm_sfence(); _InterlockedCompareExchange64(&t{0}, 1, 0);",
    "volatile __int64 t{0} = 0;_InterlockedAnd64(&t{0}, 0xFF); _mm_mfence(); _mm_sfence(); _mm_lfence();",
    "volatile __int64 t{0} = 0;_mm_lfence(); _InterlockedAnd64(&t{0}, 0xFF); _InterlockedXor64(&t{0}, 0xAA); _mm_clflush(&data); _mm_sfence(); _InterlockedIncrement64(&t{0});",
    "volatile __int64 t{0} = 0;_InterlockedOr64(&t{0}, 0xDEADBEEF); _InterlockedXor64(&t{0}, 0xAA); _InterlockedCompareExchange64(&t{0}, 1, 0); _ReadWriteBarrier();",
    "volatile __int64 t{0} = 0;_ReadWriteBarrier(); _InterlockedXor64(&t{0}, 0xAA); _mm_mfence(); _InterlockedAnd64(&t{0}, 0xFF); _InterlockedIncrement64(&t{0}); _mm_sfence();",
    "volatile __int64 t{0} = 0;_mm_lfence(); __writegsqword(0x8, __readgsqword(0x8)); _mm_pause(); _InterlockedXor64(&t{0}, 0xAA); _InterlockedOr64(&t{0}, 0xDEADBEEF); _mm_clflush(&data);",
    "volatile __int64 t{0} = 0;_InterlockedIncrement64(&t{0}); _ReadWriteBarrier(); _mm_mfence(); _InterlockedXor64(&t{0}, 0xAA);",
    "volatile __int64 t{0} = 0;_InterlockedAnd64(&t{0}, 0xFF); __writegsqword(0x8, __readgsqword(0x8)); _mm_sfence(); _mm_lfence(); _ReadWriteBarrier();",
    "volatile __int64 t{0} = 0;_InterlockedXor64(&t{0}, 0xAA); _InterlockedIncrement64(&t{0}); _mm_mfence(); _mm_clflush(&data); _InterlockedExchange64(&t{0}, 1); _mm_lfence();",
    "volatile __int64 t{0} = 0;__writegsqword(0x8, __readgsqword(0x8)); _mm_pause(); _InterlockedCompareExchange64(&t{0}, 1, 0); _mm_lfence(); _ReadWriteBarrier();",
    "volatile __int64 t{0} = 0;_mm_mfence(); _ReadWriteBarrier(); _mm_sfence(); _InterlockedCompareExchange64(&t{0}, 1, 0); _mm_lfence(); _InterlockedIncrement64(&t{0});",
];



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
        outfile.write(INCLUDE_HEADERS + '\n')
        for line in lines:
            line = rename_variables(line)  # Ensure all 'x' and 't' have unique names
            line = insert_rop_and_cff(line)  # Replace ROP and CFF placeholders
            outfile.write(line + '\n')

if __name__ == "__main__":
    process_cpp_file("xorshellcoderunner.c", "obfuscated_shellcoderunner.c")
    print("Obfuscation complete: obfuscated_shellcoderunner.c")
#cl.exe /c /nologo /Od /Ob0 /Oy- /MT /W0 /GS- /Tp obfuscated_shellcoderunner.c /link /OUT:obfuscated_shellcoderunner.exe /SUBSYSTEM:CONSOLE && link.exe /FORCE obfuscated_shellcoderunner.obj

    print("Compile with:\ncl.exe /c /nologo /Od /Ob0 /Oy- /MT /W0 /GS- /Tp obfuscated_shellcoderunner.c /link /OUT:obfuscated_shellcoderunner.exe /SUBSYSTEM:CONSOLE && link.exe /FORCE obfuscated_shellcoderunner.obj")

