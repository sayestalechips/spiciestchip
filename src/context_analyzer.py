from typing import Dict, List
import pandas as pd

class ContextAnalyzer:
    def __init__(self):
        # Load DTIP personas
        self.personas = pd.read_csv('/Users/johnnysaye/Desktop/testproject/spiciest_chip/data/raw_courses/DTIP - Sheet1.csv')
        self.unwritten_rules = self._load_unwritten_rules()
        
    def analyze_context(self, query: str, user_context: Dict) -> Dict:
        """Analyze query and context for personas and AF cultural elements."""
        return {
            'detected_personas': self._detect_personas(query, user_context),
            'af_context': self._analyze_af_context(user_context),
            'facilitation_adjustments': self._get_facilitation_adjustments()
        }
    
    def _detect_personas(self, query: str, context: Dict) -> List[Dict]:
        """Detect potential personas based on query and context."""
        detected = []
        for _, persona in self.personas.iterrows():
            if self._matches_persona_characteristics(query, context, persona):
                detected.append({
                    'name': persona['Name'],
                    'characteristics': persona['Characterstics'],
                    'facilitation_tips': persona['How to Facilitate']
                })
        return detected
    
    def _analyze_af_context(self, context: Dict) -> Dict:
        """Analyze Air Force specific context."""
        return {
            'rank_dynamics': self._analyze_rank_dynamics(context),
            'cultural_considerations': self._get_cultural_considerations()
        }
