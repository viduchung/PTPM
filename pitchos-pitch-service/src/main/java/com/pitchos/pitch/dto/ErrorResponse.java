package com.pitchos.pitch.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import io.swagger.v3.oas.annotations.media.Schema;

import java.time.LocalDateTime;
import java.util.Map;

@JsonInclude(JsonInclude.Include.NON_NULL)
@Schema(description = "Cấu trúc phản hồi lỗi chuẩn của hệ thống")
public class ErrorResponse {

    @Schema(description = "Thời điểm phát sinh lỗi")
    private LocalDateTime timestamp = LocalDateTime.now();

    @Schema(description = "Mã trạng thái HTTP", example = "400")
    private int status;

    @Schema(description = "Tên lỗi HTTP", example = "Bad Request")
    private String error;

    @Schema(description = "Thông báo giải thích lỗi cho người dùng hoặc client", example = "Dữ liệu gửi lên không hợp lệ")
    private String message;

    @Schema(description = "Đường dẫn URI gây ra lỗi", example = "/api/v1/pitches")
    private String path;

    @Schema(description = "Chi tiết các trường vi phạm Validation")
    private Map<String, String> errors;

    public ErrorResponse() {
        this.timestamp = LocalDateTime.now();
    }

    public ErrorResponse(LocalDateTime timestamp, int status, String error, String message, String path, Map<String, String> errors) {
        this.timestamp = timestamp != null ? timestamp : LocalDateTime.now();
        this.status = status;
        this.error = error;
        this.message = message;
        this.path = path;
        this.errors = errors;
    }

    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        private LocalDateTime timestamp = LocalDateTime.now();
        private int status;
        private String error;
        private String message;
        private String path;
        private Map<String, String> errors;

        public Builder timestamp(LocalDateTime timestamp) { this.timestamp = timestamp; return this; }
        public Builder status(int status) { this.status = status; return this; }
        public Builder error(String error) { this.error = error; return this; }
        public Builder message(String message) { this.message = message; return this; }
        public Builder path(String path) { this.path = path; return this; }
        public Builder errors(Map<String, String> errors) { this.errors = errors; return this; }

        public ErrorResponse build() {
            return new ErrorResponse(timestamp, status, error, message, path, errors);
        }
    }

    public LocalDateTime getTimestamp() { return timestamp; }
    public void setTimestamp(LocalDateTime timestamp) { this.timestamp = timestamp; }

    public int getStatus() { return status; }
    public void setStatus(int status) { this.status = status; }

    public String getError() { return error; }
    public void setError(String error) { this.error = error; }

    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }

    public String getPath() { return path; }
    public void setPath(String path) { this.path = path; }

    public Map<String, String> getErrors() { return errors; }
    public void setErrors(Map<String, String> errors) { this.errors = errors; }
}
