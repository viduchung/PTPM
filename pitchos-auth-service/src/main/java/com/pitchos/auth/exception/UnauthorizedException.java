package com.pitchos.auth.exception;

/**
 * Sai thông tin đăng nhập hoặc chưa xác thực được danh tính → ánh xạ ra HTTP 401 Unauthorized.
 */
public class UnauthorizedException extends RuntimeException {
    public UnauthorizedException(String message) {
        super(message);
    }
}
