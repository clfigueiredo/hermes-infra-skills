---
name: web-development-design-ops
description: "Use when the user asks to create, improve, audit, or deploy high-quality custom websites, landing pages, institutional pages, dashboards, portals, or exclusive web interfaces with strong design, performance, SEO, accessibility, responsive layout, clean HTML/CSS/JS or modern frontend stacks, visual QA, Lighthouse-style validation and production-ready delivery."
version: 1.0.0
author: Hermes Tutor
license: MIT
metadata:
  hermes:
    tags: [web-development, web-design, frontend, landing-page, html, css, javascript, performance, seo, accessibility]
    related_skills: [popular-web-designs, claude-design, sketch, node-inspect-debugger, requesting-code-review]
---

# Web Development & Premium Site Design Operations

Use esta skill para criar sites, páginas personalizadas, landing pages, dashboards e interfaces web exclusivas com alto padrão visual, desempenho, responsividade, SEO e qualidade de entrega.

O objetivo não é apenas “fazer uma página”: é entregar um artefato navegável, bonito, rápido, testado e pronto para publicação.

## Quando usar

- criar site institucional, landing page, página de produto ou página comercial;
- criar página personalizada para provedor, telecom, NOC, consultoria, SaaS ou evento;
- melhorar design de HTML/CSS existente;
- criar dashboard/portal web visualmente profissional;
- transformar briefing em layout e código;
- otimizar performance, SEO, acessibilidade e responsividade;
- preparar build/deploy em Nginx, Docker, Cloudflare Pages, Vercel, Netlify ou servidor próprio.

## Princípios de qualidade

1. **Briefing antes do código**: entender objetivo, público, oferta, identidade visual, conteúdo, CTA e canais de contato.
2. **Design intencional**: escolher linguagem visual coerente; não usar visual genérico de template sem personalidade.
3. **Mobile-first**: validar em mobile, tablet e desktop.
4. **Performance como requisito**: imagens otimizadas, CSS enxuto, JS mínimo, lazy loading e fontes bem carregadas.
5. **Acessibilidade básica obrigatória**: contraste, semântica, labels, foco visível e navegação por teclado.
6. **SEO técnico mínimo**: title, description, headings, Open Graph, canonical quando aplicável, sitemap/robots em sites publicados.
7. **Verificação real**: rodar build/test/lint quando houver stack; abrir no browser e revisar visualmente.

## Briefing mínimo

Coletar ou inferir:

```text
Objetivo: vender / captar lead / apresentar empresa / dashboard / suporte
Público: quem vai acessar
Estilo: premium / tecnológico / clean / dark / institucional / telecom / SaaS
Conteúdo: seções, textos, imagens, logo, cores
CTA: WhatsApp / formulário / ligação / compra / login
Stack desejada: HTML puro / React / Next.js / Astro / Vue / outro
Destino: arquivo estático / Docker / Nginx / Vercel / Cloudflare Pages
```

Se faltar muita coisa, criar uma primeira versão com placeholders profissionais e sinalizar exatamente onde trocar conteúdo.

## Fluxo operacional

1. **Inventariar projeto**
   - Se já existe código: listar stack, scripts, estrutura e rotas.
   - Se é do zero: escolher stack mais simples que atenda o objetivo.
   - Critério: saber como rodar localmente e onde editar.

2. **Definir direção visual**
   - Escolher paleta, tipografia, espaçamento, estilo de componentes e referências.
   - Para design inspirado em marcas reais, carregar `popular-web-designs` e usar tokens como referência, sem copiar marca/logotipo.
   - Critério: direção visual descrita antes de escrever CSS pesado.

3. **Implementar em fatias verificáveis**
   - Estrutura semântica.
   - Layout responsivo.
   - Componentes.
   - Conteúdo.
   - Otimização.
   - Critério: cada fatia renderiza sem quebrar a anterior.

4. **Verificar localmente**
   - Rodar install/build/lint/test disponíveis.
   - Servir localmente.
   - Abrir no browser e inspecionar visualmente.
   - Critério: build passa e página carrega sem erro de console.

5. **QA visual e responsivo**
   - Desktop, mobile e largura intermediária.
   - Conferir hero, CTA, menu, cards, formulários, footer e estados hover/focus.
   - Critério: sem overflow horizontal, texto cortado ou contraste ruim.

6. **Preparar entrega/deploy**
   - Documentar comandos.
   - Gerar build final.
   - Configurar Nginx/Docker/hosting quando pedido.
   - Critério: artefato final servido e validado.

## Escolha de stack

Use o menor stack suficiente:

```text
HTML/CSS/JS puro: landing page simples, máxima portabilidade.
Astro: site estático rápido com conteúdo e SEO forte.
Next.js: app/site React com rotas, SSR, API, integração e deploy moderno.
Vite + React/Vue: interface SPA, dashboard ou portal leve.
Tailwind: velocidade e consistência, desde que não gere HTML ilegível.
```

Evite stack pesada para página simples. Performance e manutenção contam mais que “moda”.

## Padrão de estrutura para site estático

```text
site/
  index.html
  assets/
    css/styles.css
    js/main.js
    img/
  robots.txt
  sitemap.xml
  README.md
```

Para projetos modernos:

```text
src/
  components/
  pages/ ou app/
  styles/
  assets/
public/
package.json
README.md
```

## Design premium: checklist prático

