"""
JARVIS Advanced Agent System
Specialiserade AI-agents med olika expertområden och sudo-rättigheter
"""

import subprocess
import getpass
import asyncio
import json
import os
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
from abc import ABC, abstractmethod

class SecurityManager:
    """Hanterar säker sudo-användning och logging"""
    
    def __init__(self):
        self.sudo_log_file = "jarvis_sudo.log"
        self.allowed_sudo_commands = {
            'apt': ['install', 'update', 'upgrade', 'remove'],
            'systemctl': ['start', 'stop', 'restart', 'enable', 'disable', 'status'],
            'docker': ['run', 'stop', 'start', 'ps', 'images', 'build'],
            'ufw': ['enable', 'disable', 'status', 'allow', 'deny'],
            'mount': ['mount', 'umount'],
            'crontab': ['-e', '-l'],
        }
    
    def log_sudo_command(self, command: str, user: str, success: bool):
        """Logga alla sudo-kommandon för säkerhet"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'user': user,
            'command': command,
            'success': success
        }
        
        with open(self.sudo_log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def is_command_allowed(self, command: str) -> bool:
        """Kontrollera om sudo-kommando är tillåtet"""
        parts = command.split()
        if not parts:
            return False
        
        base_command = parts[0]
        if base_command in self.allowed_sudo_commands:
            if len(parts) > 1:
                sub_command = parts[1]
                return sub_command in self.allowed_sudo_commands[base_command]
            return True
        return False
    
    async def execute_sudo_command(self, command: str, user: str = "jarvis") -> Dict[str, Any]:
        """Exekvera sudo-kommando säkert med password-prompt"""
        
        # Kontrollera om kommando är tillåtet
        if not self.is_command_allowed(command):
            self.log_sudo_command(command, user, False)
            return {
                'success': False,
                'error': f'Kommando inte tillåtet: {command}',
                'security_violation': True
            }
        
        try:
            print(f"🔐 Sudo-rättigheter krävs för: {command}")
            password = getpass.getpass("Ange ditt lösenord: ")
            
            # Exekvera kommando med sudo
            process = await asyncio.create_subprocess_shell(
                f"echo '{password}' | sudo -S {command}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                self.log_sudo_command(command, user, True)
                return {
                    'success': True,
                    'output': stdout.decode().strip(),
                    'command': command
                }
            else:
                self.log_sudo_command(command, user, False)
                return {
                    'success': False,
                    'error': stderr.decode().strip(),
                    'command': command
                }
                
        except Exception as e:
            self.log_sudo_command(command, user, False)
            return {
                'success': False,
                'error': f'Sudo execution error: {str(e)}',
                'command': command
            }

class BaseAgent(ABC):
    """Bas-klass för alla specialiserade agents"""
    
    def __init__(self, name: str, speciality: str):
        self.name = name
        self.speciality = speciality
        self.security_manager = SecurityManager()
        self.conversation_history = []
    
    @abstractmethod
    async def process_request(self, request: str, context: Dict = None) -> Dict[str, Any]:
        """Process en förfrågan specifik för denna agent"""
        pass
    
    def can_handle(self, request: str) -> float:
        """Returnera confidence score (0-1) för om denna agent kan hantera förfrågan"""
        keywords = self.get_keywords()
        request_lower = request.lower()
        
        # Count exact matches and partial matches
        exact_matches = sum(1 for keyword in keywords if keyword in request_lower)
        
        # Bonus för längre keyword matches
        word_matches = 0
        request_words = request_lower.split()
        for keyword in keywords:
            if keyword in request_words:
                word_matches += 1
        
        # Calculate confidence with bonus for exact word matches
        total_score = exact_matches + (word_matches * 1.5)
        confidence = min(total_score / max(len(keywords), 5), 1.0)
        
        return confidence
    
    @abstractmethod
    def get_keywords(self) -> List[str]:
        """Returnera keywords som denna agent hanterar"""
        pass
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Returnera agent's kapaciteter"""
        return {
            'name': self.name,
            'speciality': self.speciality,
            'keywords': self.get_keywords(),
            'sudo_enabled': True
        }

class CoderAgent(BaseAgent):
    """Senior Developer Agent - Programmering och arkitektur"""
    
    def __init__(self):
        super().__init__("Senior Developer", "Full-stack utveckling och arkitektur")
        self.supported_languages = [
            'python', 'java', 'cpp', 'c++', 'bash', 'go', 'rust', 
            'javascript', 'typescript', 'html', 'css', 'sql'
        ]
    
    def get_keywords(self) -> List[str]:
        return [
            'kod', 'programmera', 'utveckla', 'code', 'script', 'funktion',
            'bug', 'fel', 'optimera', 'refactor', 'arkitektur', 'api',
            'databas', 'docker', 'git', 'deploy', 'test', 'debug'
        ] + self.supported_languages
    
    async def process_request(self, request: str, context: Dict = None) -> Dict[str, Any]:
        """Process coding-relaterade förfrågningar"""
        
        request_lower = request.lower()
        
        # Code generation
        if any(word in request_lower for word in ['skapa', 'generera', 'skriv kod']):
            return await self._generate_code(request)
        
        # Code review
        elif any(word in request_lower for word in ['granska', 'review', 'förbättra']):
            return await self._code_review(request)
        
        # Environment setup
        elif any(word in request_lower for word in ['installera', 'setup', 'konfigurera']):
            return await self._setup_environment(request)
        
        # Git operations
        elif any(word in request_lower for word in ['git', 'commit', 'push', 'clone']):
            return await self._git_operations(request)
        
        else:
            return await self._general_coding_help(request)
    
    async def _generate_code(self, request: str) -> Dict[str, Any]:
        """Generera kod baserat på beskrivning"""
        
        # Analysera vad som begärs
        if 'api' in request.lower() and 'python' in request.lower():
            code = '''
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Generated API", version="1.0.0")

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

items_db = []

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.get("/items", response_model=List[Item])
async def get_items():
    return items_db

@app.post("/items", response_model=Item)
async def create_item(item: Item):
    items_db.append(item)
    return item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
            return {
                'success': True,
                'code': code,
                'language': 'python',
                'description': 'FastAPI REST API med CRUD operationer',
                'instructions': [
                    'Spara som main.py',
                    'Installera: pip install fastapi uvicorn',
                    'Kör: python main.py',
                    'Testa: http://localhost:8000/docs'
                ]
            }
        
        elif 'bash script' in request.lower():
            script = '''#!/bin/bash

