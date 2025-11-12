from .interpreter import NaturalLanguageInterpreter as NLI
from typing import Dict, Optional, Any, List, Tuple
from dotenv import load_dotenv

load_dotenv()


def sql_from_LLM(nl: str, schema: str = "", api_key: Optional[str] = None) -> str:
    interpreter = NLI(api_key=api_key)

    if schema == "":
        return "you need to set a database schema"

    interpreter.set_database_schema(schema)

    result = interpreter.interpret_with_validation(nl)

    if result["success"]:
        return result["sql_query"]
    else:
        raise Exception(result["error"])


def interpretation_from_LLM(
    query_result: List[Tuple[Any, ...]],
    columns: List[str],
    original_query: str,
    api_key: Optional[str] = None,
    schema: str = "",
):
    interpreter = NLI(api_key=api_key)

    if schema == "":
        return "you need to set a database schema"

    interpreter.set_database_schema(schema)

    result = interpreter.interpret_query_result_as_text(
        query_result, columns, original_query
    )

    if result["success"]:
        return result["interpretation"]
    else:
        raise Exception(result["error"])
