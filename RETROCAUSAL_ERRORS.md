# 20 Least Expected Retrocasual Reasons for localhost Refused (Inverted Preconditions)

Retrocasual: Preconditions backward-causally generating 'refused'. Wild/rare fixes:

1. VSCode port 8000 used by extension (kill VSCode tasks).
2. Windows IPv6 localhost::1 binding fail (edit hosts to 127.0.0.1).
3. Opera VPN auto-proxy localhost (Opera settings → VPN off).
4. Hyper-V WSL2 port forward missing (`netsh interface portproxy add v4tov4 listenport=8000 listenaddress=0.0.0.0 connectport=8000 connectaddress=127.0.0.1`).
5. Antivirus real-time scan blocks uvicorn.exe.
6. PowerShell execution policy blocks subprocess (Set-ExecutionPolicy RemoteSigned).
7. DNS cache poison localhost (`ipconfig /flushdns`).
8. Windows Defender firewall Python rule deny outbound 8000.
9. Docker desktop NAT conflict port 8000.
10. Dual NIC/router loopback block (disable WiFi).
11. Time sync NTP desync JWT localhost trust.
12. User proxy.pac script loops localhost.
13. IPv4 localhost disabled registry (regedit Tcpip → EnableLoopback).
14. Pending Windows update socket backlog full.
15. USB network adapter phantom localhost hijack.
16. Virtual machine nested localhost collision.
17. Sandboxie/VMware sandbox port monopolize.
18. Group Policy proxy enforce localhost redirect.
19. Corrupt %WINDIR%\System32\drivers\etc\hosts (backup/restore).
20. Cosmic ray bitflip uvicorn bind (reboot server hardware).