# Automatiserat setup script
set -e

echo "🚀 Startar setup..."

# Uppdatera systemet
sudo apt update && sudo apt upgrade -y

# Installera development tools
sudo apt install -y git curl wget vim build-essential

# Installera Python och pip
sudo apt install -y python3 python3-pip python3-venv

# Skapa utvecklingsmiljö
mkdir -p ~/dev
cd ~/dev

echo "✅ Setup klart!"
'''
            return {
                'success': True,
                'code': script,
                'language': 'bash',
                'description': 'Automatiserat development setup script',
                'instructions': [
                    'Spara som setup.sh',
                    'Gör exekverbar: chmod +x setup.sh',
                    'Kör: ./setup.sh'
                ]
            }
        
        return {
            'success': True,
            'message': 'Kod-generering klar! Specificera mer detaljer för bättre resultat.',
            'suggestions': [
                'Vilket programmeringsspråk?',
                'Vilken typ av applikation?',
                'Specifika krav eller funktioner?'
            ]
        }
    
    async def _setup_environment(self, request: str) -> Dict[str, Any]:
        """Setup utvecklingsmiljö"""
        
        if 'docker' in request.lower():
            commands = [
                'apt update',
                'apt install -y docker.io docker-compose',
                'systemctl start docker',
                'systemctl enable docker',
                'usermod -aG docker bjorn'
            ]
            
            results = []
            for cmd in commands:
                result = await self.security_manager.execute_sudo_command(cmd)
                results.append(result)
            
            return {
                'success': all(r['success'] for r in results),
                'message': 'Docker installation klar!' if all(r['success'] for r in results) else 'Några kommandon misslyckades',
                'details': results,
                'next_steps': [
                    'Logga ut och in igen för docker group',
                    'Testa: docker run hello-world',
                    'Skapa Dockerfile för ditt projekt'
                ]
            }
        
        elif 'python' in request.lower():
            commands = [
                'apt update',
                'apt install -y python3 python3-pip python3-venv python3-dev'
            ]
            
            results = []
            for cmd in commands:
                result = await self.security_manager.execute_sudo_command(cmd)
                results.append(result)
            
            return {
                'success': all(r['success'] for r in results),
                'message': 'Python development environment setup klar!',
                'details': results,
                'next_steps': [
                    'Skapa virtual environment: python3 -m venv myenv',
                    'Aktivera: source myenv/bin/activate',
                    'Installera packages: pip install -r requirements.txt'
                ]
            }
        
        return {
            'success': True,
            'message': 'Specificera vilken utvecklingsmiljö du vill setuppa',
            'options': ['docker', 'python', 'nodejs', 'java', 'go']
        }
    
    async def _git_operations(self, request: str) -> Dict[str, Any]:
        """Hantera Git-operationer"""
        
        # Detta skulle normalt integrera med git commands
        return {
            'success': True,
            'message': 'Git-operationer implementeras...',
            'available_operations': [
                'clone repository',
                'commit changes', 
                'push to remote',
                'create branch',
                'merge branches'
            ]
        }
    
    async def _code_review(self, request: str) -> Dict[str, Any]:
        """Code review och förbättringsförslag"""
        
        return {
            'success': True,
            'message': 'Code review funktionalitet implementeras...',
            'review_areas': [
                'Code quality och readability',
                'Performance optimizations',
                'Security vulnerabilities',
                'Best practices',
                'Documentation'
            ]
        }
    
    async def _general_coding_help(self, request: str) -> Dict[str, Any]:
        """Allmän coding-hjälp"""
        
        return {
            'success': True,
            'message': f'Kodhjälp för: {request}',
            'capabilities': [
                '💻 Code generation i 10+ språk',
                '🔍 Code review och optimering',
                '🏗️ Arkitektur design',
                '🐳 DevOps automation',
                '🔧 Development environment setup',
                '📊 Performance analysis'
            ],
            'suggestion': 'Var mer specifik med din coding-fråga för bättre hjälp!'
        }

class SystemAnalystAgent(BaseAgent):
    """System Analytiker/Utvecklare Agent"""
    
    def __init__(self):
        super().__init__("System Analytiker", "System optimering och infrastruktur")
    
    def get_keywords(self) -> List[str]:
        return [
            'system', 'optimera', 'performance', 'säkerhet', 'backup',
            'firewall', 'nätverk', 'server', 'service', 'process',
            'disk', 'minne', 'cpu', 'monitoring', 'log', 'cron'
        ]
    
    async def process_request(self, request: str, context: Dict = None) -> Dict[str, Any]:
        """Process system-relaterade förfrågningar"""
        
        request_lower = request.lower()
        
        if any(word in request_lower for word in ['backup', 'säkerhetskopia']):
            return await self._setup_backup(request)
        
        elif any(word in request_lower for word in ['firewall', 'säkerhet']):
            return await self._configure_security(request)
        
        elif any(word in request_lower for word in ['optimera', 'performance']):
            return await self._system_optimization(request)
        
        elif any(word in request_lower for word in ['status', 'monitor']):
            return await self._system_monitoring(request)
        
        else:
            return await self._general_system_help(request)
    
    async def _setup_backup(self, request: str) -> Dict[str, Any]:
        """Setup automatiska backups"""
        
        backup_script = '''#!/bin/bash
# JARVIS Automatic Backup Script

BACKUP_DIR="/home/bjorn/backups"
SOURCE_DIRS="/home/bjorn/Documents /home/bjorn/kod /home/bjorn/Skrivbord/Jarvis"
DATE=$(date +%Y%m%d_%H%M%S)

# Skapa backup directory
mkdir -p "$BACKUP_DIR"

# Backup med rsync
for dir in $SOURCE_DIRS; do
    if [ -d "$dir" ]; then
        echo "Backing up $dir..."
        rsync -av "$dir" "$BACKUP_DIR/backup_$DATE/"
    fi
done

# Komprimera backup
tar -czf "$BACKUP_DIR/backup_$DATE.tar.gz" "$BACKUP_DIR/backup_$DATE/"
rm -rf "$BACKUP_DIR/backup_$DATE/"

