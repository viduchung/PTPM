package com.pitchos.auth.controller;

import com.pitchos.auth.dto.ErrorResponse;
import com.pitchos.auth.dto.UserResponse;
import com.pitchos.auth.service.AuthService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.ArraySchema;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/v1/users")
@Tag(name = "2. Quản lý Người dùng (User Management)", description = "Các API tra cứu thông tin người dùng, yêu cầu Bearer JWT Token")
public class UserController {

    private final AuthService authService;

    public UserController(AuthService authService) {
        this.authService = authService;
    }

    @Operation(summary = "Lấy thông tin tài khoản đang đăng nhập",
               description = "Trả về thông tin của chính người dùng ứng với JWT Token đang gửi lên.",
               security = @SecurityRequirement(name = "BearerAuth"))
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Lấy thông tin thành công",
                    content = @Content(mediaType = "application/json",
                            schema = @Schema(implementation = UserResponse.class))),
            @ApiResponse(responseCode = "401", description = "Chưa đăng nhập / Thiếu JWT Token",
                    content = @Content(mediaType = "application/json",
                            schema = @Schema(implementation = ErrorResponse.class)))
    })
    @GetMapping("/me")
    public ResponseEntity<UserResponse> getCurrentUser(Authentication authentication) {
        return ResponseEntity.ok(authService.getCurrentUser(authentication.getName()));
    }

    @Operation(summary = "Tra cứu thông tin người dùng theo ID",
               description = "Tài khoản vai trò 'user' chỉ xem được thông tin của chính mình (kiểm tra quyền sở hữu tài nguyên); "
                       + "vai trò 'chusan' và 'admin' xem được mọi tài khoản.",
               security = @SecurityRequirement(name = "BearerAuth"))
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Tìm thấy thông tin người dùng",
                    content = @Content(mediaType = "application/json",
                            schema = @Schema(implementation = UserResponse.class))),
            @ApiResponse(responseCode = "401", description = "Chưa đăng nhập / Thiếu JWT Token",
                    content = @Content(mediaType = "application/json",
                            schema = @Schema(implementation = ErrorResponse.class))),
            @ApiResponse(responseCode = "403", description = "Tài khoản 'user' cố xem thông tin của người khác",
                    content = @Content(mediaType = "application/json",
                            schema = @Schema(implementation = ErrorResponse.class))),
            @ApiResponse(responseCode = "404", description = "Không tìm thấy người dùng với ID tương ứng",
                    content = @Content(mediaType = "application/json",
                            schema = @Schema(implementation = ErrorResponse.class)))
    })
    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getUserById(
            @Parameter(description = "Mã ID của người dùng", example = "1")
            @PathVariable Long id,
            Authentication authentication) {

        return ResponseEntity.ok(authService.getUserById(id, authentication.getName()));
    }

    @Operation(summary = "Lấy danh sách toàn bộ người dùng",
               description = "Chỉ dành riêng cho vai trò Quản trị viên (admin). Tài khoản 'user' hoặc 'chusan' gọi API này sẽ nhận 403 Forbidden.",
               security = @SecurityRequirement(name = "BearerAuth"))
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Lấy danh sách người dùng thành công",
                    content = @Content(mediaType = "application/json",
                            array = @ArraySchema(schema = @Schema(implementation = UserResponse.class)))),
            @ApiResponse(responseCode = "401", description = "Chưa đăng nhập / Thiếu JWT Token",
                    content = @Content(mediaType = "application/json",
                            schema = @Schema(implementation = ErrorResponse.class))),
            @ApiResponse(responseCode = "403", description = "Không đủ quyền truy cập (yêu cầu vai trò admin)",
                    content = @Content(mediaType = "application/json",
                            schema = @Schema(implementation = ErrorResponse.class)))
    })
    @GetMapping
    public ResponseEntity<List<UserResponse>> getAllUsers() {
        return ResponseEntity.ok(authService.getAllUsers());
    }
}
