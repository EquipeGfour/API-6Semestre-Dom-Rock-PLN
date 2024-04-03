import pandas as pd
from text_processing import process_text

# Lê a planilha Excel
df = pd.read_excel('entrada.xlsx')

# Escolha a coluna que deseja processar
column_name = 'nome_da_coluna'

# Aplica a função process_text à coluna selecionada
df[column_name] = df[column_name].apply(process_text)

# Salva a planilha processada
df.to_excel('saida.xlsx', index=False)