echo "Backup klar: $BACKUP_DIR/backup_$DATE.tar.gz"
'''
        
        # Setup cron job för automatiska backups
        cron_entry = "0 2 * * 0 /home/bjorn/backup_script.sh >> /var/log/jarvis_backup.log 2>&1"
        
        return {
            'success': True,
            'backup_script': backup_script,
            'cron_schedule': cron_entry,
            'instructions': [
                'Spara script som ~/backup_script.sh',
                'chmod +x ~/backup_script.sh',
                'Lägg till i crontab för veckovis backup',
                'Testa manuellt först'
            ],
            'message': 'Backup-system konfigurerat för veckovis automatiska backups'
        }
    
    async def _configure_security(self, request: str) -> Dict[str, Any]:
        """Konfigurera system-säkerhet"""
        
        security_commands = [
            'ufw enable',
            'ufw default deny incoming',
            'ufw default allow outgoing',
            'ufw allow 22/tcp',  # SSH
            'ufw allow 80/tcp',  # HTTP
            'ufw allow 443/tcp', # HTTPS
        ]
        
        results = []
        for cmd in security_commands:
            result = await self.security_manager.execute_sudo_command(cmd)
            results.append(result)
        
        return {
            'success': all(r['success'] for r in results),
            'message': 'Grundläggande firewall-säkerhet konfigurerad',
            'configured_rules': security_commands,
            'results': results,
            'additional_security': [
                'Installera fail2ban för brute-force protection',
                'Konfigurera automatiska säkerhetsuppdateringar',
                'Setup SSH key-based authentication',
                'Aktivera auditd för system logging'
            ]
        }
    
    async def _system_monitoring(self, request: str) -> Dict[str, Any]:
        """System monitoring och status"""
        
        try:
            # Samla system-information
            cpu_info = subprocess.run(['cat', '/proc/cpuinfo'], capture_output=True, text=True)
            memory_info = subprocess.run(['free', '-h'], capture_output=True, text=True)
            disk_info = subprocess.run(['df', '-h'], capture_output=True, text=True)
            uptime_info = subprocess.run(['uptime'], capture_output=True, text=True)
            
            return {
                'success': True,
                'system_status': {
                    'cpu': cpu_info.stdout.split('\n')[0] if cpu_info.returncode == 0 else 'N/A',
                    'memory': memory_info.stdout if memory_info.returncode == 0 else 'N/A',
                    'disk': disk_info.stdout if disk_info.returncode == 0 else 'N/A',
                    'uptime': uptime_info.stdout.strip() if uptime_info.returncode == 0 else 'N/A'
                },
                'monitoring_suggestions': [
                    'Installera htop för real-time monitoring',
                    'Setup Prometheus + Grafana för advanced monitoring',
                    'Konfigurera logrotate för log management',
                    'Skapa alerting för kritiska system events'
                ]
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Kunde inte hämta system-info: {str(e)}'
            }
    
    async def _system_optimization(self, request: str) -> Dict[str, Any]:
        """System optimering"""
        
        optimization_commands = [
            'apt update && apt upgrade -y',
            'apt autoremove -y',
            'apt autoclean'
        ]
        
        return {
            'success': True,
            'message': 'System-optimering förslag',
            'optimization_steps': [
                'Uppdatera alla packages',
                'Ta bort onödiga packages',
                'Rensa package cache',
                'Defragmentera disk (om ext4)',
                'Optimera swap usage'
            ],
            'automated_commands': optimization_commands,
            'manual_checks': [
                'Kontrollera startup services',
                'Analysera disk usage patterns',
                'Review installed applications',
                'Check for memory leaks'
            ]
        }
    
    async def _general_system_help(self, request: str) -> Dict[str, Any]:
        """Allmän systemhjälp"""
        
        return {
            'success': True,
            'message': f'System-hjälp för: {request}',
            'capabilities': [
                '🔧 System optimization och performance tuning',
                '🔐 Säkerhetskonfiguration och firewall setup',
                '💾 Automatiska backup-lösningar',
                '📊 System monitoring och alerting',
                '🛠️ Service management och automation',
                '📝 Log analysis och troubleshooting'
            ],
            'suggestion': 'Specificera vad du vill göra med systemet för detaljerad hjälp!'
        }

# Lägg till fler agents här...
class UniversityTutorAgent(BaseAgent):
    """University Tutor Agent för akademisk hjälp"""
    
    def __init__(self):
        super().__init__("University Tutor", "Akademisk vägledning och utbildning")
        self.subjects = [
            'matematik', 'fysik', 'kemi', 'biologi', 'datalogi', 
            'programmering', 'statistik', 'ekonomi', 'filosofi'
        ]
    
    def get_keywords(self) -> List[str]:
        return [
            'studera', 'kurs', 'tentamen', 'uppsats', 'forskning', 'akademisk',
            'teori', 'bevis', 'formel', 'koncept', 'förklara', 'lära',
            'university', 'universitet', 'skola', 'utbildning', 'lektion'
        ] + self.subjects
    
    async def process_request(self, request: str, context: Dict = None) -> Dict[str, Any]:
        """Process akademiska förfrågningar"""
        
        request_lower = request.lower()
        
        if any(word in request_lower for word in ['förklara', 'explain', 'vad är']):
            return await self._explain_concept(request)
        elif any(word in request_lower for word in ['studera', 'study plan', 'schema']):
            return await self._create_study_plan(request)
        elif any(word in request_lower for word in ['tentamen', 'exam', 'förbered']):
            return await self._exam_preparation(request)
        elif any(word in request_lower for word in ['uppsats', 'essay', 'skriva']):
            return await self._essay_help(request)
        else:
            return await self._general_academic_help(request)
    
    async def _explain_concept(self, request: str) -> Dict[str, Any]:
        """Förklara akademiska koncept"""
        
        # Exempel för matematiska koncept
        if any(word in request.lower() for word in ['derivata', 'derivative', 'integral']):
            explanation = '''
# Matematisk Förklaring: Derivata

## Definition
Derivatan av en funktion f(x) vid punkt x beskriver funktionens förändringshastighet vid den punkten.

## Intuition
- Tänk på en bil som åker längs en väg
- Funktionen f(x) = bilens position vid tid x
- Derivatan f'(x) = bilens hastighet vid tid x

