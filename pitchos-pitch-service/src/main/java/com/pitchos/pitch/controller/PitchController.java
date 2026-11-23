package com.pitchos.pitch.controller;

import com.pitchos.pitch.dto.CreatePitchRequest;
import com.pitchos.pitch.dto.ErrorResponse;
import com.pitchos.pitch.dto.PitchResponse;
import com.pitchos.pitch.dto.UpdatePitchStatusRequest;
import com.pitchos.pitch.entity.PitchStatus;
import com.pitchos.pitch.entity.PitchType;
import com.pitchos.pitch.service.PitchService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.ArraySchema;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.net.URI;
import java.util.List;

@RestController
@RequestMapping("/api/v1/pitches")
@Tag(name = "1. Quản lý Sân bóng (Pitch Management)", description = "Các API tra cứu, thêm mới và cập nhật trạng thái sân bóng đá mini")
public class PitchController {

    private final PitchService pitchService;

    public PitchController(PitchService pitchService) {
        this.pitchService = pitchService;
    }

    @Operation(summary = "Lấy danh sách sân bóng công khai",
               description = "Khách hàng và chủ sân có thể xem danh sách tất cả các sân bóng. Hỗ trợ lọc theo loại sân (san_5, san_7, san_10) và trạng thái (hoat_dong, bao_tri).")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Lấy danh sách sân thành công",
                    content = @Content(mediaType = "application/json",
                            array = @ArraySchema(schema = @Schema(implementation = PitchResponse.class))))
    })
    @GetMapping
    public ResponseEntity<List<PitchResponse>> getAllPitches(
            @Parameter(description = "Loại sân cần lọc: san_5, san_7, san_10")
            @RequestParam(required = false) PitchType pitchType,
            @Parameter(description = "Trạng thái hoạt động: hoat_dong, bao_tri")
            @RequestParam(required = false) PitchStatus status) {

        List<PitchResponse> pitches = pitchService.getAllPitches(pitchType, status);
        return ResponseEntity.ok(pitches);
    }

    @Operation(summary = "Lấy thông tin chi tiết một sân bóng theo ID",
               description = "Tra cứu thông tin chi tiết của sân bóng bao gồm cấu hình, đơn giá thuê mỗi giờ và trạng thái hoạt động. API này được Booking Service gọi sang qua FeignClient.")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Tìm thấy thông tin sân bóng",
                    content = @Content(mediaType = "application/json",
                            schema = @Schema(implementation = PitchResponse.class))),
            @ApiResponse(responseCode = "404", description = "Không tìm thấy sân bóng với ID tương ứng",
                    content = @Content(mediaType = "application/json",
                            schema = @Schema(implementation = ErrorResponse.class)))
    })
    @GetMapping("/{id}")
    public ResponseEntity<PitchResponse> getPitchById(
            @Parameter(description = "Mã ID của sân bóng", example = "1")
            @PathVariable Long id) {

        PitchResponse pitch = pitchService.getPitchById(id);
        return ResponseEntity.ok(pitch);
    }

    @Operation(summary = "Thêm mới sân bóng vào hệ thống",
               description = "Chỉ dành riêng cho vai trò Chủ sân (chusan) hoặc Quản trị viên (admin). Yêu cầu gửi kèm Bearer Token hợp lệ.",
               security = @SecurityRequirement(name = "BearerAuth"))
    @ApiResponses(value = {
            @ApiResponse(responseCode = "201", description = "Tạo sân bóng mới thành công",
                    content = @Content(mediaType = "application/json",
                            schema = @Schema(implementation = PitchResponse.class))),
            @ApiResponse(responseCode = "400", description = "Dữ liệu đầu vào không hợp lệ (tên trống, giá âm, v.v.)",
                    content = @Content(mediaType = "application/json",
                            schema = @Schema(implementation = ErrorResponse.class))),
            @ApiResponse(responseCode = "401", description = "Chưa đăng nhập / Thiếu JWT token",
                    content = @Content(mediaType = "application/json",
                            schema = @Schema(implementation = ErrorResponse.class))),
            @ApiResponse(responseCode = "403", description = "Không đủ quyền truy cập (tài khoản role user)",
                    content = @Content(mediaType = "application/json",
                            schema = @Schema(implementation = ErrorResponse.class)))
    })
    @PostMapping
    public ResponseEntity<PitchResponse> createPitch(
            @Valid @RequestBody CreatePitchRequest request) {

        PitchResponse created = pitchService.createPitch(request);
        URI location = ServletUriComponentsBuilder.fromCurrentRequest()
                .path("/{id}")
                .buildAndExpand(created.getId())
                .toUri();

        return ResponseEntity.created(location).body(created);
    }

    @Operation(summary = "Cập nhật trạng thái sân bóng (hoạt động / bảo trì)",
               description = "Cho phép Chủ sân (chusan) hoặc Admin (admin) chuyển đổi trạng thái của sân bóng sang 'hoat_dong' hoặc 'bao_tri'.",
               security = @SecurityRequirement(name = "BearerAuth"))
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Cập nhật trạng thái thành công",
                    content = @Content(mediaType = "application/json",
                            schema = @Schema(implementation = PitchResponse.class))),
            @ApiResponse(responseCode = "400", description = "Trạng thái gửi lên không đúng định dạng",
                    content = @Content(mediaType = "application/json",
                            schema = @Schema(implementation = ErrorResponse.class))),
            @ApiResponse(responseCode = "401", description = "Chưa đăng nhập / Thiếu JWT token",
                    content = @Content(mediaType = "application/json",
                            schema = @Schema(implementation = ErrorResponse.class))),
            @ApiResponse(responseCode = "403", description = "Không đủ quyền truy cập (tài khoản role user)",
                    content = @Content(mediaType = "application/json",
                            schema = @Schema(implementation = ErrorResponse.class))),
            @ApiResponse(responseCode = "404", description = "Không tìm thấy sân bóng cần cập nhật",
                    content = @Content(mediaType = "application/json",
                            schema = @Schema(implementation = ErrorResponse.class)))
    })
    @PatchMapping("/{id}/status")
    public ResponseEntity<PitchResponse> updatePitchStatus(
            @Parameter(description = "Mã ID của sân bóng cần đổi trạng thái", example = "1")
            @PathVariable Long id,
            @Valid @RequestBody UpdatePitchStatusRequest request) {

        PitchResponse updated = pitchService.updatePitchStatus(id, request);
        return ResponseEntity.ok(updated);
    }
}
