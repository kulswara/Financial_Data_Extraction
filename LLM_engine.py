from openai import OpenAI

# Initialize the OpenAI client with your API key
client = OpenAI(api_key="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")


def generate_text_response(table_data):
    prompt = f""" Json format : {{
    "Standalone_financial_results_for_all_months": {{
        "Quarter ended 31 December 2024": {{
            "Revenue from operations": "",
            "Other income": "",
            "Total income": "",
            "Cost of construction and development": "",
            "Changes in inventories of work-in-progress and finished properties": "",
            "Employee benefit expense": "",
            "Finance costs": "",
            "Depreciation and amortisation expenses": "",
            "Other expenses": "",
            "Total expenses": "",
            "Profit/loss before tax": "",
            "Current tax": "",
            "Deferred tax": "",
            "Profit/loss for the period/year": "",
            "Other comprehensive income/loss": "",
            "Total comprehensive income/loss for the period/year, net of tax": ""
        }},
        "Quarter ended 30 September 2024": {{
            "Revenue from operations": "",
            "Other income": "",
            "Total income": "",
            "Cost of construction and development": "",
            "Changes in inventories of work-in-progress and finished properties": "",
            "Employee benefit expense": "",
            "Finance costs": "",
            "Depreciation and amortisation expenses": "",
            "Other expenses": "",
            "Total expenses": "",
            "Profit/loss before tax": "",
            "Current tax": "",
            "Deferred tax": "",
            "Profit/loss for the period/year": "",
            "Other comprehensive income/loss": "",
            "Total comprehensive income/loss for the period/year, net of tax": ""
        }},
        "Quarter ended 31 December 2023": {{
            "Revenue from operations": "",
            "Other income": "",
            "Total income": "",
            "Cost of construction and development": "",
            "Changes in inventories of work-in-progress and finished properties": "",
            "Employee benefit expense": "",
            "Finance costs": "",
            "Depreciation and amortisation expenses": "",
            "Other expenses": "",
            "Total expenses": "",
            "Profit/loss before tax": "",
            "Current tax": "",
            "Deferred tax": "",
            "Profit/loss for the period/year": "",
            "Other comprehensive income/loss": "",
            "Total comprehensive income/loss for the period/year, net of tax": ""
        }},
        "Year to date period ended 31 December 2024": {{
            "Revenue from operations": "",
            "Other income": "",
            "Total income": "",
            "Cost of construction and development": "",
            "Changes in inventories of work-in-progress and finished properties": "",
            "Employee benefit expense": "",
            "Finance costs": "",
            "Depreciation and amortisation expenses": "",
            "Other expenses": "",
            "Total expenses": "",
            "Profit/loss before tax": "",
            "Current tax": "",
            "Deferred tax": "",
            "Profit/loss for the period/year": "",
            "Other comprehensive income/loss": "",
            "Total comprehensive income/loss for the period/year, net of tax": ""
        }},
        "Year to date period ended 31 December 2023": {{
            "Revenue from operations": "",
            "Other income": "",
            "Total income": "",
            "Cost of construction and development": "",
            "Changes in inventories of work-in-progress and finished properties": "",
            "Employee benefit expense": "",
            "Finance costs": "",
            "Depreciation and amortisation expenses": "",
            "Other expenses": "",
            "Total expenses": "",
            "Profit/loss before tax": "",
            "Current tax": "",
            "Deferred tax": "",
            "Profit/loss for the period/year": "",
            "Other comprehensive income/loss": "",
            "Total comprehensive income/loss for the period/year, net of tax": ""
        }},
        "Year ended 31 March 2024": {{
            "Revenue from operations": "",
            "Other income": "",
            "Total income": "",
            "Cost of construction and development": "",
            "Changes in inventories of work-in-progress and finished properties": "",
            "Employee benefit expense": "",
            "Finance costs": "",
            "Depreciation and amortisation expenses": "",
            "Other expenses": "",
            "Total expenses": "",
            "Profit/loss before tax": "",
            "Current tax": "",
            "Deferred tax": "",
            "Profit/loss for the period/year": "",
            "Other comprehensive income/loss": "",
            "Total comprehensive income/loss for the period/year, net of tax": ""
        }}
    }},
    "Balance_sheet": "Balance_sheet_are_not_present",
    "Cash_flow_statements": "Cash_flow_statements_are_not_present"
    
}}



extracted teable data : {table_data}"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Specify GPT-4o model
            messages=[
                {"role": "system", "content": "You are an expert Data Engineer. Given the table data extracted from the financial PDF file, your task is to extract the values in JSON format for both standalone and consolidated financial data. I have provided the format for standalone financial data. Use the same format for consolidated data if it exists in the document . If not , please don't include in the output."},
                {"role": "user", "content": prompt}
            ]
            )
        # Extract and return the response text
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"


# result = generate_text_response(prompt_template)
# print(result)