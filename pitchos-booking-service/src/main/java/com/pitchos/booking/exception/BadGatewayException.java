package com.pitchos.booking.exception;

/**
 * Provider trả về response hợp lệ về mặt HTTP nhưng DỮ LIỆU KHÔNG DÙNG ĐƯỢC
 * (đơn giá null hoặc <= 0) → 502 Bad Gateway (KT2 - IT03).
 *
 * Phân biệt rõ với:
 *  - 400 Bad Request: dữ liệu người dùng gửi sai, hoặc sân đang bảo trì (lỗi nghiệp vụ).
 *  - 503 Service Unavailable: không gọi được Provider (sập, timeout, không còn instance).
 */
public class BadGatewayException extends RuntimeException {
    public BadGatewayException(String message) {
        super(message);
    }
}
