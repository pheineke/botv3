from datetime import datetime, timedelta

def clean_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    cleaned_lines = []
    clean0 = []
    for line in lines:
        lineval = line.strip().split(',')[2]
        cleaned_lines.append(lineval)
        
    def find_equal_intervals(lst):
        equal_intervals = []
        start_index = 0
        current_element = None
        
        for i, element in enumerate(lst):
            if element != current_element:
                if i > start_index:
                    equal_intervals.append((start_index, i - 1, current_element))
                start_index = i
                current_element = element

        # Füge das letzte Intervall hinzu, falls es gleich ist
        if lst and lst[-1] == current_element:
            equal_intervals.append((start_index, len(lst) - 1, current_element))

        return equal_intervals
    intervals = find_equal_intervals(cleaned_lines)

    for index0, index1, val in intervals:
        if index0 != index1:
            clean0.append(lines[index0])
            clean0.append(lines[index1])
        else:
            clean0.append(lines[index0])

    

    with open(file_path, 'w') as file:
        for elem in clean0:
            file.write(f'{elem}')

# Beispielaufruf der Funktion
clean_data('data.txt')
