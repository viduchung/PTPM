package com.pitchos.booking.dto;

import jakarta.validation.constraints.NotNull;
import lombok.*;

import java.time.LocalDateTime;

/**
 * Body của POST /api/v1/bookings. userId không gửi trong body mà lấy từ JWT Token.
 */
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class BookingRequest {

    @NotNull(message = "pitchId không được để trống")
    private Long pitchId;

    @NotNull(message = "startTime không được để trống")
    private LocalDateTime startTime;

    @NotNull(message = "endTime không được để trống")
    private LocalDateTime endTime;
}
