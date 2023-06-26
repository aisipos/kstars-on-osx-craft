
# This installs the xcode command line tools if not installed yet.
# Yes these tools will be automatically installed if the user has never used git before
# But sometimes they need to be installed again.

if ! command -v xcode-select &> /dev/null
then
		announce "Installing xcode command line tools"
		xcode-select --install
fi


#This will install homebrew if it hasn't been installed yet, or reset homebrew if desired.
if [[ $(command -v brew) == "" ]]
then
		announce "Installing Homebrew."
		/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
		#This will remove all the homebrew packages if desired.
		if [ -n "$REMOVE_ALL" ]
		then
			  announce "You have selected the REMOVE_ALL option.  Warning, this will clear all currently installed homebrew packages."
			  read -p "Do you really wish to proceed? (y/n)" runscript
			  if [ "$runscript" != "y" ]
			  then
				    echo "Quitting the script as you requested."
				    exit
			  fi
			  brew remove --force $(brew list) --ignore-dependencies
		fi  
fi

#This will install KStars dependencies from Homebrew.
announce "Installing Homebrew Dependencies."
brew upgrade

# python is required for craft to work.
brew install python

# Craft does build ninja and install it to the craft directory, but QT Creator expects the homebrew version.
brew install ninja

# It would be good to sort this out.  gpg2 should be built in craft.  This is needed for translations to work.
brew install gpg
brew install svn

# This is because gpg is not called gpg2 and translations call on gpg2.  Fix this??
ln -sf $(brew --prefix)/bin/gpg $(brew --prefix)/bin/gpg2

announce "Installing craft"
mkdir -p ${CRAFT_DIR}
curl https://raw.githubusercontent.com/KDE/craft/master/setup/CraftBootstrap.py -o setup.py && $(brew --prefix)/bin/python3 setup.py --prefix "${CRAFT_DIR}"
