"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
from pathlib import Path
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header
from pydantic import BaseModel

load_dotenv()

class PromptInfo(BaseModel):
    description: str
    system_prompt: str
    user_prompt: str
    version: str
    created_at: str
    tags: list[str]

def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    prompt = ChatPromptTemplate(
        [
            ("system", prompt_data["system_prompt"]),
            ("user", prompt_data["user_prompt"]),
        ]
    )

    # print(prompt_data)
    # return
    result = hub.push(
        repo_full_name=f"killertiger/{prompt_name}",
        new_repo_description=prompt_data["description"],
        object=prompt,
        # system_prompt=prompt_data["system_prompt"],
        # user_prompt=prompt_data["user_prompt"],
        # version=prompt_data["version"],
        # created_at=prompt_data["created_at"],
        tags=prompt_data["tags"],
        new_repo_is_public=True,
    )
    print(result)


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    if len(prompt_data) != 1:
        return False, ["O arquivo deve conter exatamente um prompt."]

    prompt_data = next(iter(prompt_data.values()))  # Extrai o conteúdo do prompt
    try:
        PromptInfo(**prompt_data)
        return True, []
    except Exception as e:
        return False, [str(e)]
    


def main():
    """Função principal"""
    ...
    files = Path("prompts").glob("*.yml")
    for file in files:
        prompt_dict = load_yaml(file)  # Carrega e valida cada prompt
        is_valid, errors = validate_prompt(prompt_dict)
        if not is_valid:
            print(f"Erro de validação para {file.name}: {errors}")
            return
        prompt_name = next(iter(prompt_dict.keys()))  # Extrai o nome do prompt
        push_prompt_to_langsmith(prompt_name, prompt_dict[prompt_name])  # Push para o Hub
    print("Todos os prompts são válidos. Iniciando push...")

if __name__ == "__main__":
    sys.exit(main())
