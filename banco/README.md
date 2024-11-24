# Criando o Banco:

## Rodar o Script SQL:
1 - Copie o arquivo create_tables.sql para dentro do container:

```bash
docker cp create_tables.sql sistema_alunos_db:/create_tables.sql
```
2 - Acesse o container do PostgreSQL:

```bash
docker exec -it sistema_alunos_db psql -U admin -d sistema_alunos
```
Dentro do terminal do PostgreSQL, rode o script:

```sql
\i /create_tables.sql
```