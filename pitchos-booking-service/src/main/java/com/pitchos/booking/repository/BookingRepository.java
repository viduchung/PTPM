package com.pitchos.booking.repository;

import com.pitchos.booking.entity.Booking;
import com.pitchos.booking.entity.BookingStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface BookingRepository extends JpaRepository<Booking, Long> {

    List<Booking> findByUserId(Long userId);

    List<Booking> findByPitchId(Long pitchId);

    List<Booking> findByStatus(BookingStatus status);

    List<Booking> findByUserIdOrderByCreatedAtDesc(Long userId);

    /**
     * THUẬT TOÁN KIỂM TRA TRÙNG LỊCH THI ĐẤU (HÙNG PHỤ TRÁCH - CÂU 2 Ý 3)
     * Điều kiện trùng lịch giữa 2 khoảng thời gian [start_new, end_new] và [start_old, end_old]:
     *   b.startTime < :endTime AND b.endTime > :startTime
     * Đồng thời loại trừ các đơn đã bị từ chối (status <> 'tu_choi').
     */
    @Query("SELECT COUNT(b) FROM Booking b " +
           "WHERE b.pitchId = :pitchId " +
           "  AND b.status <> com.pitchos.booking.entity.BookingStatus.tu_choi " +
           "  AND b.startTime < :endTime " +
           "  AND b.endTime > :startTime")
    Long countOverlappingBookings(@Param("pitchId") Long pitchId,
                                  @Param("startTime") LocalDateTime startTime,
                                  @Param("endTime") LocalDateTime endTime);

    @Query("SELECT b FROM Booking b " +
           "WHERE b.pitchId = :pitchId " +
           "  AND b.status <> com.pitchos.booking.entity.BookingStatus.tu_choi " +
           "  AND b.startTime < :endTime " +
           "  AND b.endTime > :startTime")
    List<Booking> findOverlappingBookings(@Param("pitchId") Long pitchId,
                                         @Param("startTime") LocalDateTime startTime,
                                         @Param("endTime") LocalDateTime endTime);
}
