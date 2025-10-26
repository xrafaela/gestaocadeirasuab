#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Integração com Moodle UAB
Responsável por todas as interações com o portal Moodle
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class MoodleUAB:
    """
    Classe principal para integração com Moodle UAB
    """

    def __init__(self, username: str = None, password: str = None):
        self.base_url = "https://moodle.uab.pt"
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
        )
        self.is_logged_in = False
        self.token = None
        self.userid = None
        self.courses = []
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data", "moodle")
        os.makedirs(self.data_dir, exist_ok=True)

    def login(self, username: str = None, password: str = None) -> bool:
        """
        Realiza login automático no Moodle UAB

        Returns:
            bool: True se login bem-sucedido, False caso contrário
        """
        if username:
            self.username = username
        if password:
            self.password = password

        if not self.username or not self.password:
            print("❌ Credenciais não fornecidas")
            return False

        try:
            # Passo 1: Obter página de login
            login_url = f"{self.base_url}/login/index.php"
            response = self.session.get(login_url)

            if response.status_code != 200:
                print(f"❌ Erro ao acessar página de login: {response.status_code}")
                return False

            # Passo 2: Extrair logintoken
            soup = BeautifulSoup(response.text, "html.parser")
            logintoken_input = soup.find("input", {"name": "logintoken"})

            if not logintoken_input:
                print("❌ Token de login não encontrado")
                return False

            logintoken = logintoken_input.get("value")

            # Passo 3: Enviar credenciais
            login_data = {
                "username": self.username,
                "password": self.password,
                "logintoken": logintoken,
                "rememberusername": "1",
            }

            response = self.session.post(
                login_url, data=login_data, allow_redirects=True
            )

            # Verificar se login foi bem-sucedido
            if "sesskey" in response.text or "logout.php" in response.text:
                self.is_logged_in = True
                print("✅ Login realizado com sucesso!")

                # Extrair sesskey e userid
                self._extract_session_info(response.text)

                # Salvar sessão
                self._save_session()

                return True
            else:
                print("❌ Falha no login - Credenciais inválidas")
                return False

        except Exception as e:
            print(f"❌ Erro durante login: {e}")
            return False

    def _extract_session_info(self, html: str):
        """Extrai informações da sessão (sesskey, userid, token)"""
        try:
            # Extrair sesskey
            match = re.search(r'"sesskey":"([^"]+)"', html)
            if match:
                self.token = match.group(1)

            # Extrair userid
            match = re.search(r'"userid":(\d+)', html)
            if match:
                self.userid = int(match.group(1))

        except Exception as e:
            print(f"⚠️ Erro ao extrair informações da sessão: {e}")

    def _save_session(self):
        """Salva a sessão atual em arquivo"""
        try:
            session_file = os.path.join(self.data_dir, "session.json")
            session_data = {
                "cookies": self.session.cookies.get_dict(),
                "token": self.token,
                "userid": self.userid,
                "timestamp": datetime.now().isoformat(),
            }

            with open(session_file, "w") as f:
                json.dump(session_data, f, indent=2)

        except Exception as e:
            print(f"⚠️ Erro ao salvar sessão: {e}")

    def _load_session(self) -> bool:
        """Carrega sessão salva anteriormente"""
        try:
            session_file = os.path.join(self.data_dir, "session.json")

            if not os.path.exists(session_file):
                return False

            with open(session_file, "r") as f:
                session_data = json.load(f)

            # Verificar se sessão não expirou (24 horas)
            timestamp = datetime.fromisoformat(session_data["timestamp"])
            if datetime.now() - timestamp > timedelta(hours=24):
                return False

            # Restaurar sessão
            for name, value in session_data["cookies"].items():
                self.session.cookies.set(name, value)

            self.token = session_data.get("token")
            self.userid = session_data.get("userid")
            self.is_logged_in = True

            return True

        except Exception as e:
            print(f"⚠️ Erro ao carregar sessão: {e}")
            return False

    def get_enrolled_courses(self) -> List[Dict]:
        """
        Busca todas as disciplinas matriculadas

        Returns:
            List[Dict]: Lista de disciplinas com informações
        """
        if not self.is_logged_in:
            print("❌ Usuário não está logado")
            return []

        try:
            # Acessar página principal do usuário
            dashboard_url = f"{self.base_url}/my/"
            response = self.session.get(dashboard_url)

            if response.status_code != 200:
                return []

            soup = BeautifulSoup(response.text, "html.parser")
            courses = []

            # Buscar cursos na página
            course_elements = soup.find_all("div", class_="card-deck")

            for element in course_elements:
                course_links = element.find_all("a", href=True)

                for link in course_links:
                    href = link.get("href")

                    if "/course/view.php?id=" in href:
                        course_id = re.search(r"id=(\d+)", href)

                        if course_id:
                            course_name = link.get_text(strip=True)

                            if course_name:
                                courses.append(
                                    {
                                        "id": int(course_id.group(1)),
                                        "name": course_name,
                                        "url": href
                                        if href.startswith("http")
                                        else self.base_url + href,
                                    }
                                )

            self.courses = courses

            # Salvar cursos
            self._save_courses(courses)

            print(f"✅ Encontradas {len(courses)} disciplinas")
            return courses

        except Exception as e:
            print(f"❌ Erro ao buscar disciplinas: {e}")
            return []

    def get_course_assignments(self, course_id: int) -> List[Dict]:
        """
        Busca tarefas e prazos de uma disciplina

        Args:
            course_id: ID da disciplina

        Returns:
            List[Dict]: Lista de tarefas com prazos
        """
        if not self.is_logged_in:
            return []

        try:
            course_url = f"{self.base_url}/course/view.php?id={course_id}"
            response = self.session.get(course_url)

            if response.status_code != 200:
                return []

            soup = BeautifulSoup(response.text, "html.parser")
            assignments = []

            # Buscar atividades do tipo "assign"
            activities = soup.find_all("li", class_="activity")

            for activity in activities:
                if "assign" in activity.get("class", []):
                    name_elem = activity.find("span", class_="instancename")

                    if name_elem:
                        name = name_elem.get_text(strip=True)
                        link = activity.find("a", href=True)

                        # Buscar prazo
                        deadline = self._extract_deadline(activity)

                        assignments.append(
                            {
                                "name": name,
                                "url": link["href"] if link else "",
                                "deadline": deadline,
                                "course_id": course_id,
                            }
                        )

            return assignments

        except Exception as e:
            print(f"❌ Erro ao buscar tarefas: {e}")
            return []

    def _extract_deadline(self, element) -> Optional[str]:
        """Extrai prazo de entrega de um elemento"""
        try:
            # Buscar texto de prazo
            text = element.get_text()

            # Padrões de data em português
            patterns = [
                r"(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})",
                r"(\d{1,2})/(\d{1,2})/(\d{4})",
                r"(\d{4})-(\d{2})-(\d{2})",
            ]

            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    return match.group(0)

            return None

        except:
            return None

    def get_course_materials(self, course_id: int) -> List[Dict]:
        """
        Busca materiais disponíveis em uma disciplina

        Args:
            course_id: ID da disciplina

        Returns:
            List[Dict]: Lista de materiais (PDFs, vídeos, etc)
        """
        if not self.is_logged_in:
            return []

        try:
            course_url = f"{self.base_url}/course/view.php?id={course_id}"
            response = self.session.get(course_url)

            if response.status_code != 200:
                return []

            soup = BeautifulSoup(response.text, "html.parser")
            materials = []

            # Buscar recursos
            resources = soup.find_all("li", class_="activity")

            for resource in resources:
                # PDF
                if "resource" in resource.get("class", []):
                    name_elem = resource.find("span", class_="instancename")
                    link = resource.find("a", href=True)

                    if name_elem and link:
                        materials.append(
                            {
                                "name": name_elem.get_text(strip=True),
                                "url": link["href"],
                                "type": "pdf"
                                if ".pdf" in link["href"].lower()
                                else "document",
                                "course_id": course_id,
                            }
                        )

                # URL/Link
                elif "url" in resource.get("class", []):
                    name_elem = resource.find("span", class_="instancename")
                    link = resource.find("a", href=True)

                    if name_elem and link:
                        materials.append(
                            {
                                "name": name_elem.get_text(strip=True),
                                "url": link["href"],
                                "type": "url",
                                "course_id": course_id,
                            }
                        )

            return materials

        except Exception as e:
            print(f"❌ Erro ao buscar materiais: {e}")
            return []

    def download_material(self, url: str, filename: str) -> bool:
        """
        Baixa um material do Moodle

        Args:
            url: URL do material
            filename: Nome do arquivo para salvar

        Returns:
            bool: True se download bem-sucedido
        """
        try:
            response = self.session.get(url, stream=True)

            if response.status_code != 200:
                return False

            filepath = os.path.join(self.data_dir, "materials", filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"✅ Material baixado: {filename}")
            return True

        except Exception as e:
            print(f"❌ Erro ao baixar material: {e}")
            return False

    def get_forum_posts(self, course_id: int) -> List[Dict]:
        """
        Busca posts de fóruns de uma disciplina

        Args:
            course_id: ID da disciplina

        Returns:
            List[Dict]: Lista de posts de fóruns
        """
        if not self.is_logged_in:
            return []

        try:
            course_url = f"{self.base_url}/course/view.php?id={course_id}"
            response = self.session.get(course_url)

            soup = BeautifulSoup(response.text, "html.parser")
            forums = []

            # Buscar fóruns
            forum_activities = soup.find_all("li", class_="activity")

            for activity in forum_activities:
                if "forum" in activity.get("class", []):
                    link = activity.find("a", href=True)

                    if link:
                        forum_id = re.search(r"id=(\d+)", link["href"])

                        if forum_id:
                            forum_posts = self._get_forum_discussions(forum_id.group(1))
                            forums.extend(forum_posts)

            return forums

        except Exception as e:
            print(f"❌ Erro ao buscar posts de fóruns: {e}")
            return []

    def _get_forum_discussions(self, forum_id: str) -> List[Dict]:
        """Busca discussões de um fórum específico"""
        try:
            forum_url = f"{self.base_url}/mod/forum/view.php?id={forum_id}"
            response = self.session.get(forum_url)

            soup = BeautifulSoup(response.text, "html.parser")
            discussions = []

            # Buscar discussões
            discussion_elements = soup.find_all("tr", class_="discussion")

            for discussion in discussion_elements:
                topic = discussion.find("a", class_="discussionname")
                author = discussion.find("a", href=re.compile(r"/user/view.php"))

                if topic:
                    discussions.append(
                        {
                            "title": topic.get_text(strip=True),
                            "url": topic["href"] if "href" in topic.attrs else "",
                            "author": author.get_text(strip=True)
                            if author
                            else "Desconhecido",
                            "forum_id": forum_id,
                        }
                    )

            return discussions

        except:
            return []

    def get_grades(self, course_id: int) -> Dict:
        """
        Busca notas de uma disciplina

        Args:
            course_id: ID da disciplina

        Returns:
            Dict: Informações de notas
        """
        if not self.is_logged_in:
            return {}

        try:
            grades_url = f"{self.base_url}/grade/report/user/index.php?id={course_id}"
            response = self.session.get(grades_url)

            if response.status_code != 200:
                return {}

            soup = BeautifulSoup(response.text, "html.parser")
            grades = {}

            # Buscar tabela de notas
            grade_table = soup.find("table", class_="generaltable")

            if grade_table:
                rows = grade_table.find_all("tr")

                for row in rows:
                    cells = row.find_all("td")

                    if len(cells) >= 2:
                        item_name = cells[0].get_text(strip=True)
                        grade_value = cells[1].get_text(strip=True)

                        grades[item_name] = grade_value

            return grades

        except Exception as e:
            print(f"❌ Erro ao buscar notas: {e}")
            return {}

    def sync_calendar(self) -> List[Dict]:
        """
        Sincroniza eventos do calendário do Moodle

        Returns:
            List[Dict]: Lista de eventos do calendário
        """
        if not self.is_logged_in:
            return []

        try:
            calendar_url = f"{self.base_url}/calendar/view.php?view=month"
            response = self.session.get(calendar_url)

            soup = BeautifulSoup(response.text, "html.parser")
            events = []

            # Buscar eventos
            event_elements = soup.find_all("div", class_="event")

            for event in event_elements:
                title = event.find("a")
                date_elem = event.find("div", class_="date")

                if title:
                    events.append(
                        {
                            "title": title.get_text(strip=True),
                            "url": title["href"] if "href" in title.attrs else "",
                            "date": date_elem.get_text(strip=True) if date_elem else "",
                        }
                    )

            # Salvar eventos
            self._save_calendar_events(events)

            return events

        except Exception as e:
            print(f"❌ Erro ao sincronizar calendário: {e}")
            return []

    def check_notifications(self) -> List[Dict]:
        """
        Verifica notificações em tempo real

        Returns:
            List[Dict]: Lista de notificações não lidas
        """
        if not self.is_logged_in:
            return []

        try:
            # API de notificações do Moodle
            notifications_url = (
                f"{self.base_url}/message/output/popup/notifications.php"
            )
            response = self.session.get(notifications_url)

            if response.status_code == 200:
                # Tentar parsear como JSON
                try:
                    data = response.json()
                    return data.get("notifications", [])
                except:
                    pass

            return []

        except Exception as e:
            print(f"❌ Erro ao verificar notificações: {e}")
            return []

    def auto_download_new_materials(self) -> List[str]:
        """
        Baixa automaticamente materiais novos de todas as disciplinas

        Returns:
            List[str]: Lista de materiais baixados
        """
        downloaded = []

        for course in self.courses:
            materials = self.get_course_materials(course["id"])

            for material in materials:
                if material["type"] == "pdf":
                    filename = f"{course['id']}_{material['name']}.pdf"

                    # Verificar se já foi baixado
                    if not self._material_exists(filename):
                        if self.download_material(material["url"], filename):
                            downloaded.append(filename)

        return downloaded

    def _material_exists(self, filename: str) -> bool:
        """Verifica se material já foi baixado"""
        filepath = os.path.join(self.data_dir, "materials", filename)
        return os.path.exists(filepath)

    def _save_courses(self, courses: List[Dict]):
        """Salva lista de cursos em arquivo"""
        try:
            courses_file = os.path.join(self.data_dir, "courses.json")

            with open(courses_file, "w", encoding="utf-8") as f:
                json.dump(courses, f, indent=2, ensure_ascii=False)

        except Exception as e:
            print(f"⚠️ Erro ao salvar cursos: {e}")

    def _save_calendar_events(self, events: List[Dict]):
        """Salva eventos do calendário"""
        try:
            events_file = os.path.join(self.data_dir, "calendar_events.json")

            with open(events_file, "w", encoding="utf-8") as f:
                json.dump(events, f, indent=2, ensure_ascii=False)

        except Exception as e:
            print(f"⚠️ Erro ao salvar eventos: {e}")

    def get_sync_status(self) -> Dict:
        """
        Retorna status da sincronização

        Returns:
            Dict: Status atual da sincronização
        """
        return {
            "logged_in": self.is_logged_in,
            "courses_count": len(self.courses),
            "last_sync": self._get_last_sync_time(),
            "materials_downloaded": self._count_downloaded_materials(),
        }

    def _get_last_sync_time(self) -> Optional[str]:
        """Retorna timestamp da última sincronização"""
        try:
            session_file = os.path.join(self.data_dir, "session.json")

            if os.path.exists(session_file):
                with open(session_file, "r") as f:
                    data = json.load(f)
                    return data.get("timestamp")

            return None

        except:
            return None

    def _count_downloaded_materials(self) -> int:
        """Conta materiais baixados"""
        try:
            materials_dir = os.path.join(self.data_dir, "materials")

            if os.path.exists(materials_dir):
                return len(
                    [
                        f
                        for f in os.listdir(materials_dir)
                        if os.path.isfile(os.path.join(materials_dir, f))
                    ]
                )

            return 0

        except:
            return 0


