import os
from typing import Dict, Optional, Any, List, Tuple
from openai import OpenAI
from service import utils


class NaturalLanguageInterpreter:

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API Key not found. Configure OPENAI_API_KEY in .env")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.database_schema = ""

    def set_database_schema(self, schema: str):
        self.database_schema = schema

    # TODO: melhorar o prompt para ele retornar menos texto e mais visualização numérica
    def _build_system_prompt(self, prompt_type: int = 1) -> str:
        if prompt_type == 1:
            return f"""You are an SQL and database expert.
                Your task is to convert natural language questions into valid SQL queries.

                **IMPORTANT:**
                - Generate ONLY SELECT queries (read-only)
                - Return ONLY the SQL query, without additional explanations
                - Use LIMIT when appropriate to limit results
                - Be precise and efficient

                **Database Schema:**
                {self.database_schema if self.database_schema else "Schema not provided"}

                **Response Format:**
                Return only the pure SQL query, without markdown, without explanations.
                Example: SELECT * FROM users WHERE age > 18 LIMIT 10
                """
        elif prompt_type == 2:
            return """You are a data analyst assistant.
                Your task is to interpret SQL query results and explain them in natural language (Portuguese - pt-BR).

                **IMPORTANT:**
                - Summarize the main findings from the data
                - Explain what the data shows in simple, clear terms
                - Be concise and objective
                - Do NOT generate SQL queries
                - Respond ONLY in Portuguese (pt-BR)
                - Provide insights and patterns if visible in the data

                Analyze the following query result and provide a natural language interpretation:
                """
        else:
            raise ValueError(
                f"Invalid prompt_type: {prompt_type}. Use 1 for SQL generation or 2 for interpretation."
            )

    def interpret_nl(
        self,
        nl: str,
        temperature: float = 1.0,  # creativity
        max_completion_tokens: int = 2000,  # words limit
    ) -> Dict[str, Any]:

        try:
            messages: List[Dict[str, Any]] = [
                {
                    "role": "system",
                    "content": self._build_system_prompt(prompt_type=1),
                },
                {"role": "user", "content": nl},
            ]

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,  # type: ignore
                temperature=temperature,
                max_completion_tokens=max_completion_tokens,
                n=1,
            )

            content = response.choices[0].message.content
            if content is None:
                raise ValueError("No message returned")

            sql_query = content.strip()
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
        self, nl: str, allowed_tables: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        result = self.interpret_nl(nl)

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

    def _generate_context(
        self,
        query_result: List[Tuple[Any, ...]],
        columns: List[str],
        original_query: str,
    ) -> str:

        result_json = utils.tuples_to_json(query_result, columns)

        context = ""
        if original_query:
            context += f"SQL utilizada:\n{original_query}\n\n"
        context += f"Resultado da consulta (em JSON):\n{result_json}"

        return context

    def interpret_query_result_as_text(
        self,
        query_result: List[Tuple[Any, ...]],
        columns: List[str],
        original_query: str,
        temperature: float = 1.0,  # creativity
        max_completion_tokens: int = 2000,  # words limit
    ) -> Dict[str, Any]:

        try:

            context = self._generate_context(query_result, columns, original_query)

            messages: List[Dict[str, Any]] = [
                {
                    "role": "system",
                    "content": self._build_system_prompt(prompt_type=2),
                },
                {"role": "user", "content": context},
            ]

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,  # type: ignore
                temperature=temperature,
                max_completion_tokens=max_completion_tokens,
                n=1,
            )

            content = response.choices[0].message.content
            if content is None:
                raise ValueError("No message returned")

            interpretation = content.strip()

            tokens_used = response.usage.total_tokens if response.usage else 0

            return {
                "success": True,
                "interpretation": interpretation,
                "error": None,
                "model_used": self.model,
                "tokens_used": tokens_used,
            }

        except Exception as e:
            error_message = str(e)

            if "authentication" in error_message.lower():
                return {
                    "success": False,
                    "interpretation": None,
                    "error": "Authentication error. Check your API Key.",
                }
            elif "rate_limit" in error_message.lower():
                return {
                    "success": False,
                    "interpretation": None,
                    "error": "Request limit exceeded. Try again later.",
                }
            else:
                return {
                    "success": False,
                    "interpretation": None,
                    "error": f"Error: {error_message}",
                }