- Hero com mensagem clara em até 5 segundos.
- CTA principal visível acima da dobra.
- Hierarquia tipográfica: H1 forte, subtítulo legível, cards escaneáveis.
- Espaçamento consistente: 4/8/12/16/24/32/48/64/96 px.
- Paleta curta: fundo, texto, muted, borda, primária, destaque.
- Componentes com estados: hover, focus, disabled quando aplicável.
- Imagens/ícones coerentes com o nicho.
- Layout com grid real, não elementos soltos.
- Footer com contato, links e informações úteis.

## Performance obrigatória

Aplicar sempre que possível:

```text
- imagens em WebP/AVIF quando possível;
- width/height em imagens para evitar layout shift;
- lazy loading em imagens abaixo da dobra;
- CSS crítico simples;
- JS mínimo e sem bibliotecas desnecessárias;
- fontes com preload/preconnect quando externas;
- evitar animações pesadas;
- minificar build em produção;
- cache headers no servidor/CDN.
```

Comandos úteis:

```bash
# descobrir scripts
cat package.json 2>/dev/null | jq '.scripts'

# instalar e buildar, se Node
npm install
npm run build
npm run lint 2>/dev/null || true
npm run test 2>/dev/null || true

# servir estático simples
python3 -m http.server 8080
```

Se disponível, usar Lighthouse/PageSpeed/Playwright para validar. Quando não houver Lighthouse local, pelo menos validar carregamento, console e responsividade no browser.

## SEO mínimo

Toda página pública deve ter:

```html
<title>Título objetivo com marca</title>
<meta name="description" content="Descrição clara em até ~155 caracteres">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:type" content="website">
<meta property="og:image" content="...">
<link rel="canonical" href="https://dominio/">
```

Hierarquia:

```text
1 H1 por página
H2 para seções principais
H3 para cards/subseções
links com texto descritivo
alt em imagens relevantes
```

## Acessibilidade mínima

Verificar:

```text
- contraste suficiente;
- botões e links focáveis;
- aria-label em botões apenas com ícone;
- labels em inputs;
- navegação por teclado;
- não depender só de cor para informar estado;
- respeitar prefers-reduced-motion para animações.
```

CSS recomendado:

```css
:focus-visible {
  outline: 3px solid var(--color-focus, #60a5fa);
  outline-offset: 3px;
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Deploy em servidor próprio com Nginx

Exemplo estático:

```nginx
server {
  listen 80;
  server_name exemplo.com www.exemplo.com;
  root /var/www/exemplo/dist;
  index index.html;

  location / {
    try_files $uri $uri/ /index.html;
  }

  location ~* \.(?:css|js|jpg|jpeg|gif|png|webp|avif|svg|ico|woff2)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
  }
}
```

Validação:

```bash
nginx -t
systemctl reload nginx
curl -I http://exemplo.com
```

## Docker simples para site estático

```dockerfile
FROM nginx:alpine
COPY dist/ /usr/share/nginx/html/
```

```bash
docker build -t site-custom .
docker run --rm -p 8080:80 site-custom
curl -I http://127.0.0.1:8080
```

## Formulários e WhatsApp

Para CTA WhatsApp:

```html
<a href="https://wa.me/55DDDNUMERO?text=Ol%C3%A1%2C%20quero%20mais%20informa%C3%A7%C3%B5es" rel="noopener">Falar no WhatsApp</a>
```

Não publicar número privado sem confirmação. Para formulários, validar:

- proteção anti-spam;
- HTTPS;
- consentimento LGPD quando coletar dados pessoais;
- destino seguro do lead;
- mensagem de sucesso/erro.

## QA antes de entregar

Comandos conforme stack:

```bash
npm run build
npm run lint
npm run test
```

Verificações manuais:

```text
- abriu sem erro no navegador;
- console sem erro crítico;
- mobile sem overflow horizontal;
- CTA funciona;
- formulário testado ou explicitamente mockado;
- imagens carregam;
- textos sem placeholder acidental;
- links principais funcionam;
- performance aceitável.
```

## Relatório final padrão

```text
Status: OK/atenção/falha
Projeto: <nome/stack>
Entregue: <páginas/componentes>
Validação: <build/lint/browser/deploy>
Link/arquivo: <URL ou caminho>
Próximo passo: <conteúdo, domínio, deploy, integração etc.>
```

## Armadilhas comuns

1. **Design bonito mas lento**: animação, imagem e fonte precisam ter orçamento.
2. **Desktop perfeito e mobile quebrado**: validar mobile cedo.
3. **Copiar marca de referência**: usar inspiração de linguagem visual, não identidade protegida.
4. **CTA confuso**: cada página precisa de ação principal clara.
5. **Sem verificação real**: não declarar pronto sem build/browser.
6. **SEO esquecido**: title/description/OG fazem diferença no compartilhamento.
7. **Formulário sem backend**: deixar claro se está funcional ou apenas visual.
8. **JS excessivo**: site institucional geralmente não precisa SPA pesada.
9. **Imagens sem otimização**: causa LCP ruim e consumo alto no mobile.
10. **Segredos no frontend**: nunca colocar tokens/API keys no código entregue ao navegador.

## Checklist de validação

- [ ] briefing/objetivo entendido;
- [ ] direção visual definida;
- [ ] layout responsivo implementado;
- [ ] SEO básico presente;
- [ ] acessibilidade básica presente;
- [ ] performance considerada;
- [ ] build/lint/test executados quando disponíveis;
- [ ] página aberta no navegador e revisada visualmente;
- [ ] deploy/artefato final validado;
- [ ] relatório final com comandos e resultado real.
