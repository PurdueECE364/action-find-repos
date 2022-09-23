FLAGS = --secret-file .env
ACT = act $(FLAGS)

test_ece364prelabs:
	$(ACT) -W test_integration/test_ece364prelabs/workflow.yml

test_firebase:
	$(ACT) -W test_integration/test_firebase/workflow.yml

test: test_ece364prelabs test_firebase