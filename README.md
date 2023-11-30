# pyxml2sftp
Realiza o upload de arquivos XML de um compartilhamento de pastas baseado em servidor Windows para um SFTP remoto.

Utilizado subir arquivos XML de um compartilhamento de arquivos Windows para o Servidor SFTP do Protheus no Cloud, para processamento da rotina de importação de XML, dessa forma o usuário não precisa entrar na pasta protheus_data/ para subir os arquivos, evitando problemas e compartilhamento de credenciais.

Testado com Python 3.12.0

1. Instale as dependências presentes no arquivo requirements.txt 
2. Crie um arquivo .env com base no .env.example e preencha com as credenciais
3. Execute o arquivo server.py
