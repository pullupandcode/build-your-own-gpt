#!/usr/bin/env zsh
############################
# This script creates symlinks from the home directory to any desired dotfiles in $HOME/dotfiles
# And also installs MacOS Software
# And also installs Homebrew Packages and Casks (Apps)
# And also sets up VS Code
############################

#!/usr/bin/env zsh

echo "Installing Xcode Command Line Tools"

xcode-select --install

echo "Complete the installation of Xcode Command Line Tools before proceeding."
echo "Press enter to continue..."
read

echo "Xcode Command Line Tools installed"

echo "Now installing Homebrew..."
# Install Homebrew if it isn't already installed
if ! command -v brew &>/dev/null; then
    echo "Homebrew not installed. Installing Homebrew."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Attempt to set up Homebrew PATH automatically for this session
    if [ -x "/opt/homebrew/bin/brew" ]; then
        # For Apple Silicon Macs
        echo "Configuring Homebrew in PATH for Apple Silicon Mac..."
        echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
    fi
else
    echo "Homebrew is already installed."
fi

# Verify brew is now accessible
if ! command -v brew &>/dev/null; then
    echo "Failed to configure Homebrew in PATH. Please add Homebrew to your PATH manually."
    exit 1
fi

# Update Homebrew and Upgrade any already-installed formulae
brew update
brew upgrade
brew upgrade --cask
brew cleanup

echo "now setting up your applications"

apps=(
    "visual-studio-code"
    "ollama"
    "postman"
)

# Loop over the array to install each application.
for app in "${apps[@]}"; do
    if brew list --cask | grep -q "^$app\$"; then
        echo "$app is already installed. Skipping..."
    else
        echo "Installing $app..."
        brew install --cask "$app"
    fi
done

echo "Applications installed"

echo "Now installing pyenv, to manage your python installation"
curl https://pyenv.run | bash

echo "installation complete. Press enter to continue"
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.zshrc && echo 'eval "$(pyenv init --path)"' >> ~/.zshrc && echo 'eval "$(pyenv init -)"' >> ~/.zshrc && echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc && source ~/.zshrc

echo "Now installing python 3.10.14 using pyenv"
pyenv install 3.10.14
pyenv local 3.10.14

echo "python 3.10.14 is now installed"

# Verify brew is now accessible
if ! command source ./venv/bin/activate &>/dev/null; then
    echo "You don't have a virtualenv setup, let's create one now"

    echo "creating a new virtual environment in order to install dependencies"

    python -m venv ./venv
fi

source ./venv/bin/activate

echo "Now installing local dependencies for this project"
pip install -r requirements.txt

echo "Setting up ollama with LLaMa 3, an open-source LLM"
ollama pull llama3
ollama pull nomic-embed-text

echo "Setting up Visual Studio Code"

# Install VS Code Extensions
extensions=(
    esbenp.prettier-vscode
    formulahendry.code-runner
    foxundermoon.shell-format
    ms-python.black-formatter
    ms-python.isort
    ms-python.pylint
    ms-python.python
    ms-toolsai.jupyter
    ms-vscode.theme-predawnkit
    mtxr.sqltools
    mtxr.sqltools-driver-sqlite
)

# Get a list of all currently installed extensions.
installed_extensions=$(code --list-extensions)

for extension in "${extensions[@]}"; do
    if echo "$installed_extensions" | grep -qi "^$extension$"; then
        echo "$extension is already installed. Skipping..."
    else
        echo "Installing $extension..."
        code --install-extension "$extension"
    fi
done

echo "VS Code extensions have been installed."

echo "starting Ollama server locally"
ollama serve;

open /Applications/Visual\ Studio\ Code .
