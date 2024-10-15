# Documentação

## Se a base de dados não existir, cria e base:

1. Verifique de o PostgrSql está instalado e rodando. Se não extiver instale.
2. Abra um cliente SQL (por exemplo o DBeaver).
3. Crie a base com o mais recente script com o nome do tipo dump-optview-AAAAMMDDHHMM

## Se a base existir atualize com o último script não registrado na tabela versions:

1. Verifique de o PostgrSql esstá sendo executado. Se não extiver suba o serviço.
2. Abra um cliente SQL (por exemplo o DBeaver).
3. Execute

```
SELECT * FROM versions ORDER BY 
```

4. Observe o resulado e olhe último executado e execute em ordem os outros scripts  do tipo migrate-optview-AAAAMMDDHHMMsql.

## Configure ao sistema

1. Crie o arquivo site/app/our_secrets.py baseado no modelo do site/app/our_secrets_model.py.
2. Prrencha as chaves necessárias:
   a. SECRET_SESSION_KEY é a chave para cifrar os cookies locais e manter a sessão, 
      se ela for mudada todos os usuários vão ter de fazer login novamente.
3. São necessários alguns ajsutes no site/app/config.py:
   * EMAIL_SITE_URL deve ter o domínio do site para os e-mails enviados terem o link certo.
   * EMAIL_ADDRESS_FROM deve ter o endereço de onde os e-mails são enviados.

## Para executar o projeto, siga os passos abaixo:

1. Crie um ambiente virtual:
   ```
   python -m venv venv
   ```

2. Ative o ambiente virtual:
   ```
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Exporte a variável de ambiente FLASK_APP:
   ```
   export FLASK_APP=optview.py
   ```

5. Entre no diretório site/app:
   ```
   cd site/app
   ```

6. Execute o Flask:
   ```
   flask run
   ```

Agora o projeto deve estar em execução e acessível através do navegador.