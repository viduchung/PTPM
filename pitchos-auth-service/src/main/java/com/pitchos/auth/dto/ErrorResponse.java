package com.pitchos.auth.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;
import java.util.Map;

/**
 * Cấu trúc phản hồi lỗi chuẩn, giữ đúng khuôn JSON dùng chung với Pitch Service (Linh)
 * và Booking Service (Nhật) để client chỉ cần xử lý một định dạng lỗi duy nhất.
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Schema(description = "Cấu trúc phản hồi lỗi chuẩn của hệ thống")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ErrorResponse {

    @Schema(description = "Thời điểm phát sinh lỗi")
    @Builder.Default
    private LocalDateTime timestamp = LocalDateTime.now();

    @Schema(description = "Mã trạng thái HTTP", example = "401")
    private int status;

    @Schema(description = "Tên lỗi HTTP", example = "Unauthorized")
    private String error;

    @Schema(description = "Thông báo giải thích lỗi cho người dùng hoặc client", example = "Chưa xác thực danh tính")
    private String message;

    @Schema(description = "Đường dẫn URI gây ra lỗi", example = "/api/v1/users/1")
    private String path;

    @Schema(description = "Chi tiết các trường vi phạm Validation")
    private Map<String, String> errors;
}
