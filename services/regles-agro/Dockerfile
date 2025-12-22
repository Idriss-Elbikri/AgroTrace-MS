# --- Étape 1 : Compilation (Build) ---
FROM maven:3.8.5-openjdk-17 AS builder
WORKDIR /app
# On copie le fichier de configuration Maven
COPY pom.xml .
# On copie le code source
COPY src ./src
# On compile le projet et on crée le JAR (en sautant les tests pour aller vite)
RUN mvn clean package -DskipTests

# --- Étape 2 : Exécution (Run) ---
FROM eclipse-temurin:17-jdk-jammy
WORKDIR /app
# On récupère le JAR créé à l'étape 1
COPY --from=builder /app/target/*.jar app.jar

# Configuration pour Spring Boot
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]