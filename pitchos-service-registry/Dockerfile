# ====================================================================
# DOCKERFILE MULTI-STAGE: PITCHOS SERVICE REGISTRY (EUREKA SERVER)
# Nguoi viet: Hoang
#
# Vi sao dung multi-stage?
#   Giai doan build can Maven va toan bo JDK (hon 400MB) de bien dich.
#   Giai doan runtime chi can mot file .jar va mot JRE. Tach hai giai doan
#   giup anh cuoi cung KHONG mang theo Maven, ma nguon va cache .m2 -
#   vua nho hon nhieu lan, vua giam be mat tan cong.
# ====================================================================

# -------------------- GIAI DOAN 1: BUILD --------------------
FROM maven:3.9.6-eclipse-temurin-17 AS build
WORKDIR /build

# Copy pom.xml truoc va tai dependency rieng mot lop: neu ma nguon doi ma
# pom.xml khong doi, Docker tai su dung lop cache nay, khoi tai lai thu vien.
COPY pom.xml .
RUN mvn -B dependency:go-offline

COPY src ./src
RUN mvn -B clean package -DskipTests

# -------------------- GIAI DOAN 2: RUNTIME --------------------
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

# Tao user thuong va chay ung dung bang user nay. Mac dinh container chay
# bang root; neu ke tan cong thoat duoc ra khoi tien trinh Java, ho se co
# quyen root tren container. Day la yeu cau bao mat bat buoc cua TH8.
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=build /build/target/*.jar app.jar
RUN chown appuser:appgroup /app/app.jar

USER appuser

EXPOSE 8761

ENTRYPOINT ["java", "-jar", "/app/app.jar"]
