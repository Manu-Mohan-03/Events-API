# 1. Use Python Base Slim (The "OS" + Python)
FROM python:3.13-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy your requirements file
COPY requirements.txt .

# 4. install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the project (So pip install dont have to run whenever code changes)
COPY . .

#6. Expose the port
EXPOSE 5001

# 7. The final command to start the program/app
CMD ["python", "app.py"]