# Funções auxiliares para facilitar o uso


def create_moodle_client(username: str = None, password: str = None) -> MoodleUAB:
    """
    Cria e retorna uma instância do cliente Moodle

    Args:
        username: Nome de usuário (opcional)
        password: Senha (opcional)

    Returns:
        MoodleUAB: Instância do cliente
    """
    return MoodleUAB(username, password)


def quick_sync(username: str, password: str) -> Dict:
    """
    Realiza sincronização rápida de todos os dados do Moodle

    Args:
        username: Nome de usuário
        password: Senha

    Returns:
        Dict: Resumo da sincronização
    """
    client = MoodleUAB(username, password)

    results = {
        "success": False,
        "courses": [],
        "assignments": [],
        "materials": [],
        "calendar": [],
        "notifications": [],
    }

    # Login
    if not client.login():
        return results

    # Buscar disciplinas
    results["courses"] = client.get_enrolled_courses()

    # Buscar tarefas de cada disciplina
    for course in results["courses"]:
        assignments = client.get_course_assignments(course["id"])
        results["assignments"].extend(assignments)

    # Sincronizar calendário
    results["calendar"] = client.sync_calendar()

    # Verificar notificações
    results["notifications"] = client.check_notifications()

    # Baixar materiais novos
    results["materials"] = client.auto_download_new_materials()

    results["success"] = True

    return results


if __name__ == "__main__":
    # Teste básico
    print("🔧 Módulo de Integração Moodle UAB")
    print("=" * 50)

    # Carregar credenciais do ambiente (se disponível)
    username = os.getenv("MOODLE_USERNAME")
    password = os.getenv("MOODLE_PASSWORD")

    if username and password:
        print(f"Testando login para: {username}")
        client = MoodleUAB(username, password)

        if client.login():
            print("\n📚 Buscando disciplinas...")
            courses = client.get_enrolled_courses()

            for course in courses:
                print(f"  - {course['name']}")
        else:
            print("Falha no teste de login")
    else:
        print("⚠️ Credenciais não configuradas")
        print("💡 Configure: export MOODLE_USERNAME='seu_usuario'")
        print("💡 Configure: export MOODLE_PASSWORD='sua_senha'")
