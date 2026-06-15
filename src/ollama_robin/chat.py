import os
import sys
import ollama
from exa_py import Exa
import robin_stocks.robinhood as rh
from dotenv import load_dotenv

# Import our modular tools package
from ollama_robin.tools.schemas import tools
from ollama_robin.tools.handlers import handle_tool_call

# Load environment variables
load_dotenv()
load_dotenv('.env.local')

def main():
    model = 'gemma4:e4b'
    
    # Verify/get model list
    try:
        response = ollama.list()
        models = [m.model for m in response.models]
        if not models:
            print("No models found. Please pull a model first.")
            sys.exit(1)
        if model not in models and len(models) > 0:
            matching_models = [m for m in models if 'gemma4' in m]
            model = matching_models[0] if matching_models else models[0]
    except Exception as e:
        print(f"Warning: Could not connect to Ollama. Error: {e}")
        sys.exit(1)
        
    # Check for Exa API Key
    exa_api_key = os.environ.get("EXA_API_KEY")
    exa_client = None
    if exa_api_key:
        exa_client = Exa(api_key=exa_api_key)
        print("Exa Search Tool enabled.")
    else:
        print("Warning: EXA_API_KEY not found in environment. Exa Search Tool is disabled.")

    # Check for Robinhood login
    rb_username = os.environ.get("ROBINHOOD_USERNAME")
    rb_password = os.environ.get("ROBINHOOD_PASSWORD")
    rb_enabled = False
    
    if rb_username and rb_password:
        try:
            print("Attempting login to Robinhood...")
            login_res = rh.login(username=rb_username, password=rb_password)
            if login_res:
                rb_enabled = True
                print("Successfully logged into Robinhood.")
            else:
                print("Warning: Robinhood login failed.")
        except Exception as e:
            print(f"Warning: Could not login to Robinhood. Error: {e}")
    else:
        print("Warning: ROBINHOOD_USERNAME/ROBINHOOD_PASSWORD not set. Robinhood tools disabled.")

    # Active tools list based on configuration
    active_tools = []
    if exa_client:
        active_tools.append(tools[0])  # search_web
    if rb_enabled:
        active_tools.extend(tools[1:])

    print(f"--- Chatting with model: {model} (type 'exit' or 'quit' to stop) ---")
    messages = []
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
                
            messages.append({'role': 'user', 'content': user_input})
            
            # Send message with active tools
            response = ollama.chat(
                model=model,
                messages=messages,
                tools=active_tools if active_tools else None
            )
            
            assistant_message = response.get('message', {})
            tool_calls = assistant_message.get('tool_calls', [])
            
            thinking = assistant_message.get('content', '')
            if thinking:
                print(f"\n{model} (thinking):\n{thinking}")
            
            # If model requested tool execution
            if tool_calls:
                messages.append(assistant_message)
                
                for tool_call in tool_calls:
                    func_name = tool_call.get('function', {}).get('name')
                    args = tool_call.get('function', {}).get('arguments', {})
                    
                    tool_response = handle_tool_call(func_name, args, exa_client, rb_enabled)
                    
                    messages.append({
                        'role': 'tool',
                        'name': func_name,
                        'content': tool_response
                    })
                
                # Fetch final response after tools execution
                print(f"{model}: ", end="", flush=True)
                response_content = ""
                
                # Stream the final response
                stream = ollama.chat(model=model, messages=messages, stream=True)
                for chunk in stream:
                    content = chunk['message']['content']
                    print(content, end="", flush=True)
                    response_content += content
                print()
                
                messages.append({'role': 'assistant', 'content': response_content})
                
            else:
                content = assistant_message.get('content', '')
                if not thinking:
                    print(f"{model}: {content}")
                messages.append(assistant_message)
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == '__main__':
    main()
