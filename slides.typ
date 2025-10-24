// Base (16:9)
#set page(width: 1024pt, height: 640pt, margin: 56pt)
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
    - Motivação
    - Objetivos
    - Tecnologias: HTTP/2, Protobuf, gRPC (async), Pydantic v2, FastAPI
  ]
)

#slide(
  "Motivação",
  [
    - REST no backend interno: overhead/latência com JSON e HTTP/1.1
    - Streaming nativo e contratos estáveis
    - Interoperabilidade entre linguagens/stack
    - Padrão: REST para o externo; gRPC na comunicação entre serviços
  ]
)

#slide(
  "HTTP/2",
  [
    - Uma conexão, múltiplos streams (multiplexação de requisições)
    - Controle de fluxo por conexão e por stream
    - Cabeçalhos comprimidos (HPACK); trailers para status/metadata
  ]
)

#slide(
  "Protobuf",
  [
    - Serialização binária compacta e rápida
    - Campos numerados (wire types) com evolução compatível
    - optional / oneof / repeated / map
  ]
)

#slide(
  "gRPC (async)",
  [
    - RPCs: unary, server-streaming, client-streaming, bidi
    - Deadlines, cancelamento; status codes + trailers
    - Limites/compactação de mensagens
    - Server-streaming eficiente com `grpc.aio`/asyncio
  ]
)

#slide(
  "Pydantic v2 + FastAPI <-> gRPC",
  [
    - `ProtoModel`: to_proto / from_proto (mapeamento explícito)
    - `extra: "forbid"` (hardening de esquema)
    - FastAPI como fachada: /orders
    - Adapters individualizados; gRPC interno para baixa latência e streaming
  ]
)

#slide(
  "Demo",
  [
    - Subir: `docker compose up`
    - REST: criar/listar
    - gRPC: create/list
    - Bruno: coleções REST e gRPC com `.proto`
    - Disponível em: `https://github.com/zsinx6/probable-palm-tree`
  ]
)

#slide(
  "Boas práticas & Pitfalls",
  [
    - Boas práticas:
      - Versionar serviço (`orders.v1` `->` `v2`) e manter tipos compatíveis
      - Testes de contrato (Pydantic `<->` Protobuf) e E2E gRPC
    - Evitar:
      - Renumerar campos no `.proto`
      - Misturar regra de negócio nos adapters
      - Buffers gigantes em streams (*don’t buffer the world*)
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