## Formell Definition
f'(x) = lim(h→0) [f(x+h) - f(x)]/h

## Grundläggande Regler
1. **Konstant regel:** (c)' = 0
2. **Kraft regel:** (x^n)' = n·x^(n-1)
3. **Summa regel:** (f + g)' = f' + g'
4. **Produkt regel:** (f·g)' = f'·g + f·g'
5. **Kvot regel:** (f/g)' = (f'·g - f·g')/g²

## Praktiska Tillämpningar
- Optimering (hitta maximum/minimum)
- Fysik (hastighet, acceleration)
- Ekonomi (marginalkostnader)
- Teknik (signalbehandling)

## Övningsexempel
Beräkna derivatan av f(x) = 3x² + 2x - 1
Svar: f'(x) = 6x + 2
'''
            
            return {
                'success': True,
                'explanation': explanation,
                'type': 'concept_explanation',
                'subject': 'Matematik',
                'practice_problems': [
                    'Beräkna derivatan av f(x) = x³ - 4x + 7',
                    'Hitta kritiska punkter för g(x) = x² - 6x + 8',
                    'Använd produktregeln för h(x) = x²·sin(x)'
                ],
                'next_topics': [
                    'Integraler och fundamental theorem',
                    'Kedjeregeln för sammansatta funktioner',
                    'Tillämpningar inom fysik och ekonomi'
                ]
            }
        
        return {
            'success': True,
            'message': 'Specificera vilket koncept du vill ha förklarat',
            'available_subjects': self.subjects
        }
    
    async def _create_study_plan(self, request: str) -> Dict[str, Any]:
        """Skapa studieplan"""
        
        study_plan = '''
# Personlig Studieplan - JARVIS Academic Assistant

## Veckoschema Template

### Måndag
- **09:00-11:00:** Matematik (teori)
- **11:30-12:30:** Programmering (praktik)
- **14:00-16:00:** Fysik (problemlösning)
- **19:00-20:00:** Repetition och anteckningar

### Tisdag  
- **09:00-10:30:** Datalogi (föreläsning review)
- **11:00-12:30:** Matematik (övningar)
- **14:00-15:30:** Projekt arbete
- **16:00-17:00:** Group study session

### Onsdag
- **10:00-12:00:** Fysik laborationer
- **13:00-15:00:** Programmering projekt
- **15:30-17:00:** Matematik extra övningar
- **19:00-20:00:** Flashcards och memorering

### Torsdag
- **09:00-11:00:** Datalogi (algoritmer)
- **11:30-12:30:** Quick review sessions
- **14:00-16:00:** Uppsats arbete
- **16:30-17:30:** Research och källor

### Fredag
- **09:00-10:30:** Matematik (svåra problem)
- **11:00-12:00:** Programmering debugging
- **14:00-16:00:** Project presentation prep
- **16:30-17:30:** Weekly review

## Studieteknik Rekommendationer

### Active Learning
- Feynman Technique: Förklara för andra
- Spaced Repetition: Anki flashcards
- Practice Testing: Mock exams

### Time Management
- Pomodoro Technique (25 min fokus, 5 min paus)
- Time blocking för olika ämnen
- Buffer time för oväntade uppgifter

### Resource Management
- Digitala verktyg: Notion, Obsidian, Anki
- Physical: Whiteboard för problemlösning
- Backup plans för tech failures

## Månadsvis Mål
- **Vecka 1:** Grundläggande förståelse
- **Vecka 2:** Tillämpning och övningar  
- **Vecka 3:** Fördjupning och svåra problem
- **Vecka 4:** Review, mock exams, preparation
'''
        
        return {
            'success': True,
            'study_plan': study_plan,
            'type': 'study_schedule',
            'customization_tips': [
                'Anpassa efter dina peak performance timmar',
                'Lägg till buffer time för svåra ämnen',
                'Inkludera breaks och physical activity',
                'Balance mellan teori och praktik',
                'Weekly reviews för att justera planen'
            ],
            'productivity_tools': [
                'Pomodoro timer apps',
                'Anki för spaced repetition',
                'Notion för note-taking',
                'Calendar blocking',
                'Progress tracking apps'
            ]
        }
    
    async def _general_academic_help(self, request: str) -> Dict[str, Any]:
        """Allmän akademisk hjälp"""
        return {
            'success': True,
            'message': 'Academic Tutor hjälp tillgänglig!',
            'capabilities': [
                '📚 Konceptförklaringar inom matematik, fysik, datalogi',
                '📅 Personliga studieplaner och scheman',
                '📝 Uppsats- och forskningshjälp',
                '🎯 Tentamensförberedelser',
                '🧠 Studieteknik och memorering',
                '📊 Progress tracking och motivation'
            ],
            'subjects': self.subjects,
            'suggestion': 'Specificera vilket ämne eller vilket typ av hjälp du behöver!'
        }

class StudyCoachAgent(BaseAgent):
    """Study Coach Agent för motivation och produktivitet"""
    
    def __init__(self):
        super().__init__("Study Coach", "Motivation och produktivitetscoaching")
        self.coaching_areas = [
            'motivation', 'produktivitet', 'time management', 'stress management',
            'goal setting', 'habit building', 'procrastination'
        ]
    
    def get_keywords(self) -> List[str]:
        return [
            'motivation', 'produktivitet', 'stress', 'prokrastinering', 'mål',
            'vana', 'rutiner', 'tid', 'fokus', 'koncentration', 'burnout',
            'balans', 'disciplin', 'coaching', 'utveckling', 'tillväxt'
        ] + self.coaching_areas
    
    async def process_request(self, request: str, context: Dict = None) -> Dict[str, Any]:
        """Process coaching-relaterade förfrågningar"""
        
        request_lower = request.lower()
        
        if any(word in request_lower for word in ['motivation', 'motivera', 'orka']):
            return await self._motivation_boost(request)
        elif any(word in request_lower for word in ['prokrastinering', 'procrastination', 'skjuta upp']):
            return await self._procrastination_help(request)
        elif any(word in request_lower for word in ['stress', 'ångest', 'overwhelmed']):
            return await self._stress_management(request)
        elif any(word in request_lower for word in ['mål', 'goal', 'planera']):
            return await self._goal_setting(request)
        else:
            return await self._general_coaching(request)
    
    async def _motivation_boost(self, request: str) -> Dict[str, Any]:
        """Motivation och energi boost"""
        
        motivation_strategies = '''
