# --- Etapa 1: Build da aplicação Next.js ---
FROM node:20-alpine AS builder
WORKDIR /app

# Copia os ficheiros de dependências e instala os pacotes
COPY package.json package-lock.json ./
RUN npm ci

# Copia o restante código do frontend
COPY . .

# Gera o build otimizado de produção (usa o output: "standalone" do next.config.ts)
RUN npm run build

# --- Etapa 2: Imagem final leve de produção ---
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# Copia apenas os ficheiros necessários para correr em produção
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000

CMD ["node", "server.js"]