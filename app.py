"""
BreatheEasy Business Agent - Deployment Script
Created by: Hassan Khalil
Course: EECE 503P - Assignment 3

This script runs the BreatheEasy chatbot as a standalone application.
It can be deployed to HuggingFace Spaces or run locally.
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
from PyPDF2 import PdfReader

# Load environment variables (override any existing ones)
load_dotenv(override=True)

# Initialize OpenAI client
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OpenAI API key not found. Please check your .env file.")

client = OpenAI(api_key=api_key)

# Storage for leads and feedback
customer_leads = []
customer_feedback = []

# Load business information
def load_business_summary():
    """Load business summary from text file"""
    try:
        with open('me/business_summary.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("Warning: business_summary.txt not found")
        return ""

def load_business_pdf():
    """Load and extract text from business PDF"""
    try:
        reader = PdfReader('me/about_business.pdf')
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except FileNotFoundError:
        print("Warning: about_business.pdf not found")
        return ""

business_summary = load_business_summary()
business_pdf_content = load_business_pdf()

# Tool functions
def record_customer_interest(name, email, message):
    """
    Record customer interest/lead information.

    Args:
        name (str): Customer's name
        email (str): Customer's email address
        message (str): Customer's message or interest details

    Returns:
        str: Confirmation message
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lead_data = {
        'timestamp': timestamp,
        'name': name,
        'email': email,
        'message': message
    }

    customer_leads.append(lead_data)

    # Log to console
    print("\n" + "="*60)
    print("NEW CUSTOMER LEAD RECORDED")
    print("="*60)
    print(f"Timestamp: {timestamp}")
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Message: {message}")
    print("="*60 + "\n")

    # Save to file
    try:
        with open('customer_leads.json', 'w') as f:
            json.dump(customer_leads, f, indent=2)
    except Exception as e:
        print(f"Error saving lead to file: {e}")

    return f"Thank you {name}! Your information has been recorded. We'll contact you at {email} shortly."

def record_feedback(question):
    """
    Record customer feedback or unanswered questions.

    Args:
        question (str): The question or feedback that couldn't be answered

    Returns:
        str: Confirmation message
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    feedback_data = {
        'timestamp': timestamp,
        'question': question
    }

    customer_feedback.append(feedback_data)

    # Log to console
    print("\n" + "="*60)
    print("UNANSWERED QUESTION RECORDED")
    print("="*60)
    print(f"Timestamp: {timestamp}")
    print(f"Question: {question}")
    print("="*60 + "\n")

    # Save to file
    try:
        with open('customer_feedback.json', 'w') as f:
            json.dump(customer_feedback, f, indent=2)
    except Exception as e:
        print(f"Error saving feedback to file: {e}")

    return "Your question has been recorded and will be reviewed by our team."

def check_service_availability(location, service_type):
    """
    Check if BreatheEasy services are available in the customer's area.

    Args:
        location (str): Customer's city or zip code
        service_type (str): Type of service requested

    Returns:
        str: Availability information
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Log to console
    print("\n" + "="*60)
    print("SERVICE AVAILABILITY CHECK")
    print("="*60)
    print(f"Timestamp: {timestamp}")
    print(f"Location: {location}")
    print(f"Service Type: {service_type}")
    print("="*60 + "\n")

    # Service areas (simulated - in production would check real database)
    available_areas = ["beirut", "lebanon", "downtown", "hamra", "ashrafieh",
                      "verdun", "raouche", "gemmayzeh", "mar mikhael"]

    location_lower = location.lower()
    is_available = any(area in location_lower for area in available_areas)

    if is_available:
        return f"Great news! BreatheEasy services are available in {location}. We can provide {service_type} service in your area."
    else:
        return f"We're currently expanding our services. {location} is not in our service area yet, but we're recording your interest for future expansion."

