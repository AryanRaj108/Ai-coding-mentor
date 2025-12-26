import google.generativeai as genai

# Configure Gemini API with your API key
GEMINI_API_KEY = "AIzaSyBRmhgyfTFKfxkIQXRQyyMWkHDST6I7M8w"  # Replace with secrets for production
genai.configure(api_key=GEMINI_API_KEY)

# Load the Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

# Only allow "array"-related questions
ALLOWED_KEYWORDS = {"code", "coding", "program", "programming", "algorithm", "syntax", "function", "class", "variable",
    "loop", "condition", "array", "list", "string", "debug", "compile", "run",
    "object", "inheritance", "polymorphism", "recursion", "data structure", "database", "sql",
    "python", "java", "cpp", "c++", "javascript", "html", "css", "ruby", "php", "swift", "kotlin",
    "go", "rust", "perl", "bash", "shell", "typescript", "scala", "matlab"}

def get_mentor_response(user_input):
    input_lower = user_input.lower()

    # Check if input contains only array-related keywords
    if any(keyword in input_lower for keyword in ALLOWED_KEYWORDS):
        prompt = f"As an AI coding mentor, explain the concept and give a code example for: {user_input}"
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error with Gemini API: {str(e)}"
    else:
        return "⚠️ I'm restricted to answering **only questions related to arrays**. Please ask about 1D, 2D, or language-specific arrays."


