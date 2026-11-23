package com.pitchos.booking.client;

import com.pitchos.booking.dto.PitchResponseDTO;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

import java.util.Map;

/**
 * CONSUMER → PROVIDER (KT2 - Mục 2.2).
 *
 * Booking Service đóng vai trò Consumer, gọi HTTP GET sang Provider pitchos-pitch-service
 * để lấy đơn giá (pricePerHour) và trạng thái sân (hoat_dong / bao_tri).
 *
 * KT2: khai báo CHỈ bằng Service ID (name), KHÔNG còn thuộc tính url cứng.
 * Feign tra cứu Service ID trong danh bạ Eureka, sau đó Spring Cloud LoadBalancer
 * chọn một instance Provider theo thuật toán Round-Robin (8082 / 8084).
 */
@FeignClient(name = "pitchos-pitch-service")
public interface PitchClient {

    /** Lấy thông tin sân: 404 khi sân không tồn tại (xem CustomErrorDecoder). */
    @GetMapping("/api/v1/pitches/{id}")
    PitchResponseDTO getPitchById(@PathVariable("id") Long id);

    /**
     * Lấy thông tin instance Provider đang phục vụ request, dùng để chứng minh cân bằng tải
     * khi gửi 20 request liên tiếp qua Consumer (bộ test TC03).
     */
    @GetMapping("/api/v1/instance-info")
    Map<String, Object> getInstanceInfo();
}
