# Development stage
FROM node:18-alpine AS development

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# # Create environment files
# RUN echo "REACT_APP_API_URL=http://localhost:5000" > .env.development

EXPOSE 3000

CMD ["npm", "start"]

# Production stage
FROM node:18-alpine AS production

WORKDIR /app

COPY package*.json ./
RUN npm install --production

COPY . .

# # Create production env file
# RUN echo "REACT_APP_API_URL=http://103.253.20.13:5000" > .env.production
# Tại sao ở đây để 103.253.20.13:5000 mà ko phải 103.253.20.13:25037?
# À, là vì trong docker-compose.prod.yml, mình đã map port 5000 của backend vào port 25037 của frontend
# và trong docker-compose.prod.yml, mình đã set cái biến ENV product => call tới config.js trong frontend
# => config.js sẽ lấy cái biến ENV product để set lại REACT_APP_API_URL = http://103.253.20.13:25037
# => và khi truy cập vào frontend, mình phải dùng port 25037 để truy cập vào backend
# => và khi truy cập vào frontend, mình phải dùng port 25037 để truy cập vào backend
# nên thật ra dòng này vô nghĩa 

RUN npm install @babel/plugin-proposal-private-property-in-object --save-dev
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"] 