# ====================================================================
# BOOKING SERVICE (CONSUMER) - DOCKERFILE MULTI-STAGE (KT2 - Nhật)
# Giai đoạn 1 (builder): biên dịch bằng Maven, không đưa Maven vào ảnh chạy.
# Giai đoạn 2 (runtime) : chỉ chứa JRE 17 + file .jar, chạy bằng user thường.
# ====================================================================

# -------- Giai đoạn 1: BUILD --------
FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /build

# Copy pom trước để Docker cache lớp tải dependency, lần build sau nhanh hơn
COPY pom.xml .
RUN mvn -B dependency:go-offline

COPY src ./src
RUN mvn -B clean package -DskipTests

# -------- Giai đoạn 2: RUNTIME --------
FROM eclipse-temurin:17-jre
WORKDIR /app

# curl phục vụ HEALTHCHECK gọi /actuator/health (ảnh JRE không có sẵn)
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# KHÔNG chạy quyền root: tạo user thường và chuyển quyền sở hữu thư mục ứng dụng
RUN groupadd --system appgroup \
    && useradd --system --gid appgroup --create-home appuser

COPY --from=builder /build/target/*.jar /app/app.jar
RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 8083

# Container Status (Docker) ≠ App Health (Actuator): healthcheck dưới đây đọc đúng
# trạng thái ứng dụng, để docker compose ps báo "healthy" khi app thật sự sẵn sàng.
HEALTHCHECK --interval=15s --timeout=5s --start-period=60s --retries=5 \
    CMD curl -fsS http://localhost:8083/actuator/health | grep -q '"status":"UP"' || exit 1

ENTRYPOINT ["java", "-jar", "/app/app.jar"]
