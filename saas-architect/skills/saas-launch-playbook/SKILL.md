---
name: saas-launch-playbook
description: >
  PROACTIVELY activate when the user is working on any SaaS-related task:
  (1) Defining ICP, positioning, or value proposition,
  (2) Designing pricing models or subscription billing,
  (3) Building onboarding flows, signup, trial, or freemium logic,
  (4) Implementing payment integration (Stripe, billing, webhooks),
  (5) Creating landing pages, email sequences, or lead capture,
  (6) Setting up analytics, tracking events, or SaaS dashboards,
  (7) Implementing feature flags, usage limits, or upgrade triggers,
  (8) Building health scores, churn prediction, or retention systems,
  (9) Designing API pricing, rate limiting, or usage-based billing,
  (10) SEO, AEO, content strategy, or marketing automation,
  (11) Discussing growth strategy, PLG, funnels, ABM, or community,
  (12) Any conversation involving MRR, ARR, churn, NRR, LTV, CAC, or SaaS metrics.
  Also activate when the user mentions "SaaS", "assinatura", "recorrência", "plano", "trial", "freemium", "onboarding", "churn", or "upgrade".
version: 1.0.0
---

# SaaS Architect — Playbook Completo para Construção de SaaS

Guia de referência para Claude ao auxiliar na construção de qualquer produto SaaS — da ideia ao scale. Todo o conhecimento abaixo deve ser aplicado contextualmente, priorizando o que é relevante para o estágio e tipo de SaaS do usuário.

---

## FUNDAMENTOS: O que resolver ANTES de escrever código

### ICP (Ideal Customer Profile)

Sem ICP definido, todo código de marketing, onboarding e pricing é desperdício. O ICP responde:

- **Quem é?** Cargo, tamanho da empresa (B2B), faixa etária/renda (B2C)
- **Qual a dor principal?** Específica e mensurável (ex: "perco 3h/semana em planilhas")
- **Onde busca soluções?** Google, YouTube, LinkedIn, Reddit, comunidades?
- **Quanto pode/quer pagar?** Define se o modelo é freemium, low-ticket ou enterprise

Valide com 10-20 entrevistas antes de automatizar qualquer aquisição.

### Proposta de Valor (1 frase)

Fórmula: **"[SeuApp] ajuda [quem] a [fazer o quê] sem [dor principal]."**

Exemplos:
- "O FinControl ajuda freelancers a organizar finanças sem planilhas complexas."
- "O DevPipeline ajuda times de dev a automatizar deploys sem DevOps dedicado."

### Pricing Strategy

| Modelo | Quando usar | Exemplos |
|--------|-------------|----------|
| **Freemium** | Produto simples, mercado grande, efeito de rede | Slack, Notion |
| **Free Trial (7-14 dias)** | Valor rápido de perceber | HubSpot, Semrush |
| **Trial + Cartão** | Qualifica leads sérios, reduz churn de trial | Netflix, Shopify |
| **Demo-led (Enterprise)** | Ticket alto, decisão complexa | Salesforce, Workday |
| **Usage-based** | Valor cresce com uso | AWS, Twilio, Stripe |

Regras de ouro:
- Comece com 2-3 planos no máximo.
- Preço baixo para entrar, valor alto para expandir.
- O dinheiro real de SaaS vem de **expansão**, não de aquisição.
- Teste preços agressivamente nos primeiros meses.

---

## PRODUCT-LED GROWTH (PLG)

O produto é o motor de aquisição, conversão e expansão. Fluxo:

```
Descobre → Testa grátis → Percebe valor → Converte sozinho → Convida outros
```

### Onboarding (o ponto mais crítico)

- **Wizard guiado** que leva ao "momento aha" em < 5 minutos.
- Personalize por caso de uso ("Sou freelancer" vs "Sou gestor de time").
- Checklists de progresso + celebrações visuais ao completar etapas.
- Se parou no meio → email em 24h com vídeo de 60s do próximo passo.
- **"Momento aha"** = quando o usuário entende o valor real. Ex: primeiro relatório automático, primeiro deal rastreado. Identifique e otimize toda a jornada até ele.

