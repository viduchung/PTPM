package com.pitchos.booking.exception;

/** Yêu cầu không hợp lệ về nghiệp vụ (trùng lịch, sân bảo trì, sai giờ...) → 400 Bad Request. */
public class BadRequestException extends RuntimeException {
    public BadRequestException(String message) {
        super(message);
    }
}
