---
description: Implementa tracking de métricas SaaS e cria dashboard com os KPIs essenciais — MRR, churn, NRR, LTV, CAC, activation rate, health score. Configura eventos de analytics e queries para o dashboard.
---

# Metrics — Dashboard de Métricas SaaS

## Objetivo
Instrumentar o produto com tracking de eventos e criar as queries/views para um dashboard com os KPIs que todo SaaS precisa monitorar.

## Instruções

1. **Configure o tracking de eventos no produto:**

   **Eventos obrigatórios a rastrear (desde o dia 1):**
   - `user_signed_up` — com source/utm
   - `user_activated` — completou onboarding / momento aha
   - `user_logged_in` — com timestamp para calcular frequência
   - `trial_started` — com plano e data de expiração
   - `trial_converted` — trial → pagante
   - `trial_expired` — sem conversão
   - `subscription_created` — com plano e valor
   - `subscription_upgraded` — de qual para qual plano
   - `subscription_downgraded` — de qual para qual plano
   - `subscription_cancelled` — com motivo (se coletado)
   - `payment_succeeded` — com valor
   - `payment_failed` — para dunning
   - `feature_used` — com nome da feature (para adoption tracking)
   - `invite_sent` — para viralidade
   - `support_ticket_created` — para health score

2. **Implemente as métricas calculadas:**

   **Receita:**
   - MRR = soma de todas as assinaturas ativas no mês
   - MRR por componente: New, Expansion, Contraction, Churned
   - ARR = MRR × 12
   - ARPU = MRR / total de clientes ativos
   - Quick Ratio = (New + Expansion) / (Churned + Contraction)

   **Retenção:**
   - Customer Churn Rate = clientes perdidos / clientes início do período
   - Revenue Churn Rate = MRR perdido / MRR início do período
   - NRR = (MRR início + Expansion - Contraction - Churn) / MRR início × 100
   - GRR = (MRR início - Contraction - Churn) / MRR início × 100

   **Aquisição:**
   - CAC = gastos em aquisição / novos clientes
   - LTV = ARPU / churn rate mensal
   - LTV:CAC ratio
   - CAC Payback = CAC / (ARPU × margem bruta)
   - Trial → Paid conversion rate

   **Engajamento:**
   - DAU / MAU e ratio DAU/MAU
   - Activation Rate = % de signups que atingiram momento aha
   - Feature Adoption por feature
   - Time to Value = mediana do tempo signup → ativação

   **Health Score (por cliente):**
   - Baseado em: logins, features usadas, tickets, NPS, dias desde último login
   - Score 0-100 com classificação: healthy (>70), at-risk (40-70), critical (<40)

3. **Gere a implementação:**
   - Código de tracking (PostHog, Mixpanel, Amplitude, ou custom).
   - Queries SQL ou ORM para calcular cada métrica.
   - Endpoint de API que retorna as métricas agregadas.
   - Se usar ferramenta de BI: configuração do dashboard.
   - Se custom: componente de dashboard com charts.
   - Cron/job para calcular métricas diárias e armazenar histórico.

4. **Defina alertas automáticos:**
   - MRR caiu > 5% no mês → alerta.
   - Churn subiu acima do threshold → alerta.
   - Health score de cliente enterprise caiu para critical → alerta + notifica CS.
   - Activation rate caiu > 10% → investigar mudanças recentes.

## Argumentos

$ARGUMENTS

Exemplos:
- `/saas-architect:metrics` — Instrumenta o projeto atual com tracking + dashboard.
- `/saas-architect:metrics PostHog + FastAPI` — Usa PostHog como analytics.
- `/saas-architect:metrics health-score` — Implementa só o health score.
- `/saas-architect:metrics --sql` — Gera queries SQL para as métricas.
