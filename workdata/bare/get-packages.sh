#!/bin/bash

set -x

#wget --recursive --level inf --xattr --no-parent --span-hosts --domains files.pythonhosted.org --convert-links 'https://pypi.org/simple/bottle/'
#wget --recursive --level inf --xattr --no-parent --span-hosts --domains files.pythonhosted.org --convert-links 'https://pypi.org/simple/isodate/'
#wget --recursive --level inf --xattr --no-parent --span-hosts --domains files.pythonhosted.org --convert-links 'https://pypi.org/simple/iniconfig/'
#wget --recursive --level inf --xattr --no-parent --span-hosts --domains files.pythonhosted.org --convert-links --content-on-error 'https://pypi.org/simple/nonexistantpackagehere/'
wget --xattr --convert-links --content-on-error 'https://pypi.org/simple/'
