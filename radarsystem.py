SPEED_LIMITS = {"Private": 80, "Truck": 60, "Bus": 70}
SPEED_FEE = 300
SEATBELT_FEE = 100


def speed_rule(obs):
    limit = SPEED_LIMITS.get(obs["car_type"])
    if limit is not None and obs["speed"] > limit:
        return {"rule": "Speed", "desc": f"speed of {obs['speed']} exceeded max allowed {limit}", "fee": SPEED_FEE}
    return None


def seatbelt_rule(obs):
    if not obs["seatbelt"]:
        return {"rule": "Seatbelt", "desc": "Seatbelt not fastned", "fee": SEATBELT_FEE}
    return None


class QuantumRadar:

    def __init__(self, rules):
        self.rules = rules          
        self.fines = []             

    def process(self, obs):
        violations = [v for v in (rule(obs) for rule in self.rules) if v]
        if not violations:
            return

        total = sum(v["fee"] for v in violations)
        self.fines.append({"plate": obs["plate"], "violations": violations})

        print(f"Traffic fine for car {obs['plate']}")
        print(f"Total amount: {total} EGP")
        print("Violations:")
        for v in violations:
            print(f"- {v['desc']} : {v['fee']} EGP")

    def getAllPossibleFines(self):
        totals = {}
        for fine in self.fines:
            total = sum(v["fee"] for v in fine["violations"])
            totals[fine["plate"]] = totals.get(fine["plate"], 0) + total
        return totals

    def get_violation_counts(self):
        counts = {}
        for fine in self.fines:
            for v in fine["violations"]:
                counts[v["rule"]] = counts.get(v["rule"], 0) + 1
        return counts


class Main:
    @staticmethod
    def run():
        radar = QuantumRadar([speed_rule, seatbelt_rule])

        observations = [
            {"plate": "ABC1234", "car_type": "Private", "speed": 94, "seatbelt": False},
            {"plate": "TRK555", "car_type": "Truck", "speed": 72, "seatbelt": True},
            {"plate": "BUS111", "car_type": "Bus", "speed": 60, "seatbelt": False},
        ]

        for obs in observations:
            radar.process(obs)
            print()

        print("All fines:", radar.getAllPossibleFines())
        print("Violation counts:", radar.get_violation_counts())


if __name__ == "__main__":
    Main.run()