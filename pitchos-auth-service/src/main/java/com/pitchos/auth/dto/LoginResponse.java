package com.pitchos.auth.dto;

import com.pitchos.auth.entity.Role;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

/**
 * Kết quả đăng nhập thành công: cấp phát Bearer JWT Token kèm thông tin định danh cơ bản.
 */
@Schema(description = "Phản hồi đăng nhập thành công kèm JWT Token")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class LoginResponse {

    @Schema(description = "Chuỗi JWT Access Token ký bằng HMAC-SHA256",
            example = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjaHVzYW4iLCJ1c2VySWQiOjIsInJvbGUiOiJjaHVzYW4ifQ.xxx")
    private String accessToken;

    @Schema(description = "Loại token, luôn là Bearer", example = "Bearer")
    @Builder.Default
    private String tokenType = "Bearer";

    @Schema(description = "Thời gian sống của token tính theo giây", example = "86400")
    private Long expiresIn;

    @Schema(description = "Mã ID người dùng", example = "2")
    private Long userId;

    @Schema(description = "Tên đăng nhập", example = "chusan")
    private String username;

    @Schema(description = "Họ và tên đầy đủ", example = "Trần Văn Chủ Sân")
    private String fullName;

    @Schema(description = "Vai trò: admin | chusan | user", example = "chusan")
    private Role role;
}
