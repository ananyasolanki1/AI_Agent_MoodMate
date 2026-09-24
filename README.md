# ReviewMate

AI-powered customer review analysis and mobile phone recommendation system using LangChain, Groq, Gradio, and MySQL.

## Aim

Analyze customer reviews using AI to identify sentiment and emotion, and recommend two similar-priced phones based on the review.

## Setup Instructions

1. Create a `.env` file in the root directory of the project.

2. Add your credentials:

```env
GROQ_API_KEY=your_actual_api_key_here
MYSQL_PASSWORD=your_mysql_password_here
```

3. Install the required packages:

```bash
pip install pandas python-dotenv langchain langchain-groq gradio mysql-connector-python
```

4. Create the MySQL database and required tables.

5. Load the product data into MySQL:

```bash
python data/load_products.py
```

6. Run the application:

```bash
python app.py
```

The application will open through the Gradio interface.

## Tech Stack

- Python
- LangChain
- Groq
- Gradio
- MySQL
- Pandas

## Note

Keep your `.env` file private and do not commit it to GitHub.
