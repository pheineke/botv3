import subprocess

class Helper():
    def __init__(self) -> None:
        self.requirementspath = "requirements.txt"

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

    async def install_requirements_if_missing(self):
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
        self.sort_requirements()
        await self.install_requirements_if_missing()