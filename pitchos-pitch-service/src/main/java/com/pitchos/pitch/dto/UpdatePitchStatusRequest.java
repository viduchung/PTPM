package com.pitchos.pitch.dto;

import com.pitchos.pitch.entity.PitchStatus;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotNull;

@Schema(description = "Yêu cầu cập nhật trạng thái hoạt động của sân")
public class UpdatePitchStatusRequest {

    @NotNull(message = "Trạng thái sân không được để trống (hoat_dong hoặc bao_tri)")
    @Schema(description = "Trạng thái mới của sân bóng", example = "bao_tri")
    private PitchStatus status;

    public UpdatePitchStatusRequest() {
    }

    public UpdatePitchStatusRequest(PitchStatus status) {
        this.status = status;
    }

    public PitchStatus getStatus() { return status; }
    public void setStatus(PitchStatus status) { this.status = status; }
}
