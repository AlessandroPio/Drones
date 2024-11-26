import os
import json
from tabnanny import verbose

from pyswip import Prolog
from Config import Log


class DroneMissionManager:
    def __init__(self, files, verbose=False):
        self.files = files
        self.prolog = None
        self.relations = {
            "droni": {},
            "missioni": []
        }
        self.verbose = verbose

    def load_prolog_file(self, file_path):
        if os.path.exists(file_path):
            if self.verbose:
                print(f"Caricamento del file Prolog: '{file_path}'")
            prolog = Prolog()
            prolog.consult(file_path)
            return prolog
        else:
            if self.verbose:
                print(f"Il file '{file_path}' non esiste.")
            return None

    def extract_facts(self, prolog, fact_name, arity):
        query = f"{fact_name}({', '.join([f'Var{i}' for i in range(1, arity + 1)])})"
        try:
            facts = list(prolog.query(query))
            if self.verbose:
                print(f"Fatti estratti: {fact_name}/{arity} -> {facts}")
            return facts
        except Exception as e:
            if verbose: print(f"Errore nell'estrazione di '{fact_name}/{arity}': {e}")
            return []

    def process_prolog_files(self):
        all_facts = {}
        for file_path in self.files:
            prolog = self.load_prolog_file(file_path)
            if prolog:
                all_facts[file_path] = {
                    "stato_drone": self.extract_facts(prolog, "stato_drone", 2),
                    "batteria_drone": self.extract_facts(prolog, "batteria_drone", 2),
                    "coordinate_drone": self.extract_facts(prolog, "coordinate_drone", 3),
                    "stato_missione": self.extract_facts(prolog, "stato_missione", 2)
                }
        return all_facts

    def create_relations(self, all_facts):
        for facts in all_facts.values():
            for drone_fact in facts.get("stato_drone", []):
                drone_name = drone_fact["Var1"]
                drone_status = drone_fact["Var2"]
                self.relations["droni"].setdefault(drone_name, {})["stato"] = drone_status

            for battery_fact in facts.get("batteria_drone", []):
                drone_name = battery_fact["Var1"]
                self.relations["droni"].setdefault(drone_name, {})["batteria"] = battery_fact["Var2"]

            for coord_fact in facts.get("coordinate_drone", []):
                drone_name = coord_fact["Var1"]
                x, y = coord_fact["Var2"], coord_fact["Var3"]
                self.relations["droni"].setdefault(drone_name, {})["coordinate"] = (x, y)

            for mission_fact in facts.get("stato_missione", []):
                mission_id = str(mission_fact["Var1"])
                mission_status = mission_fact["Var2"]

                assigned_drone = None
                if mission_id == "1":
                    assigned_drone = "drone1"

                self.relations["missioni"].append({
                    "id": str(mission_id),
                    "stato": mission_status,
                    "drone": assigned_drone
                })

    def get_mission_details(self, mission_id):
        mission = next((m for m in self.relations["missioni"] if m["id"] == str(mission_id)), None)
        if not mission:
            if self.verbose:
                print(f"Missione con ID '{mission_id}' non trovata.")
            return {}

        drone_id = str(mission["drone"])
        drone_info = self.relations["droni"].get(drone_id, {})

        if drone_info.get("coordinate") == (0, 0) and mission["stato"] == "completata":
            drone_info.pop("coordinate", None)

        mission_details = {
            "missione": {
                "id": str(mission["id"]),
                "stato": mission["stato"],
                "drone_assegnato": str(drone_id),
                "drone_info": drone_info
            }
        }

        if self.verbose:
            print(Log.header(mission_details))

        return mission_details

    def run(self, mission_id):
        all_facts = self.process_prolog_files()

        if self.verbose:
            print("\nFatti estratti:")
            for file, facts in all_facts.items():
                print(f"File: {file}")
                for fact, values in facts.items():
                    print(f"  {fact}: {values}")

            print("\nRelazioni:")
            print(json.dumps(self.relations, indent=4))

        self.create_relations(all_facts)
        mission_details = self.get_mission_details(mission_id)

        return mission_details