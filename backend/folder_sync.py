#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sistema de Sincronização de Pastas de Disciplinas
Monitora pastas específicas para cada disciplina e sincroniza com o sistema
"""

import os
import sqlite3
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import time

class DisciplineFolderHandler(FileSystemEventHandler):
    """Handler para monitorar mudanças nas pastas das disciplinas"""
    
    def __init__(self, disciplina_id, folder_path, db_path):
        self.disciplina_id = disciplina_id
        self.folder_path = folder_path
        self.db_path = db_path
        
    def on_created(self, event):
        if not event.is_directory:
            self._index_file(event.src_path, 'created')
    
    def on_modified(self, event):
        if not event.is_directory:
            self._index_file(event.src_path, 'modified')
    
    def on_deleted(self, event):
        if not event.is_directory:
            self._remove_file(event.src_path)
    
    def _index_file(self, file_path, action):
        """Indexa um arquivo no banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        file_path = Path(file_path)
        relative_path = file_path.relative_to(self.folder_path)
        
        # Calcular hash do arquivo
        file_hash = self._calculate_file_hash(file_path)
        
        cursor.execute("""
            INSERT OR REPLACE INTO arquivos_disciplinas 
            (disciplina_id, nome_arquivo, caminho_completo, caminho_relativo, 
             tamanho, tipo, hash, data_modificacao, data_sincronizacao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            self.disciplina_id,
            file_path.name,
            str(file_path),
            str(relative_path),
            file_path.stat().st_size,
            file_path.suffix,
            file_hash,
            datetime.fromtimestamp(file_path.stat().st_mtime),
            datetime.now()
        ))
        
        conn.commit()
        conn.close()
        
        print(f"📁 {action.capitalize()}: {file_path.name} para {self.disciplina_id}")
    
    def _remove_file(self, file_path):
        """Remove um arquivo do índice"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM arquivos_disciplinas 
            WHERE caminho_completo = ?
        """, (str(file_path),))
        
        conn.commit()
        conn.close()
        
        print(f"🗑️ Removido: {Path(file_path).name}")
    
    def _calculate_file_hash(self, file_path):
        """Calcula o hash SHA256 de um arquivo"""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except:
            return None


class FolderSyncManager:
    """Gerenciador de sincronização de pastas"""
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.observers = {}
        self.init_db()
        self.load_mappings()
        
    def init_db(self):
        """Inicializa as tabelas do banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de mapeamento disciplina -> pasta
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mapeamento_pastas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                disciplina_id TEXT NOT NULL UNIQUE,
                disciplina_nome TEXT NOT NULL,
                caminho_pasta TEXT NOT NULL,
                ativo BOOLEAN DEFAULT 1,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabela de arquivos indexados
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS arquivos_disciplinas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                disciplina_id TEXT NOT NULL,
                nome_arquivo TEXT NOT NULL,
                caminho_completo TEXT NOT NULL UNIQUE,
                caminho_relativo TEXT,
                tamanho INTEGER,
                tipo TEXT,
                hash TEXT,
                data_modificacao TIMESTAMP,
                data_sincronizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (disciplina_id) REFERENCES mapeamento_pastas(disciplina_id)
            )
        """)
        
        # Tabela de logs de sincronização
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs_sincronizacao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                disciplina_id TEXT,
                acao TEXT,
                arquivo TEXT,
                status TEXT,
                mensagem TEXT,
                data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def load_mappings(self):
        """Carrega os mapeamentos do banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        mappings = cursor.execute("""
            SELECT disciplina_id, caminho_pasta 
            FROM mapeamento_pastas 
            WHERE ativo = 1
        """).fetchall()
        
        conn.close()
        
        for disc_id, folder_path in mappings:
            if os.path.exists(folder_path):
                self.start_monitoring(disc_id, folder_path)
    
    def add_mapping(self, disciplina_id, disciplina_nome, folder_path):
        """Adiciona um novo mapeamento disciplina -> pasta"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Verificar se a pasta existe
        if not os.path.exists(folder_path):
            return {"success": False, "error": "Pasta não encontrada"}
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO mapeamento_pastas 
                (disciplina_id, disciplina_nome, caminho_pasta, ativo)
                VALUES (?, ?, ?, 1)
            """, (disciplina_id, disciplina_nome, folder_path))
            
            conn.commit()
            conn.close()
            
            # Iniciar monitoramento
            self.start_monitoring(disciplina_id, folder_path)
            
            # Fazer scan inicial da pasta
            self.scan_folder(disciplina_id, folder_path)
            
            return {"success": True, "message": "Mapeamento adicionado com sucesso"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def remove_mapping(self, disciplina_id):
        """Remove um mapeamento"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE mapeamento_pastas 
            SET ativo = 0 
            WHERE disciplina_id = ?
        """, (disciplina_id,))
        
        # Remove arquivos indexados
        cursor.execute("""
            DELETE FROM arquivos_disciplinas 
            WHERE disciplina_id = ?
        """, (disciplina_id,))
        
        conn.commit()
        conn.close()
        
        # Parar monitoramento
        self.stop_monitoring(disciplina_id)
        
        return {"success": True, "message": "Mapeamento removido"}
    
    def get_mappings(self):
        """Retorna todos os mapeamentos ativos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        mappings = cursor.execute("""
            SELECT m.*, 
                   COUNT(a.id) as total_arquivos,
                   SUM(a.tamanho) as tamanho_total
            FROM mapeamento_pastas m
            LEFT JOIN arquivos_disciplinas a ON m.disciplina_id = a.disciplina_id
            WHERE m.ativo = 1
            GROUP BY m.disciplina_id
            ORDER BY m.disciplina_nome
        """).fetchall()
        
        conn.close()
        
        return [dict(m) for m in mappings]
    
    def get_files(self, disciplina_id):
        """Retorna arquivos de uma disciplina"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        files = cursor.execute("""
            SELECT * FROM arquivos_disciplinas 
            WHERE disciplina_id = ?
            ORDER BY data_modificacao DESC
        """, (disciplina_id,)).fetchall()
        
        conn.close()
        
        return [dict(f) for f in files]
    
    def scan_folder(self, disciplina_id, folder_path):
        """Faz scan completo de uma pasta"""
        folder_path = Path(folder_path)
        
        if not folder_path.exists():
            return {"success": False, "error": "Pasta não encontrada"}
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        files_indexed = 0
        
        # Limpar arquivos antigos
        cursor.execute("""
            DELETE FROM arquivos_disciplinas 
            WHERE disciplina_id = ?
        """, (disciplina_id,))
        
        # Indexar todos os arquivos
        for file_path in folder_path.rglob('*'):
            if file_path.is_file():
                relative_path = file_path.relative_to(folder_path)
                
                # Calcular hash
                sha256_hash = hashlib.sha256()
                try:
                    with open(file_path, "rb") as f:
                        for byte_block in iter(lambda: f.read(4096), b""):
                            sha256_hash.update(byte_block)
                    file_hash = sha256_hash.hexdigest()
                except:
                    file_hash = None
                
                cursor.execute("""
                    INSERT INTO arquivos_disciplinas 
                    (disciplina_id, nome_arquivo, caminho_completo, caminho_relativo, 
                     tamanho, tipo, hash, data_modificacao)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    disciplina_id,
                    file_path.name,
                    str(file_path),
                    str(relative_path),
                    file_path.stat().st_size,
                    file_path.suffix,
                    file_hash,
                    datetime.fromtimestamp(file_path.stat().st_mtime)
                ))
                
                files_indexed += 1
        
        conn.commit()
        conn.close()
        
        return {"success": True, "files_indexed": files_indexed}
    
    def start_monitoring(self, disciplina_id, folder_path):
        """Inicia monitoramento de uma pasta"""
        if disciplina_id in self.observers:
            return  # Já está sendo monitorada
        
        if not os.path.exists(folder_path):
            return
        
        observer = Observer()
        handler = DisciplineFolderHandler(disciplina_id, folder_path, self.db_path)
        observer.schedule(handler, folder_path, recursive=True)
        observer.start()
        
        self.observers[disciplina_id] = observer
        print(f"👁️ Monitorando: {folder_path} para {disciplina_id}")
    
    def stop_monitoring(self, disciplina_id):
        """Para o monitoramento de uma pasta"""
        if disciplina_id in self.observers:
            self.observers[disciplina_id].stop()
            self.observers[disciplina_id].join()
            del self.observers[disciplina_id]
            print(f"🛑 Parado monitoramento para {disciplina_id}")
    
    def stop_all(self):
        """Para todos os monitoramentos"""
        for disciplina_id in list(self.observers.keys()):
            self.stop_monitoring(disciplina_id)
    
    def search_files(self, query, disciplina_id=None):
        """Busca arquivos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        sql = """
            SELECT a.*, m.disciplina_nome 
            FROM arquivos_disciplinas a
            JOIN mapeamento_pastas m ON a.disciplina_id = m.disciplina_id
            WHERE a.nome_arquivo LIKE ?
        """
        params = [f"%{query}%"]
        
        if disciplina_id:
            sql += " AND a.disciplina_id = ?"
            params.append(disciplina_id)
        
        sql += " ORDER BY a.data_modificacao DESC LIMIT 50"
        
        files = cursor.execute(sql, params).fetchall()
        conn.close()
        
        return [dict(f) for f in files]
    
    def get_stats(self):
        """Retorna estatísticas gerais"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Total de disciplinas mapeadas
        stats['total_disciplinas'] = cursor.execute("""
            SELECT COUNT(*) FROM mapeamento_pastas WHERE ativo = 1
        """).fetchone()[0]
        
        # Total de arquivos
        stats['total_arquivos'] = cursor.execute("""
            SELECT COUNT(*) FROM arquivos_disciplinas
        """).fetchone()[0]
        
        # Tamanho total
        tamanho = cursor.execute("""
            SELECT SUM(tamanho) FROM arquivos_disciplinas
        """).fetchone()[0]
        stats['tamanho_total'] = tamanho if tamanho else 0
        
        # Arquivos por tipo
        stats['tipos'] = {}
        tipos = cursor.execute("""
            SELECT tipo, COUNT(*) as count 
            FROM arquivos_disciplinas 
            GROUP BY tipo 
            ORDER BY count DESC
        """).fetchall()
        for tipo, count in tipos:
            stats['tipos'][tipo if tipo else 'sem_extensao'] = count
        
        conn.close()
        
        return stats


# Função auxiliar para formatar tamanho de arquivo
def format_file_size(size_in_bytes):
    """Formata tamanho de arquivo para formato legível"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.1f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.1f} TB"