Medical Assistant and Adiver
Welcome to the Medical Report Analyzer! This tool assists you in analyzing medical reports by extracting data from a PDF, locating relevant health articles, and offering personalized health recommendations—all in a single interface. Let’s dive in!

🚀 Key Features
Blood Report Analysis: Automatically extracts and summarizes content from a PDF blood report.
Health Information Search: Finds relevant health articles based on the extracted analysis.
Custom Recommendations: Offers easy-to-understand health tips based on the analysis results.
🛠️ Setup Guide
Follow the steps below to set up and run the application on your system.

1. Clone This Repository
Begin by cloning the repository to your local system:

bash
Copy code
git clone https://github.com/ansuman-shukla/Medical_CREW.git
2. Create and Activate a Virtual Environment
It is advisable to set up a virtual environment to handle dependencies:

bash
Copy code
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
3. Install Required Dependencies
Now, install the necessary Python packages:

bash
Copy code
pip install -r requirements.txt
4. Configure Environment Variables
Set up a .env file in the root directory of the project to store your API keys:

bash
Copy code
touch .env
Open the .env file in your preferred text editor and insert the following:

env
Copy code
SERPER_API_KEY=your-serper-api-key
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL_NAME=your-model-name
OPENAI_API_BASE=your-openai-api-base-url
Ensure you replace the placeholder values with your actual API keys and settings.

5. Run the Application
You can now launch the Streamlit app:

bash
Copy code
streamlit run app.py
6. Upload a PDF
Once the app is running, upload a PDF by clicking the "Browse file" button.



7. Start the Analysis and View Results
Click on the "Analyze Report" button to initiate the analysis. The results, including a summary of the blood test and health advice with clickable links to sources, will be shown on the same page.

🔍 How AI Agents Work
This application utilizes AI agents to analyze medical reports and provide health recommendations. Here’s an overview of how it functions:

1. Medical Analyst Agent
Role: The Medical Analyst is the first agent to take action. It’s responsible for analyzing the blood test report and pulling out critical information.
Task: This agent processes the uploaded PDF, extracts the text, and delivers a simplified summary of the blood test.
2. Health Researcher Agent
Role: After the Medical Analyst completes its task, the Health Researcher takes over.
Task: This agent searches for related health articles based on the analysis of the blood test and compiles a list of articles with URLs and summaries.
3. Health Advisor Agent
Role: Lastly, the Health Advisor reviews the analysis and the articles gathered by the Health Researcher.
Task: This agent formulates personalized health recommendations by summarizing the blood test and providing actionable advice with links to relevant sources.
4. Sequential Process Flow
Execution: The application follows a sequential process where each agent finishes its task before passing the output to the next agent. This ensures the final recommendations are well-researched and based on a comprehensive analysis.
5. Final Output
Result: The output is a clear and concise report in Markdown format, featuring a blood test summary and a list of health recommendations with clickable article links.
🧰 Development Guide
For developers looking to modify the code, follow these additional steps:

1. Enable Logging
Logging is already set up in the application, so you can monitor detailed logs in the terminal where you run the app.

2. Customize Agents and Tasks
The agent and task initialization logic is located in the app.py file. Feel free to tweak it to suit your needs.

3. Update Dependencies
If you add any new dependencies, ensure to update the requirements.txt file with the following command:

bash
Copy code
pip freeze > requirements.txt
4. Testing
Make sure to test any changes by running the application with various PDF files to ensure functionality.

