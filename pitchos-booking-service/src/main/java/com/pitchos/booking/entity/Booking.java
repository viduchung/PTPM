package com.pitchos.booking.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "bookings")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Booking {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * NGUYÊN TẮC DATABASE-PER-SERVICE:
     * Lưu Logical ID dạng số nguyên (BIGINT), tuyệt đối KHÔNG tạo Foreign Key vật lý sang pitchos_user_db.
     */
    @Column(name = "user_id", nullable = false)
    private Long userId;

    /**
     * NGUYÊN TẮC DATABASE-PER-SERVICE:
     * Lưu Logical ID dạng số nguyên (BIGINT), tuyệt đối KHÔNG tạo Foreign Key vật lý sang pitchos_pitch_db.
     */
    @Column(name = "pitch_id", nullable = false)
    private Long pitchId;

    @Column(name = "start_time", nullable = false)
    private LocalDateTime startTime;

    @Column(name = "end_time", nullable = false)
    private LocalDateTime endTime;

    @Column(name = "total_price", nullable = false, precision = 12, scale = 2)
    private BigDecimal totalPrice;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    @Builder.Default
    private BookingStatus status = BookingStatus.cho_duyet;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
}
