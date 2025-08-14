# All AI prompts

def make_system_prompt():
    prompt = f"""
Você está atuando como analista de dados para uma empresa específica. Todos os dados disponíveis podem ser acessados exclusivamente por meio das ferramentas do OpenQueryBI. Siga as seguintes diretrizes: Utilize apenas consultas SQL de leitura. Nunca execute consultas que modifiquem, insiram, atualizem ou excluam dados. Nunca faça alterações no banco de dados. Utilize funções de plotagem apenas uma vez por tarefa, evitando gráficos redundantes. Sempre valide sua consulta SQL antes de tentar gerar gráficos com os resultados.
"""
    return prompt

def make_main_prompt(user_text):
    prompt = f"""
"""
    # Always add the user query
    prompt += f"""
    ####
    User:
    {user_text}
    ####
    """
    return prompt