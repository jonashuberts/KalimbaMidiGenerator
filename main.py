#Todo: Success display after generation. English GUI.
import json
import music21
import tkinter as tk
from tkinter import filedialog
import os

# Funktion, die die ausgewählte Datei liest und verarbeitet
def process_file():
    # Dateiauswahl-Dialog anzeigen
    filename = filedialog.askopenfilename()
    
    # Lesen von JSON-Daten aus der ausgewählten Datei
    with open(filename) as f:
        kal_data = json.load(f)
    # Filtern von leeren Noten und leeren Maßnahmen
    kal_data["song"] = [[note for note in measure if note["note"]] for measure in kal_data["song"] if measure]
    # Schreiben von JSON-Daten in die Datei "out.kal"
    with open("out.kal", "w") as f:
        json.dump(kal_data, f)
    # Lesen von JSON-Daten aus der Datei "out.kal" und Umkehrung der "song"-Liste
    with open("out.kal") as f:
        data = json.load(f)
        data["song"] = data["song"][::-1]
    # Schreiben von JSON-Daten in die Datei "out2.kal"
    with open("out2.kal", "w") as f:
        json.dump(data, f)

    # Lese die .kal-Datei im JSON-Format
    with open('out2.kal') as f:
        data = json.load(f)
    # Erstelle eine Partitur und füge eine Stimme hinzu
    score = music21.stream.Score()
    part = music21.stream.Part()
    score.append(part)
    # Erstelle ein music21.Tempo-Objekt und füge es zur Partitur hinzu
    tempo = music21.tempo.MetronomeMark(number=int(data['tempo']))
    part.append(tempo)
    # Durchlaufe jede Gruppe von Noten und füge sie der Stimme hinzu
    for group in data['song']:
        notes = []
        rests = []
        for note_data in group:
            if note_data['note'] == 'rest':
                # Erstelle eine Pause, falls die Notiz ein Ruhezeichen ist
                rest = music21.note.Rest()
                rest.duration.quarterLength = 4/note_data['time']
                rests.append(rest)
            else:
                # Erstelle eine Note, falls die Notiz eine Note ist
                note = music21.note.Note(note_data['note'])
                note.duration.quarterLength = 4/note_data['time']
                notes.append(note)
        if len(rests) == len(group):
            # Wenn alle Elemente Ruhezeichen sind, füge eine Pause zur Partitur hinzu
            measure = music21.stream.Measure()
            for rest in rests:
                measure.append(rest)
            part.append(measure)
        elif len(notes) == 1:
            part.append(notes[0])
        else:
            chord = music21.chord.Chord(notes)
            part.append(chord)
    # Schreibe die Partitur in eine MIDI-Datei und speichere sie ab
    score.write('midi', fp=filename[:-4]+'.mid')

    files_to_remove = ['out.kal', 'out2.kal']
    for file in files_to_remove:
        os.remove(file)
    #pass

# GUI erstellen
root = tk.Tk()
root.title("Kalimba Midi Generator (.kal to .mid)")
root.geometry("300x100")

# Button erstellen
button = tk.Button(root, text="Datei auswählen", command=process_file)
button.pack(pady=20)

root.mainloop() # Starten der GUI-Schleife