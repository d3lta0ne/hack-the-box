FROM openjdk:8-jdk-slim

# Install Maven
RUN apt-get update && apt-get install -y maven && rm -rf /var/lib/apt/lists/*

# Copy the entire project into the container
COPY . /app

# Set the working directory
WORKDIR /app

# Compile the project
RUN mvn clean package

# Copy the compiled JAR file to the final location
RUN cp target/breathtaking_view-0.0.1-SNAPSHOT.jar /app/breathtaking_view-0.0.1-SNAPSHOT.jar

# Handle the flag
COPY flag.txt /
RUN FLAG_NAME=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 12) && cp /flag.txt "/flag_${FLAG_NAME}_.txt" && rm /flag.txt

# Set the command to run the application
CMD ["java", "-jar", "breathtaking_view-0.0.1-SNAPSHOT.jar"]

# Expose the port the application runs on
EXPOSE 8081
