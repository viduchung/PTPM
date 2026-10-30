package com.pitchos.auth.dto;

import com.pitchos.auth.entity.Role;
import com.pitchos.auth.entity.User;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;

/**
 * Thông tin người dùng trả về cho client.
 * Tuyệt đối không chứa trường password (dù đã băm BCrypt) để tránh rò rỉ dữ liệu nhạy cảm.
 */
@Schema(description = "Thông tin tài khoản người dùng")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class UserResponse {

    @Schema(description = "Mã ID người dùng", example = "1")
    private Long id;

    @Schema(description = "Tên đăng nhập", example = "chusan")
    private String username;

    @Schema(description = "Địa chỉ email", example = "chusan@gmail.com")
    private String email;

    @Schema(description = "Họ và tên đầy đủ", example = "Trần Văn Chủ Sân")
    private String fullName;

    @Schema(description = "Số điện thoại", example = "0987654321")
    private String phone;

    @Schema(description = "Vai trò trong hệ thống: admin | chusan | user", example = "chusan")
    private Role role;

    @Schema(description = "Thời điểm tạo tài khoản")
    private LocalDateTime createdAt;

    /**
     * Chuyển đổi Entity sang DTO phản hồi (cùng quy ước fromEntity với PitchResponse của Linh)
     */
    public static UserResponse fromEntity(User user) {
        return UserResponse.builder()
                .id(user.getId())
                .username(user.getUsername())
                .email(user.getEmail())
                .fullName(user.getFullName())
                .phone(user.getPhone())
                .role(user.getRole())
                .createdAt(user.getCreatedAt())
                .build();
    }
}
