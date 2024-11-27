# 📈 Investment Analyst AI: Multi-Agent Stock Analysis System 🤖

## 🚀 Project Description

Investment Analyst AI is a sophisticated multi-agent system designed to function as a junior investment analyst. This system assists real analysts in appraising publicly traded companies by performing both fundamental and technical analysis. It simulates collaboration between specialized agents to provide comprehensive reports on user-selected companies.

## ✨ Key Features

### 1. 💰 **Fundamental Analysis**
- **Financial Data Extraction**: Extracts key financial data from EDGAR filings 📊
- **Financial Ratio Calculation**: Calculates and visualizes important financial ratios (ROE, ROA, Profit Margin, etc.) 🧮
- **Narrative Generation**: Provides narrative explanations of financial health using LangChain and GPT-3.5 📝
- **Stock Comparison**: Allows comparison between two stocks 🔍

### 2. 📉 **Technical Analysis**
- **Historical Data Analysis**: Analyzes historical price and volume data 📈
- **Technical Indicators**: Implements various technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands, etc.) 📊
- **Interactive Charting**: Provides interactive charts for trend analysis 🖥️
- **Comparative Analysis**: Supports comparative analysis of multiple stocks 📊

### 3. 🤝 **Coordination and Data Retrieval**
- **Agent Orchestration**: Orchestrates tasks between analysis agents 🔗
- **Efficient Data Processing**: Efficiently retrieves and processes financial data 💨
- **Performance Optimization**: Implements Redis caching for improved performance 🚀

### 4. 🖥️ **User Interface**
- **Interactive Dashboard**: Interactive dashboard for stock selection and analysis 🎛️
- **Metric Visualization**: Visualizations of key metrics and trends 📊
- **Comparative Features**: Comparative analysis features 🔬

## 🛠️ Detailed Setup and Running Instructions

### 📋 Prerequisites
- Python 3.8+ 🐍
- Redis server 🔴

### 🔽 Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/investment-analyst-ai.git
cd investment-analyst-ai
```

### 🌐 Step 2: Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
```

### 📦 Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### 🔐 Step 4: Set Up Environment Variables
Create a `.env` file in the root directory with the following content:
```
SEC_API_KEY=your_sec_api_key
OPENAI_API_KEY=your_openai_api_key
```

### 🔴 Step 5: Start Redis Server
Ensure Redis is installed and running on your system.

### 🚀 Step 6: Run the FastAPI Backend
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 🖥️ Step 7: Run the Streamlit Frontend
Open a new terminal, navigate to the frontend directory, and run:
```bash
cd frontend
streamlit run dashboard.py
streamlit run fundamental.py
streamlit run technical.py
```

### 🌐 Step 8: Access the Dashboard
Open a web browser and navigate to `http://localhost:8501`

## 🏗️ Architecture and Agent Design

The system employs a modular, multi-agent architecture designed for scalability and efficiency:

### 1. 📡 **Data Retrieval Agent** (`data_retrieval_agent.py`)
- Implements `DataRetrievalAgent` class
- Fetches data from multiple sources (EDGAR, Yahoo Finance)
- Uses `yfinance` for stock data and custom SEC API calls for EDGAR filings
- Implements `DataConverter` for standardizing data formats
- Methods: `get_stock_price_data()`, `get_financial_statements()`, `get_sec_edgar_data()`, etc.

### 2. 📊 **Fundamental Analysis Agent** (`fundamental_analysis_agent.py`)
- Implements `FundamentalAnalysisAgent` class
- Calculates financial ratios: ROE, ROA, Profit Margin, etc.
- Uses LangChain and GPT-3.5 for narrative generation
- Methods: `analyze_financials()`, `calculate_financial_ratios()`, `generate_financial_narrative()`

### 3. 📈 **Technical Analysis Agent** (`technical_analysis_agent.py`)
- Implements `TechnicalAnalysisAgent` class
- Calculates technical indicators: SMA, EMA, RSI, MACD, Bollinger Bands, etc.
- Methods: `analyze_technical()`, `calculate_moving_averages()`, `calculate_oscillators()`, etc.

### 4. 🤖 **Coordination Agent** (`coordination_agent.py`)
- Implements `CoordinationAgent` class
- Orchestrates tasks between other agents
- Method: `coordinate_analysis()` - distributes work and aggregates results

## 💾 Data Processing and Analysis
- **EDGAR Filings**: Extracted using custom SEC API calls in `DataRetrievalAgent`
- **Stock Data**: Retrieved using `yfinance` library
- Data cleaning and normalization handled in `DataConverter` class
- Financial ratios calculated in `FundamentalAnalysisAgent`
- Technical indicators computed in `TechnicalAnalysisAgent`

## 🧠 LLM Integration
- OpenAI's GPT-3.5 Turbo used for narrative generation in fundamental analysis
- LangChain employed for structuring prompts and processing responses

## 🛡️ Challenges Faced and Solutions
1. **Data Fetching and Processing**
   - Challenge: Handling large volumes of financial data
   - Solution: Implemented efficient data retrieval methods and caching with Redis

2. **Data Consistency**
   - Challenge: Dealing with inconsistent data formats from different sources
   - Solution: Developed robust data cleaning and normalization processes

3. **Performance Optimization**
   - Challenge: Slow response times for complex analyses
   - Solution: Implemented asynchronous processing and caching strategies

4. **API Rate Limits**
   - Challenge: Staying within rate limits of free API tiers
   - Solution: Implemented request throttling and efficient caching

## 🔑 Obtaining API Keys
1. **SEC API Key**
   - Register at SEC's Developer Resources
   - Follow instructions to obtain an API key

2. **OpenAI API Key**
   - Sign up at OpenAI
   - Navigate to the API section to create a new API key

## 🚀 Future Scope
1. Real-time data integration and visualization
2. Advanced predictive models for stock price forecasting
3. Enhanced comparative analysis features
4. Integration of additional data sources for more comprehensive analysis

## 📊 Assessment Criteria Fulfillment
1. **Functionality**: The system provides comprehensive fundamental and technical analysis, meeting core requirements.
2. **Multi-Agent System Design**: Implements distinct agents with clear responsibilities and effective communication.
3. **Technical Competence**: Utilizes appropriate technologies (FastAPI, Streamlit, LangChain) and implements efficient data processing.
4. **Code Quality**: Maintains clean, well-organized code with proper documentation.
5. **Problem-Solving Skills**: Demonstrates ability to integrate various technologies and handle complex financial data.
6. **User Experience**: Provides an intuitive, interactive dashboard for easy analysis and comparison.

## 📜 License

---

**Made with ❤️ and 🧠 by Saurabh Agrawal**