# 🚀 Motivation Boost - JARVIS Study Coach

## Omedelbar Energi (Nu!)
1. **5-minuters regel:** Starta med bara 5 minuter
2. **Win the morning:** Gör något litet framgångsrikt först
3. **Environment change:** Byt plats, ny energi
4. **Power pose:** 2 minuter confident body language
5. **Motiverande musik:** Skapa en "Study Beast Mode" playlist

## Mental Reset Techniques
### The "Why" Ladder
- Varför studerar du detta? → För att klara kursen
- Varför vill du klara kursen? → För examen
- Varför vill du ha examen? → För drömjobbet
- Varför vill du ha drömjobbet? → För att förverkliga din potential

### Progress Visualization
- Skriv ner vad du redan lärt dig denna vecka
- Lista 3 konkreta skills du utvecklat
- Tänk på framtida-dig som tackar nuvarande-dig

## Långsiktig Motivation
### Identity-Based Habits
- "Jag är någon som alltid följer igenom"
- "Jag är en person som prioriterar lärande"
- "Jag är disciplinerad och konsekvent"

### Reward System
- Micro-rewards: Favoritfika efter 1h studie
- Daily rewards: Netflix episode efter studiedag
- Weekly rewards: Något du verkligen ser fram emot
- Monthly rewards: Större belöning för månadsvis progress

## Emergency Motivation Protocol
När allt känns hopplöst:

1. **Micro-commitment:** Bara öppna boken (inget mer)
2. **Study buddy:** Ring någon och studera tillsammans
3. **Change the stakes:** Berätta för någon vad du ska göra idag
4. **Future self letter:** Skriv till dig om 1 år - vad vill du att hen ska tacka dig för?
5. **Rest and reset:** Ibland behöver hjärnan vila först

## Mantras för Tuffa Dagar
- "Jag behöver inte känna mig motiverad för att agera"
- "Disciplin bygger motivation, inte tvärtom"
- "Varje liten action är en röst för den person jag vill bli"
- "Future me will be grateful for what I do today"
'''
        
        return {
            'success': True,
            'motivation_guide': motivation_strategies,
            'type': 'motivation_coaching',
            'immediate_actions': [
                '🎯 Välj EN liten sak att göra nu (5-10 min)',
                '🎵 Sätt på motiverande musik',
                '💪 Gör en power pose i 2 minuter',
                '📝 Skriv ner VARFÖR du studerar',
                '🏆 Sätt en belöning för när du är klar'
            ],
            'emergency_contacts': [
                'Study buddy telefonnummer',
                'Online study communities',
                'Academic counselor',
                'JARVIS for instant pep talk!'
            ]
        }
    
    async def _procrastination_help(self, request: str) -> Dict[str, Any]:
        """Anti-prokrastinering strategier"""
        
        anti_procrastination = '''
# 🎯 Anti-Procrastination Toolkit

## Akut Ingripande (När du prokrastinerar NU)

### 2-Minute Rule
- Om det tar mindre än 2 minuter: GÖR DET NU
- Om det tar mer: Skriv ner första steget (som tar <2 min)

### Pomodoro Escape
1. Sätt timer på 25 minuter
2. Jobba BARA på en sak
3. Efter 25 min: 5 min paus (obligatorisk!)
4. Repeat. Efter 4 cykler: 30 min paus

### Environment Design
- **Remove distractions:** Telefon i annan rum
- **Add friction:** Logga ut från social media
- **Make it easier:** Ha allt förberett innan du börjar

## Root Cause Analysis

### Varför prokrastinerar vi?
1. **Perfectionism:** "Det måste bli perfekt"
   - **Fix:** Aim för "good enough" först
2. **Overwhelm:** "Det är för mycket"
   - **Fix:** Break it down i tiny steps
3. **Fear of failure:** "Tänk om jag inte klarar det"
   - **Fix:** Reframe som learning opportunity
4. **Lack of clarity:** "Jag vet inte vart jag ska börja"
   - **Fix:** Spend 5 min planning first

### The Procrastination Equation
Motivation = (Expectancy × Value) / (Impulsiveness × Delay)

**Increase:**
- Expectancy: "Jag KAN klara detta"
- Value: "Detta är VIKTIGT för mig"

**Decrease:**
- Impulsiveness: Remove distractions
- Delay: Make rewards immediate

## Systemlösningar

### Time Blocking
```
09:00-09:30: Email & planning
09:30-11:00: Deep work session 1
11:00-11:15: Break
11:15-12:45: Deep work session 2
12:45-13:45: Lunch
13:45-15:15: Less demanding tasks
```

### Implementation Intentions
"When X happens, I will do Y"
- "When I sit down at my desk, I will open my textbook"
- "When I feel like checking my phone, I will take 3 deep breaths first"
- "When I finish a study session, I will immediately plan the next one"

## Advanced Techniques

### Temptation Bundling
- Listen to favorite podcast ONLY while doing boring admin tasks
- Watch Netflix ONLY while doing flashcards
- Drink fancy coffee ONLY during study sessions

### The "Good Enough" Approach
- Första draft behöver bara existera, inte vara bra
- 80% completed > 0% perfect
- Done is better than perfect

