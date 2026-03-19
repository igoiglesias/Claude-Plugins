---
description: Implementa integração completa com Stripe — planos, checkout, webhooks, portal do cliente, trial, usage-based billing, e lógica de upgrade/downgrade. Gera código production-ready.
---

# Billing — Integração Stripe e Gestão de Assinaturas

## Objetivo
Implementar o sistema de billing completo do SaaS com Stripe, cobrindo todo o ciclo de vida da assinatura.

## Instruções

1. **Detecte o stack do projeto** (FastAPI, Next.js, Laravel, etc.) e adapte o código.

2. **Implemente o core de billing:**

   **a) Configuração de planos no Stripe:**
   - Products e Prices (mensal + anual com desconto).
   - Metadata para feature flags e limites.
   - Script de seed para criar planos via API do Stripe.

   **b) Checkout e assinatura:**
   - Stripe Checkout Session (hosted) ou Payment Element (embedded).
   - Lógica de trial period (7 ou 14 dias).
   - Mapeamento user → Stripe customer_id no banco.

   **c) Webhooks (crítico):**
   - `checkout.session.completed` → ativa assinatura.
   - `invoice.paid` → renova período.
   - `invoice.payment_failed` → dunning (aviso de falha + retry).
   - `customer.subscription.updated` → upgrade/downgrade.
   - `customer.subscription.deleted` → cancelamento, marca churn.
   - Verificação de assinatura do webhook (segurança).
   - Idempotência (processar cada evento uma única vez).

   **d) Customer Portal:**
   - Link para portal do Stripe (gerenciar cartão, cancelar, trocar plano).
   - Ou portal customizado se o projeto precisar.

   **e) Feature gating (limitadores):**
   - Middleware/decorator que verifica o plano do usuário.
   - Limites por plano (ex: max projetos, max membros, max API calls).
   - Lógica de soft limit (avisa em 80%) e hard limit (bloqueia em 100%).
   - Cache do status da assinatura (não consultar Stripe a cada request).

   **f) Usage-based billing (se aplicável):**
   - Stripe Metered Billing ou Usage Records.
   - Tracking de uso com agregação por período.
   - Dashboard de uso para o cliente.

3. **Gere código completo e testável:**
   - Rotas/endpoints de billing.
   - Models/schemas para subscription no banco.
   - Webhook handler com logging.
   - Testes para cenários críticos (falha de pagamento, upgrade, cancelamento).
   - Variáveis de ambiente necessárias.

4. **Inclua segurança:**
   - Nunca expor Stripe Secret Key no frontend.
   - Verificar webhook signatures.
   - Rate limiting nos endpoints de billing.
   - Validar que o user tem permissão de alterar a subscription.

## Argumentos

$ARGUMENTS

Exemplos:
- `/saas-architect:billing` — Implementa billing para o projeto atual.
- `/saas-architect:billing FastAPI + Stripe, 3 planos, trial de 14 dias`
- `/saas-architect:billing usage-based API billing, preço por request`
- `/saas-architect:billing adicionar plano anual com 20% de desconto`
