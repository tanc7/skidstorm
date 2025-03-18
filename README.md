# SCUDSTORM/SKIDSTORM

Mass regeneration of evasive payloads.

It was discovered that methods such as rapid loading of dynamic APIs even if hidden with IAT table hiding can be flagged as malware. You can use tricks like adding junk code (Intrinsic Chain Obfuscation) and massive control-flow flattened loops to break apart the assembly to evade this.

Another detection trick is XOR obfuscation loops. You can sandwich control-flow flattening functions, rolled loops, junk code, Intrinsic Gadgets, ROP Gadgets (requires a separate ASM file for MSVC compilers). You can even sandwich the junk code between each line in a XOR deobfuscation loop.

# Training video

Please see the silent training video for how to use.
[SCUD STORM Training Video](https://youtu.be/VxMo6JfrHHQ)

# Mixed Boolean Arithmetics

In the prototypes.h file you can find seven different obfuscated XOR macros that you can use instead of a simple hat ^ bitwise operator.

# Opaque Predicates
There is also a opaque predicates file for you to abuse to create false control-flow graphs using five opaquely true, five opaquely false, and one opaquely indeterminate predicate to cause more unpredictability. You should use the opaque predicates when needed, such as defeating Import Hashing. By importing one API function at a time you can change the Import Hash (IMPHASH) to restart your attack campaign by having it profile as a new strain of malware.

# How to use

First, on your Maldev Windows VM you need to add the following files in the same path. Your obfuscated_shellcoderunner.c file from the build tool, your prototypes.h file (you might want to obfuscate this), and your opaquepredicates.hpp whenever you need to use them, either to mess with IMPHASHes or to create false control-flow graphs.

The xorshellcoderunner.c file is NOT meant to be compiled, you run the 64bitobfuscator.py for 64-bit binaries or 32-bit for x86 binaries.

1. Generate your payload as a msfvenom bin file
2. Run XOR.py to convert it into shellcode
3. Add shellcode to the runner
4. Mark Intrinsic Chain Obfuscated Components as //ROP64 (misnomer, it's not rop gadgets, it's intrinsic chain gadgets)
5. Mark Control Flow Flattening functions with //CFF, highly advised to mark your prototypes.h file Init() functions to evade rapid dynamic API loading
6. Run the obfuscator
7. Run the payload on a fully patched Windows Host
8. Profit
9. Then walk back through in the debugger to ensure how it works
10. Decoded MSF payload


# The name

This is the ONLY release.

I am a huge hater of copy-and-paste types that compile payloads, submit them to VirusTotal, and then go to their local powerpoint meeting to chase clout among the ignorant corpos. They win no respect from their technical teams that they are laying off anyways. Therefore, public releases of SCUDSTORM is now called SKIDSTORM. If you want to do something original, go fork this repo and do it on your own. Or call it something else. 

I have updated versions of SCUDSTORM at all times to implement kernel-driver attacks through a hidden DLL to escalate privileges on the implant, as well as another module to inject rootkit installers into sacrificial apps. These versions are not for public release and is the property of Cybersecurity & Growth by Daniel M. Kelley and scamkillers.org

The name itself came from a superweapon in a video game called Command & Conquer: Generals.
[Overpowered SCUD Storm](https://youtu.be/PKmuqkPiuIA?si=63hzbZ9ZyXs_bF9-)
