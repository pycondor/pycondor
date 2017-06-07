tests:
	py.test -v pycondor

distribution:
	rm dist/*
	python setup.py sdist
	python setup.py bdist_wheel --universal

upload:
	twine upload dist/*

release: distribution upload

deploy-docs:
	cd docs; mkdocs gh-deploy --clean; cd -;
