# BreatheEasy Business Agent

**Student Name:** Hassan Khalil
**Course:** EECE 503P - Assignment 3

## 🌐 Live Demo

**Try it now on Hugging Face Spaces:** [https://huggingface.co/spaces/hassankhalil/breatheeasy-chatbot](https://huggingface.co/spaces/hassankhalil/breatheeasy-chatbot)

> 🚀 The chatbot is deployed and live! No installation needed - just click the link above to start chatting.

---

## Overview

This project implements an AI-powered customer service chatbot for **BreatheEasy**, a fictitious eco-friendly home cleaning business. The chatbot uses OpenAI's GPT-4 with function calling to answer customer questions, collect leads, and record feedback.

## Business Description

BreatheEasy is a premium home cleaning service focused on:
- **Eco-friendly cleaning products** - Only certified non-toxic, hypoallergenic products
- **Allergy-safe protocols** - Specialized cleaning methods for allergy sufferers
- **Full product transparency** - Complete disclosure of all products used
- **Health-first approach** - Prioritizing health over just appearance

### Services Offered:
1. Deep Cleaning Services
2. Move-In/Move-Out Cleaning
3. Allergen Treatment Services
4. Regular Maintenance Cleaning

## Project Structure

```
Assignment3/
│
├── me/
│   ├── about_business.pdf          # Detailed business profile (PDF)
│   └── business_summary.txt        # Short business summary (TXT)
│
├── business_agent.ipynb            # Main chatbot notebook
├── app.py                          # Deployment script
├── create_pdf.py                   # Script to generate PDF
├── .env                            # API keys (not in repo)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
└── (Generated at runtime)
    ├── customer_leads.json         # Collected customer leads
    └── customer_feedback.json      # Unanswered questions/feedback
```

## Features

### 1. Intelligent Question Answering
The chatbot can answer questions about:
- Services and pricing
- Allergy-safe protocols
- Eco-friendly products
- Team members
- Company values and mission

### 2. Tool Functions

**`record_customer_interest(name, email, message)`**
- Records customer contact information
- Saves leads to `customer_leads.json`
- Logs to console for monitoring
- Triggered when customers want to schedule services or request quotes

**`record_feedback(question)`**
- Records unanswered questions or feedback
- Saves to `customer_feedback.json`
- Logs to console for monitoring
- Triggered when the chatbot doesn't know the answer

### 3. Gradio Interface
- User-friendly chat interface
- Pre-loaded example questions
- Retry, undo, and clear functionality
- Professional branding

## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root (already created):

```
OPENAI_API_KEY=your_api_key_here
```

### 3. Generate PDF (if needed)

```bash
python create_pdf.py
```

## Running the Application

### Option 1: Jupyter Notebook

```bash
jupyter notebook business_agent.ipynb
```

Then run all cells to launch the chatbot.

### Option 2: Python Script

```bash
python app.py
```

This will start a Gradio server and provide:
- Local URL (e.g., http://127.0.0.1:7860)
- Public URL (shareable link)

## Usage Examples

### Example 1: Service Inquiry
**User:** "What services do you offer?"
**Bot:** Lists all four services with descriptions

### Example 2: Lead Collection
**User:** "I'm interested in scheduling a deep cleaning"
**Bot:** Asks for name, email, and details
**User:** "My name is John Doe, email is john@example.com, I need cleaning next week"
**Bot:** Uses `record_customer_interest()` tool to save the lead

### Example 3: Allergy Concern
**User:** "I have severe allergies. Can you help?"
**Bot:** Explains allergy-safe protocols and allergen treatment services

### Example 4: Unknown Question
**User:** "Do you offer carpet installation?"
**Bot:** Uses `record_feedback()` tool to log the question for team review

## Testing the Chatbot

Run through these test scenarios:

1. ✅ **General Questions** - Ask about services, products, team
2. ✅ **Lead Generation** - Express interest in booking
3. ✅ **Product Transparency** - Ask about cleaning products used
4. ✅ **Health Concerns** - Mention allergies or respiratory issues
5. ✅ **Unknown Questions** - Ask about services not offered
6. ✅ **Contact Information** - Request phone/email/hours

## Data Collection

### Customer Leads
All leads are saved to `customer_leads.json` with:
- Timestamp
- Customer name
- Email address
- Interest/message details

### Customer Feedback
All unanswered questions are saved to `customer_feedback.json` with:
- Timestamp
- Question/feedback content

## Technical Details

- **LLM Model:** GPT-4o-mini (OpenAI)
- **Framework:** Gradio for UI
- **Function Calling:** OpenAI Tools API
- **PDF Generation:** ReportLab
- **PDF Reading:** PyPDF2
- **Environment Management:** python-dotenv

## Deployment Options

### Local Development
```bash
python app.py
```

### HuggingFace Spaces (Bonus)
1. Create a new Space on HuggingFace
2. Upload all files except `.env`
3. Add `OPENAI_API_KEY` as a secret in Space settings
4. The app will auto-deploy

## Assignment Checklist

- ✅ Fictional business created (BreatheEasy)
- ✅ Business summary in TXT format
- ✅ Business profile in PDF format
- ✅ `record_customer_interest()` tool implemented
- ✅ `record_feedback()` tool implemented
- ✅ System prompt with business context
- ✅ OpenAI ChatCompletion with tool calling
- ✅ Gradio ChatInterface
- ✅ Tool functions log to console and file
- ✅ Complete Jupyter notebook
- ✅ Deployment script (app.py)
- ✅ Requirements.txt
- ✅ Professional documentation

## Future Enhancements

- Add database storage instead of JSON files
- Implement email notifications for new leads
- Add pricing calculator tool
- Integrate calendar for appointment scheduling
- Add multi-language support
- Deploy to production with authentication

## License

This is an educational project for EECE 503P.

## Contact

For questions about this project:
- **Student:** Hassan Khalil
- **Email:** [Your University Email]
- **Course:** EECE 503P - Fall 2025-26
