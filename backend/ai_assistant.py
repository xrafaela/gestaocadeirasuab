import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Optional, Dict, List


class AIAssistant:
    def __init__(self):
        load_dotenv()
        # Tentar OpenRouter primeiro, depois OpenAI
        self.api_key = os.getenv('OPENROUTER_API_KEY') or os.getenv('OPENAI_API_KEY')
        self.client = None
        self.using_openrouter = False

        if self.api_key:
            if os.getenv('OPENROUTER_API_KEY'):
                # Configurar para OpenRouter
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url="https://openrouter.ai/api/v1"
                )
                self.using_openrouter = True
                print("✓ IA configurada com OpenRouter")
            else:
                # Configurar para OpenAI padrão
                self.client = OpenAI(api_key=self.api_key)
                print("✓ IA configurada com OpenAI")
        else:
            print("⚠ Nenhuma chave API encontrada (OPENROUTER_API_KEY ou OPENAI_API_KEY)")

    def is_configured(self) -> bool:
        """Verifica se a IA está configurada"""
        return self.client is not None

    def is_available(self) -> bool:
        """Alias para is_configured - compatibilidade com app.py"""
        return self.is_configured()

    def chat(self, message: str, context: str = "") -> str:
        """Envia uma mensagem para o chat da IA"""
        if not self.client:
            return "Assistente IA não configurado. Configure sua chave API (OPENROUTER_API_KEY ou OPENAI_API_KEY)."

        try:
            # Preparar o prompt com contexto
            system_prompt = """Você é um assistente de estudos especializado em ajudar estudantes universitários.
            Você tem acesso ao calendário de estudos do aluno e pode ajudá-lo a organizar seus estudos."""

            if context:
                system_prompt += f"\n\nContexto atual:\n{context}"

            # Definir modelo baseado na API
            model = "openai/gpt-3.5-turbo" if self.using_openrouter else "gpt-3.5-turbo"

            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=500,
                temperature=0.7
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Erro ao processar mensagem: {str(e)}"

    def generate_study_plan(self, subject: str, deadline: str, current_knowledge: str = "") -> Dict:
        """Gera um plano de estudos personalizado"""
        if not self.client:
            return {"error": "Assistente IA não configurado"}

        try:
            prompt = f"""Crie um plano de estudos detalhado para a disciplina '{subject}' com prazo até {deadline}.

            Nível de conhecimento atual: {current_knowledge if current_knowledge else 'Iniciante'}

            Forneça o plano no formato JSON com a seguinte estrutura:
            {{
                "subject": "nome da disciplina",
                "weeks": [
                    {{
                        "week": 1,
                        "topics": ["tópico 1", "tópico 2"],
                        "hours": 10,
                        "goals": "objetivos da semana"
                    }}
                ],
                "tips": ["dica 1", "dica 2"]
            }}"""

            model = "openai/gpt-3.5-turbo" if self.using_openrouter else "gpt-3.5-turbo"

            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em planejamento de estudos."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )

            import json
            plan = json.loads(response.choices[0].message.content)
            return plan

        except Exception as e:
            return {"error": f"Erro ao gerar plano: {str(e)}"}

    def analyze_progress(self, completed_tasks: List[Dict], pending_tasks: List[Dict]) -> str:
        """Analisa o progresso do aluno e fornece feedback"""
        if not self.client:
            return "Assistente IA não configurado"

        try:
            prompt = f"""Analise o progresso do aluno:

            Tarefas concluídas: {len(completed_tasks)}
            Tarefas pendentes: {len(pending_tasks)}

            Detalhes das tarefas pendentes:
            {[task.get('title', 'Sem título') for task in pending_tasks[:5]]}

            Forneça uma análise construtiva e sugestões de melhoria."""

            model = "openai/gpt-3.5-turbo" if self.using_openrouter else "gpt-3.5-turbo"

            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Você é um mentor educacional que fornece feedback motivador."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Erro ao analisar progresso: {str(e)}"

    def suggest_study_schedule(self, tasks: List[Dict], available_hours: int) -> str:
        """Sugere um cronograma de estudos otimizado"""
        if not self.client:
            return "Assistente IA não configurado"

        try:
            prompt = f"""Com base nas seguintes tarefas e {available_hours} horas disponíveis por semana,
            sugira um cronograma de estudos otimizado:

            Tarefas:
            {[f"{task.get('title', 'Sem título')} - Prazo: {task.get('deadline', 'Sem prazo')}" for task in tasks[:10]]}

            Forneça um cronograma semanal detalhado com distribuição equilibrada das tarefas."""

            model = "openai/gpt-3.5-turbo" if self.using_openrouter else "gpt-3.5-turbo"

            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em gestão de tempo e produtividade."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Erro ao sugerir cronograma: {str(e)}"


# Função auxiliar para criar instância (compatibilidade com app.py)
def create_ai_assistant() -> AIAssistant:
    """Cria e retorna uma instância do assistente de IA"""
    return AIAssistant()