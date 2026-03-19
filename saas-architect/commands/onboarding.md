---
description: Projeta e implementa o fluxo de onboarding do SaaS — do signup ao "momento aha". Inclui wizard guiado, sequência de emails, tooltips, checklists e gatilhos de reengajamento.
---

# Onboarding — Fluxo de Ativação

## Objetivo
Criar o fluxo completo de onboarding que leva o usuário do signup ao "momento aha" no menor tempo possível. A ativação é o ponto mais crítico de todo SaaS — se o usuário não percebe valor rápido, ele cancela.

## Instruções

1. **Identifique o "momento aha" do produto:**
   - Examine o código e features do projeto.
   - Pergunte ao usuário se não for óbvio: "Qual é a primeira coisa que faz o usuário pensar 'isso é útil'?"
   - Exemplos: primeiro relatório gerado, primeiro item criado, primeiro membro convidado, primeira automação rodando.

2. **Desenhe o wizard de primeiro acesso:**
   - Máximo 3-5 passos até o "momento aha".
   - Cada passo com objetivo claro e progresso visível.
   - Personalização: "Qual seu objetivo?" ou "Como você vai usar?" para adaptar a experiência.
   - Use dados do signup (cargo, empresa) para pré-preencher quando possível.
   - Celebração visual ao completar (confetti, mensagem motivacional).

3. **Crie a checklist in-app:**
   - Lista de 4-6 ações que representam ativação completa.
   - Progresso visual (barra ou %).
   - Persista no dashboard até 100% completo.
   - Cada item com link direto para a ação.

4. **Projete a sequência de emails de onboarding:**
   ```
   Email 1 (imediato): Boas-vindas + primeiro passo claro
   Email 2 (dia 2):    Feature principal + link para tutorial
   Email 3 (dia 4):    Caso de sucesso de cliente similar
   Email 4 (dia 7):    Feature avançada que aumenta valor percebido
   Email 5 (dia 10):   Oferta de upgrade ou extensão de trial
   Email 6 (dia 13):   FOMO — último dia + benefícios do pago
   Email 7 (dia 14):   Trial expirou — oferta de reativação
   ```

5. **Implemente gatilhos de reengajamento:**
   - Parou no meio do setup → email em 24h com vídeo curto.
   - Não logou em 3 dias → push notification + email.
   - Completou setup mas não usou feature core → tooltip guiando.

6. **Gere código concreto:**
   - Componentes de UI (wizard, checklist, tooltips, modais).
   - Backend: tracking de progresso de onboarding por usuário.
   - Templates de email (HTML ou texto).
   - Lógica de gatilhos (cron jobs ou event-driven).

## Argumentos

$ARGUMENTS

Exemplos:
- `/saas-architect:onboarding` — Analisa o projeto e cria o fluxo.
- `/saas-architect:onboarding momento aha: primeiro relatório financeiro gerado`
- `/saas-architect:onboarding framework: Next.js, emails: Resend`