### Social Accountability
- Study streams on Twitch/YouTube
- Body doubling sessions
- Regular check-ins med study buddy
- Progress photos/videos för social media
'''
        
        return {
            'success': True,
            'anti_procrastination_guide': anti_procrastination,
            'type': 'procrastination_coaching',
            'immediate_intervention': [
                '⏰ Sätt 25-minuters timer NU',
                '📱 Lägg undan telefonen',
                '📝 Skriv ner första steget (2-min task)',
                '🏗️ Break big task in 5 smaller pieces',
                '👥 Text en vän om vad du ska göra'
            ],
            'habit_tracking': {
                'daily_question': 'På en skala 1-10, hur produktiv var jag idag?',
                'weekly_review': 'Vad fungerade bra? Vad kan förbättras?',
                'monthly_adjustment': 'Vilka system behöver uppdateras?'
            }
        }
    
    async def _general_coaching(self, request: str) -> Dict[str, Any]:
        """Allmän coaching hjälp"""
        return {
            'success': True,
            'message': 'Study Coach hjälp tillgänglig!',
            'capabilities': [
                '🔥 Motivation och energi boosting',
                '⏰ Prokrastinering bekämpning',
                '🧘 Stress management tekniker',
                '🎯 Goal setting och achievement',
                '🔄 Habit building och behavior change',
                '📈 Progress tracking och accountability'
            ],
            'coaching_areas': self.coaching_areas,
            'suggestion': 'Berätta vad du kämpar med så kan jag ge specifik coaching!'
        }

class DataScientistAgent(BaseAgent):
    """Data Scientist Agent för analys och ML"""
    
    def __init__(self):
        super().__init__("Data Scientist", "Dataanalys, ML och AI")
        self.ml_frameworks = ['tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy']
    
    def get_keywords(self) -> List[str]:
        return [
            'data', 'analys', 'dataset', 'ml', 'machine learning', 'ai',
            'pandas', 'numpy', 'matplotlib', 'seaborn', 'jupyter',
            'statistik', 'regression', 'clustering', 'classification',
            'neural network', 'deep learning', 'visualisering'
        ] + self.ml_frameworks
    
    async def process_request(self, request: str, context: Dict = None) -> Dict[str, Any]:
        """Process data science förfrågningar"""
        
        request_lower = request.lower()
        
        if any(word in request_lower for word in ['analys', 'analyze', 'dataset']):
            return await self._data_analysis(request)
        elif any(word in request_lower for word in ['ml', 'machine learning', 'träna modell']):
            return await self._ml_pipeline(request)
        elif any(word in request_lower for word in ['visualisera', 'plot', 'graf']):
            return await self._data_visualization(request)
        else:
            return await self._general_data_help(request)
    
    async def _data_analysis(self, request: str) -> Dict[str, Any]:
        """Generera data analysis kod"""
        
        analysis_code = '''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Ladda och inspektera data
df = pd.read_csv('your_data.csv')

# Grundläggande statistik
print("📊 Dataset Info:")
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print("\\n" + "="*50)

print("📈 Beskrivande statistik:")
print(df.describe())
print("\\n" + "="*50)

print("❓ Missing values:")
print(df.isnull().sum())
print("\\n" + "="*50)

# Korrelationsanalys
plt.figure(figsize=(12, 8))
correlation_matrix = df.select_dtypes(include=[np.number]).corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Korrelationsmatris')
plt.tight_layout()
plt.show()

# Outlier detection
def detect_outliers(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return data[(data[column] < lower_bound) | (data[column] > upper_bound)]

# Data cleaning suggestions
print("🧹 Data Cleaning Rekommendationer:")
numeric_cols = df.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    outliers = detect_outliers(df, col)
    if len(outliers) > 0:
        print(f"• {col}: {len(outliers)} potentiella outliers")
'''
        
        return {
            'success': True,
            'code': analysis_code,
            'language': 'python',
            'description': 'Komplett dataanalys pipeline',
            'next_steps': [
                'Ersätt \'your_data.csv\' med din datafil',
                'Installera: pip install pandas numpy matplotlib seaborn scipy',
                'Kör analysen steg för steg',
                'Anpassa baserat på dina specifika behov'
            ]
        }
    
    async def _ml_pipeline(self, request: str) -> Dict[str, Any]:
        """Generera ML pipeline kod"""
        
        ml_code = '''
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Data Loading och Preprocessing
df = pd.read_csv('your_data.csv')

# Hantera missing values
df = df.fillna(df.mean(numeric_only=True))  # För numeriska
df = df.fillna(df.mode().iloc[0])  # För kategoriska

# Feature engineering
# Lägg till dina egna features här
X = df.drop('target_column', axis=1)  # Features
y = df['target_column']  # Target

# Encoding kategoriska variabler
categorical_columns = X.select_dtypes(include=['object']).columns
le = LabelEncoder()
for col in categorical_columns:
    X[col] = le.fit_transform(X[col].astype(str))

# 2. Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Feature Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 4. Model Training och Evaluation
models = {
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(random_state=42),
    'Logistic Regression': LogisticRegression(random_state=42)
}

results = {}
for name, model in models.items():
    # Cross-validation
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
    
    # Träna på hela training set
    model.fit(X_train_scaled, y_train)
    
    # Predictions
    y_pred = model.predict(X_test_scaled)
    
    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    
    results[name] = {
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std(),
        'test_accuracy': accuracy,
        'model': model
    }
    
    print(f"\\n{name}:")
    print(f"CV Score: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
    print(f"Test Accuracy: {accuracy:.3f}")

# 5. Bästa modell
best_model_name = max(results.keys(), key=lambda k: results[k]['test_accuracy'])
best_model = results[best_model_name]['model']

print(f"\\n🏆 Bästa modell: {best_model_name}")
print(f"Test Accuracy: {results[best_model_name]['test_accuracy']:.3f}")

# Feature importance (för tree-baserade modeller)
if hasattr(best_model, 'feature_importances_'):
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': best_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=feature_importance.head(10), x='importance', y='feature')
    plt.title('Top 10 Feature Importance')
    plt.tight_layout()
    plt.show()
'''
        
        return {
            'success': True,
            'code': ml_code,
            'language': 'python',
            'description': 'Komplett ML pipeline med modellval och evaluation',
            'next_steps': [
                'Anpassa för ditt specifika dataset',
                'Ersätt \'target_column\' med din target variabel',
                'Installera: pip install scikit-learn pandas numpy matplotlib seaborn',
                'Experimentera med olika hyperparametrar'
            ]
        }
    
    async def _general_data_help(self, request: str) -> Dict[str, Any]:
        """Allmän data science hjälp"""
        return {
            'success': True,
            'message': 'Data Science hjälp tillgänglig!',
            'capabilities': [
                '📊 Exploratory Data Analysis (EDA)',
                '🤖 Machine Learning pipelines',
                '📈 Data visualization och reporting',
                '🔧 Feature engineering och selection',
                '📋 Statistical analysis och hypothesis testing',
                '🎯 Model evaluation och hyperparameter tuning'
            ],
            'tools': self.ml_frameworks,
            'suggestion': 'Specificera vad du vill göra med datan för detaljerad hjälp!'
        }

class DesignAgent(BaseAgent):
    """Grafisk Designer Agent"""
    
    def __init__(self):
        super().__init__("UI/UX Designer", "Grafisk design och användarupplevelse")
        self.design_tools = ['figma', 'photoshop', 'illustrator', 'css', 'html']
    
    def get_keywords(self) -> List[str]:
        return [
            'design', 'ui', 'ux', 'grafik', 'layout', 'färg', 'typografi',
            'logo', 'ikon', 'wireframe', 'mockup', 'prototyp', 'css',
            'responsiv', 'användarvänlig', 'tillgänglighet', 'branding'
        ] + self.design_tools
    
    async def process_request(self, request: str, context: Dict = None) -> Dict[str, Any]:
        """Process design-relaterade förfrågningar"""
        
        request_lower = request.lower()
        
        if any(word in request_lower for word in ['css', 'style', 'styling']):
            return await self._generate_css(request)
        elif any(word in request_lower for word in ['färgschema', 'color', 'palette']):
            return await self._color_scheme(request)
        elif any(word in request_lower for word in ['layout', 'wireframe', 'struktur']):
            return await self._layout_design(request)
        else:
            return await self._general_design_help(request)
    
    async def _generate_css(self, request: str) -> Dict[str, Any]:
        """Generera modern CSS"""
        
        css_code = '''
/* Modern CSS Framework - JARVIS Design System */

:root {
  /* Färgpaletten */
  --primary: #3b82f6;
  --primary-dark: #1e40af;
  --secondary: #f59e0b;
  --accent: #10b981;
  --danger: #ef4444;
  --warning: #f59e0b;
  --success: #10b981;
  
  /* Grå-skala */
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-300: #d1d5db;
  --gray-400: #9ca3af;
  --gray-500: #6b7280;
  --gray-600: #4b5563;
  --gray-700: #374151;
  --gray-800: #1f2937;
  --gray-900: #111827;
  
  /* Typography */
  --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  
  /* Spacing */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-12: 3rem;
  
  /* Border radius */
  --radius-sm: 0.25rem;
  --radius: 0.5rem;
  --radius-lg: 1rem;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
}

/* Reset och grundläggande styling */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: var(--font-primary);
  line-height: 1.6;
  color: var(--gray-800);
  background-color: var(--gray-50);
}

/* Modern knapp-component */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-3) var(--space-6);
  border: none;
  border-radius: var(--radius);
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: var(--shadow-sm);
}

