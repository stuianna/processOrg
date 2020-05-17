test:
	@coverage run -m unittest discover
	@coverage report

package:
	@python3 setup.py sdist bdist_wheel

testRelease: 
	@python3 -m twine upload --repository-url https://test.pypi.org/legacy/ --skip-existing dist/*

release: 
	@python3 -m twine upload --skip-existing dist/*

install:
	@pip3 install --user . --upgrade

clean:
	@rm -rf __pycache__
	@rm -rf tags
	@rm -rf dist
	@rm -rf build
	@rm -rf *.egg-info
