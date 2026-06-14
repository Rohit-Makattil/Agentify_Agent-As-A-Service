import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

MODEL_TYPE = os.getenv("MODEL_TYPE", "gemini")  # default = gemini
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# -------------------------------------------------------------
# ✅ Helper to wrap the user's prompt with clear instructions
# -------------------------------------------------------------
def prompt_with_instruction(user_prompt: str, theme: str = "") -> str:
    theme_instruction = f"\nCRITICAL DESIGN THEME: You MUST heavily style the CSS to match a '{theme}' aesthetic. Use explicit color palettes, background gradients, modern box-shadows, and fonts that fit this exact theme. If it is a dark theme, ensure the background is dark and text is light." if theme else ""
    return (
        "You are an expert frontend web developer and UI/UX designer. "
        "Generate clean, highly aesthetic, production-ready HTML, CSS, and JavaScript for a website.\n"
        f"{theme_instruction}\n"
        "CRITICAL INSTRUCTIONS TO PREVENT BASIC DESIGNS:\n"
        "1. EXPAND ON SHORT PROMPTS: Even if the user's prompt is very short, YOU MUST intelligently expand it into a FULL, PREMIUM landing page. Do not just output one or two sentences.\n"
        "2. REQUIRED SECTIONS: Automatically include a sleek Navbar, a visually stunning Hero section with calls-to-action, at least 2 content sections (like Features, Services, or About), and a modern Footer.\n"
        "3. RICH AESTHETICS: Use beautiful typography, smooth hover effects, micro-animations, padding, and modern layout structures (flexbox/grid). Make it look like an expensive, award-winning website.\n"
        "4. DEFAULT CONTENT: Use high-quality placeholder text, creative dummy data, and font-awesome icons to make the interface feel populated and alive. Do not leave the page empty.\n"
        "5. IMPORTANT: The design MUST reflect the theme specified. DO NOT USE GENERIC STYLES.\n"
        "Keep code concise but complete. Separate each file clearly using the exact markdown tags below:\n"
        "```html\n<!-- HTML -->\n```\n"
        "```css\n/* CSS */\n```\n"
        "```javascript\n// JS\n```\n\n"
        f"User prompt: {user_prompt}"
    )

def modify_prompt_with_instruction(current_files: dict, edit_prompt: str, theme: str = "") -> str:
    theme_instruction = f" CRITICAL THEME REQUIREMENT: Ensure the updates strictly maintain and enhance the '{theme}' aesthetic (colors, backgrounds, layout)." if theme else ""
    
    files_context = ""
    for filename, content in current_files.items():
        files_context += f"file: {filename}\n```\n{content}\n```\n\n"

    return (
        "You are an expert frontend web developer. You are given an existing website's HTML, CSS, and JS code. "
        "Your task is to MODIFY the existing code based on the user's specific instruction. "
        f"USER INSTRUCTION: {edit_prompt}\n\n"
        "GUIDELINES:\n"
        "1. ONLY modify parts of the code relevant to the instruction.\n"
        "2. Preserve the rest of the structure, layout, and content.\n"
        "3. Ensure the code remains clean, valid, and fully functional.\n"
        f"4.{theme_instruction}\n"
        "5. Return the COMPLETE content for all three files even if some parts haven't changed, to maintain consistency.\n\n"
        "EXISTING CODE:\n"
        f"{files_context}"
        "\nIMPORTANT: Separate each file clearly using the exact markdown tags below:\n"
        "```html\n<!-- HTML -->\n```\n"
        "```css\n/* CSS */\n```\n"
        "```javascript\n// JS\n```"
    )


