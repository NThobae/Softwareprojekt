# Softwareprojekt Trustedfirmware M

Bei dieser Applikation wird eine LED, die im Secure Bereich ist, mit einem Button, das im Non-Secure Bereich ist, getoggelt.
Weitere Features folgen.

Diese Applikation läuft auf dem NUCLEO-L552ZE-Q Board von STMicroelectronics.

Die Schnittstelle zwischen Secure und Non-Secure bilden die beiden Dateien secure_nsc.h (im Non-Secure Bereich) und secure_nsc_c (im Secure Bereich)
In secure_nsc.h ist die Funktion Toggle_Pin() definiert. Diese Funktion kann die Non-Secure Applikation bei einem Tastendruck ausführen. 

Toggle_Pin() wird dann im Secure Bereich ausgeführt (secure_nsc.c) und die LED getoggelt. 

--------------------------------------------------------------------
Will man diese Applikation auf dem Board testen, muss man den Board erst richtig initialisieren!
--------------------------------------------------------------------

1. Schritt:

- Board mit dem PC verbinden (Micro USB).
- STM32CubeProgrammer starten und mit Board verbinden.
- Bei der ST Link Konfiguration einen Firmware Update starten.
- Option Bytes wie folgt konfigurieren:
  TZEN =1 (Haken setzen)        //aktiviert Trustzone auf dem Board
  DBANK =1                      //teilt den FLASH (512KByte) in 2 Regionen (Bank1 und Bank2)
  Secure Area 1:  SECWM1_PSTRT=0x0  SECWM1_PEND=0x7F  wenn SECWM1_PSTRT < SECWM1_PEND, ist der Secure Bereich aktiviert für diese Bank.
                                                      Eine Bank besteht aus 128 mal 2 Kbyte Blöcken. In diesen Fall (0x0-0x7f) werden alle Blöcke als Secure initialisiert.
                                                      Das heißt Bank1 ist komplett Secure.
  Secure Area 2:  SECWM2_PSTRT=0x1  SECWM2_PEND=0x0   wenn SECWM1_PSTRT > SECWM1_PEND, ist die komplette Bank Non-Secure. 
                                                      Das heißt, Bank2 ist Non-Secure.

Mit dieser Konfiguration haben wir einen Secure Bereich für die Firmware und einen Non-Secure Bereich für unsere Applikation.

2. Schritt:
Das Board ist jetzt Initialisert und das Programm kann gestartet werden:
  Rechtsklick auf TrustZone-ToggleLED_Secure -> Debug As -> STM32 Cortex-M C/C++ Applikation
  
  

