"""
JARVIS NLP Service
Natural Language Processing för intent recognition och kommando-routing
"""

import re
import nltk
from typing import Dict, List, Tuple, Any, Optional
from fuzzywuzzy import fuzz, process
from textblob import TextBlob
import json
import os
from datetime import datetime

class NLPService:
    """Advanced NLP för kommando-tolkning och intent recognition"""
    
    def __init__(self):
        self.setup_nltk()
        self.load_intent_patterns()
        self.load_command_mappings()
        
        print("🧠 NLP Service initialiserad")
    
    def setup_nltk(self):
        """Konfigurera NLTK data"""
        try:
            # Ladda ner nödvändiga NLTK data
            nltk_data = ['punkt', 'averaged_perceptron_tagger', 'stopwords', 'wordnet']
            for data in nltk_data:
                try:
                    nltk.data.find(f'tokenizers/{data}')
                except LookupError:
                    print(f"Laddar ner NLTK data: {data}")
                    nltk.download(data, quiet=True)
        except Exception as e:
            print(f"⚠️ NLTK setup varning: {e}")
    
    def load_intent_patterns(self):
        """Ladda intent-patterns för kommando-klassificering"""
        self.intent_patterns = {
            'research': [
                r'.*research.*',
                r'.*forsk.*',
                r'.*undersök.*',
                r'.*ta reda på.*',
                r'.*hitta information.*',
                r'.*sök efter.*',
                r'.*vad vet du om.*',
                r'.*berätta om.*'
            ],
            'agent_list': [
                r'.*list.*agents?.*',
                r'.*visa.*agents?.*',
                r'.*vilka.*agents?.*',
                r'.*ls.*agents?.*',
                r'.*agents.*lista.*',
                r'.*specialister.*',
                r'.*experter.*'
            ],
            'agent_request': [
                r'.*agent\s+\w+.*',
                r'.*be.*\w+.*agent.*',
                r'.*använd.*\w+.*specialist.*',
                r'.*kontakta.*\w+.*expert.*'
            ],
            'memory': [
                r'.*minne.*',
                r'.*kom ihåg.*',
                r'.*spara.*',
                r'.*memory.*',
                r'.*vad minns du.*'
            ],
            'system': [
                r'.*system.*',
                r'.*status.*',
                r'.*kör.*kommando.*',
                r'.*execute.*',
                r'.*run.*'
            ],
            'learn': [
                r'.*lär.*',
                r'.*learn.*',
                r'.*träna.*',
                r'.*förbättra.*'
            ],
            'help': [
                r'.*hjälp.*',
                r'.*help.*',
                r'.*kommandon.*',
                r'.*vad kan du.*',
                r'.*hur.*'
            ]
        }
    
    def load_command_mappings(self):
        """Mappa naturligt språk till JARVIS-kommandon"""
        self.command_mappings = {
            # Agent-relaterade
            'lista agents': 'agents',
            'visa agents': 'agents',
            'vilka agents finns': 'agents',
            'specialister': 'agents',
            'experter': 'agents',
            
            # Forskning
            'forska om': 'research',
            'undersök': 'research',
            'ta reda på': 'research',
            'berätta om': 'research',
            'vad vet du om': 'research',
            
            # Minne
            'kom ihåg': 'learn',
            'spara': 'learn',
            'minns': 'memory',
            
            # System
            'status': 'system status',
            'systemstatus': 'system status',
            
            # Hjälp
            'vad kan du': 'help',
            'kommandon': 'help'
        }
    
    def extract_intent(self, text: str) -> Dict[str, Any]:
        """Extrahera intent från naturligt språk"""
        text_lower = text.lower().strip()
        
        # Direkt kommando-matching först
        for phrase, command in self.command_mappings.items():
            if phrase in text_lower:
                return {
                    'intent': 'direct_command',
                    'command': command,
                    'confidence': 0.95,
                    'method': 'phrase_mapping',
                    'original_text': text
                }
        
        # Pattern-baserad intent recognition
        best_intent = None
        best_confidence = 0.0
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    confidence = 0.8
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_intent = intent
        
        # Fuzzy matching för agent-kommandon
        if 'agent' in text_lower:
            agent_match = self.extract_agent_request(text)
            if agent_match:
                return {
                    'intent': 'agent_request',
                    'agent_type': agent_match['agent_type'],
                    'request': agent_match['request'],
                    'confidence': agent_match['confidence'],
                    'method': 'agent_extraction',
                    'original_text': text
                }
        
        # Fallback till keyword-baserad analys
        if not best_intent:
            best_intent, best_confidence = self.keyword_analysis(text_lower)
        
        return {
            'intent': best_intent or 'general_query',
            'confidence': best_confidence,
            'method': 'pattern_matching',
            'original_text': text,
            'processed_text': text_lower
        }
    
    def extract_agent_request(self, text: str) -> Optional[Dict[str, Any]]:
        """Extrahera agent-typ och förfrågan från text"""
        # Kända agent-typer
        agent_types = [
            'coder', 'system_analyst', 'data_scientist', 'designer',
            'content_creator', 'university_tutor', 'study_coach', 'image_generator'
        ]
        
        # Svenska aliaser
        agent_aliases = {
            'kodare': 'coder',
            'programmerare': 'coder',
            'utvecklare': 'coder',
            'systemanalytiker': 'system_analyst',
            'datavetare': 'data_scientist',
            'dataanalytiker': 'data_scientist',
            'designer': 'designer',
            'formgivare': 'designer',
            'innehållsskapare': 'content_creator',
            'skribent': 'content_creator',
            'författare': 'content_creator',
            'lärare': 'university_tutor',
            'tutor': 'university_tutor',
            'coach': 'study_coach',
            'studiecoach': 'study_coach',
            'bildgenerator': 'image_generator',
            'ai_artist': 'image_generator'
        }
        
        text_lower = text.lower()
        
        # Sök efter agent-typ
        found_agent = None
        for agent in agent_types:
            if agent in text_lower:
                found_agent = agent
                break
        
        # Kolla aliaser
        if not found_agent:
            for alias, agent in agent_aliases.items():
                if alias in text_lower:
                    found_agent = agent
                    break
        
        if found_agent:
            # Extrahera förfrågan (ta bort agent-referenser)
            request = text
            for remove_word in ['agent', found_agent] + list(agent_aliases.keys()):
                request = re.sub(rf'\b{remove_word}\b', '', request, flags=re.IGNORECASE)
            
            request = ' '.join(request.split()).strip()
            
            return {
                'agent_type': found_agent,
                'request': request,
                'confidence': 0.85
            }
        
        return None
    
    def keyword_analysis(self, text: str) -> Tuple[str, float]:
        """Fallback keyword-baserad intent-analys"""
        keywords = {
            'research': ['forskning', 'information', 'data', 'fakta', 'sök', 'hitta'],
            'system': ['system', 'dator', 'kommando', 'status', 'process'],
            'agent_list': ['lista', 'visa', 'vilka', 'agents', 'specialister'],
            'memory': ['minne', 'kom ihåg', 'spara', 'lagra'],
            'learn': ['lär', 'träna', 'förbättra', 'utveckla'],
            'help': ['hjälp', 'guide', 'instruktion', 'vägledning']
        }
        
        word_count = {}
        words = text.split()
        
        for intent, intent_keywords in keywords.items():
            count = sum(1 for word in words if any(kw in word for kw in intent_keywords))
            if count > 0:
                word_count[intent] = count / len(words)
        
        if word_count:
            best_intent = max(word_count, key=word_count.get)
            confidence = word_count[best_intent]
            return best_intent, min(confidence * 2, 0.7)  # Max 0.7 för keyword-analys
        
        return 'general_query', 0.1
    
    def enhance_command_understanding(self, text: str) -> Dict[str, Any]:
        """Förbättra kommando-förståelse med NLP"""
        
        # Grundläggande språkanalys utan problematiska TextBlob funktioner
        analysis = {
            'language': 'sv' if any(word in text.lower() for word in 
                ['och', 'eller', 'med', 'för', 'att', 'är', 'som']) else 'en'
        }
        
        # Intent extraction
        intent_info = self.extract_intent(text)
        analysis.update(intent_info)
        
        # Kontextuell förbättring
        if analysis['intent'] == 'research':
            # Extrahera ämne för forskning
            topic = self.extract_research_topic(text)
            if topic:
                analysis['extracted_topic'] = topic
        
        elif analysis['intent'] == 'agent_list':
            analysis['suggested_command'] = 'agents'
        
        return analysis
    
    def extract_research_topic(self, text: str) -> Optional[str]:
        """Extrahera forskningsämne från text"""
        # Ta bort kommando-ord
        topic = text
        remove_words = ['research', 'forska', 'om', 'undersök', 'ta reda på', 'berätta']
        
        for word in remove_words:
            topic = re.sub(rf'\b{word}\b', '', topic, flags=re.IGNORECASE)
        
        topic = ' '.join(topic.split()).strip()
        
        return topic if topic else None
    
    def suggest_corrections(self, text: str) -> List[str]:
        """Föreslå rättelser för felstavade kommandon"""
        common_commands = [
            'research', 'learn', 'memory', 'system', 'agents', 'help',
            'agent coder', 'agent designer', 'agent data_scientist',
            'forska', 'lär', 'minne', 'system status', 'hjälp'
        ]
        
        # Hitta närliggande kommandon
        matches = process.extract(text, common_commands, limit=3, scorer=fuzz.ratio)
        
        return [match[0] for match in matches if match[1] > 60]
    
    def get_nlp_stats(self) -> Dict[str, Any]:
        """Returnera NLP-statistik och status"""
        return {
            'service': 'NLP Service',
            'intents_loaded': len(self.intent_patterns),
            'command_mappings': len(self.command_mappings),
            'nltk_status': 'active',
            'supported_languages': ['sv', 'en'],
            'features': [
                'Intent Recognition',
                'Command Mapping', 
                'Agent Extraction',
                'Fuzzy Matching',
                'Sentiment Analysis'
            ]
        }

# Exportera klassen
__all__ = ['NLPService']
