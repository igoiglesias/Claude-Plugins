---
description: Audita a maturidade da estratégia de crescimento do SaaS — avalia funil, automações, retenção, métricas, e identifica os gargalos mais críticos com recomendações priorizadas por impacto.
---

# Growth Audit — Diagnóstico de Crescimento

## Objetivo
Avaliar o estado atual do SaaS em termos de estratégia de crescimento e entregar um diagnóstico com os 3 gargalos mais críticos e ações priorizadas.

## Instruções

1. **Examine o projeto para identificar o que já existe:**

   **Aquisição:**
   - [ ] Landing page existe? Tem formulário de captura?
   - [ ] Blog/conteúdo SEO existe?
   - [ ] Google Ads ou paid media configurado?
   - [ ] Lead magnets (ebooks, templates, calculadoras)?
   - [ ] Presença em Product Hunt, G2, Capterra?
   - [ ] AEO — Schema markup, páginas FAQ, documentação pública?

   **Conversão:**
   - [ ] Free trial ou freemium implementado?
   - [ ] Onboarding guiado existe (wizard, checklist)?
   - [ ] Sequência de emails de welcome configurada?
   - [ ] Social proof no site (depoimentos, logos, números)?
   - [ ] Demo automatizada ou interativa?

   **Retenção:**
   - [ ] Health score implementado?
   - [ ] Emails de reengajamento para inativos?
   - [ ] NPS ou pesquisa de satisfação automatizada?
   - [ ] Alertas de churn risk?
   - [ ] Relatórios de valor para o cliente ("nos últimos 90 dias você...")?

   **Expansão:**
   - [ ] Gatilhos de upgrade implementados (limites, modais)?
   - [ ] Plano anual com desconto disponível?
   - [ ] Cross-sell de features/add-ons?
   - [ ] Programa de referral?

   **Métricas:**
   - [ ] MRR e componentes sendo rastreados?
   - [ ] Churn rate medido?
   - [ ] CAC e LTV calculados?
   - [ ] Dashboard de métricas ativo?
   - [ ] Activation rate medido?

2. **Classifique o estágio:**

   | Estágio | Critérios |
   |---------|-----------|
   | **Pre-PMF** | < 50 clientes pagantes, churn > 5%, sem métricas |
   | **Early** | 50-200 pagantes, churn estabilizando, métricas básicas |
   | **Growth** | 200-1000 pagantes, NRR > 100%, funil medido |
   | **Scale** | 1000+ pagantes, múltiplos canais, expansão > aquisição |

3. **Identifique os 3 maiores gargalos** (exemplos):
   - "Onboarding inexistente — activation rate provavelmente < 20%"
   - "Zero emails automatizados — perdendo conversões de trial"
   - "Sem tracking de churn — não sabe quantos clientes está perdendo"
   - "Pricing sem upgrade path — clientes não têm para onde expandir"
   - "Sem retargeting — visitantes do site são perdidos para sempre"

4. **Gere o relatório:**
   - **Estágio atual:** X
   - **Score por área** (0-10): Aquisição, Conversão, Retenção, Expansão, Métricas
   - **Top 3 gargalos** com impacto estimado
   - **Quick wins** (implementáveis em < 1 semana)
   - **Próximos passos estratégicos** (por ordem de prioridade e impacto)
   - **O que NÃO fazer agora** (evitar desperdício de energia no estágio atual)

## Argumentos

$ARGUMENTS

Exemplos:
- `/saas-architect:growth-audit` — Audita o projeto inteiro.
- `/saas-architect:growth-audit foco em retenção` — Audita só retenção.
- `/saas-architect:growth-audit estágio: early, B2B, ticket R$200/mês`
