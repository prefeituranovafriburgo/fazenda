# Fazenda

Um projeto Django modular para gerenciar recursos e funcionalidades do sistema "Fazenda".

**Sumário**

- **Sobre:** visão geral do projeto
- **Principais apps:** lista dos apps incluídos
- **Pré-requisitos:** ferramentas necessárias
- **Instalação rápida:** passos para rodar localmente
- **Configuração:** como preparar variáveis de ambiente
- **Execução:** comandos úteis
- **Observações:** dicas para desenvolvimento

## Sobre

Este repositório contém uma aplicação Django organizada em apps (por exemplo `administracao`, `financas`, `agenda_tributaria`, `ferramentas_site`, etc.). O layout é pensado para facilitar desenvolvimento modular e deploy em ambientes com MySQL/Redis (opcional) ou modo rápido com SQLite.

> Nota: alguns apps (como `administracao` e `guardiao`) existem no código, mas podem estar comentados em `INSTALLED_APPS` por padrão.

## Principais apps

- `administracao` — interface administrativa específica do projeto
- `financas` — funcionalidades relacionadas a finanças e notícias
- `agenda_tributaria` — agenda e eventos tributários
- `ferramentas_site` — utilitários públicos do site
- `guardiao` — app presente, mas geralmente desativado por padrão

## Pré-requisitos

- Python 3.10+ (ou 3.8+ compatível)
- pip
- Virtualenv (recomendado)
- Redis (apenas se for utilizar `channels`/WebSockets)
- MySQL client se usar banco MySQL (opcional — SQLite disponível para testes rápidos)

## Instalação rápida (Windows - PowerShell)

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

## Configuração de variáveis de ambiente

O projeto carrega variáveis a partir de um arquivo YAML na raiz chamado `.envvars.yaml`. Crie esse arquivo com os valores necessários. Exemplo mínimo:

```yaml
db_name: 'fazenda_db'
db_user: 'user'
db_host: 'localhost'
db_port: 3306
db_pw: 'senha'
django_secret_key: 'troque-por-uma-chave-secreta'
debug_mode: true
email_sistema: 'seu-email@example.com'
email_pw: 'senha-email'
sqlite_mode: true
hCAPTCHA_Public_Key: ''
hCAPTCHA_Secret_Key: ''
GOOGLE_OAUTH2_PUBLIC_KEY: ''
GOOGLE_OAUTH2_SECRET_KEY: ''
FACEBOOK_DEVELOPER_PUBLIC_KEY: ''
FACEBOOK_DEVELOPER_SECRET_KEY: ''
el_api_token: ''
el_id_client: ''
```

- Defina `sqlite_mode: true` para um modo rápido com banco SQLite local.
- Se for usar MySQL, ajuste `sqlite_mode: false` e preencha `db_*` com as credenciais.

## Rodando localmente

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Para coletar arquivos estáticos antes de deploy:

```powershell
python manage.py collectstatic --noinput
```

## Redis / Channels

Se você pretende usar funcionalidades em tempo real (`channels`), instale e execute o Redis localmente (padrão em `127.0.0.1:6379`) ou configure conforme necessário em `settings/settings.py`.

## Ativar apps opcionais

Os apps `administracao` e `guardiao` podem estar comentados em `settings/INSTALLED_APPS`. Para ativá-los:

1. Abra `settings/settings.py` e remova o comentário das linhas correspondentes em `INSTALLED_APPS`.
2. Em seguida, descomente a rota em `settings/urls.py` (por exemplo `path('administracao/', include('administracao.urls'))`).
3. Rode `python manage.py migrate` caso o app possua migrações pendentes.

## Testes

Se houver testes definidos, rode:

```powershell
python manage.py test
```

## Contribuição

Contribuições são bem-vindas. Abra uma issue descrevendo a sugestão ou bug e depois um pull request com uma descrição clara das mudanças.

## Licença

Defina a licença do projeto conforme sua escolha (por exemplo MIT). Se desejar, posso adicionar um arquivo `LICENSE` padrão.

---

Se quiser que eu personalize o README com informações adicionais (ex.: detalhes de deploy, badges, exemplos de uso de APIs internas, ou capturas de tela), me diga o que prefere que eu inclua.
