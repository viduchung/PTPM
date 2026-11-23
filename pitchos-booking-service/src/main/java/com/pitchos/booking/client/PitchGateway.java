package com.pitchos.booking.client;

import com.pitchos.booking.dto.PitchResponseDTO;
import com.pitchos.booking.exception.ServiceUnavailableException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.Map;

/**
 * Lớp chắn giữa nghiệp vụ và hạ tầng gọi Provider (KT2).
 *
 * Nhiệm vụ duy nhất: khi danh bạ Eureka không còn instance nào của pitchos-pitch-service,
 * Spring Cloud LoadBalancer ném IllegalStateException (lỗi hạ tầng) — chuyển nó thành
 * ServiceUnavailableException để GlobalExceptionHandler trả 503 sạch sẽ, thay vì 500 mơ hồ.
 *
 * Các lỗi còn lại (Connection refused, timeout, Provider trả 4xx/5xx) do Feign ném
 * FeignException / RetryableException và đã có handler riêng.
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class PitchGateway {

    private static final String SERVICE_ID = "pitchos-pitch-service";

    private final PitchClient pitchClient;

    public PitchResponseDTO getPitchById(Long pitchId) {
        try {
            return pitchClient.getPitchById(pitchId);
        } catch (IllegalStateException ex) {
            throw noInstanceAvailable(ex);
        }
    }

    public Map<String, Object> getInstanceInfo() {
        try {
            return pitchClient.getInstanceInfo();
        } catch (IllegalStateException ex) {
            throw noInstanceAvailable(ex);
        }
    }

    private ServiceUnavailableException noInstanceAvailable(IllegalStateException ex) {
        log.warn("Eureka không còn instance nào của {}: {}", SERVICE_ID, ex.getMessage());
        return new ServiceUnavailableException(
                "Không còn instance nào của " + SERVICE_ID + " trong danh bạ Eureka");
    }
}
