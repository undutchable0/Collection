~~~Function of these PS scripts


"harvest-psapvdi.ps1" = This script will copy CPI and PROQA from the desired host and place them locally in the same folder the script was ran.

"implement-psapvdi.ps1" = This script will then copy the CPI and PROQA files from the local directories made by the previous script, add the correct user to local admin, and install simplehelp. The user will have choice to loop through a list
of devices in the target.txt file, or to make a manual single target choice.

**note the simplehelp installer .exe will need to be in the directory the scripts are run, as it will be copied to the target machine(s). 
