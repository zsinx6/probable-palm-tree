PROTO_DIR := proto
OUT_DIR := generated

PROTO_FILES := \
  $(PROTO_DIR)/orders_types.proto \
  $(PROTO_DIR)/orders_service.proto

.PHONY: proto clean slide format

format:
	uv run ruff format .
	uv run ruff check . --fix

slide:
	typst compile slides.typ

proto:
	@mkdir -p $(OUT_DIR)
	@touch $(OUT_DIR)/__init__.py
	@uv run python -m grpc_tools.protoc \
	  -I$(PROTO_DIR) \
	  --python_out=$(OUT_DIR) \
	  --grpc_python_out=$(OUT_DIR) \
	  $(PROTO_FILES)
	@# Patch: imports absolutos -> imports qualificados no pacote generated
	@sed -E -i 's/^import[[:space:]]+orders_types_pb2([[:space:]]+as[[:space:]]+[A-Za-z_][A-Za-z0-9_]*)?/from generated import orders_types_pb2\1/' $(OUT_DIR)/*_pb2*.py
	@sed -E -i 's/^from[[:space:]]+orders_types_pb2[[:space:]]+import[[:space:]]+/from generated.orders_types_pb2 import /' $(OUT_DIR)/*_pb2*.py

clean:
	@rm -rf $(OUT_DIR)
