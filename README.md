# Fazenda

Projeto Django modular para gerenciar recursos e funcionalidades do site "Fazenda".

**Sumário**

- **Sobre:** descrição do projeto
- **Requisitos:** dependências e versões
- **Instalação rápida:** comandos para rodar localmente
- **Configuração:** arquivo de variáveis e exemplos
- **Execução:** migrações, criação de superusuário e servidor


## Sobre

Aplicação Django organizada por apps (por exemplo: `financas`, `agenda_tributaria`).

## Requisitos

- Python 3.10+ (ou 3.8+ compatível)
- pip   
- virtualenv ou venv (recomendado)
- MySQL em produção

As dependências do projeto estão listadas em [requirements.txt](requirements.txt).

## Instalação rápida (Windows)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Configuração (.envvars.yaml)

O projeto carrega variáveis a partir de um arquivo YAML chamado `.envvars.yaml`. A leitura é feita por [settings/envvars.py](settings/envvars.py).


## Banco de dados

- `sqlite_mode: true` → banco SQLite local criado em `settings/` (arquivo .db).
- `sqlite_mode: false` → configurações MySQL usando `db_name`, `db_user`, `db_pw`, `db_host`, `db_port`.


## Executando localmente

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Coletar arquivos estáticos (pré-deploy):

```powershell
python manage.py collectstatic --noinput
```


## Observações e dicas rápidas

- A configuração de envio de e-mail e chaves externas é controlada por `.envvars.yaml`.
- O projeto usa `channels` + `channels_redis` para funcionalidades em tempo real; instale e execute Redis se precisar desse recurso.
- Verifique [settings/settings.py](settings/settings.py) para valores sensíveis e comportamento (e.g., `DEBUG`, `STATIC_ROOT`, `MEDIA_ROOT`).
