FROM mhart/alpine-node:latest

WORKDIR /react_static/
RUN mkdir /react_components

COPY package.json /react_static/

RUN npm install

COPY ./src/ /react_static/src

