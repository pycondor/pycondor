tests:
	py.test -v pycondor

dist:
	rm dist/*
	python setup.py sdist
	python setup.py bdist_wheel --universal

upload:
	twine upload dist/*

release: dist upload

deploy-docs:
	mkdocs gh-deploy --clean docs
