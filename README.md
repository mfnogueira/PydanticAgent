# Stock Price AI Assistant

Este projeto demonstra como utilizar a biblioteca **Pydantic AI** para criar agentes personalizados que processam consultas utilizando modelos de linguagem. O exemplo abrange dois casos de uso:
1. **Script básico (`main.py`)** para consultas diretas.
2. **Interface interativa (`ui.py`)** com **Gradio**.

## 📚 Descrição

O **Stock Price AI Assistant** utiliza a biblioteca **Pydantic AI** para configurar um agente que busca preços de ações em tempo real com o suporte da biblioteca `yfinance`. 

## 🔧 Requisitos

- Python 3.8 ou superior
- Dependências listadas no arquivo `requirements.txt`

## 🛠️ Instalação

1. Clone este repositório:
    ```bash
    git clone https://github.com/seu_usuario/stock-price-ai-assistant.git
    cd stock-price-ai-assistant
    ```

2. Crie um ambiente virtual e ative-o:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/MacOS
    .venv\Scripts\activate     # Windows
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Crie um arquivo `.env` na raiz do projeto e adicione sua chave de API da Groq:
    ```
    GROQ_API_KEY=sua_chave_de_api_aqui
    ```

## 🖥️ Funcionalidades

### 1. Script Principal (`main.py`)

O arquivo `main.py` é um exemplo direto e básico de como configurar e executar um agente de IA com **Pydantic AI**. 

#### Exemplo de Execução
No terminal, execute:
```bash
python main.py
```

### Fluxo de Funcionamento
1. O agente é configurado para buscar preços de ações.
2. As consultas são realizadas diretamente no código (não interativo).
3. As respostas incluem o preço da ação e mensagens adicionais.

## 🖥️ Funcionamento

O agente utiliza a biblioteca **Pydantic AI** para integrar um modelo de linguagem que responde a perguntas sobre preços de ações. A funcionalidade principal é configurada da seguinte forma:

### Modelo de Dados

O agente retorna informações formatadas usando um modelo baseado em **Pydantic**:

```python
class StockPriceResult(BaseModel):
    symbol: str  # Símbolo da ação (ex.: "AAPL")
    price: float  # Preço atual da ação
    currency: str = "USD"  # Moeda padrão: USD
    message: str  # Mensagem adicional gerada pelo agente
```

## Ferramenta Personalizada

Uma ferramenta foi registrada no agente para buscar dados de ações usando `yfinance`:

```python
@stock_agent.tool_plain
def get_stock_price(symbol: str) -> dict:
    ticker = yf.Ticker(symbol)
    price = ticker.fast_info.last_price
    return {
        "price": round(price, 2),
        "currency": "USD"
    }
```

## Integração com Gradio

O Gradio cria uma interface amigável para interagir com o agente:
```python
demo = gr.Interface(
    fn=get_stock_info,
    inputs=gr.Textbox(label="Ask about any stock price", placeholder="What is Apple's current stock price?"),
    outputs=gr.Textbox(label="Stock Information"),
    title="Stock Price AI Assistant",
    description="Ask me about any stock price and I'll fetch the latest information for you!"
)
```
## 🧪 Exemplos

### Pergunta
```bash
    Qual é o preço atual das ações da Apple?
```
## Resposta

```bash
Stock: AAPL
Price: $123.45 USD
Message: The stock price data was fetched successfully.
```

## 📂 Estrutura do Projeto

```bash
├── main.py
├── ui.py               
├── requirements.txt    
├── .env               
├── README.md           


## ⚙️ Tecnologias Utilizadas
-  Pydantic AI
- Gradio
- YFinance
- Python 3.12