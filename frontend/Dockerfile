FROM node:20-alpine AS base

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"

RUN npm i -g corepack@0.31.0
RUN corepack enable

WORKDIR /app

COPY ./frontend/package.json ./
COPY ./frontend/pnpm-lock.yaml ./

FROM base as prod-deps
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --prod --frozen-lockfile

FROM base AS build
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile
COPY ./frontend .
COPY ./.env .
RUN pnpm run build

FROM nginx:alpine

COPY ./frontend/nginx.conf /etc/nginx/nginx.conf
COPY --from=prod-deps /app/node_modules /app/node_modules
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
