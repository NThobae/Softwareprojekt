# Leicht modifizierte readme der Vorgänger:


## Einleitung

Hauptziel unseres Softwareprojekts war es die Trusted Firmware-M (TF-M) auf dem Nucelo L552ZE-Q Board laufen zu lassen.
Neben diesem Hauptziel haben wir uns noch mit möglichen Angriffen auf die Trusted Firmware beschäftigt welche in der Dokumentation (Dokumentation/Softwareprojekt___Dokumentation.pdf) zu finden sind.
Um einen schnellen Start in die Nutzung von Trusted Firmware-M zu ermöglichen haben wir in diesem README die wichtistgen Informationen übersichtlich dargestellt.

Die verwendete TF-M stammt aus dem [STM32CubeL5 Github Repository](https://github.com/STMicroelectronics/STM32CubeL5).
In dem Repository findet man eine Projekt Datei der TF-M für das STM32L562E-DK Board.
Um diese Projektdatei für das L552ZE-Q Board anzupassen mussten wir unter anderem Teile der Hardware Verschlüsselung deaktivieren, um
die alternative Software Verschlüsselung zu nutzen, da das STM32L562E-DK Board über Hardware verfügt die dem L552ZE-Q Board fehlt.
Außerdem mussten wir die UART Schnittstelle dem L552ZE-Q Board entsprechend umstellen. Details dazu weiter unten in Teil 3 dieses READMEs.

Diese Änderungen befinden sich unter /TF-M_ported_for_L552ZE-Q/.
(Das original wie es unter drive zu finden war ist [hier](https://github.com/KurfuerstPilz/Softwareprojekt/releases/download/v0.0.1/Softwareprojekt-20201117T142257Z-001.zip))
Neben den Boardspezifischen Anpassungen des Firmware Pakets haben wir Fehler behoben die von Entwicklerseite in der Firmware gemacht worden. 
Die gemachten Anpassungen sind vergleichbar mit denen die wir für die SBSFU Firmware gemacht haben und können unter [hier](https://github.com/KurfuerstPilz/Softwareprojekt/blob/add_ported_project_from_drive/Dokumentation/vorgaenger/Softwareprojekt___Dokumentation.pdf) in Abschnitt 5 - "SBSFU Firmware" nachgelesen werden. Hauptsächlich wurden falsche Pfadangaben und Compilierbefehle behoben.


## Anleitung

Wir haben unter Ubuntu 20.04 gearbeitet.

Benötigte Software:
	STM32CubeIDE
	Python 2
	STM32CubeProgrammer
	ST-LINK-SERVER Software*
	STSW-LINK007 Software*
	Minicom (oder ähnliche ymodem fähige Terminals)

Schritte:

1. Den Softwareorjekt Ordner entpacken

2. STM32CubeIDE öffnen

3. File>Open Projects From File System...>Directory den TFM Ordner unter Softwareprojekt/TF-M_ported_for_L552ZE-Q/Projects/TFM auswählen

4. Finish drücken

5. Im Terminal die Dateien Softwareprojekt/TF-M_ported_for_L552ZE-Q/Projects/TFM/TFM_Appli/STM32CubeIDE/postbuild.sh mit chmod ausführbar machen.

6. In der STM32CubeIDE die Projektdateien builden. Die Dateien sind jeweils unter TFM/TFM_SBSFU_Boot und TFM/TFM_Appli zu finden und in der IDE an den blauen Icons zu erkennen. Die Projektdateien müssen in der Reihenfolge TFM_SBSFU_Boot, dann TFM_Appli_Secure, dann TFM_Appli_NonSecure gebuildet werden. Die Projektdateien werden mit dem Hammerwerkzeug gebuildet.

7. Bei dem Buildprozess muss genau auf die Hinweise der CDT Build Console in der IDE geachtet werden. Ggf. müssen diverse Python Libarys nachinstalliert werden (bspw. Cryptography und libncurses5). Außerdem muss Python 2 installiert sein. Einen erfolgreichen Build Prozess von TFM_Appli_Secure und TFM_Appli_NonSecure erkennt man an der abschließenden Zeile "secure sign done" bzw. "non secure sign done"

8. Nun sollte spätestens das Board angeschlossen werden (Micro USB TypB). Sollte sich auf dem Board bereits sicherheitssensitive Firmware befinden kann es nötig sein den Jumper JP5 auf dem Board anzuheben und wieder drauf zustecken um das Board zu unlocken. Um das Board zu initilaisieren muss nun das …\SBSFU_Boot\STM32CubeIDE\regression.sh Skript ausgeführt werden. Das Skript ruft die CubeProgrammer_CLI auf und stellt die Statusbytes und Speicherbereiche des Boards korrekt ein.

9. Nun kann die Firmware auf das Board geflasht werden. Dazu wird das SBSFU_Boot\STM32CubeIDE\TFM_UPDATE.sh Skript ausgeführt. Auch hier sollte darauf geachtet werden, ob während der Ausführung des Skripts Fehler auftreten. Beispielsweise könnten Speicherbereiche als write protected deklariert sein. Eigentlich sollten diese Einstellungen allerdings durch das regression.sh Skript richtig eingestellt sein.

10. Nun kann mit einem ymodem-fähigen Terminal mit dem Board kommuniziert werden. Wir haben minicom genutzt. Nach der Installation kann das Programm mittels "sudo minicom -s -con" in die Einstellungen gestartet werden. Dort muss unter "SerialPort" der Port zu "/dev/ttyACM0" geändert werden. Danach können mittels "Esc" die Einstellungen verlassen werden. Entfernt man den Jumper JP5 auf dem Board und setzt in wieder drauf booted die Firmware, dann kann über die Tastatur mit der Application auf dem Board kommuniziert werden.



*evtl. notwendige Treiber, verfügbar unter https://www.st.com/en/evaluation-tools/nucleo-l552ze-q.html#tools-software 


## Änderungen um die Firmware auf dem Nucelo L552ZE-Q zu nutzen

#### Kommunikationsschnittstelle: 

Das Board hat ein virtuelles COM Port. Das heißt man kann mithilfe eines Terminals auf dem PC mit dem Board kommunizieren. Beim L552ZE-Q wird hier standardmäßig die LPUART1 mit dem ST-LINK/V2-1 MCU verbunden. 
Dass die Kommunikation über die LPUART1 erfolgen soll wird beim SBSFU mit der Datei low_level_com.c über die Struktur TFM_DRIVER_STDIO definiert. Mit dieser Struktur kann man unter anderem die UART Schnittstelle initialisieren, Daten senden/empfangen. Die Trustedfirmware nutzt diese Stuktur in der Datei uart_stdout.c um die Print-Befehle standardmäßig über die LPUART1 auszugeben. Hier ist zu beachten, dass neben der Clock für die LPUART1, auch die Clock für PWR und VDDIO2 initialisiert wird. Ansonsten funktioniert die Kommunikation nicht. Dies ist beim anderen Board (L562E-DK) nicht nötig. Der virtuelle COM Port ist hier außerdem standardmäßig mit USART1 verbunden. 

Neben der SBSFU gibt es eine Secure und eine Non-Secure Applikation. Die Non-Secure Applikation definiert die LPUART1 Schnittstelle in der Datei com.h. Die Secure Applikation wiederum über die low_level_com.c Datei wie beim SBSFU.


#### Ordnerstruktur:

Für das Projekt wurde die ursprüngliche Ordnerstruktur der CubeL5 Library verändert. Diese hat zum Teil viele Dateien, die für dieses Projekt nicht relevant sind. Außerdem wurde die Anzahl der Ordnerebenen minimiert. 
Einfach Dateien herumschieben, Ebenen löschen und hoffen, dass das Programm läuft, ist in diesem Fall jedoch nicht die gute Herangehensweise. Die Projektdatei .cproject (TFM/TFM_SBSFU_Boot/STM32CubeIDE) sagt dem IDE unter anderem wo die Include Dateien zu finden sind. Diese Include Pfade kann man unter Project→Properties→C/C++ General→ Paths and Symbols→ Includes verändern. Neben den Include Dateien ist es auch wichtig der IDE zu sagen, wo die Quellcode-Datein sind. Dazu geht man wieder bei Properties→Resource→Linked Resource und öffnet den Tab „Linked Resources“. Hier prüft man, ob die IDE alle Dateien gefunden hat. 
Anmerkung: In unserem Fall hat die IDE teilweise fehlerhaft und hat die Include Pfade nicht in die .cprojekt Datei übernommen. Man kann diese Datei dann manuell mit einem Texteditor verändern. 
 

#### Mbedtls:

Die mbedtls Bibliothek kann Verschlüsselungen mithilfe von Hardware ausführen oder rein durch die Software. Zu der unterstützenden Hardware können unter anderem Public-Key Accelerator (PKA) sein. Da unser Board (im gegensatz zum L562E-DK) die Cryptographie und PKA Hardware nicht hat, werden im ersten Schritt in der Datei stm32l5xx_hal_conf.h folgende Preprozessor Anweisungen auskommentiert:
#define HAL_CRYP_MODULE_ENABLED
#define HAL_PKA_MODULE_ENABLED
Im nächsten Schritt wird in der Datei tfm_mbedcrypto_config.h der mbedtls Bibliothek gesagt, dass es die Verschlüsselungen ohne die Hilfe von diesen nicht vorhanden Hardware Komponenten durchführen soll. Das funktioniert, indem man Definitionen, die mit „_ALT“ enden auskommentiert (Außer MBEDTLS_ENTROPY_HARDWARE_ALT). Damit bestimmt man, dass für alle Algorithmen und Verfahren die mbedtls Software genutzt wird. 
Anmerkung: Beim anderen L562E-DK Board kann man die Hardware Komponenten aktivieren zum Beispiel mit der Auskommentierung von #define MBEDTLS_AES_ENCRYPT_ALT und #define MBEDTLS_AES_DENCRYPT_ALT in der tfm_mbedcrypto_config.h. Mit dem Code aes_alt.c wird dann die Verschlüsselungen mithilfe der Hardware durchgeführt.

### Hilfreiche Dokumente

Die vier hilfreichsten Dokumente bei der Arbeit mit Trusted Firmware auf dem Nucelo L552ZE-Q waren diese vier, welche sich leicht mit einer Google Suche finden lassen:

- UM2671 Getting started with STM32CubeL5 TFM application
- UM2656 Getting started with STM32CubeL5 for STM32L5 Series
- RM0438 Reference manualSTM32L552xx and STM32L562xx advanced Arm®-based
- AN5447 Overview of Secure Boot and Secure Firmware Update solution on Arm® TrustZone® STM32L5 Series microcontrollers



Wir wünschen potentiell nachfolgenden Softwareprojekten viel Spaß mit TF-M :) 
