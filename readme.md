# 📚 Paper Analyzer (Mistral-Powered)

This project is a pure Python backend that uses the Mistral AI API to analyze exam questions and extract the most frequently occurring high-level topics. It's perfect for competitive exams, semester question paper analysis, and education-focused AI applications.

Just Load YOur Papers(pdf form) in /papers and run main.py

## 🚀 Features

* 🔍 Analyze multiple questions in one go
* 🎯 Extract 5–6 most common technical topics
* ⚡ Powered by Mistral API
* 📂 Simple script-based usage (`main.py`)
* 🛡️ Environment-safe with `.env` file



## 🛠️ Installation & Setup

### 1. Clone the repository

bash
git clone https://github.com/mahivram/Paper_Analyzer.git
cd paper-analyzer


### 2. Create a virtual environment

bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate


### 3. Install dependencies

bash
pip install -r requirements.txt


### 4. Set up your `.env` file

Create a `.env` file in the root directory:


MISTRAL_API_KEY=your_mistral_api_key_here


> 🔐 Never share or commit your `.env` file.



## ▶️ Running the Script

This project is not an API server (yet). You simply run the script to analyze questions from a text file.

### Example usage:

bash
python main.py


Make sure your `important_questions.txt` file exists and contains one question per line.



## 🧾 Dependencies

Install these using `pip install -r requirements.txt`:

txt
requests
python-dotenv


Generate `requirements.txt` if needed:

bash
pip freeze > requirements.txt




## 🛡️ .gitignore (Auto-Ignored Files)

gitignore
# Python
__pycache__/
*.pyc

# Virtual Environment
venv/

# Environment variables
.env

# OS/system
.DS_Store
Thumbs.db




## 🌐 Deployment

This project is currently script-based and not meant for server deployment. However, you can easily turn it into a REST API later using FastAPI or Flask.

Let me know if you want to upgrade it to an API.



## 🧽 Contributions

Feel free to fork this repo and contribute via pull requests. If you have suggestions for more advanced analysis (e.g., using embeddings or ranking), open an issue!



## 📄 License

MIT License. Use freely with attribution.



> Built with ❤️ using Python + Mistral API
