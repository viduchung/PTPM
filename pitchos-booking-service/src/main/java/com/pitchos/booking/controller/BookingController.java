package com.pitchos.booking.controller;

import com.pitchos.booking.dto.BookingRequest;
import com.pitchos.booking.dto.BookingResponse;
import com.pitchos.booking.dto.UpdateStatusRequest;
import com.pitchos.booking.service.BookingService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/bookings")
@RequiredArgsConstructor
public class BookingController {

    private final BookingService bookingService;

    /** Khách hàng đặt sân → 201 Created. userId lấy từ JWT Token. */
    @PostMapping
    public ResponseEntity<BookingResponse> createBooking(@AuthenticationPrincipal Long userId,
                                                         @Valid @RequestBody BookingRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED).body(bookingService.createBooking(userId, request));
    }

    /** Danh sách đơn đặt của khách hàng hiện tại → 200 OK. */
    @GetMapping("/my-bookings")
    public ResponseEntity<List<BookingResponse>> getMyBookings(@AuthenticationPrincipal Long userId) {
        return ResponseEntity.ok(bookingService.getMyBookings(userId));
    }

    /**
     * KT2 (TC03) - Kiểm tra cân bằng tải qua Consumer: Booking gọi sang Provider theo Service ID
     * và trả về thông tin instance Pitch mà Spring Cloud LoadBalancer vừa chọn.
     * Gửi 20 request liên tiếp vào endpoint này để lập bảng phân phối giữa 2 instance (8082 / 8084).
     * Endpoint công khai (không cần token) để chạy được bằng Postman Collection Runner.
     */
    @GetMapping("/pitch-instance")
    public ResponseEntity<Map<String, Object>> getServingPitchInstance() {
        return ResponseEntity.ok(bookingService.getServingPitchInstance());
    }

    /** Chủ sân duyệt / từ chối đơn → 200 OK. */
    @PatchMapping("/{id}/status")
    public ResponseEntity<BookingResponse> updateStatus(@PathVariable("id") Long id,
                                                        @Valid @RequestBody UpdateStatusRequest request) {
        return ResponseEntity.ok(bookingService.updateStatus(id, request.getStatus()));
    }
}
