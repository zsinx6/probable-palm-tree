// Base (16:9)
#set page(width: 1280pt, height: 720pt, margin: 56pt)
#set text(size: 30pt)
#set heading(numbering: none)
#let gap = 18pt

#show: page.with(
  footer: context[
    #let total_pages = counter(page).final().at(0)
    [
      #text(size: 18pt)[#counter(page).display("1") / #total_pages]
    ]
  ]
)

#let slide(title, body) = {
  heading(title)
  v(gap)
  set text(size: 34pt)
  body
  pagebreak()
}

#let slide_final(title, body) = {
  heading(title)
  v(gap)
  set text(size: 34pt)
  body
}

#slide(
  " Microserviços com gRPC e FastAPI",
  []
)

#slide(
  "Sobre mim",
  [
    - Lucas Carvalho — `@zsinx6`
    - USP São Carlos
    - grupy-sanca
  ]
)

#slide(
  "gRPC + Protobuf + HTTP/2 com Python",
  [
    - objetivos
    - decisões arquiteturais
    - tecnologias: HTTP/2, Protobuf, gRPC (async), Pydantic v2, FastAPI
  ]
)

#slide(
  "Motivação",
  [
    - REST no backend interno: overhead/latência com JSON e HTTP/1.1
    - precisamos de streaming nativo e contratos estáveis
    - interoperabilidade entre linguagens/stack
    - padrão: REST na borda; gRPC na comunicação entre serviços
  ]
)

#slide(
  "HTTP/2",
  [
    - uma conexão, múltiplos streams (multiplexação de requisições)
    - elimina HOL no nível HTTP (ainda existe no TCP)
    - controle de fluxo por conexão e por stream (WINDOW_UPDATE)
    - cabeçalhos comprimidos (HPACK); trailers para status/metadata
    - ALPN negocia `h2` (TLS na prática); `h2c` útil em dev interno
    - server push não é utilizado pelo gRPC; ping/keepalive e GOAWAY
  ]
)

#slide(
  "Protobuf",
  [
    - serialização binária compacta e rápida
    - campos numerados (wire types) com evolução compatível
    - optional / oneof / repeated / map
    - valores monetários sem float (inteiro + escala)
  ]
)

#slide(
  "gRPC (async)",
  [
    - RPCs: unary, server-streaming, client-streaming, bidi
    - deadlines, cancelamento; status codes + trailers
    - limites/compactação de mensagens
    - server-streaming eficiente com `grpc.aio`/asyncio
  ]
)

#slide(
  "Pydantic v2 + FastAPI <-> gRPC",
  [
    - `ProtoModel`: to_proto / from_proto (mapeamento explícito)
    - `extra: "forbid"` (hardening de esquema)
    - FastAPI como fachada: /health e /orders
    - adapters finos; gRPC interno para baixa latência e streaming
  ]
)

#slide(
  "Demo",
  [
    - subir: `docker compose up`
    - REST: criar/listar (curl)
    - gRPC: health/create/list (grpcurl)
    - Bruno: coleções REST e gRPC com `.proto`
    - disponível em `https://github.com/zsinx6/probable-palm-tree`
  ]
)

#slide(
  "Boas práticas & Pitfalls",
  [
    - boas práticas:
      - versionar serviço (`orders.v1` `->` `v2`) e manter tipos compatíveis
      - testes de contrato (Pydantic `<->` Protobuf) e E2E gRPC
    - evitar / pitfalls:
      - renumerar campos no `.proto`
      - misturar regra de negócio nos adapters
      - buffers gigantes em streams (*don’t buffer the world*)
      - depender de `PYTHONPATH` em vez de empacotar `generated/`
  ]
)


#slide(
  "Conclusões",
  [
    - HTTP/2 + Protobuf + gRPC: performance e contratos fortes
    - Pydantic v2 + adapters: domínio limpo, tipado e testável
    - REST na borda; gRPC entre serviços; evolução segura
  ]
)

#slide_final(
  "Dúvidas?",
  []
)
