"""
JARVIS Image & Visual Agent med Google Imagen API
Specialiserad agent för bildgenerering och visuell design
"""

import json
import base64
import asyncio
import aiohttp
import subprocess
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime

class ImageAgent:
    """Image & Visual Agent med Google Imagen API"""
    
    def __init__(self):
        self.name = "Visual Designer"
        self.speciality = "Bildgenerering och visuell design"
        self.project_id = "bjornshomelab"  # Din Google Cloud project
        self.location = "europe-west1"     # Välj region
        self.imagen_models = [
            "imagen-4.0-generate-001",      # Senaste modellen
            "imagen-4.0-fast-generate-001", # Snabb variant
            "imagen-3.0-generate-002"       # Fallback
        ]
    
    def get_keywords(self) -> List[str]:
        return [
            'bild', 'image', 'foto', 'grafik', 'illustration', 'design',
            'generera', 'skapa', 'rita', 'visualisera', 'logo', 'banner',
            'poster', 'thumbnail', 'ikon', 'avatar', 'bakgrund', 'texture',
            'art', 'konstwerk', 'stiliserad', 'realistisk', 'cartoon',
            'upscale', 'förbättra', 'redigera'
        ]
    
    def can_handle(self, request: str) -> float:
        """Returnera confidence score för om denna agent kan hantera förfrågan"""
        keywords = self.get_keywords()
        request_lower = request.lower()
        
        # Count exact matches and partial matches
        exact_matches = sum(1 for keyword in keywords if keyword in request_lower)
        
        # Bonus för visuella termer
        visual_terms = ['bild', 'image', 'grafik', 'design', 'generera', 'skapa']
        visual_matches = sum(2 for term in visual_terms if term in request_lower)
        
        total_score = exact_matches + visual_matches
        confidence = min(total_score / 10, 1.0)  # Normalisera till 0-1
        
        return confidence
    
    async def get_access_token(self) -> str:
        """Hämta Google Cloud access token"""
        try:
            result = subprocess.run(
                ['gcloud', 'auth', 'print-access-token'],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                raise Exception(f"Kunde inte hämta access token: {result.stderr}")
        except Exception as e:
            raise Exception(f"gcloud CLI inte tillgänglig: {e}")
    
    async def generate_image(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generera bild med Google Imagen API"""
        
        try:
            access_token = await self.get_access_token()
        except Exception as e:
            return {
                'success': False,
                'error': f'Kunde inte autentisera: {e}'
            }
        
        # API parametrar
        model = kwargs.get('model', 'imagen-3.0-generate-002')
        sample_count = kwargs.get('sample_count', 1)
        aspect_ratio = kwargs.get('aspect_ratio', '1:1')
        enhance_prompt = kwargs.get('enhance_prompt', True)
        negative_prompt = kwargs.get('negative_prompt', '')
        
        # API endpoint
        url = f"https://{self.location}-aiplatform.googleapis.com/v1/projects/{self.project_id}/locations/{self.location}/publishers/google/models/{model}:predict"
        
        # Request payload
        payload = {
            "instances": [
                {
                    "prompt": prompt
                }
            ],
            "parameters": {
                "sampleCount": sample_count,
                "aspectRatio": aspect_ratio,
                "enhancePrompt": enhance_prompt,
                "safetySetting": "block_medium_and_above",
                "personGeneration": "allow_adult"
            }
        }
        
        if negative_prompt:
            payload["instances"][0]["negativePrompt"] = negative_prompt
        
        # Headers
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        return await self._process_image_response(result, prompt)
                    else:
                        error_text = await response.text()
                        return {
                            'success': False,
                            'error': f'API error {response.status}: {error_text}'
                        }
        except Exception as e:
            return {
                'success': False,
                'error': f'Request error: {str(e)}'
            }
    
    async def _process_image_response(self, response: dict, original_prompt: str) -> Dict[str, Any]:
        """Processa API response och spara bilder"""
        
        if 'predictions' not in response:
            return {
                'success': False,
                'error': 'Inget resultat från API'
            }
        
        predictions = response['predictions']
        generated_images = []
        
        # Skapa output directory
        output_dir = Path("generated_images")
        output_dir.mkdir(exist_ok=True)
        
        for i, prediction in enumerate(predictions):
            if 'bytesBase64Encoded' in prediction:
                # Decode base64 image
                image_data = base64.b64decode(prediction['bytesBase64Encoded'])
                
                # Generate filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"jarvis_image_{timestamp}_{i+1}.png"
                filepath = output_dir / filename
                
                # Save image
                with open(filepath, 'wb') as f:
                    f.write(image_data)
                
                generated_images.append({
                    'filename': filename,
                    'filepath': str(filepath),
                    'mime_type': prediction.get('mimeType', 'image/png'),
                    'enhanced_prompt': prediction.get('prompt', original_prompt)
                })
        
        return {
            'success': True,
            'images_generated': len(generated_images),
            'images': generated_images,
            'original_prompt': original_prompt,
            'output_directory': str(output_dir)
        }
    
    async def upscale_image(self, image_path: str, upscale_factor: str = "x2") -> Dict[str, Any]:
        """Förstora en befintlig bild"""
        
        if not Path(image_path).exists():
            return {
                'success': False,
                'error': f'Bildfil finns inte: {image_path}'
            }
        
        try:
            access_token = await self.get_access_token()
        except Exception as e:
            return {
                'success': False,
                'error': f'Kunde inte autentisera: {e}'
            }
        
        # Läs och base64-encoda bilden
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
            image_b64 = base64.b64encode(image_bytes).decode()
        
        # API endpoint (använd äldre modell för upscaling)
        url = f"https://{self.location}-aiplatform.googleapis.com/v1/projects/{self.project_id}/locations/{self.location}/publishers/google/models/imagegeneration@002:predict"
        
        payload = {
            "instances": [
                {
                    "prompt": "",
                    "image": {
                        "bytesBase64Encoded": image_b64
                    }
                }
            ],
            "parameters": {
                "sampleCount": 1,
                "mode": "upscale",
                "upscaleConfig": {
                    "upscaleFactor": upscale_factor
                }
            }
        }
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        return await self._process_upscale_response(result, image_path, upscale_factor)
                    else:
                        error_text = await response.text()
                        return {
                            'success': False,
                            'error': f'Upscale API error {response.status}: {error_text}'
                        }
        except Exception as e:
            return {
                'success': False,
                'error': f'Upscale request error: {str(e)}'
            }
    
    async def _process_upscale_response(self, response: dict, original_path: str, factor: str) -> Dict[str, Any]:
        """Processa upscale response"""
        
        if 'predictions' not in response or not response['predictions']:
            return {
                'success': False,
                'error': 'Inget upscale resultat från API'
            }
        
        prediction = response['predictions'][0]
        
        if 'bytesBase64Encoded' not in prediction:
            return {
                'success': False,
                'error': 'Ingen upscaled bild i response'
            }
        
        # Decode image
        image_data = base64.b64decode(prediction['bytesBase64Encoded'])
        
        # Generate filename
        original_name = Path(original_path).stem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        upscaled_filename = f"{original_name}_upscaled_{factor}_{timestamp}.png"
        
        output_dir = Path("generated_images")
        output_dir.mkdir(exist_ok=True)
        upscaled_path = output_dir / upscaled_filename
        
        # Save upscaled image
        with open(upscaled_path, 'wb') as f:
            f.write(image_data)
        
        return {
            'success': True,
            'original_image': original_path,
            'upscaled_image': str(upscaled_path),
            'upscale_factor': factor,
            'mime_type': prediction.get('mimeType', 'image/png')
        }
    
    async def process_request(self, request: str, context: Dict = None) -> Dict[str, Any]:
        """Process visuella förfrågningar"""
        
        request_lower = request.lower()
        
        # Image generation
        if any(word in request_lower for word in ['generera', 'skapa', 'rita', 'designa']):
            return await self._handle_generation(request)
        
        # Image upscaling
        elif any(word in request_lower for word in ['upscale', 'förstora', 'förbättra']):
            return await self._handle_upscaling(request)
        
        # General visual help
        else:
            return await self._general_visual_help(request)
    
    async def _handle_generation(self, request: str) -> Dict[str, Any]:
        """Hantera bildgenerering"""
        
        # Extrahera prompt från request (förenklad)
        prompt = request
        
        # Ta bort command words för att få ren prompt
        command_words = ['generera', 'skapa', 'rita', 'designa', 'bild', 'image']
        for word in command_words:
            prompt = prompt.replace(word, '').strip()
        
        if not prompt:
            return {
                'success': False,
                'error': 'Ingen bildprompt angiven',
                'suggestion': 'Exempel: "generera en vacker solnedgång över havet"'
            }
        
        print(f"🎨 Genererar bild med prompt: {prompt}")
        
        result = await self.generate_image(prompt)
        
        if result['success']:
            response = f"🎨 Bildgenerering klar! {result['images_generated']} bild(er) skapade.\n\n"
            
            for i, image in enumerate(result['images'], 1):
                response += f"📁 Bild {i}: {image['filename']}\n"
                if 'enhanced_prompt' in image and image['enhanced_prompt'] != result['original_prompt']:
                    response += f"🔧 Förbättrad prompt: {image['enhanced_prompt']}\n"
            
            response += f"\n📂 Sparade i: {result['output_directory']}"
            
            result['message'] = response
        
        return result
    
    async def _handle_upscaling(self, request: str) -> Dict[str, Any]:
        """Hantera bildförstoring"""
        
        # För demonstration - i verkligheten skulle vi extrahera filsökväg från request
        return {
            'success': True,
            'message': 'Bildförstoring implementeras...',
            'available_factors': ['x2', 'x4'],
            'instruction': 'Specificera bildsökväg och förstorningsfaktor'
        }
    
    async def _general_visual_help(self, request: str) -> Dict[str, Any]:
        """Allmän visuell hjälp"""
        
        return {
            'success': True,
            'message': 'Visual Designer hjälp tillgänglig!',
            'capabilities': [
                '🎨 AI-bildgenerering med Google Imagen',
                '🔍 Bildförstoring och kvalitetsförbättring',
                '🎯 Prompt engineering för optimala resultat',
                '📐 Anpassade aspektförhållanden och stilar',
                '🚫 Säkerhetsfilter och ansvarsfull AI',
                '💾 Automatisk bildsparning och organisation'
            ],
            'image_styles': [
                'Fotografisk realism',
                'Digital konst',
                'Illustration och cartoon',
                'Minimalistisk design',
                'Vintage och retro',
                'Abstrakt konst'
            ],
            'example_prompts': [
                '"en vacker solnedgång över havet, fotografisk stil"',
                '"minimalistisk logo för tech-företag, blå och vit"',
                '"fantasilandskap med berg och drakar, digital art"',
                '"modern kontorsdesign, Skandinavisk stil"'
            ],
            'suggestion': 'Beskriv vilken typ av bild du vill ha så skapar jag den åt dig!'
        }
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Returnera agent's kapaciteter"""
        return {
            'name': self.name,
            'speciality': self.speciality,
            'keywords': self.get_keywords(),
            'sudo_enabled': False,  # ImageAgent behöver inte sudo
            'features': [
                'AI-driven bildgenerering',
                'Text-to-image conversion',
                'Image upscaling och förbättring',
                'Stilanpassning och filter',
                'Logo och grafisk design',
                'Konceptuell visualisering'
            ],
            'supported_formats': ['PNG', 'JPEG', 'WebP'],
            'max_image_size': '2048x2048',
            'api_powered': 'Google Imagen API'
        }

# Test function för ImageAgent
async def test_image_agent():
    """Test ImageAgent funktionalitet"""
    agent = ImageAgent()
    
    print("🎨 Testing Image Agent...")
    
    # Test 1: Capability check
    print(f"Can handle 'skapa en bild': {agent.can_handle('skapa en bild')}")
    print(f"Can handle 'generera logo': {agent.can_handle('generera logo')}")
    print(f"Can handle 'koda python': {agent.can_handle('koda python')}")
    
    # Test 2: General help
    result = await agent.process_request("hjälp med bilder")
    print(f"\nGeneral help: {result.get('success')}")
    if 'capabilities' in result:
        print("Capabilities:", len(result['capabilities']))

if __name__ == "__main__":
    asyncio.run(test_image_agent())
