package com.pitchos.booking.dto;

import lombok.*;

import java.math.BigDecimal;

/**
 * Thông tin sân nhận về từ Pitch Service (GET /api/v1/pitches/{id}).
 */
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class PitchResponseDTO {

    private Long id;
    private String name;
    private BigDecimal pricePerHour;
    private String status;   // hoat_dong | bao_tri
}
