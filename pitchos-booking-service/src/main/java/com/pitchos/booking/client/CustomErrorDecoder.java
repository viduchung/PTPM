package com.pitchos.booking.client;

import com.pitchos.booking.exception.ResourceNotFoundException;
import feign.Response;
import feign.codec.ErrorDecoder;
import org.springframework.stereotype.Component;

/**
 * Bắt mã lỗi Pitch Service trả về:
 *  - 404: khách truyền pitchId không có thực → ném ResourceNotFoundException (trả 404 cho client).
 *  - Mã khác: để Feign ném FeignException như mặc định (GlobalExceptionHandler trả 503).
 */
@Component
public class CustomErrorDecoder implements ErrorDecoder {

    private final ErrorDecoder defaultDecoder = new ErrorDecoder.Default();

    @Override
    public Exception decode(String methodKey, Response response) {
        if (response.status() == 404) {
            return new ResourceNotFoundException("Không tìm thấy sân bóng với pitchId đã gửi");
        }
        return defaultDecoder.decode(methodKey, response);
    }
}
