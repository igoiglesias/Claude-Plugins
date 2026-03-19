---
description: Projeta a estratégia de pricing do SaaS — modelo, planos, limites, preços e gatilhos de upgrade. Inclui análise de concorrência e estratégia de expansão de receita.
---

# Pricing — Estratégia de Monetização

## Objetivo
Desenhar a estratégia completa de pricing, incluindo modelo, planos, valor, limites e lógica de upgrade.

## Instruções

1. **Analise o contexto do SaaS:**
   - Examine o código do projeto (se disponível) para entender features e limites existentes.
   - Identifique o ICP e o mercado-alvo.
   - Pesquise concorrentes mencionados em $ARGUMENTS ou encontrados no código.

2. **Recomende o modelo de pricing:**
   - **Freemium** se: produto simples, mercado grande, efeito de rede.
   - **Free Trial (7-14 dias)** se: valor rápido de perceber.
   - **Trial + Cartão** se: precisa qualificar leads sérios.
   - **Demo-led** se: ticket alto (> US$ 500/mês), decisão complexa.
   - **Usage-based** se: valor cresce proporcionalmente com uso.
   - **Híbrido** se: base fixa + variável por uso (ex: Slack, Vercel).
   - Justifique a escolha baseada no tipo de produto e ICP.

3. **Desenhe a tabela de planos:**
   - 2-3 planos (Free/Starter, Pro, Enterprise/Business).
   - Para cada plano: nome, preço mensal, preço anual (com desconto), features incluídas, limites.
   - Defina claramente o que está no free vs pago (o free deve dar valor real mas criar desejo pelo pago).
   - Inclua limite de uso que funciona como gatilho natural de upgrade.

4. **Estratégia de expansão (onde está o dinheiro real):**
   - Seats/usuários adicionais.
   - Add-ons e features premium.
   - Aumento de limites (armazenamento, API calls, projetos).
   - Plano anual com desconto (anchor pricing).

5. **Implemente os gatilhos de upgrade no produto:**
   - Código para verificar limites e mostrar paywall/modal.
   - Lógica de "soft limit" (avisa em 80%) vs "hard limit" (bloqueia em 100%).
   - Endpoints de billing com Stripe (se aplicável).

6. **Output:** Tabela de pricing + código dos limiters + copy dos modais de upgrade.

## Argumentos

$ARGUMENTS

Exemplos:
- `/saas-architect:pricing` — Analisa o projeto atual e sugere pricing.
- `/saas-architect:pricing concorrentes: Notion, Coda, Airtable`
- `/saas-architect:pricing modelo usage-based para API de processamento de imagens`
