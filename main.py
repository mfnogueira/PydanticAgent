from pydantic_ai import Agent
from pydantic import BaseModel
from dotenv import load_dotenv
import yfinance as yf
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Garante que a chave de API está configurada no ambiente
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("A chave de API 'GROQ_API_KEY' não foi encontrada no arquivo .env.")

class StockPriceResult(BaseModel):
    symbol: str
    price: float
    currency: str = "USD"
    message: str

# Criação do agente com a chave de API
stock_agent = Agent(
    model="groq:llama3-8b-8192",
    api_key=api_key,
    result_type=StockPriceResult,
    system_prompt=(
        "You're a helpful financial assistant that can look up stock prices. "
        "Use the get_stock_price tool to fetch current data."
    )
)

@stock_agent.tool_plain
def get_stock_price(symbol: str) -> dict:
    ticker = yf.Ticker(symbol)
    price = ticker.fast_info.last_price
    return {
        "price": round(price, 2),
        "currency": "USD"
    }

result = stock_agent.run_sync("What is Apple's current stock price?")
print(f"Stock Price: ${result.data.price:.2f} {result.data.currency}")
print(f"Message: {result.data.message}")
