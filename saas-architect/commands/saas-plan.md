---
description: Cria o plano completo de um SaaS do zero — ICP, proposta de valor, pricing, MVP scope, stack técnico e cronograma de lançamento. O ponto de partida para qualquer novo produto.
---

# SaaS Plan — Planeje seu SaaS do zero

## Objetivo
Gerar um documento estratégico completo para um novo SaaS, cobrindo todas as decisões fundamentais antes de escrever código.

## Instruções

1. **Colete informações do usuário (se não fornecidas em $ARGUMENTS):**
   - Qual problema o SaaS resolve?
   - Quem é o público-alvo? (B2B/B2C, perfil, tamanho)
   - Já tem validação? (entrevistas, lista de espera, protótipo)
   - Qual o orçamento e recursos disponíveis? (solo dev, time pequeno, com investimento)
   - Existe concorrência direta? Quais?

2. **Gere o plano com estas seções:**

   **a) ICP (Ideal Customer Profile):**
   - Perfil detalhado do cliente ideal
   - Dor principal (específica e mensurável)
   - Canais onde esse público busca soluções
   - Disposição e capacidade de pagamento

   **b) Proposta de Valor:**
   - Frase única no formato: "[App] ajuda [quem] a [fazer o quê] sem [dor]"
   - 3 diferenciais em relação a concorrentes ou alternativas (incluindo planilhas/manual)
   - "Momento aha" — qual é a primeira experiência de valor no produto

   **c) Modelo de Pricing:**
   - Recomendação entre: Freemium, Free Trial, Trial+Cartão, Demo-led, Usage-based
   - Estrutura de planos (2-3 planos com features e limites)
   - Sugestão de preços baseada no mercado e ICP
   - Estratégia de expansão (como o cliente vai gastar mais com o tempo)

   **d) MVP Scope:**
   - Features obrigatórias para o dia 1 (o mínimo que entrega o "momento aha")
   - Features para v2 (pós-validação com primeiros clientes)
   - Features que NÃO devem estar no MVP (overengineering comum)

   **e) Stack Técnico Recomendado:**
   - Backend, frontend, banco de dados
   - Pagamentos (Stripe, webhooks, billing)
   - Analytics (eventos a rastrear desde o dia 1)
   - Email (transacional + marketing)
   - Infra (deploy, CI/CD, monitoring)
   - Adaptar à stack que o usuário já conhece quando possível

   **f) Cronograma de Lançamento:**
   - Fase 1 (pré-lançamento): 4-8 semanas
   - Fase 2 (lançamento): semanas 1-4
   - Fase 3 (crescimento): meses 2-6
   - Fase 4 (escala): meses 6-12
   - Com checklist de ações por fase

   **g) Métricas para o Dashboard do Dia 1:**
   - Quais KPIs rastrear imediatamente (MRR, churn, activation rate, etc.)
   - Ferramentas para medir
   - Metas iniciais realistas

3. **Entregue como um arquivo Markdown** bem estruturado que o usuário possa salvar como documento de referência do projeto.

## Argumentos

$ARGUMENTS

Exemplos:
- `/saas-architect:saas-plan App de controle financeiro para freelancers`
- `/saas-architect:saas-plan CRM para pequenas agências de marketing, B2B, time de 2 devs`
- `/saas-architect:saas-plan API de geração de PDFs, usage-based, developer-first`
