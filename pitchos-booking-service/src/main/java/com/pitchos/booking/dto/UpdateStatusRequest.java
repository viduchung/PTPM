package com.pitchos.booking.dto;

import com.pitchos.booking.entity.BookingStatus;
import jakarta.validation.constraints.NotNull;
import lombok.*;

/**
 * Body của PATCH /api/v1/bookings/{id}/status: {"status": "da_duyet"} hoặc {"status": "tu_choi"}.
 */
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class UpdateStatusRequest {

    @NotNull(message = "status không được để trống")
    private BookingStatus status;
}
