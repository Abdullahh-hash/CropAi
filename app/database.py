# app/database.py
class MockDatabase:
    def __init__(self):
        self.diseases = {}
        self.history = []

    def seed_data(self):
        self.diseases = {
            "tomato_leaf_mold": {
                "name": "Tomato Leaf Mold",
                "severity": "critical",
                "treatment_protocols": {
                    "immediate": [
                        "Isolate affected plants immediately to prevent spore migration.",
                        "Prune lower infected limbs to decrease micro-climate moisture accumulation.",
                        "Reduce overhead canopy watering entirely; switch over to low-profile ground irrigation lines."
                    ],
                    "biological": [
                        "Deploy targeted Bacillus subtilis organic strains uniformly over leaf zones.",
                        "Apply customized high-concentration compost tea extracts to strengthen foliage biological defense."
                    ],
                    "preventative": [
                        "Maintain operational ambient relative humidity below 85% inside green shelters.",
                        "Introduce competitive air-circulation grid currents across standard rows.",
                        "Select certified disease-resistant crop varieties for upcoming operational rotations."
                    ]
                }
            },
            "apple_scab": {
                "name": "Apple Scab",
                "severity": "warning",
                "treatment_protocols": {
                    "immediate": [
                        "Rake and destroy fallen leaves and debris around tree bases.",
                        "Prune infected twigs during dry periods."
                    ],
                    "biological": [
                        "Apply copper-based or sulfur-based organic foliar inputs.",
                        "Introduce beneficial soil microbes to accelerate leaf litter breakdown."
                    ],
                    "preventative": [
                        "Space trees properly to allow complete sunlight penetration.",
                        "Prune trees annually to maximize internal branch aeration."
                    ]
                }
            }
        }

db = MockDatabase()

def init_db():
    db.seed_data()
    print("✨ Database initialized with agricultural diagnostic protocol keys.")