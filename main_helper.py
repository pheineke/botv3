import asyncio
import subprocess
from datetime import datetime, timedelta



class Helper():
    def __init__(self) -> None:
        self.requirementspath = "requirements.txt"

    def parse_datetime(self, dt_str):
        return datetime.strptime(dt_str, "%Y-%m-%d,%H:%M")

    def sort_requirements(self):
            try:
                with open(self.requirementspath, 'r') as file:
                    lines = file.readlines()
                    lines = [str(x).replace('\n','') for x in lines]
                sorted_lines = sorted(lines)
                print(sorted_lines)
                with open(self.requirementspath, 'w') as file:
                    for line in sorted_lines:
                        file.write(line+'\n')
                
                print("Die Zeilen in der Datei wurden alphabetisch sortiert.")
            
            except FileNotFoundError:
                print(f"Die Datei '{self.requirementspath}' wurde nicht gefunden.")

    def install_requirements_if_missing(self):
        self.sort_requirements()
        try:
            # Öffne die requirements.txt-Datei und lies die Anforderungen
            with open(self.requirementspath, "r") as file:
                requirements = file.readlines()
            
            # Entferne Leerzeichen und Zeilenumbrüche am Anfang und Ende jeder Anforderung
            requirements = [req.strip() for req in requirements]

            # Überprüfe, ob jedes Paket installiert ist
            missing_packages = []
            for req in requirements:
                try:
                    # Überprüfe, ob das Paket installiert ist
                    subprocess.check_output(["pip", "show", req], stderr=subprocess.DEVNULL)
                except subprocess.CalledProcessError:
                    # Wenn das Paket nicht installiert ist, füge es zur Liste der fehlenden Pakete hinzu
                    missing_packages.append(req)
            
            if missing_packages:
                print("Folgende Pakete sind nicht installiert und werden jetzt installiert:")
                for package in missing_packages:
                    subprocess.run(["pip", "install", package])
                print("Alle fehlenden Pakete wurden installiert.")
            else:
                print("Alle Pakete sind bereits installiert.")
        
        except FileNotFoundError:
            print(f"Die Datei '{self.requirementspath}' wurde nicht gefunden.")

    async def do(self):
        file_path = self.requirementspath
        
        with open(file_path, 'r') as file:
            last_botstart_time = None
            for line in file:
                parts = line.strip().split(',')
                if parts[-1] == 'BOTSTART':
                    last_botstart_time = self.parse_datetime(parts[0] + ',' + parts[1])

            if last_botstart_time:
                current_time = datetime.now()
                time_difference = current_time - last_botstart_time
                if time_difference <= timedelta(hours=5):
                    self.install_requirements_if_missing()