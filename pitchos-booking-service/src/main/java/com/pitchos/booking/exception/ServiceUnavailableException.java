package com.pitchos.booking.exception;

/**
 * Không gọi được Provider: toàn bộ instance đã dừng, mất kết nối hoặc quá thời gian chờ
 * → 503 Service Unavailable (KT2 - IT04, IT05).
 */
public class ServiceUnavailableException extends RuntimeException {
    public ServiceUnavailableException(String message) {
        super(message);
    }
}