# -------------------------------------------------------------
# ✅ OpenAI (optional) - only used if MODEL_TYPE=openai
# -------------------------------------------------------------
def call_openai(prompt: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content


# -------------------------------------------------------------
# ✅ Gemini (default) - free tier via Google AI Studio
# -------------------------------------------------------------
import google.generativeai as genai

def get_latest_gemini_flash():
    # genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    # models = [m.name for m in genai.list_models() if "generateContent" in m.supported_generation_methods]
    # flash_models = [m for m in models if "flash" in m]
    # # Pick the latest or stable version
    # for m in ["models/gemini-2.5-flash", "models/gemini-2.0-flash-lite"]:
    #     if m in flash_models:
    #         return m
    return "gemini-2.5-flash"

def _stream_gemini(model, prompt: str) -> str:
    """Streams a Gemini model response and returns the full text."""
    response = model.generate_content(prompt, stream=True)
    full_text = ""
    for chunk in response:
        if chunk.text:
            full_text += chunk.text
    return full_text

def call_gemini(prompt: str) -> str:
    import google.generativeai as genai
    import concurrent.futures

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment.")
    genai.configure(api_key=api_key)

    # Try working models in order of preference based on current API availability
    models_to_try = [
        "gemini-2.0-flash-lite",      # Fast, highest rate limits
        "gemini-2.0-flash",           # High quality, good limits
        "gemini-2.5-flash-lite",      # New but good limits
        "gemini-flash-latest",        # Dynamic fallback
        "gemini-2.5-flash"            # Lowest daily limit, try last
    ]

    last_error = None
    for model_name in models_to_try:
        try:
            print(f"Trying model: {model_name}")
            model = genai.GenerativeModel(model_name)
            
            # Add RPM rate-limit auto-retry loop
            for attempt in range(2):
                try:
                    # Use a thread with 120s timeout to prevent 504 Deadline Exceeded hanging forever
                    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                        future = executor.submit(_stream_gemini, model, prompt)
                        result = future.result(timeout=120)
                    print(f"✅ Success with model: {model_name}")
                    return result
                except Exception as inner_e:
                    inner_err_str = str(inner_e).lower()
                    if ("429" in inner_err_str or "quota" in inner_err_str) and attempt == 0:
                        import re, time
                        match = re.search(r'retry in (\d+\.?\d*)s', inner_err_str)
                        if match:
                            delay = float(match.group(1)) + 1
                            if delay <= 15.0:
                                print(f"⏳ Burst RPM hit. Auto-pausing for {delay:.1f}s...")
                                time.sleep(delay)
                                continue
                            else:
                                print(f"⚠️ Exhausted hard limit (Wait time {delay:.1f}s). Skipping to next model instead of hanging!")
                                raise inner_e  # Escalate immediately
                    raise inner_e  # Escalate out of inner loop if not recoverable or already retried

        except concurrent.futures.TimeoutError:
            last_error = f"{model_name} timed out after 120s"
            print(f"⚠️ {last_error}, trying next model...")
            continue
        except Exception as e:
            err_str = str(e).lower()
            # Catch timeouts, missing models, and generic auth dropouts to auto-failover
            if any(err in err_str for err in ["504", "deadline", "timed out", "404", "not found"]):
                last_error = err_str
                print(f"⚠️ {model_name} failed ({err_str[:50]}...), cascading to next model...")
                import time
                time.sleep(1) # Nano backoff
                continue
            
            # If we STILL have a quota error here, it means we exhausted retries or hit a hard Daily cap
            if "429" in err_str or "quota" in err_str:
                last_error = err_str
                print(f"⚠️ {model_name} quota exhausted critically, cascading to next model...")
                continue
                
            raise  # Re-raise explicit catastrophic errors (like bad API keys)




    raise RuntimeError(f"All Gemini models failed. Last error: {last_error}")


# -------------------------------------------------------------
# ✅ Local Model (optional, placeholder for your fine-tuned model)
# -------------------------------------------------------------
def call_local_model(prompt: str) -> str:
    # You can later replace this with your own model
    return f"<p>This is a placeholder response for local model.</p>\nPrompt: {prompt}"


# -------------------------------------------------------------
# ✅ Main Function to Generate Website Code
# -------------------------------------------------------------
def generate_code_from_prompt(user_prompt: str, theme: str = "") -> dict:
    full_prompt = prompt_with_instruction(user_prompt, theme)

    if MODEL_TYPE == "openai":
        response_text = call_openai(full_prompt)
    elif MODEL_TYPE == "local":
        response_text = call_local_model(full_prompt)
    else:
        response_text = call_gemini(full_prompt)

    files = parse_files_from_model_text(response_text)
    return {'files': files, 'raw': response_text}

def modify_code_from_prompt(current_files: dict, edit_prompt: str, theme: str = "") -> dict:
    full_prompt = modify_prompt_with_instruction(current_files, edit_prompt, theme)

    if MODEL_TYPE == "openai":
        response_text = call_openai(full_prompt)
    elif MODEL_TYPE == "local":
        response_text = call_local_model(full_prompt)
    else:
        response_text = call_gemini(full_prompt)

    files = parse_files_from_model_text(response_text)
    
    # Merge with current files if any were missed by the LLM
    final_files = current_files.copy()
    for filename, content in files.items():
        if content.strip():
            final_files[filename] = content
            
    return {'files': final_files, 'raw': response_text}


# -------------------------------------------------------------
# ✅ Extract HTML, CSS, JS from the model's output
# -------------------------------------------------------------
def parse_files_from_model_text(output_text: str) -> dict:
    files = {}

    import re
    # Try multiple common formats for code blocks
    html_match = re.search(r"```(?:html|index\.html)\s*([\s\S]*?)```", output_text, re.IGNORECASE)
    css_match = re.search(r"```(?:css|style\.css)\s*([\s\S]*?)```", output_text, re.IGNORECASE)
    js_match = re.search(r"```(?:(?:java)?script|js|script\.js)\s*([\s\S]*?)```", output_text, re.IGNORECASE)

    if html_match:
        files["index.html"] = html_match.group(1).strip()
    if css_match:
        files["style.css"] = css_match.group(1).strip()
    if js_match:
        files["script.js"] = js_match.group(1).strip()
    
    # Fallback: if no code blocks found, check if raw text looks like HTML
    if not files:
        # Check if the entire response is an HTML block
        if "<html" in output_text.lower() or "<!doctype html" in output_text.lower():
            # Try to strip markdown quotes if it wrapped the entire thing in generic ```
            content = re.sub(r"^```.*\n", "", output_text)
            content = re.sub(r"```$", "", content).strip()
            files["index.html"] = content
            
    return files


# -------------------------------------------------------------
# ✅ Example usage (for local testing)
# -------------------------------------------------------------
if __name__ == "__main__":
    example_prompt = "Create a landing page for a travel website with a header, hero section, and footer."
    result = generate_code_from_prompt(example_prompt)
    print("=== index.html ===\n", result['files']["index.html"])
    print("\n=== style.css ===\n", result['files']["style.css"])
    print("\n=== script.js ===\n", result['files']["script.js"])