### Loops Virais

- **Convites:** "Adicione seu sócio/contador" (acesso grátis ao convidado)
- **Compartilhamento:** Relatórios com marca d'água "Gerado por [SeuApp]"
- **Integrações:** Zapier, Google Sheets, Slack — conecte com o que o cliente já usa
- **Referral:** Recompense quem traz novos usuários

### Gatilhos de Upgrade

- 80% do limite do plano free → popup suave com benefícios do pago
- Tentou usar feature premium → modal + trial de 7 dias da feature
- 30 dias de uso ativo → email com desconto no plano anual
- Novo membro adicionado ao time → sugestão de plano team/enterprise

---

## FUNIL DE VENDAS AUTOMATIZADO

```
TOFU (Topo)     → Atrair atenção e gerar leads
MOFU (Meio)     → Nutrir, educar e qualificar
BOFU (Fundo)    → Converter em trial/cliente
PÓS-VENDA       → Reter, expandir, transformar em promotor
```

### TOFU — Atrair
- Landing pages otimizadas com formulários de captura
- Lead magnets: ebooks, templates, calculadoras, checklists
- Chatbot na homepage (qualifica em 3 perguntas)
- Blog SEO + CTAs para captura de email
- Webinars automatizados (gravados, rodando sob demanda)

### MOFU — Nutrir
- Sequência de email drip (5-7 emails em 2-3 semanas)
- Segmentação por comportamento (abriu email? clicou? visitou pricing?)
- Lead scoring automático (pontuação sobe com engajamento)
- Retargeting ads para quem visitou o site mas não converteu

### BOFU — Converter
- Free trial com setup < 2 minutos
- Demo automatizada (vídeo + tour guiado no produto)
- Social proof: depoimentos, logos, números de impacto
- Urgência: "últimos 3 dias do trial" + email automático

### PÓS-VENDA — Expandir
- Onboarding automatizado (emails + in-app guides)
- Health score baseado em uso do produto
- Alertas de churn risk para CS
- Upsell quando atinge limites de uso
- NPS automático a cada 90 dias

---

## EMAIL MARKETING — Sequências Essenciais

### Welcome (pós-signup)
```
Email 1 (imediato): Boas-vindas + primeiro passo claro
Email 2 (dia 2):    Dica de feature principal + tutorial
Email 3 (dia 4):    Caso de sucesso de cliente similar
Email 4 (dia 7):    "Você sabia que pode [feature avançada]?"
Email 5 (dia 10):   Oferta de upgrade ou extensão de trial
Email 6 (dia 13):   Último dia! FOMO + benefícios do pago
Email 7 (dia 14):   Trial expirou — oferta especial de reativação
```

### Nutrição (lead que baixou material, não fez trial)
```
Email 1 (imediato): Entrega do material + apresentação
Email 2 (dia 3):    Artigo educativo sobre a dor do lead
Email 3 (dia 6):    "Antes vs Depois de usar [SeuApp]"
Email 4 (dia 9):    Convite para webinar ou demo
Email 5 (dia 12):   Depoimento + CTA para trial
```

### Reativação (usuário inativo)
```
Email 1 (7 dias sem login):  "Sentimos sua falta — novidades"
Email 2 (14 dias):           "Precisa de ajuda? Agende 15 min"
Email 3 (21 dias):           "Último aviso: workspace arquivado em 7 dias"
```

### Gatilhos Comportamentais
| Gatilho | Ação |
|---------|------|
| Visitou pricing | Email comparativo + case de ROI |
| Conta criada sem setup | Email com vídeo de 60s do setup |
| Usou feature X pela primeira vez | "Dica avançada para tirar mais de X" |
| Não logou em 7 dias | Push + email de reengajamento |
| Atingiu limite do free | Email + in-app: benefícios do upgrade |
| Convidou membro do time | "Times que usam juntos economizam X%" |

Emails com gatilho comportamental convertem **3-5x mais** que campanhas genéricas.

