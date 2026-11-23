package com.pitchos.auth.controller;

import com.pitchos.auth.dto.ErrorResponse;
import com.pitchos.auth.dto.LoginRequest;
import com.pitchos.auth.dto.LoginResponse;
import com.pitchos.auth.dto.RegisterRequest;
import com.pitchos.auth.dto.UserResponse;
import com.pitchos.auth.service.AuthService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.net.URI;

@RestController
@RequestMapping("/api/v1/auth")
@Tag(name = "1. Xác thực (Authentication)", description = "Đăng ký tài khoản và đăng nhập cấp phát Bearer JWT Token")
public class AuthController {

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @Operation(summary = "Đăng ký tài khoản mới",
               description = "Tạo tài khoản khách hàng mới với vai trò mặc định 'user'. Mật khẩu được băm BCrypt trước khi lưu xuống CSDL.")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "201", description = "Đăng ký tài khoản thành công",
                    content = @Content(mediaType = "application/json",
                            schema = @Schema(implementation = UserResponse.class))),
            @ApiResponse(responseCode = "400", description = "Dữ liệu không hợp lệ hoặc tên đăng nhập / email đã tồn tại",
                    content = @Content(mediaType = "application/json",
                            schema = @Schema(implementation = ErrorResponse.class)))
    })
    @PostMapping("/register")
    public ResponseEntity<UserResponse> register(@Valid @RequestBody RegisterRequest request) {
        UserResponse created = authService.register(request);
        URI location = ServletUriComponentsBuilder
                .fromCurrentContextPath()
                .path("/api/v1/users/{id}")
                .buildAndExpand(created.getId())
                .toUri();

        return ResponseEntity.created(location).body(created);
    }

    @Operation(summary = "Đăng nhập hệ thống và nhận JWT Token",
               description = "Xác thực tên đăng nhập / mật khẩu, nếu đúng sẽ cấp phát Access Token ký HMAC-SHA256 "
                       + "chứa các claim: sub (username), userId, role (admin | chusan | user), fullName, iat, exp. "
                       + "Token này dùng chung cho cả Pitch Service (8082) và Booking Service (8083).")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Đăng nhập thành công, trả về Bearer Token",
                    content = @Content(mediaType = "application/json",
                            schema = @Schema(implementation = LoginResponse.class))),
            @ApiResponse(responseCode = "400", description = "Thiếu tên đăng nhập hoặc mật khẩu",
                    content = @Content(mediaType = "application/json",
                            schema = @Schema(implementation = ErrorResponse.class))),
            @ApiResponse(responseCode = "401", description = "Sai tên đăng nhập hoặc mật khẩu",
                    content = @Content(mediaType = "application/json",
                            schema = @Schema(implementation = ErrorResponse.class)))
    })
    @PostMapping("/login")
    public ResponseEntity<LoginResponse> login(@Valid @RequestBody LoginRequest request) {
        return ResponseEntity.ok(authService.login(request));
    }
}