.btn-primary {
  background-color: var(--primary);
  color: white;
}

.btn-primary:hover {
  background-color: var(--primary-dark);
  transform: translateY(-1px);
  box-shadow: var(--shadow);
}

/* Modern kort-component */
.card {
  background: white;
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  box-shadow: var(--shadow);
  border: 1px solid var(--gray-200);
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

/* Flexbox utilities */
.flex {
  display: flex;
}

.flex-col {
  flex-direction: column;
}

.items-center {
  align-items: center;
}

.justify-center {
  justify-content: center;
}

.justify-between {
  justify-content: space-between;
}

/* Grid system */
.grid {
  display: grid;
  gap: var(--space-4);
}

.grid-2 {
  grid-template-columns: repeat(2, 1fr);
}

.grid-3 {
  grid-template-columns: repeat(3, 1fr);
}

.grid-4 {
  grid-template-columns: repeat(4, 1fr);
}

/* Responsivt */
@media (max-width: 768px) {
  .grid-2,
  .grid-3,
  .grid-4 {
    grid-template-columns: 1fr;
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  :root {
    --gray-50: #111827;
    --gray-100: #1f2937;
    --gray-800: #f9fafb;
    --gray-900: #ffffff;
  }
  
  body {
    background-color: var(--gray-100);
    color: var(--gray-800);
  }
}
'''
        
        return {
            'success': True,
            'code': css_code,
            'language': 'css',
            'description': 'Modern CSS framework med design system',
            'features': [
                'CSS Custom Properties för teming',
                'Modern komponenter (knappar, kort)',
                'Flexbox och Grid utilities',
                'Responsiv design',
                'Dark mode support',
                'Accessibility-fokuserat'
            ]
        }
    
    async def _general_design_help(self, request: str) -> Dict[str, Any]:
        """Allmän design hjälp"""
        return {
            'success': True,
            'message': 'Design hjälp tillgänglig!',
            'capabilities': [
                '🎨 Modern CSS och styling',
                '📱 Responsiv design',
                '🌈 Färgscheman och paletter',
                '📐 Layout och composition',
                '🔤 Typografi och readability',
                '♿ Accessibility och inclusivity'
            ],
            'suggestion': 'Specificera vad du vill designa för detaljerad hjälp!'
        }

class ContentCreatorAgent(BaseAgent):
    """Content Creator Agent"""
    
    def __init__(self):
        super().__init__("Content Creator", "Innehållsskapande och copywriting")
        self.content_types = ['blog', 'social media', 'marketing', 'technical writing']
    
    def get_keywords(self) -> List[str]:
        return [
            'content', 'innehåll', 'text', 'artikel', 'blog', 'copy',
            'marknadsföring', 'social media', 'skriv', 'redigera',
            'seo', 'headline', 'rubrik', 'storytelling', 'brand'
        ] + self.content_types
    
    async def process_request(self, request: str, context: Dict = None) -> Dict[str, Any]:
        """Process content creation förfrågningar"""
        
        request_lower = request.lower()
        
        if any(word in request_lower for word in ['blog', 'artikel', 'post']):
            return await self._create_blog_content(request)
        elif any(word in request_lower for word in ['social media', 'instagram', 'twitter']):
            return await self._social_media_content(request)
        elif any(word in request_lower for word in ['marknadsföring', 'marketing', 'copy']):
            return await self._marketing_copy(request)
        else:
            return await self._general_content_help(request)
    
    async def _create_blog_content(self, request: str) -> Dict[str, Any]:
        """Skapa blog innehåll"""
        
        # Template för blog post
        blog_template = '''
# [Engaging Headline: Sätt Din Hook Här]

## Introduktion
- Fånga läsarens uppmärksamhet med en stark öppning
- Presentera problemet eller möjligheten
- Ge en förhandsvisning av vad läsaren kommer att lära sig

## Huvudinnehåll

### Sektion 1: [Huvudpunkt 1]
- Förklara konceptet tydligt
- Använd exempel och analogier
- Inkludera actionable insights

### Sektion 2: [Huvudpunkt 2]
- Bygg på föregående sektion
- Ge praktiska tips och strategier
- Använd bullet points för läsbarhet

### Sektion 3: [Huvudpunkt 3]
- Fördjupa dig i ämnet
- Dela personliga erfarenheter eller case studies
- Inkludera data och statistik när relevant

## Praktiska Tips
1. **Tip 1:** Konkret råd som läsaren kan implementera direkt
2. **Tip 2:** Steg-för-steg process eller checklista
3. **Tip 3:** Vanliga misstag att undvika

## Slutsats
- Sammanfatta de viktigaste takeaways
- Uppmuntra till handling (call-to-action)
- Avsluta med en reflektion eller fråga för engagement

---

**SEO Optimering:**
- Primärt keyword: [ditt huvudkeyword]
- Sekundära keywords: [relaterade termer]
- Meta description: [120-155 tecken som sammanfattar artikeln]
- Alt-text för bilder: [beskrivande text med keywords]

**Content Marketing Strategi:**
- Social media teasers
- Email newsletter utdrag
- Återanvändning för andra format (video, podcast, infographic)
'''
        
        return {
            'success': True,
            'template': blog_template,
            'type': 'blog_post',
            'description': 'Komplett blog post template med SEO fokus',
            'tips': [
                'Använd storytelling för att engagera läsare',
                'Inkludera visuella element (bilder, grafer)',
                'Optimera för mobile-friendly läsning',
                'Lägg till internal och external links',
                'Använd engaging headlines och subheadings'
            ]
        }
    
    async def _general_content_help(self, request: str) -> Dict[str, Any]:
        """Allmän content creation hjälp"""
        return {
            'success': True,
            'message': 'Content Creation hjälp tillgänglig!',
            'capabilities': [
                '📝 Blog posts och artiklar',
                '📱 Social media content',
                '📈 Marketing copy och sales pages',
                '📧 Email marketing campaigns',
                '🎯 SEO-optimerat innehåll',
                '📚 Technical writing och dokumentation'
            ],
            'content_types': self.content_types,
            'suggestion': 'Specificera vilken typ av innehåll du vill skapa!'
        }

class AgentRouter:
    """Router som väljer rätt agent för varje förfrågan"""
    
    def __init__(self):
        self.agents = {
            'coder': CoderAgent(),
            'system_analyst': SystemAnalystAgent(),
            'data_scientist': DataScientistAgent(),
            'designer': DesignAgent(),
            'content_creator': ContentCreatorAgent(),
            'university_tutor': UniversityTutorAgent(),
            'study_coach': StudyCoachAgent(),
        }
        
        # Försök ladda ImageAgent (kräver google-cloud-aiplatform)
        try:
            from .image_agent import ImageAgent
            self.agents['image_generator'] = ImageAgent()
            print(f"✅ AgentRouter initialiserad med {len(self.agents)} specialiserade agents (inkl. Image AI)")
        except ImportError:
            print(f"✅ AgentRouter initialiserad med {len(self.agents)} specialiserade agents (Image AI ej tillgänglig)")
            print("💡 Installera google-cloud-aiplatform för AI-bildgenerering")
    
    async def route_request(self, request: str, context: Dict = None) -> Dict[str, Any]:
        """Route förfrågan till bästa agent"""
        
        # Beräkna confidence scores för alla agents
        scores = {}
        for name, agent in self.agents.items():
            scores[name] = agent.can_handle(request)
        
        # Välj agent med högst score
        best_agent_name = max(scores, key=scores.get)
        best_score = scores[best_agent_name]
        
        print(f"🤖 Agent routing - Bästa match: {best_agent_name} (confidence: {best_score:.2f})")
        
        if best_score > 0.1:  # Lägre threshold för mer flexibel routing
            agent = self.agents[best_agent_name]
            result = await agent.process_request(request, context)
            result['agent_used'] = best_agent_name
            result['confidence'] = best_score
            result['agent_name'] = agent.name
            return result
        else:
            return {
                'success': False,
                'message': 'Ingen specialiserad agent hittades för denna förfrågan',
                'available_agents': {
                    name: agent.name for name, agent in self.agents.items()
                },
                'scores': scores,
                'suggestion': 'Prova att specificera mer eller använd "agents list" för att se tillgängliga specialister'
            }
    
    def get_all_capabilities(self) -> Dict[str, Any]:
        """Returnera alla agents och deras kapaciteter"""
        return {
            name: agent.get_capabilities() 
            for name, agent in self.agents.items()
        }
    
    def list_agents(self) -> str:
        """Returnera formaterad lista över alla agents"""
        agent_list = "🤖 **JARVIS Specialiserade Agents:**\n\n"
        
        for name, agent in self.agents.items():
            agent_list += f"**{agent.name}** (`{name}`)\n"
            agent_list += f"• Specialitet: {agent.speciality}\n"
            keywords = agent.get_keywords()[:5]  # Visa bara första 5 keywords
            agent_list += f"• Keywords: {', '.join(keywords)}{'...' if len(agent.get_keywords()) > 5 else ''}\n\n"
        
        agent_list += "💡 Använd: 'agent <typ> <förfrågan>' för att direkt kontakta en specialist\n"
        agent_list += "📖 Exempel: 'agent coder skapa en REST API' eller 'agent designer modern CSS'"
        
        return agent_list
    
    async def direct_agent_request(self, agent_type: str, request: str, context: Dict = None) -> Dict[str, Any]:
        """Direktkontakt med specifik agent"""
        
        if agent_type in self.agents:
            agent = self.agents[agent_type]
            print(f"🎯 Direktkontakt med {agent.name}")
            
            result = await agent.process_request(request, context)
            result['agent_used'] = agent_type
            result['agent_name'] = agent.name
            result['direct_request'] = True
            return result
        else:
            return {
                'success': False,
                'error': f'Agent "{agent_type}" finns inte',
                'available_agents': list(self.agents.keys())
            }

# Export main classes
__all__ = [
    'AgentRouter', 'SecurityManager', 
    'CoderAgent', 'SystemAnalystAgent', 'DataScientistAgent', 
    'DesignAgent', 'ContentCreatorAgent', 'UniversityTutorAgent', 'StudyCoachAgent'
]