# sparc-tools

To run phoebus from a Windows follow the followingsteps on the Win PC.
The installers are located in smb://dante@192.168.197.157/sparcstorage/space/SPARCutils/Windows
Install PUTTY
Install VcXsrv
    After installing, run XLaunch and accept defaults:
    Multiple windows
    Start no client
    Disable access control
Configure PuTTY for X11 forwarding
    Go to Connection/SSH/X11
    Check Enable X11 forwarding
    Set X display location to localhost:0
Save the PUTTY session and load it to connect
Login with the sparc credentials
From terminal run
    sh phoebus/phoebus.sh