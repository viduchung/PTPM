package com.pitchos.auth.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

/**
 * Dữ liệu đăng ký tài khoản mới. Tài khoản tạo qua API này luôn mặc định vai trò 'user',
 * không cho phép client tự khai báo role để tránh leo thang đặc quyền.
 */
@Schema(description = "Thông tin yêu cầu đăng ký tài khoản mới")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class RegisterRequest {

    @NotBlank(message = "Tên đăng nhập không được để trống")
    @Size(min = 4, max = 50, message = "Tên đăng nhập phải từ 4 đến 50 ký tự")
    @Schema(description = "Tên đăng nhập", example = "khachhang01")
    private String username;

    @NotBlank(message = "Email không được để trống")
    @Email(message = "Email không đúng định dạng")
    @Size(max = 100, message = "Email không được vượt quá 100 ký tự")
    @Schema(description = "Địa chỉ email", example = "khachhang01@gmail.com")
    private String email;

    @NotBlank(message = "Mật khẩu không được để trống")
    @Size(min = 6, max = 100, message = "Mật khẩu phải có ít nhất 6 ký tự")
    @Schema(description = "Mật khẩu dạng văn bản thuần, sẽ được băm BCrypt trước khi lưu", example = "123456")
    private String password;

    @NotBlank(message = "Họ và tên không được để trống")
    @Size(max = 100, message = "Họ và tên không được vượt quá 100 ký tự")
    @Schema(description = "Họ và tên đầy đủ", example = "Nguyễn Văn Khách Hàng")
    private String fullName;

    @Pattern(regexp = "^$|^(0|\\+84)\\d{9}$", message = "Số điện thoại phải gồm 10 chữ số bắt đầu bằng 0 (ví dụ 0912345678)")
    @Schema(description = "Số điện thoại liên hệ", example = "0912345678")
    private String phone;
}
