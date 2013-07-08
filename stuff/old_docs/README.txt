Setup instructions and stuff related here

Base requirements:
- Python 2.6 (we used 2.6.7)
- GIT (we used git version 1.7.4.4)


###############################################################################
# Setup GIT, bash #############################################################
###############################################################################

Add this to your ~/.profile:

    export GIT_SSL_NO_VERIFY='1'

The integration for GIT and bash can be done with the scripts I added into the
"setup/Bash_setup" folder. They are hidden files(preceded their names with a dot)


###############################################################################
# Base folder structure, GIT repo checkout ####################################
###############################################################################

    cd ~
    mkdir Dev
    cd Dev
    mkdir Tesis
    cd Tesis
    mkdir Code
    cd Code

    git clone https://<usename>@tesis_git.matiasherranz.com/proj.git
    git checkout develop
    git pull origin develop

###############################################################################
#  Create the virtualenv ######################################################
###############################################################################

Install virtualenv:
    cd ~/Dev/Tesis
    sudo easy_install virtualenv

Create the virtualenv:
    virtualenv -p python2.6  ~/Dev/Tesis/EnvTesis

Activate it(using the alias I make in the sample .profile file).
Run this command:

    tesis_start

###############################################################################
#  Install the dependecies and Python packages required #######################
###############################################################################

    cd ~/Dev/Tesis/Code/proj/setup/
    pip install -r pip-requirements.txt
