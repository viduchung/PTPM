package com.pitchos.booking.unit;

import com.pitchos.booking.client.CustomErrorDecoder;
import com.pitchos.booking.exception.ResourceNotFoundException;
import feign.FeignException;
import feign.Request;
import feign.RequestTemplate;
import feign.Response;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.nio.charset.StandardCharsets;
import java.util.Collections;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Kiem tra CustomErrorDecoder phan loai dung loi do Provider tra ve (KT2):
 *  - 404 cua GET /api/v1/pitches/{id} la loi nghiep vu  -> 404 cho client.
 *  - 404 cua endpoint khac va moi ma 5xx la loi ha tang -> FeignException -> 503 cho client.
 */
@DisplayName("CustomErrorDecoder: phan loai loi tu Provider")
class CustomErrorDecoderTest {

    private final CustomErrorDecoder decoder = new CustomErrorDecoder();

    @Test
    @DisplayName("404 cua getPitchById -> ResourceNotFoundException (client nhan 404)")
    void sanKhongTonTai() {
        Exception result = decoder.decode("PitchClient#getPitchById(Long)", response(404));

        assertThat(result).isInstanceOf(ResourceNotFoundException.class);
        assertThat(result).hasMessage("Không tìm thấy sân bóng với pitchId đã gửi");
    }

    @Test
    @DisplayName("404 cua getInstanceInfo -> FeignException (client nhan 503, khong bao sai san)")
    void endpointKhacTra404() {
        Exception result = decoder.decode("PitchClient#getInstanceInfo()", response(404));

        assertThat(result).isInstanceOf(FeignException.class);
    }

    @Test
    @DisplayName("500 cua Provider -> FeignException (client nhan 503)")
    void providerLoi500() {
        Exception result = decoder.decode("PitchClient#getPitchById(Long)", response(500));

        assertThat(result).isInstanceOf(FeignException.class);
    }

    private Response response(int status) {
        Request request = Request.create(Request.HttpMethod.GET,
                "http://pitchos-pitch-service/api/v1/pitches/9999",
                Collections.emptyMap(), null, StandardCharsets.UTF_8, new RequestTemplate());
        return Response.builder()
                .status(status)
                .reason("test")
                .request(request)
                .headers(Collections.emptyMap())
                .build();
    }
}
