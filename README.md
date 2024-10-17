# Run this command to build application

## Ative o Pipenv
pipenv install
pipenv shell

## Teste a aplicação
pipenv run python main.py

## Gerar o executavel Sem console
pyinstaller -F -n EnvioAutomatio -i Images/icone.ico --noconsole --clean main.py

## Gerar o executavel Com console para debug
pyinstaller -F -n EnvioAutomatico -i Images/icone.ico  --clean main.py
