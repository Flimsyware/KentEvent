"Setting up pip installs"

$pip = pip
$pypip = py -m pip
if($pip)
{
    "Pip"
    pip install flask
    pip install flask_bootstrap
    pip install validate_email
}
elseif($pypip)
{
    "py -m pip"
    py -m pip install flask
    py -m pip install flask_bootstrap
    py -m pip install validate_email
}

"Setting Enviroment Variables"
$env:FLASK_ENV = "development"
$env:FLASK_APP = "flaskr"



# clear



# clear
# "pip installed all dependancies"


