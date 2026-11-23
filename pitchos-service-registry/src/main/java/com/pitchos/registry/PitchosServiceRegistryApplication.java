package com.pitchos.registry;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.server.EnableEurekaServer;

/**
 * PITCHOS SERVICE REGISTRY (Netflix Eureka Server) - Cổng 8761.
 *
 * VAI TRÒ TRONG KIẾN TRÚC:
 * Đây là "cuốn danh bạ" trung tâm của hệ thống PitchOS. Mỗi microservice khi khởi động
 * sẽ tự đăng ký tên định danh (Service ID) kèm địa chỉ mạng (host, port) vào đây, rồi
 * định kỳ gửi Heartbeat để chứng minh mình còn sống. Nhờ vậy, Booking Service (Consumer)
 * có thể gọi Pitch Service (Provider) bằng tên 'pitchos-pitch-service' thay vì gắn cứng
 * một địa chỉ IP hoặc URL cố định.
 *
 * PHÂN BIỆT VỚI API GATEWAY:
 * Eureka Server KHÔNG tiếp nhận và KHÔNG định tuyến request nghiệp vụ từ bên ngoài vào.
 * Nó chỉ hoạt động ở tầng nội bộ, trả lời duy nhất một câu hỏi: "dịch vụ tên X hiện đang
 * nằm ở những địa chỉ nào?". Việc tiếp nhận request từ Client, định tuyến, kiểm tra bảo
 * mật tại tầng biên là nhiệm vụ của API Gateway - một thành phần hoàn toàn khác.
 *
 * @EnableEurekaServer là annotation bật toàn bộ hạ tầng Registry: bảng đăng ký trong bộ
 * nhớ, REST API cho Eureka Client, và Dashboard tại http://localhost:8761.
 */
@SpringBootApplication
@EnableEurekaServer
public class PitchosServiceRegistryApplication {

    public static void main(String[] args) {
        SpringApplication.run(PitchosServiceRegistryApplication.class, args);
    }
}
