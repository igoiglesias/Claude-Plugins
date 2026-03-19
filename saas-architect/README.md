# SaaS Architect — Claude Code Plugin

> Assistente completo para construção de SaaS — do ICP ao scale.
> Baseado em práticas reais de Stripe, Slack, HubSpot, Notion, Calendly e Figma.

## O que faz

Transforma o Claude Code num co-fundador técnico que entende tanto a estratégia de negócio quanto a implementação. Cobre todo o ciclo de vida de um SaaS: validação, pricing, onboarding, billing, métricas, retenção e crescimento.

## Instalação

### Via marketplace local

```bash
# Se já tem um marketplace local configurado, copie a pasta para dentro dele
cp -r saas-architect /caminho/do/seu/marketplace/

# Adicione ao marketplace.json:
# { "name": "saas-architect", "source": "./saas-architect", "description": "..." }

# No Claude Code:
/plugin install saas-architect@seu-marketplace
```

### Via --plugin-dir (desenvolvimento)

```bash
claude --plugin-dir /caminho/para/saas-architect
```

## Commands

| Comando | O que faz |
|---------|-----------|
| `/saas-architect:saas-plan` | Plano completo do SaaS — ICP, pricing, MVP, stack, cronograma |
| `/saas-architect:pricing` | Estratégia de pricing — modelo, planos, limites, gatilhos de upgrade |
| `/saas-architect:onboarding` | Fluxo de ativação — wizard, emails, checklist, reengajamento |
| `/saas-architect:billing` | Integração Stripe — checkout, webhooks, portal, feature gates |
| `/saas-architect:metrics` | Dashboard de KPIs — MRR, churn, NRR, health score, alertas |
| `/saas-architect:growth-audit` | Diagnóstico de crescimento — gargalos, score por área, ações |

## Agents

| Agent | Especialidade |
|-------|--------------|
| **saas-strategist** | Consultoria estratégica — PLG, go-to-market, pricing, priorização, unit economics |
| **growth-engineer** | Implementação — billing, onboarding, analytics, email automation, feature gates |

## Skill

O **saas-launch-playbook** ativa automaticamente quando Claude detecta tarefas relacionadas a SaaS. Contém o conhecimento completo sobre:

- ICP, posicionamento e proposta de valor
- Product-Led Growth e loops virais
- Funil automatizado (TOFU → MOFU → BOFU → Pós-venda)
- Sequências de email (welcome, nutrição, reativação)
- SEO + AEO (Answer Engine Optimization)
- Paid media e retargeting
- ABM (Account-Based Marketing)
- Retenção, health score e expansão
- Métricas essenciais e benchmarks
- Stack de ferramentas por orçamento
- Cronograma de implementação em 4 fases
- Erros fatais a evitar

## Exemplos de uso

```
# Planejando um SaaS do zero
/saas-architect:saas-plan App de gestão de projetos para agências, B2B

# Definindo pricing
/saas-architect:pricing modelo freemium, concorrentes: Trello, Asana, Monday

# Implementando Stripe
/saas-architect:billing FastAPI + Stripe, 3 planos, trial 14 dias

# Criando onboarding
/saas-architect:onboarding momento aha: primeiro projeto criado com board kanban

# Instrumentando métricas
/saas-architect:metrics PostHog + FastAPI, health score por cliente

# Auditoria de growth
/saas-architect:growth-audit estágio early, B2B, ticket R$150/mês
```

## License

MIT
