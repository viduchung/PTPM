package com.pitchos.booking.client;

import com.pitchos.booking.exception.ResourceNotFoundException;
import feign.Response;
import feign.codec.ErrorDecoder;
import org.springframework.stereotype.Component;

/**
 * Phân loại lỗi nghiệp vụ do Provider trả về (KT2 - xử lý lỗi tích hợp):
 *  - 404 của GET /api/v1/pitches/{id}: khách truyền pitchId không có thực
 *    → ResourceNotFoundException → Consumer trả 404 kèm thông báo rõ ràng (IT02).
 *  - Các mã khác: để Feign ném FeignException như mặc định
 *    → GlobalExceptionHandler quy về 503 (lỗi hạ tầng phía Provider), không trả 500 mơ hồ.
 */
@Component
public class CustomErrorDecoder implements ErrorDecoder {

    /** Tên phương thức trong PitchClient dùng để phân biệt 404 nghiệp vụ với 404 hạ tầng. */
    private static final String GET_PITCH_METHOD = "getPitchById";

    private final ErrorDecoder defaultDecoder = new ErrorDecoder.Default();

    @Override
    public Exception decode(String methodKey, Response response) {
        if (response.status() == 404 && methodKey.contains(GET_PITCH_METHOD)) {
            return new ResourceNotFoundException("Không tìm thấy sân bóng với pitchId đã gửi");
        }
        return defaultDecoder.decode(methodKey, response);
    }
}
