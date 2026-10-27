package com.pitchos.booking.client;

import com.pitchos.booking.dto.PitchResponseDTO;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

/**
 * Booking Service đóng vai trò Client, gọi HTTP GET sang Pitch Service (Port 8082)
 * để lấy đơn giá (pricePerHour) và trạng thái sân (hoat_dong / bao_tri).
 */
@FeignClient(name = "pitch-service", url = "${pitch.service.url:http://localhost:8082}")
public interface PitchClient {

    @GetMapping("/api/v1/pitches/{id}")
    PitchResponseDTO getPitchById(@PathVariable("id") Long id);
}