def calculate_quote(service_type, home_size, frequency="one-time"):
    """
    Calculate a price estimate for cleaning services.

    Args:
        service_type (str): Type of service (deep cleaning, regular maintenance, etc.)
        home_size (str): Size of home (small, medium, large, or sq ft)
        frequency (str): How often (one-time, weekly, bi-weekly, monthly)

    Returns:
        str: Price estimate information
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Log to console
    print("\n" + "="*60)
    print("QUOTE CALCULATION")
    print("="*60)
    print(f"Timestamp: {timestamp}")
    print(f"Service Type: {service_type}")
    print(f"Home Size: {home_size}")
    print(f"Frequency: {frequency}")
    print("="*60 + "\n")

    # Pricing logic (simulated)
    base_prices = {
        "deep cleaning": {"small": 150, "medium": 250, "large": 400},
        "regular maintenance": {"small": 80, "medium": 130, "large": 200},
        "allergen treatment": {"small": 200, "medium": 300, "large": 450},
        "move-in/move-out": {"small": 180, "medium": 280, "large": 420}
    }

    frequency_discounts = {
        "weekly": 0.20,      # 20% discount
        "bi-weekly": 0.15,   # 15% discount
        "monthly": 0.10,     # 10% discount
        "one-time": 0.0      # No discount
    }

    # Normalize inputs
    service_lower = service_type.lower()
    size_lower = home_size.lower()
    freq_lower = frequency.lower()

    # Find matching service
    matched_service = None
    for key in base_prices.keys():
        if key in service_lower or service_lower in key:
            matched_service = key
            break

    # Determine size
    if "small" in size_lower or "studio" in size_lower or "1" in size_lower:
        size_key = "small"
    elif "large" in size_lower or "4" in size_lower or "5" in size_lower:
        size_key = "large"
    else:
        size_key = "medium"

    if matched_service and size_key in base_prices[matched_service]:
        base_price = base_prices[matched_service][size_key]

        # Apply frequency discount
        discount = frequency_discounts.get(freq_lower, 0.0)
        final_price = base_price * (1 - discount)

        # Log the calculation to console
        print(f"Base Price: ${base_price:.2f}")
        if discount > 0:
            print(f"Discount: {int(discount*100)}% ({frequency})")
            print(f"Final Price: ${final_price:.2f} per session")
        else:
            print(f"Final Price: ${final_price:.2f}")
        print("="*60 + "\n")

        if discount > 0:
            return f"Estimated quote for {service_type} ({home_size} home, {frequency}): ${final_price:.2f} per session (${base_price:.2f} with {int(discount*100)}% {frequency} discount). This is an estimate - final pricing will be confirmed after a home assessment."
        else:
            return f"Estimated quote for {service_type} ({home_size} home): ${final_price:.2f}. This is an estimate - final pricing will be confirmed after a home assessment."
    else:
        print("Unable to calculate - invalid parameters")
        print("="*60 + "\n")
        return f"Thank you for your interest in {service_type}. For an accurate quote based on your {home_size} home, please contact us at hello@breatheeasy.com or call (555) 123-EASY."

# Define tools for OpenAI
tools = [
    {
        "type": "function",
        "function": {
            "name": "record_customer_interest",
            "description": "Record customer contact information and interest. Use this when a customer wants to schedule a service, request a quote, or leave their contact details for follow-up.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The customer's full name"
                    },
                    "email": {
                        "type": "string",
                        "description": "The customer's email address"
                    },
                    "message": {
                        "type": "string",
                        "description": "Details about their interest, service needed, or any specific requirements"
                    }
                },
                "required": ["name", "email", "message"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "record_feedback",
            "description": "Record customer questions or feedback that you cannot answer. MUST be used when customers ask about services not offered by BreatheEasy (like carpet installation, window washing, steam cleaning, lawn care, etc.). Use this immediately when a question is about services not in the official list of four services.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The question or feedback that could not be answered"
                    }
                },
                "required": ["question"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_service_availability",
            "description": "Check if BreatheEasy services are available in a specific location. Use this when customers ask about service availability in their area, city, or neighborhood.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The customer's location (city, neighborhood, or zip code)"
                    },
                    "service_type": {
                        "type": "string",
                        "description": "The type of service they're interested in"
                    }
                },
                "required": ["location", "service_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_quote",
            "description": "Calculate a price estimate for cleaning services. Use this when customers ask about pricing, costs, or want a quote. Ask for home size and service frequency if not provided.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service_type": {
                        "type": "string",
                        "description": "The type of service (deep cleaning, regular maintenance, allergen treatment, or move-in/move-out)"
                    },
                    "home_size": {
                        "type": "string",
                        "description": "Size of the home (small/1-2 bedrooms, medium/2-3 bedrooms, large/4+ bedrooms)"
                    },
                    "frequency": {
                        "type": "string",
                        "description": "Service frequency (one-time, weekly, bi-weekly, or monthly)",
                        "default": "one-time"
                    }
                },
                "required": ["service_type", "home_size"]
            }
        }
    }
]

# System prompt
system_prompt = f"""
You are a friendly and knowledgeable customer service representative for BreatheEasy, an eco-friendly home cleaning business.

BUSINESS CONTEXT:
{business_summary}

YOUR ROLE:
- Answer questions about BreatheEasy's services, pricing, team, and values
- Help customers understand our unique allergy-safe and eco-friendly approach
- Collect customer contact information when they express interest in our services
- Be warm, professional, and health-conscious in your responses
- Emphasize our commitment to health, safety, and environmental responsibility

