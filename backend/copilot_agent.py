import os
import requests
import json
import time
from typing import Optional, Dict, List
from dotenv import load_dotenv
from pathlib import Path

# Carregar .env do diretório pai (raiz do projeto)
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=str(env_path))

class CopilotAgent:
    """Classe para integrar agentes Copilot Studio"""
    
    def __init__(self, agent_name: str, secret: Optional[str] = None):
        """
        Inicializa o agente Copilot
        
        Args:
            agent_name: Nome do agente (ex: 'AC', 'FBD', 'LC')
            secret: Secret do agente (se None, tenta carregar do .env)
        """
        self.agent_name = agent_name
        self.secret = secret or os.getenv(f'COPILOT_{agent_name}_SECRET_1')
        self.token = None
        self.conversation_id = None
        self.directline_url = "https://directline.botframework.com/v3/directline"
        self.conversation_history = []
        
        if not self.secret:
            print(f"⚠️ Secret não encontrado para agente {agent_name}")
        else:
            print(f"✓ Agente {agent_name} inicializado com secret")
    
    def get_token(self) -> Optional[str]:
        """Gera um token de acesso para o agente"""
        if not self.secret:
            return None
        
        try:
            headers = {
                'Authorization': f'Bearer {self.secret}'
            }
            response = requests.post(
                f'{self.directline_url}/tokens/generate',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('token')
                self.conversation_id = data.get('conversationId')
                print(f"✓ Token gerado para {self.agent_name}")
                return self.token
            else:
                print(f"❌ Erro ao gerar token: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"❌ Erro ao gerar token: {str(e)}")
            return None
    
    def send_message(self, message: str) -> Optional[str]:
        """Envia uma mensagem para o agente e recebe resposta"""
        if not self.token or not self.conversation_id:
            if not self.get_token():
                return "Erro: Não foi possível conectar ao agente"
        
        try:
            # Enviar mensagem
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'type': 'message',
                'from': {'id': 'user'},
                'text': message
            }
            
            response = requests.post(
                f'{self.directline_url}/conversations/{self.conversation_id}/activities',
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code != 200 and response.status_code != 204:
                print(f"❌ Erro ao enviar mensagem: {response.status_code}")
                return None
            
            # Aguardar e receber resposta
            time.sleep(2)
            
            response = requests.get(
                f'{self.directline_url}/conversations/{self.conversation_id}/activities',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                activities = data.get('activities', [])
                
                # Procurar resposta do bot (última mensagem que não é do usuário)
                for activity in reversed(activities):
                    if activity.get('from', {}).get('id') != 'user' and activity.get('text'):
                        bot_response = activity.get('text')
                        # Guardar no histórico
                        self.conversation_history.append({
                            'user': message,
                            'agent': bot_response
                        })
                        return bot_response
            
            return "Agente não respondeu"
        except Exception as e:
            print(f"❌ Erro ao enviar mensagem: {str(e)}")
            return None
    
    def refresh_token(self) -> bool:
        """Atualiza o token de acesso"""
        if not self.token:
            return False
        
        try:
            headers = {
                'Authorization': f'Bearer {self.token}'
            }
            response = requests.post(
                f'{self.directline_url}/tokens/refresh',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('token')
                print(f"✓ Token atualizado para {self.agent_name}")
                return True
            return False
        except Exception as e:
            print(f"❌ Erro ao atualizar token: {str(e)}")
            return False
    
    def get_conversation_history(self) -> List[Dict]:
        """Retorna o histórico de conversas"""
        return self.conversation_history
    
    def clear_conversation(self):
        """Limpa o histórico de conversas e cria nova conversa"""
        self.conversation_history = []
        self.token = None
        self.conversation_id = None
        self.get_token()

