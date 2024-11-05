from vertexai.generative_models import GenerativeModel, GenerationConfig
from vertexai import generative_models
import vertexai
from datetime import datetime
from utils import get_environments

# pegar as variaveis do ambiente
config = get_environments()

# logar na plataforma
config.get('google_credentials_path')


## construtor do vertex search API
vertexai.init(project=config.get('project_id'), location=config.get('location'))

## criando o modelo
model = GenerativeModel(config.get('model_name'))

## classe responsavel por gerar interação com o GenIA
def generate(
        pergunta: str,
        df,
        max_output_tokens: int = 8192,
        temperature: int = 0.4,
        top_p: float = 0.4,
        stream: bool = False
):
    formatted_table = df.to_markdown(index=False)

    prompt_full =  f"""
            "perguntas do negocio": f"{pergunta}", "DataFrame": {df},
            <Contexto>
                Heineken International é uma cervejaria holandesa, fundada em 1863 por Gerard Adriaan Heineken na cidade de Amsterdã. Heineken possui cerca de 140 cervejarias em mais de 70 países, empregando aproximadamente 85.000 pessoas. Sua missão, como especialista da Heineken, é proporcionar uma análise dos dados fornecidos para um time de gerentes.
            </Contexto>
            <Dados> 
                {formatted_table}
            </Dados>
            <instrucoes>
                TAREFA: Com base nos dados fornecidos, realize uma análise completa e detalhada, respondendo a pergunta do usuário. Sua análise deve incluir:
                    - Leitura dos dados
                    - Caso o período não esteja especificado, utilize os dados dos últimos seis meses disponível.
                    - Apresente um breve contexto.
                    - Crie uma tabela com o evolutivo do volume por período e vendas por período.
                    - Apresente a variação em porcentagem.
                    - Identificação da tendência (crescente ou decrescente) entre os meses.
                    - Adição de sinais de "+" ou "-" para indicar variações.
                    - Os números deverão estar formatados de uma maneira que seja fácil de entender para humanos. Por exemplo, você deve transformar grandes números em formatos mais compactos e legíveis, como "10.9B" para bilhões, "5.3M" para milhões, e assim por diante. Forneça a versão formatada de maneira clara e compreensível. 
                    - Apresentação dos dados de maneira amigável, clara e compreensível.
                    - Incluia uma breve analise de tendência.
                    - Formate a resposta em markdown
                    - Antes de gerar a resposta, certifique-se de ter cumprido todas as instruções.
            </instrucoes>
            <Pergunta_do_usuario>{pergunta}</Pergunta_do_usuario>
            """

    prompt=[prompt_full.format(pergunta=pergunta)]
    responses = model.generate_content(
        prompt,
        generation_config={
            "max_output_tokens": max_output_tokens,
            "temperature": temperature,
            "top_p": top_p		
        },
        safety_settings={
          generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
          generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
          generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
          generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        },
        stream=stream
    )

    return responses
