from services.ai_service import get_response

def get_sql_from_ai(prompt:str)->str:
    ans = get_response(prompt, llm_provider='Anthropic')
    return ans

def find_sql_in_text(text:str)->str:
    import re
    # Regular expression to find SQL statements
    sql_pattern = re.compile(
        r"(SELECT\s+.*?;|INSERT\s+INTO\s+.*?;|UPDATE\s+.*?;|DELETE\s+FROM\s+.*?;|CREATE\s+TABLE\s+.*?;|DROP\s+TABLE\s+.*?;|ALTER\s+TABLE\s+.*?;)",
        re.IGNORECASE | re.DOTALL
    )
    
    matches = sql_pattern.findall(text)
    if matches:
        # Return the first matched SQL statement, cleaned up
        return clean_sql(matches[-1])
    else:
        return ""

def clean_sql(sql:str)->str:
    return sql.strip().rstrip(';')