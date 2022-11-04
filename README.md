# Better Bin

Die beiden Programme für den Raspberry Pi sind auf https://github.com/better-bin-project/better-bin-raspberry zu finden. _betterbin2.py_ wird auf dem Raspberry Pi nach dem Start ausgeführt. Alle Motorbewegungen werden von _stepper.py_ ausgeführt.

## betterbin2.py

Zunächst wird die Box in Startposition gefahren und dabei vom Limit Switch gestoppt. In der folgenden _while_-Schleife wird auf ein Signal des Benutzers (Knopf oder Eingabe in der Kommandozeile) gewartet. Darauf wird ein Bild aufgenommen und die Vorhersage des neuronalen Netzes einer Müllkategorie zugeordnet. Die Box wird mit Motor 1 in die entsprechende Position gefahren und die Klappe mit Motor 2 geöffnet.

_models_dict_

Gibt das vortrainierte Netz mit dem angegebenen Namen zurück.

_img_dict_ 

Ordnet Ausgaben des neuronalen Netzes einer Müllkategorie zu.

_recognize(modelname, imgpath)_

Die Bilddatei in _imgpath_ wird vorverarbeitet und durchläuft das neuronale Netz mit dem gegebenen Modell (_modelname_). Die wahrscheinlichste Vorhersage wird als String zurückgegeben.

## stepper.py

Die Datei kann ebenfalls ausgeführt werden, um Motoren manuell anzusteuern.

_doSteps(motorNum, n, t)_

Bewegt den gegebenen Motor (1 zur Boxbewegung, 2 zur Klappenbewegung) _n_ Schritte mit einer Pause von _t_ (in s) zwischen den Schritten. Um den Motor in die umgekehrte Richtung zu bewegen, muss eine negative Anzahl an Schritten angegeben werden.

