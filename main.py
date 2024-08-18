import os
import logging
from dotenv import load_dotenv
import streamlit as st
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from pypdf import PdfReader

# Load configuration from the .env file
load_dotenv()

# API keys and model configuration
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_NAME = "gpt-4o"

# Set up logging system
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def retrieve_env_variables():
    """
    Fetches and returns the necessary environment variables for the application.

    Returns:
        dict: A dictionary containing the loaded environment variables.
    """
    return {
        "SERPER_API_KEY": SERPER_API_KEY,
        "OPENAI_API_KEY": OPENAI_API_KEY,
        "OPENAI_MODEL_NAME": OPENAI_MODEL_NAME,
    }

def setup_agents():
    """
    Configures and returns the agents that the application will use.

    Returns:
        tuple: A tuple containing the initialized agent instances.
    """
    medical_analyst = Agent(
        role='Medical Analyst',
        goal='Interpret the blood test results and create a simplified summary.',
        verbose=True,
        memory=True,
        backstory=(
            "A specialist in interpreting medical data and explaining it in layman's terms."
        ),
        # max_iter=10,
        allow_delegation=False
    )

    health_researcher = Agent(
        role='Health Researcher',
        goal='Explore online resources to find articles that match the analysis of the blood test, focusing on content relevant to the person’s health concerns.',
        verbose=True,
        memory=True,
        backstory=(
            "Expert at locating reliable and pertinent health-related information on the web."
        ),
        # max_iter=10,
        # max_rpm=2,
        allow_delegation=False,
        tools=[SerperDevTool(api_key=SERPER_API_KEY)]
    )

    health_advisor = Agent(
        role='Health Advisor',
        goal='Give personalized health suggestions based on the articles found and the blood test summary.',
        verbose=True,
        memory=True,
        backstory=(
            "Experienced in offering tailored health advice."
        ),
        # max_iter=10,
        # max_rpm=2,
        allow_delegation=False
    )

    return medical_analyst, health_researcher, health_advisor

def setup_tasks(medical_analyst, health_researcher, health_advisor):
    """
    Sets up and returns the tasks for the application.

    Args:
        medical_analyst (Agent): The medical analyst agent.
        health_researcher (Agent): The health researcher agent.
        health_advisor (Agent): The health advisor agent.

    Returns:
        list: A list of tasks ready to be executed.
    """
    analyze_blood_test = Task(
        description='Extract patient details from the blood test report and summarize it in plain language.',
        expected_output='Patient details at the top, followed by a simple summary of the blood test.',
        agent=medical_analyst,
    )

    search_for_articles = Task(
        description='Look for relevant web articles that address the health issues found in the blood test summary.',
        expected_output='A compilation of articles with URLs and brief descriptions.',
        tools=[SerperDevTool(api_key=SERPER_API_KEY)],
        agent=health_researcher,
    )

    provide_recommendations = Task(
        description='''
            Offer health recommendations based on the summary and found articles. Include relevant links for each recommendation.
        ''',
        expected_output='''
            A brief summary of the blood test in simple terms, followed by a list of actionable health tips. 
            Each item should include a link to the corresponding source.

            ## Summary
            [Insert a short summary of the blood report here. If necessary, use specific data from the report (e.g., platelet count).]

            ## Recommendations
            - [First recommendation (e.g., eat a balanced diet)](https://example1.com)
            - [Second recommendation (e.g., stay hydrated)](https://example2.com)
            - [Third recommendation (e.g., exercise regularly)](https://example3.com)
        ''',
        agent=health_advisor,
    )

    return [analyze_blood_test, search_for_articles, provide_recommendations]

def main():
    st.title("Blood Test Report Analyzer")

    uploaded_file = st.file_uploader("Select a PDF file", type="pdf")

    if uploaded_file:
        # Extract text from PDF
        extracted_text = ""
        try:
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                extracted_text += page.extract_text()
        except Exception as e:
            st.error(f"Failed to read the PDF: {e}")
            logger.error(f"PDF reading error: {e}")
            return

        if st.button("Analyze Report"):
            st.write("Analyzing report...")
            logger.info("Started report analysis")

            # Initialize agents and tasks
            medical_analyst, health_researcher, health_advisor = setup_agents()
            tasks = setup_tasks(medical_analyst, health_researcher, health_advisor)

            # Form the crew and configure the process
            crew = Crew(
                agents=[medical_analyst, health_researcher, health_advisor],
                tasks=tasks,
                process=Process.sequential
            )

            # Execute the crew's process with the extracted text
            with st.spinner("Processing..."):
                try:
                    result = crew.kickoff(inputs={"text": extracted_text})
                    logger.info("Report analysis successfully completed")
                except Exception as e:
                    st.error(f"Analysis error: {e}")
                    logger.error(f"Analysis error: {e}")
                    return

            # Display the results with markdown for links and formatting
            st.subheader("Analysis Results")
            st.markdown(result)
    else:
        st.write("Please upload a PDF file to start the analysis.")

if __name__ == "__main__":
    main()
