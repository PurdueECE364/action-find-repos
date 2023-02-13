FLAGS = --secret-file .env
ACT = act $(FLAGS)

.PHONY: test_unit

test_unit:
	$(ACT) -W .github/workflows/test_unit.yml

test: test_unit