# INF0236-PrecatoryWeb
Uma aplicação web para precatórios judiciais usando Django para a classe UFG INF INF0236: Framework de Desenvolvimento Web para Consumo De Modelos Treinados de Inteligência Artficial.

## Funcionalidades

- CRUD (com exportação/importação de dados no formato .csv) de Ente Devedor, Unidade Jurisdicional, Validação, Autuação e Baixa. 
- Criação e Validação de Modelo de Validação, Autuação e Baixa. 
- Predição de Data da Baixa.

## Tecnologias

 - Python 3, uma linguagem de programação de alto nível e de propósito geral,
 - Django, um framework web para construção de páginas web;
 - Pandas, uma ferramenta de análise e manipulação de dados;
 - Sklearn, uma ferramenta para aprendizado de máquina construído sobre a biblioteca SciPy;
 - Ploty, uma ferramenta para visualização de dados interativa.

## Configuração do ambiente de desenvolvimento

1. Instale o python, na versão 3.10, através do [link](https://www.python.org/downloads/);
2. Clone este repositório https://github.com/anunciado/INF0236-PrecatoryWeb em sua máquina local;
3. Abra o projeto em sua IDE de preferência, como sugestão utilize o Visual Studio Code ou PyCharm;
4. Crie um ambiente virtual com o comando:
```
. python -m venv venv
```
5. Ative o ambiente virtual com o comando:
* No windows:
```
venv\Scripts\activate
```
* No linux:
```
source venv/bin/activate
```
6. Instale as bibliotecas no seu ambiente virtual a partir do arquivo _requirements.txt_ com o comando:
```
pip install -r requirements.txt
```
7. Execute o projeto com o comando:
```
python manage.py runserver
```

## Contribuição:

1. `Mova` a issue a ser resolvida para a coluna _In Progress_ no [board do projeto].  
2. `Clone` este repositório https://github.com/anunciado/INF0236-PrecatoryWeb.git.
3. `Crie` um branch a partir da branch _dev_.
4. `Commit` suas alterações.
5. `Realize` o push das alterações.
6. `Crie` a solicitação PR para branch _dev_.
7. `Mova` a _issue_ da coluna _In Progress_ para a coluna _Code Review_ do [board do projeto].

## Desenvolvedores

- [Luís Eduardo](https://github.com/anunciado)