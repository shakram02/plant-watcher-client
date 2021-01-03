FROM python:3-buster


ARG UNAME=python
ARG UID=1000
ARG GID=1000

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install apt-utils \
    && apt-get -y install --no-install-recommends vim git zsh sudo \
    && useradd -ms /bin/zsh ${UNAME}

USER $UNAME
RUN echo $(pwd) \
    && zsh -c "$(curl https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)" --unattended \
    && git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions \
    && sed -i "s/plugins=(.*)/plugins=(git zsh-autosuggestions)/g" ~/.zshrc \
    && zsh ~/.zshrc

WORKDIR /home/${UNAME}/app
CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"
