# Step 1: Use the official Node.js image as the base
FROM node:18-alpine

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the package.json and package-lock.json files
COPY package*.json ./

# Step 4: Install the dependencies
RUN npm install

# Step 5: Copy the rest of the application code
COPY . .

# Step 6: Build the Next.js app
RUN npm run build

# Step 7: Expose the port Next.js runs on
EXPOSE 3000

# Step 8: Set the command to start the app
CMD ["npm", "start"]
