package com.pitchos.booking.exception;

import com.pitchos.booking.dto.ErrorResponse;
import feign.FeignException;
import feign.RetryableException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

    /**
     * Provider không gọi được: tắt tiến trình / mất mạng / quá thời gian chờ (timeout)
     * → Feign ném RetryableException hoặc FeignException.
     * Quy về 503 thay vì để lỗi 500, Booking Service vẫn sống bình thường
     * (ngăn sụp đổ dây chuyền - Cascading Failure). KT2: IT04, IT05.
     */
    @ExceptionHandler({FeignException.class, RetryableException.class})
    public ResponseEntity<ErrorResponse> handleFeignFailure(FeignException ex) {
        log.warn("Không gọi được Pitch Service (status Feign = {}): {}", ex.status(), ex.getMessage());
        return build(HttpStatus.SERVICE_UNAVAILABLE,
                "Dịch vụ quản lý sân hiện không khả dụng. Vui lòng thử lại sau!");
    }

    /**
     * Toàn bộ instance Provider đã rời khỏi danh bạ Eureka: Spring Cloud LoadBalancer
     * không còn địa chỉ nào để gọi ("No instances available for pitchos-pitch-service").
     * Đây vẫn là tình huống Provider sập → 503, không phải lỗi lập trình 500. KT2: IT04.
     */
    @ExceptionHandler(ServiceUnavailableException.class)
    public ResponseEntity<ErrorResponse> handleServiceUnavailable(ServiceUnavailableException ex) {
        log.warn("Không còn instance Provider khả dụng: {}", ex.getMessage());
        return build(HttpStatus.SERVICE_UNAVAILABLE,
                "Dịch vụ quản lý sân hiện không khả dụng. Vui lòng thử lại sau!");
    }

    /**
     * Provider trả 200 nhưng dữ liệu không dùng được (đơn giá null hoặc <= 0)
     * → 502 Bad Gateway: lỗi nằm ở dữ liệu dịch vụ phía sau, không phải lỗi của người dùng.
     * KT2: IT03.
     */
    @ExceptionHandler(BadGatewayException.class)
    public ResponseEntity<ErrorResponse> handleBadGateway(BadGatewayException ex) {
        log.error("Dữ liệu nhận từ Pitch Service không hợp lệ: {}", ex.getMessage());
        return build(HttpStatus.BAD_GATEWAY, ex.getMessage());
    }

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(ResourceNotFoundException ex) {
        return build(HttpStatus.NOT_FOUND, ex.getMessage());
    }

    @ExceptionHandler(BadRequestException.class)
    public ResponseEntity<ErrorResponse> handleBadRequest(BadRequestException ex) {
        return build(HttpStatus.BAD_REQUEST, ex.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(MethodArgumentNotValidException ex) {
        String message = ex.getBindingResult().getFieldErrors().get(0).getDefaultMessage();
        return build(HttpStatus.BAD_REQUEST, message);
    }

    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ResponseEntity<ErrorResponse> handleUnreadable(HttpMessageNotReadableException ex) {
        return build(HttpStatus.BAD_REQUEST, "Dữ liệu gửi lên không đúng định dạng");
    }

    private ResponseEntity<ErrorResponse> build(HttpStatus status, String message) {
        return ResponseEntity.status(status).body(ErrorResponse.of(status, message));
    }
}
