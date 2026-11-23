# ====================================================================
# DOCKERFILE MULTI-STAGE: PITCHOS AUTH & USER SERVICE (Cong 8081)
# Nguoi viet: Hoang
#
# Luu y bao mat: KHONG ghi mat khau CSDL hay JWT_SECRET vao Dockerfile.
# Cac gia tri do duoc truyen vao luc chay bang bien moi truong (docker-compose
# doc tu file .env - file nay da duoc gan .gitignore, khong commit len Git).
# ====================================================================

# -------------------- GIAI DOAN 1: BUILD --------------------
FROM maven:3.9.6-eclipse-temurin-17 AS build
WORKDIR /build

COPY pom.xml .
RUN mvn -B dependency:go-offline

COPY src ./src
RUN mvn -B clean package -DskipTests

# -------------------- GIAI DOAN 2: RUNTIME --------------------
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=build /build/target/*.jar app.jar
RUN chown appuser:appgroup /app/app.jar

USER appuser

EXPOSE 8081

ENTRYPOINT ["java", "-jar", "/app/app.jar"]