---

## SEO + CONTENT MARKETING + AEO

### SEO por estágio do funil
- **TOFU:** "O que é [categoria]?", "X dicas para [resolver problema]"
- **MOFU:** "[SeuApp] vs [Concorrente]", "X ferramentas comparadas"
- **BOFU:** Case studies, reviews, "Como migrar de [concorrente] para [SeuApp]"

### AEO (Answer Engine Optimization) — Otimização para IAs
- Página "O que é [SeuApp]" com schema markup
- Conteúdo em formato pergunta-resposta
- Presença em listas "melhores ferramentas de [categoria]"
- Reviews em G2, Capterra, Product Hunt
- Documentação/API bem organizada

### Distribuição (1 conteúdo → 5+ formatos)
- Blog → LinkedIn (carrosseis/insights)
- Blog → YouTube (vídeos com exemplos)
- Webinars → Clips (Reels/Shorts)
- Case Studies → Copy de anúncios

---

## RETENÇÃO E EXPANSÃO

### Health Score Automatizado
| Sinal | Peso | Significado |
|-------|------|-------------|
| Logins por semana | Alto | Engajamento |
| Features utilizadas | Alto | Profundidade de uso |
| Tickets de suporte | Médio | Engajamento ou frustração |
| Usuários convidados | Alto | Stickiness |
| NPS score | Alto | Satisfação |
| Dias desde último login | Alto | Risco de churn |

### Automações por saúde do cliente
**Health score alto:**
- Relatório trimestral de valor gerado
- Convite para referral
- Early access a features novas
- Convite para case study

**Health score baixo:**
- Email: "Notamos que você não usou [feature]. Precisa de ajuda?"
- Alerta para CSM fazer outreach
- Sessão de onboarding 1:1 gratuita
- Desconto temporário se aplicável

**Expansão:**
- 80% do limite → notificação + email de upgrade
- Novo membro adicionado → sugestão de plano team
- Milestone de uso → apresentar plano Pro
- Cross-sell: "Quem usa [A] também adora [B]"

### Benchmarks de Retenção
| Métrica | Bom | Ótimo | Elite |
|---------|-----|-------|-------|
| GRR | >80% | >85% | >90% |
| NRR | >100% | >110% | >120% |
| Churn mensal | <5% | <3% | <1% |
| NPS | >30 | >50 | >70 |

Empresas SaaS top geram **40-60% da receita nova** a partir de expansão da base existente.

---

## MÉTRICAS ESSENCIAIS

### Aquisição
- **CAC** = (Gasto marketing + vendas) / Novos clientes
- **LTV** = ARPU × (1 / Churn Rate)
- **LTV:CAC** > 3:1 (abaixo = queimando dinheiro)
- **CAC Payback** < 12 meses (ideal)

### Produto
- **Activation Rate** = % que chega ao "momento aha"
- **DAU/MAU** > 20% (bom para SaaS)
- **Feature Adoption** = quais features são usadas vs ignoradas
- **Time to Value** = tempo do signup ao primeiro valor

### Receita
- **MRR** e seus componentes (New, Expansion, Contraction, Churned)
- **ARR** = MRR × 12
- **NRR** > 110% (meta)
- **Quick Ratio** = (New + Expansion) / (Churned + Contraction) — ideal > 4

### Saúde Financeira
- **Gross Margin** > 80% (padrão SaaS)
- **Rule of 40** = Growth Rate + Profit Margin > 40%
- **Burn Rate / Runway** > 12 meses

---

## PAID MEDIA — Hierarquia de Canais

1. **Google Ads (Search)** — captura demanda existente. Keywords de alta intenção.
2. **LinkedIn Ads** — melhor para B2B. Custo alto, qualidade superior.
3. **Meta Ads** — melhor para B2C e awareness B2B. Lookalike audiences.
4. **YouTube Ads** — subestimado. Vídeos "antes/depois" em 30-60s.

