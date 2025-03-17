cl.exe /c /nologo /Od /Ob0 /Oy- /MT /W0 /GS- /Tp obfuscated_shellcoderunner.c /link /OUT:obfuscated_shellcoderunner.exe /SUBSYSTEM:CONSOLE 
link.exe /FORCE obfuscated_shellcoderunner.obj