IMPORTANT GUIDELINES:
1. When customers ask about scheduling or want to book a service, ask for their name, email, and service details, then use the record_customer_interest function.
2. When customers ask about pricing or want a quote, use the calculate_quote function. Ask for home size and frequency if not provided.
3. When customers ask if service is available in their area, use the check_service_availability function.
4. If a customer asks about a service or product that is NOT explicitly listed in the SERVICES WE OFFER section below, you MUST use the record_feedback function to log the question. Do NOT try to answer questions about services we don't offer.
5. ONLY answer questions about the four services explicitly listed below. For ANY other service inquiries (carpet installation, window washing, lawn care, etc.), use record_feedback immediately.
6. Encourage customers to leave their contact information so we can provide personalized service.
7. Highlight our unique value propositions: allergy-safe protocol, product transparency, and health-first approach.
8. Be conversational and empathetic, especially when customers mention allergies or health concerns.
9. Keep responses concise but informative.

SERVICES WE OFFER:
1. Deep Cleaning Services - Comprehensive home cleaning with allergen elimination
2. Move-In/Move-Out Cleaning - Thorough preparation for new occupants
3. Allergen Treatment Services - Specialized for allergy sufferers
4. Regular Maintenance Cleaning - Weekly, bi-weekly, or monthly schedules

CONTACT INFO:
- Email: hello@breatheeasy.com
- Phone: (555) 123-EASY
- Hours: Monday-Saturday, 8am-6pm

Remember: You represent a business that genuinely cares about customer health and the environment. Let that shine through in every interaction!
"""

# Main chat function
def chat_with_breatheeasy(message, history):
    """
    Main chat function that handles user messages and tool calls.

    Args:
        message (str): User's message
        history (list): Chat history in Gradio format

    Returns:
        str: Assistant's response
    """
    # Convert Gradio history format to OpenAI format
    messages = [{"role": "system", "content": system_prompt}]

    # Add conversation history - handle both tuple and dict formats
    if history:
        for item in history:
            if isinstance(item, (list, tuple)) and len(item) == 2:
                # Tuple format: (user_msg, assistant_msg)
                human, assistant = item
                if human:
                    messages.append({"role": "user", "content": str(human)})
                if assistant:
                    messages.append({"role": "assistant", "content": str(assistant)})

    # Add current message
    messages.append({"role": "user", "content": message})

    # Call OpenAI API with tools
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        response_message = response.choices[0].message

        # Check if the model wants to call a tool
        if response_message.tool_calls:
            # Process tool calls
            messages.append(response_message)

            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Execute the appropriate function
                if function_name == "record_customer_interest":
                    function_response = record_customer_interest(
                        name=function_args.get("name"),
                        email=function_args.get("email"),
                        message=function_args.get("message")
                    )
                elif function_name == "record_feedback":
                    function_response = record_feedback(
                        question=function_args.get("question")
                    )
                elif function_name == "check_service_availability":
                    function_response = check_service_availability(
                        location=function_args.get("location"),
                        service_type=function_args.get("service_type")
                    )
                elif function_name == "calculate_quote":
                    function_response = calculate_quote(
                        service_type=function_args.get("service_type"),
                        home_size=function_args.get("home_size"),
                        frequency=function_args.get("frequency", "one-time")
                    )
                else:
                    function_response = "Unknown function called."

                # Add function response to messages
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                })

            # Get final response from the model
            second_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )

            final_content = second_response.choices[0].message.content
            return str(final_content) if final_content else "I apologize, I couldn't generate a proper response. Please try again."

        else:
            # No tool call, return the regular response
            content = response_message.content
            return str(content) if content else "I apologize, I couldn't generate a response. Please try rephrasing your question."

    except Exception as e:
        error_msg = f"I apologize, but I encountered an error: {str(e)}. Please try again or contact us directly at hello@breatheeasy.com"
        print(f"Error in chat function: {e}")
        import traceback
        traceback.print_exc()  # Print full error for debugging
        return error_msg

# Create Gradio interface
demo = gr.ChatInterface(
    fn=chat_with_breatheeasy,
    title="🌿 BreatheEasy - Eco-Friendly Home Cleaning",
    description="Welcome! I'm here to help you learn about our allergy-safe, eco-friendly cleaning services. Ask me anything about our services, pricing, or schedule a cleaning!",
    examples=[
        "What services do you offer?",
        "Tell me about your allergy-safe cleaning protocol",
        "How much does deep cleaning cost for a 3-bedroom house?",
        "Do you service the Hamra area in Beirut?",
        "I'm interested in scheduling a deep cleaning",
        "I have severe allergies. Can you help?"
    ],
    theme=gr.themes.Soft()
)

# Launch the app
if __name__ == "__main__":
    print("Starting BreatheEasy Chatbot...")
    print("="*60)
    demo.launch(
        share=True,  # Creates a public link
        server_name="0.0.0.0",  # For deployment
        server_port=7860,  # Standard Gradio port
        show_error=True
    )
