from pydantic_ai import Agent
from pydantic import BaseModel
from dotenv import load_dotenv
import yfinance as yf
import gradio as gr
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Define a variável de ambiente para a chave de API, se não estiver configurada
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("A chave de API 'GROQ_API_KEY' não foi encontrada no arquivo .env.")
os.environ["GROQ_API_KEY"] = api_key  # Garante que está no ambiente para a biblioteca

class StockPriceResult(BaseModel):
    """
    Modelo para representar os resultados do agente ao buscar informações sobre o preço de ações.
    
    Attributes:
        symbol (str): O símbolo da ação (ex.: "AAPL" para Apple).
        price (float): O preço atual da ação.
        currency (str): A moeda na qual o preço é cotado (padrão: "USD").
        message (str): Mensagem adicional gerada pelo agente.
    """
    symbol: str
    price: float
    currency: str = "USD"
    message: str

# Configura o agente de IA com o modelo correto
stock_agent = Agent(
    model="groq:llama3-groq-70b-8192-tool-use-preview",
    result_type=StockPriceResult,
    system_prompt=(
        "You are a helpful financial assistant that can look up stock prices. "
        "Use the get_stock_price tool to fetch current data."
    ),
)

@stock_agent.tool_plain
def get_stock_price(symbol: str) -> dict:
    """
    Ferramenta para buscar o preço atual de uma ação usando a biblioteca yfinance.
    
    Args:
        symbol (str): O símbolo da ação para consulta (ex.: "AAPL").
    
    Returns:
        dict: Um dicionário contendo o preço da ação e a moeda.
    """
    ticker = yf.Ticker(symbol)
    price = ticker.fast_info.last_price
    return {
        "price": round(price, 2),  # Arredonda o preço para duas casas decimais
        "currency": "USD"         # Define a moeda como USD
    }

def get_stock_info(query: str) -> str:
    """
    Processa a consulta do usuário para buscar informações sobre ações.

    Args:
        query (str): Consulta do usuário sobre o preço de uma ação.

    Returns:
        str: Uma string formatada com as informações da ação ou uma mensagem de erro.
    """
    try:
        result = stock_agent.run_sync(query)
        response = f" Stock: {result.data.symbol}\n"
        response += f" Price: ${result.data.price:.2f} {result.data.currency}\n"
        response += f"\n{result.data.message}"
        return response
    except Exception as e:
        return f"Error: {str(e)}"

# Interface Gradio para interagir com o agente
demo = gr.Interface(
    fn=get_stock_info,
    inputs=gr.Textbox(label="Ask about any stock price", placeholder="What is Apple's current stock price?"),
    outputs=gr.Textbox(label="Stock Information"),
    title="Stock Price AI Assistant",
    description="Ask me about any stock price and I'll fetch the latest information for you!"
)

if __name__ == "__main__":
    demo.launch()
