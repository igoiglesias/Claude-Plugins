# 🌐 Browser DevTools — Claude Code Plugin

> Dá ao Claude Code a capacidade de **abrir páginas no navegador**, tirar screenshots, inspecionar HTML/DOM, verificar erros no console e na rede, rodar Lighthouse, executar JavaScript, testar acessibilidade — tudo via linguagem natural.

## O que tem dentro

| Componente | O que faz |
|---|---|
| **MCP Server** (`server.py`) | 20 ferramentas de automação de browser via Selenium + Chrome DevTools Protocol |
| **Skill** (`skills/browser-devtools/`) | Auto-invocado pelo Claude quando detecta tarefas de browser |
| **Commands** | `/browser-devtools:audit`, `/browser-devtools:screenshot`, `/browser-devtools:debug` |
| **Agent** (`agents/browser-qa.md`) | Agente QA especializado em testes de browser |
| **Hooks** | `SessionStart` — instala dependências automaticamente no primeiro uso |

## Pré-requisitos

- **Python 3.10+**
- **Google Chrome** ou **Chromium**
- **Node.js + Lighthouse** (opcional, para auditorias de performance)

## Instalação

### Via Git (recomendado)

```bash
# Clonar o plugin
git clone https://github.com/seu-usuario/browser-devtools.git

# Instalar no Claude Code (escolha um scope)
claude plugin install ./browser-devtools          # projeto local
claude plugin install ./browser-devtools --user   # global para você
```

### Via diretório local

```bash
# Testar sem instalar
claude --plugin-dir ./browser-devtools
```

### Verificar

Dentro do Claude Code:
```
/plugin        → deve listar browser-devtools
/mcp           → deve mostrar browser-devtools: connected
```

## Dependências

O plugin instala automaticamente um venv Python com apenas **2 dependências externas**:

| Pacote | Motivo |
|---|---|
| `mcp[cli]` | SDK do MCP Protocol (FastMCP) |
| `selenium` | Controle do Chrome/Chromium |

**Todo o resto é Python stdlib:** `json`, `base64`, `os`, `subprocess`, `tempfile`, `time`, `pathlib`, `hashlib`, `urllib.parse`, `logging`.

O Lighthouse é chamado via `subprocess` (CLI do Node.js), sem binding Python.

## 20 Ferramentas MCP

### Ciclo de Vida
- `browser_open` — Abre URL (headless, viewport custom, emulação de 8 dispositivos móveis)
- `browser_close` — Fecha e libera recursos

### Captura
- `take_screenshot` — Screenshot (full page, viewport, elemento CSS)
- `take_pdf` — Salva página como PDF
- `get_page_html` — HTML da página ou elemento

### Inspeção
- `get_page_info` — Meta tags, headings, counts, performance timing, cookies
- `find_elements` — Query DOM com CSS selector + extrai atributos
- `get_computed_styles` — Estilos CSS computados de um elemento
- `get_console_logs` — Logs do console (filtro por nível)
- `get_network_logs` — Logs de rede (erros, falhas, requests, responses)

### Auditoria
- `run_lighthouse` — Google Lighthouse (performance, a11y, SEO, best practices)
- `check_accessibility` — Verificação rápida de acessibilidade (JS puro, sem deps extras)

### Interação
- `click_element` — Clica em elemento
- `fill_input` — Preenche campo de texto
- `select_option` — Seleciona opção em dropdown
- `navigate` — Voltar, avançar, recarregar
- `scroll_page` — Rolar (up, down, top, bottom)
- `wait_for_element` — Aguardar elemento (visible, clickable, present, gone)

### Outros
- `run_javascript` — Executa JS arbitrário no contexto da página
- `manage_cookies` — CRUD de cookies

## Exemplos de Uso

Depois de instalar, basta conversar com o Claude Code:

```
"Abre meu site em localhost:3000 e verifica se tem erros no console"

"Tira um screenshot do site em modo mobile (iPhone 14)"

"Roda Lighthouse no https://meusite.com e me dá os scores"

"Verifica a acessibilidade da página e lista os problemas"

"Abre a página, clica no botão de login, preenche email e senha"

/browser-devtools:audit https://meusite.com

/browser-devtools:debug http://localhost:8000

/browser-devtools:screenshot https://meusite.com
```

## Arquitetura

```
Claude Code
    │
    ├── SessionStart hook → scripts/setup.sh
    │   └── Cria venv em ~/.claude/plugins/data/browser-devtools/
    │       └── pip install selenium mcp
    │
    ├── MCP Server (server.py via stdio)
    │   ├── Selenium WebDriver → Chrome headless
    │   ├── Chrome DevTools Protocol → console + network logs
    │   └── subprocess → Lighthouse CLI
    │
    ├── Skill (auto-invoked on browser tasks)
    ├── Commands (/audit, /screenshot, /debug)
    └── Agent (browser-qa specialist)
```

## Estrutura do Plugin

```
browser-devtools/
├── .claude-plugin/
│   └── plugin.json          # Manifesto do plugin (obrigatório)
├── .mcp.json                # Config do MCP server
├── server.py                # Servidor MCP (Selenium + FastMCP)
├── requirements.txt         # Deps Python (apenas 2: mcp, selenium)
├── hooks/
│   └── hooks.json           # SessionStart → auto-install
├── scripts/
│   └── setup.sh             # Setup automático do venv
├── skills/
│   └── browser-devtools/
│       └── SKILL.md         # Skill auto-invocada
├── commands/
│   ├── audit.md             # /browser-devtools:audit
│   ├── screenshot.md        # /browser-devtools:screenshot
│   └── debug.md             # /browser-devtools:debug
├── agents/
│   └── browser-qa.md        # Agente QA especializado
└── README.md
```

## Dispositivos Suportados

| Device | Viewport | DPR |
|---|---|---|
| `iphone_se` | 375×667 | 2.0x |
| `iphone_12` | 390×844 | 3.0x |
| `iphone_14` | 393×852 | 3.0x |
| `iphone_15_pro` | 393×852 | 3.0x |
| `pixel_7` | 412×915 | 2.625x |
| `galaxy_s23` | 360×780 | 3.0x |
| `ipad` | 810×1080 | 2.0x |
| `ipad_pro` | 1024×1366 | 2.0x |

## Troubleshooting

**Chrome não encontrado:**
```bash
# Ubuntu/Debian
sudo apt install -y chromium-browser
# macOS
brew install --cask google-chrome
```

**Lighthouse não funciona:**
```bash
npm install -g lighthouse
lighthouse --version
```

**Plugin não conecta:**
```
/mcp                    # ver status
/plugin                 # ver se está habilitado
```

## Licença

MIT
