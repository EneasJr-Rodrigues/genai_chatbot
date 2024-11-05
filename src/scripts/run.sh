echo "Setando variáveis de ambiente..."
source ../config/.env

echo "Rodando a aplicação no localhost..."
streamlit run ../main.py \
  --browser.serverAddress=localhost \
  --server.enableCORS=false \
  --server.enableXsrfProtection=false \
  --server.port 8081

## bash run-localhost.sh local