# MoodMate

AI-powered customer feedback analysis using a LangChain agent and Groq.

## Setup Instructions

1. **Create a `.env` file** in the root directory of the project.

2. **Add your Groq API key** inside the file:
   ```env
   GROQ_API_KEY=your_actual_api_key_here
   ```

3. **Install the required packages** via your terminal:
   ```bash
   pip install pandas python-dotenv langchain langchain-groq openpyxl
   ```

4. **Download the dataset** used in this project:

   [Customer Review Dataset — Kaggle](https://www.kaggle.com/datasets/parve05/customer-review-dataset)

   Place the downloaded `redmi.csv` file in the root directory of the project.

5. **Run the application:**
   ```bash
   python3 main.py
   ```

   The analyzed reviews will be saved as:
   ```text
   MoodMate_Analysis.xlsx
   ```
