import os
from typing import Dict, Optional, Any, List
from openai import OpenAI


class NaturalLanguageInterpreter:

    def __init__(
        self, api_key: Optional[str] = None, model: str = "gpt-4"
    ):  # mudar o modelo para mini
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API Key not found. Configure OPENAI_API_KEY in .env")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.database_schema = ""

    def set_database_schema(self, schema: str):
        self.database_schema = schema

    def _build_system_prompt(self) -> str:
        return f"""You are an SQL and database expert.
                    Your task is to convert natural language questions into valid SQL queries.

                    **IMPORTANT:**
                    - Generate ONLY SELECT queries (read-only)
                    - Return ONLY the SQL query, without additional explanations
                    - Be precise and efficient

                    **Database Schema:**
                    {self.database_schema if self.database_schema else "Schema not provided"}

                    **Response Format:**
                    Return only the pure SQL query, without markdown, without explanations.
                    Example: SELECT * FROM users WHERE age > 18 LIMIT 10
                    """

    def interpret_nl(
        self,
        natural_language_query: str,
        temperature: float = 0.3,  # creativity
        max_tokens: int = 500,  # words limit
    ) -> Dict[str, Any]:

        try:
            messages: List[Dict[str, Any]] = [
                {"role": "system", "content": self._build_system_prompt()},
                {"role": "user", "content": natural_language_query},
            ]

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,  # type: ignore
                temperature=temperature,
                max_tokens=max_tokens,
                n=1,
            )

            if (
                not hasattr(response, "choices")
                or not response.choices
                or not hasattr(response.choices[0], "message")
                or not response.choices[0].message
                or not hasattr(response.choices[0].message, "content")
                or not response.choices[0].message.content
            ):
                raise ValueError("No message returned")

            sql_query = response.choices[0].message.content.strip()
            sql_query = self._clean_sql_response(sql_query)

            tokens_used = response.usage.total_tokens if response.usage else 0

            return {
                "success": True,
                "sql_query": sql_query,
                "error": None,
                "model_used": self.model,
                "tokens_used": tokens_used,
            }

        except Exception as e:
            error_message = str(e)

            if "authentication" in error_message.lower():
                return {
                    "success": False,
                    "sql_query": None,
                    "error": "Authentication error. Check your API Key.",
                }
            elif "rate_limit" in error_message.lower():
                return {
                    "success": False,
                    "sql_query": None,
                    "error": "Request limit exceeded. Try again later.",
                }
            else:
                return {
                    "success": False,
                    "sql_query": None,
                    "error": f"Error: {error_message}",
                }

    def _clean_sql_response(self, sql: str) -> str:
        if sql.startswith("```sql"):
            sql = sql[6:]
        if sql.startswith("```"):
            sql = sql[3:]
        if sql.endswith("```"):
            sql = sql[:-3]

        sql = sql.strip()

        return sql

    def interpret_with_validation(
        self, natural_language_query: str, allowed_tables: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        result = self.interpret_nl(natural_language_query)

        if not result["success"]:
            return result

        sql_query = result["sql_query"]

        validations = {
            "is_select": sql_query.upper().strip().startswith("SELECT"),
            "no_dangerous_ops": not any(
                op in sql_query.upper()
                for op in ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE"]
            ),
            "uses_allowed_tables": True,
        }

        if allowed_tables:
            validations["uses_allowed_tables"] = any(
                table.upper() in sql_query.upper() for table in allowed_tables
            )

        all_valid = all(validations.values())

        result["validations"] = validations
        result["is_safe"] = all_valid

        if not all_valid:
            result["error"] = "Generated query did not pass security validations"

        return result
