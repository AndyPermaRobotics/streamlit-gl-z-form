import json
import os
import time
from typing import Dict

import openai
import streamlit as st

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_current_date():
    """Get the current date"""

    obj = {"current_date": time.strftime("%Y-%m-%d")}

    return json.dumps(obj)


def get_completion(prompt, model="gpt-3.5-turbo-1106", temperature=0) -> str:
    messages = [{"role": "user", "content": prompt}]

    for i in range(3):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                # Step 1 - provide functions metadata
                functions=[
                    # {
                    #     "name": "get_current_weather",
                    #     "description": "Kann Auskunft über das aktuelle Wetter geben ",
                    #     "parameters": {
                    #         "type": "object",
                    #         "properties": {
                    #             "location": {
                    #                 "type": "string",
                    #                 "description": "Die Stadt, für die das Wetter abgefragt werden soll",
                    #             },
                    #             "unit": {
                    #                 "type": "string",
                    #                 "enum": ["celsius", "fahrenheit"]
                    #             },
                    #         },
                    #         "required": ["location"],
                    #     },
                    # },
                    {
                        "name": "get_current_date",
                        "description": "Kann das aktuelle Datum zurückgeben",
                        "parameters": {
                            "type": "object",
                            "properties": {},  # no parameters needed
                        },
                    },
                    # {
                    #     "name": "execute_python",
                    #     "description": "Kann Python Code ausführen",
                    #     "parameters": {
                    #         "type": "object",
                    #         "properties": {
                    #             "code": {
                    #                 "type": "string",
                    #                 "description": "Der Python Code, der ausgeführt werden soll",
                    #             },
                    #         },
                    #         "required": ["code"],
                    #     },
                    # }
                ],
                function_call="auto",
            )

            if isinstance(response, Dict):
                message = response["choices"][0]["message"]

                print(f"Received message: {message}")

                # Step 2, check if the model wants to call a function
                if message.get("function_call"):
                    function_name = message["function_call"]["name"]

                    print(f"Calling function: {function_name}")
                    print(f"Function parameters: {json.dumps(message)}")

                    arguments = json.loads(message["function_call"]["arguments"])

                    return_message = ""

                    print(f"{arguments=}")

                    if function_name == "get_current_date":
                        function_response = get_current_date()
                    elif function_name == "execute_python":
                        code = arguments.get("code")

                        print(f"{code=}")

                        return_message = f"Python Code:\n```{code}```"

                        if isinstance(code, str):
                            function_response = eval(code)
                        else:
                            raise Exception(f"Code is not a string: {code}")

                    else:
                        raise Exception(f"Unknown function: {function_name}")

                    # Step 4, send model the info on the function call and function response
                    second_response = openai.ChatCompletion.create(
                        model=model,
                        messages=[
                            {"role": "user", "content": prompt},
                            message,
                            {
                                "role": "function",
                                "name": function_name,
                                "content": str(function_response),
                            },
                        ],
                    )

                    if isinstance(second_response, Dict):
                        content = second_response["choices"][0]["message"]["content"]

                        if len(return_message) > 0:
                            return return_message + "\n\n" + content
                        else:
                            return content

                else:
                    # if no function call is needed, return the message content
                    return message["content"]

        except openai.APIError as e:
            print(f"API Error '{e}' occurred, retrying ({i+1}/3)...")
            st.error(e)
            time.sleep(1)
        except Exception as e:
            print(f"Error occurred: '{e}'. Retrying ({i+1}/3)...")
            st.error(e)
            time.sleep(3)
    raise Exception("Failed to get response from OpenAI after 3 retries")


if __name__ == "__main__":

    # Example usage
    prompt = "wie alt bist du?"
    response = get_completion(prompt)
    print(response)