Retargeting em 5 etapas:
```
Visitou site → Ad de awareness
Visitou pricing → Ad com case study + trial
Iniciou trial sem ativar → Ad de ativação
Trial expirou → Ad com desconto 20%
Cliente ativo → Ad de feature premium
```

**Retargeting tem o melhor ROI em paid media para SaaS.** Priorize antes de escalar aquisição fria.

---

## ABM (Account-Based Marketing) — Para B2B ticket > R$5k

| Tier | Contas | Abordagem |
|------|--------|-----------|
| **Tier 1** | 10-20 | Pesquisa profunda, conteúdo 100% personalizado, multichannel |
| **Tier 2** | 50-200 | Agrupadas por indústria, conteúdo semi-personalizado |
| **Tier 3** | 200+ | Automação com personalização por indústria/cargo |

ABM retorna mais que qualquer outra abordagem para B2B SaaS de ticket médio-alto.

---

## STACK DE FERRAMENTAS

### Para começar (orçamento limitado)
| Função | Ferramenta | Custo |
|--------|-----------|-------|
| CRM + Email | HubSpot Free | Grátis |
| Pagamentos | Stripe | Pay-as-you-go |
| Analytics | PostHog | Grátis até 1M eventos |
| Landing pages | Carrd ou Framer | ~$20/mês |
| Suporte | Crisp | Grátis (2 operadores) |
| Blog/SEO | WordPress ou Ghost | ~$10-25/mês |
| Automação | n8n (self-hosted) | Grátis |
| Métricas SaaS | Baremetrics | ~$50/mês |

### Para builder/indie hacker
| Função | Stack DIY |
|--------|-----------|
| Backend + API | FastAPI (Python) ou Next.js |
| Pagamentos | Stripe + webhooks customizados |
| Email | Resend ou AWS SES |
| Analytics | PostHog self-hosted ou Umami |
| Automação | n8n self-hosted + crons |
| Landing page | HTML/Tailwind ou Framer |

---

## CRONOGRAMA DE IMPLEMENTAÇÃO

### Fase 1 — Pré-lançamento (4-8 semanas)
- Definir ICP e proposta de valor
- Landing page com waitlist
- Email marketing (sequência de waitlist)
- 5-10 artigos SEO-first
- Analytics (PostHog/Mixpanel)
- Stripe + billing
- Onboarding (5-7 emails)
- Beta com 10-20 early adopters

### Fase 2 — Lançamento (semanas 1-4)
- Product Hunt + Hacker News
- Welcome emails ativos
- Google Ads (brand + high intent)
- 2-3 conteúdos/semana
- Feedback obsessivo dos primeiros usuários
- Reviews no G2/Capterra

### Fase 3 — Crescimento (meses 2-6)
- Escalar SEO (2-4 artigos/semana)
- Retargeting ads
- Lead scoring + nurturing
- Programa de referral
- Reativação de inativos
- Health score
- Primeiro webinar
- A/B testing de pricing

### Fase 4 — Escala (meses 6-12)
- Otimizar NRR com automações de expansão
- Diversificar canais (YouTube, LinkedIn, partnerships)
- Agentes de IA para campanhas
- Comunidade ativa
- CS automatizado ou primeiro CSM
- Internacionalização
- Refinar ICP com dados reais

---

## ERROS FATAIS

1. **Escalar antes de ter PMF** — Valide com 50-100 pagantes e churn < 5% primeiro.
2. **Métricas de vaidade** — Pageviews e seguidores não pagam boleto. Foque em MRR, NRR, LTV:CAC.
3. **Over-automate sem toque humano** — Primeiro faça na mão, entenda o que funciona, depois automatize.
4. **Pricing errado** — Barato demais atrai quem não valoriza. Caro demais sem valor demonstrado afasta.
5. **Ignorar churn** — Balde furado não enche. Retenção antes de aquisição.
6. **Copiar empresa grande** — Adapte ao seu estágio e recursos.
7. **Não medir o funil** — Se não sabe onde trava, está jogando dinheiro no escuro.
8. **Features em vez de dor** — O mercado paga por resultados, não por features.
