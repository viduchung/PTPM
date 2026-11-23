# ====================================================================
# DOCKERFILE MULTI-STAGE: PITCHOS-PITCH-SERVICE (PROVIDER)
# Người thực hiện: LINH - Kỹ sư Triển khai Container & Provider Pitch Service
#
# Kiến trúc 2 Giai đoạn (Multi-stage build):
#   - Stage 1 (Builder): Sử dụng Maven + JDK 17 để biên dịch mã nguồn và đóng gói JAR.
#   - Stage 2 (Runtime): Sử dụng Eclipse Temurin JRE 17 Alpine siêu nhẹ, tạo non-root user
#     để vận hành an toàn theo nguyên tắc bảo mật tối thiểu (Least Privilege - chuẩn TH8).
# ====================================================================

# -------------------- GIAI ĐOẠN 1: BUILD --------------------
FROM maven:3.9.6-eclipse-temurin-17-alpine AS builder
WORKDIR /build

# Tận dụng cơ chế layer cache của Docker: tải dependencies trước
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy toàn bộ mã nguồn vào và build file jar (bỏ qua unit test khi đóng gói image)
COPY src ./src
RUN mvn clean package -DskipTests -B

# -------------------- GIAI ĐOẠN 2: RUNTIME --------------------
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

# Tạo nhóm và người dùng không có quyền root (appuser)
# Ngăn chặn nguy cơ leo thang đặc quyền từ bên trong container nếu ứng dụng bị tấn công
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Cài đặt curl để phục vụ kiểm tra sức khỏe và debug kết nối nếu cần
RUN apk --no-cache add curl wget

# Sao chép file thực thi JAR từ Stage 1 sang Stage 2
COPY --from=builder /build/target/pitchos-pitch-service-*.jar app.jar

# Phân quyền sở hữu toàn bộ thư mục ứng dụng cho appuser
RUN chown -R appuser:appgroup /app

# Chuyển ngữ cảnh thực thi sang non-root user
USER appuser

# Khai báo các cổng mạng dịch vụ dự kiến lắng nghe (8082 cho Instance 1, 8084 cho Instance 2)
EXPOSE 8082 8084

# Cấu hình tối ưu hóa bộ nhớ JVM cho môi trường container
ENV JAVA_OPTS="-Xms256m -Xmx512m -XX:+UseG1GC"

# Khởi chạy ứng dụng
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
