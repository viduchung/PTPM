package com.pitchos.booking.exception;

/** Không tìm thấy tài nguyên (sân bóng hoặc đơn đặt) → 404 Not Found. */
public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String message) {
        super(message);
    }
}
