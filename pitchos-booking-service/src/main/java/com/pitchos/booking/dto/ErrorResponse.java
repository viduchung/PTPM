package com.pitchos.booking.dto;

import lombok.*;
import org.springframework.http.HttpStatus;

import java.time.LocalDateTime;

/**
 * Định dạng lỗi trả về client, ví dụ:
 * { "timestamp": "...", "status": 503, "error": "Service Unavailable", "message": "..." }
 */
@Getter
@AllArgsConstructor
public class ErrorResponse {

    private LocalDateTime timestamp;
    private int status;
    private String error;
    private String message;

    public static ErrorResponse of(HttpStatus status, String message) {
        return new ErrorResponse(LocalDateTime.now(), status.value(), status.getReasonPhrase(), message);
    }
}
