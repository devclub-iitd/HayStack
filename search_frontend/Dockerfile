# # build environment
# FROM node:12.2.0-alpine as build
# WORKDIR /app
# ENV PATH /app/node_modules/.bin:$PATH
# COPY package*.json /app/

# # To handle 'not get uid/gid'
# RUN npm config set unsafe-perm true

# RUN npm ci
# RUN npm install react-scripts@3.0.1 -g --silent
# COPY . /app
# RUN npm run build

# # production environment
# FROM nginx:1.16.0-alpine
# COPY --from=build /app/build /usr/share/nginx/html
# COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]


# pull official base image
FROM node:13.12.0-alpine

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
COPY package.json ./
COPY package-lock.json ./

RUN npm install react-scripts@3.4.1 -g --silent

# add app
COPY . ./

# start app
RUN npm ci
CMD npm run start