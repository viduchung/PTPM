package com.pitchos.booking.service;

import com.pitchos.booking.client.PitchClient;
import com.pitchos.booking.dto.BookingRequest;
import com.pitchos.booking.dto.BookingResponse;
import com.pitchos.booking.dto.PitchResponseDTO;
import com.pitchos.booking.entity.Booking;
import com.pitchos.booking.entity.BookingStatus;
import com.pitchos.booking.exception.BadRequestException;
import com.pitchos.booking.exception.ResourceNotFoundException;
import com.pitchos.booking.repository.BookingRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.Duration;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;

@Slf4j
@Service
@RequiredArgsConstructor
public class BookingService {

    private final BookingRepository bookingRepository;
    private final PitchClient pitchClient;

    /** Mỗi sân một khóa: các request đặt cùng sân phải lần lượt "kiểm tra trùng lịch → lưu đơn". */
    private final ConcurrentHashMap<Long, Object> pitchLocks = new ConcurrentHashMap<>();

    /**
     * Đặt sân: gọi Pitch Service lấy giá → tính tổng tiền → kiểm tra trùng lịch → lưu đơn cho_duyet.
     * Pitch Service bị tắt thì pitchClient ném FeignException → GlobalExceptionHandler trả 503.
     */
    public BookingResponse createBooking(Long userId, BookingRequest request) {
        if (!request.getEndTime().isAfter(request.getStartTime())) {
            throw new BadRequestException("endTime phải sau startTime");
        }

        // 1. Gọi Pitch Service qua OpenFeign
        PitchResponseDTO pitch = pitchClient.getPitchById(request.getPitchId());
        log.info("Pitch Service trả về sân {}: giá {} /giờ, trạng thái {}",
                pitch.getId(), pitch.getPricePerHour(), pitch.getStatus());

        if (!"hoat_dong".equals(pitch.getStatus())) {
            throw new BadRequestException("Sân đang bảo trì, không thể đặt");
        }

        // 2. totalPrice = số giờ * pricePerHour
        long minutes = Duration.between(request.getStartTime(), request.getEndTime()).toMinutes();
        BigDecimal totalPrice = pitch.getPricePerHour()
                .multiply(BigDecimal.valueOf(minutes))
                .divide(BigDecimal.valueOf(60), 2, RoundingMode.HALF_UP);

        // 3-4. Kiểm tra trùng lịch và lưu đơn phải liền một khối cho từng sân: nếu 2 request gửi đồng thời
        // cùng kiểm tra xong rồi mới lưu thì cả 2 đều qua → 1 khung giờ bị đặt 2 lần.
        // Khóa nằm trong bộ nhớ nên chỉ đúng khi chạy 1 instance Booking Service.
        synchronized (pitchLocks.computeIfAbsent(request.getPitchId(), id -> new Object())) {
            // Câu truy vấn của Hùng, bỏ qua đơn tu_choi
            Long overlapping = bookingRepository.countOverlappingBookings(
                    request.getPitchId(), request.getStartTime(), request.getEndTime());
            if (overlapping > 0) {
                throw new BadRequestException("Khung giờ này đã có người đặt");
            }

            // Lưu đơn với trạng thái cho_duyet (save() tự commit trước khi nhả khóa)
            Booking booking = Booking.builder()
                    .userId(userId)
                    .pitchId(request.getPitchId())
                    .startTime(request.getStartTime())
                    .endTime(request.getEndTime())
                    .totalPrice(totalPrice)
                    .status(BookingStatus.cho_duyet)
                    .build();

            return BookingResponse.from(bookingRepository.save(booking));
        }
    }

    public List<BookingResponse> getMyBookings(Long userId) {
        return bookingRepository.findByUserIdOrderByCreatedAtDesc(userId).stream()
                .map(BookingResponse::from)
                .toList();
    }

    /** Chủ sân duyệt (da_duyet) hoặc từ chối (tu_choi) đơn. */
    public BookingResponse updateStatus(Long bookingId, BookingStatus status) {
        if (status == BookingStatus.cho_duyet) {
            throw new BadRequestException("status chỉ được là da_duyet hoặc tu_choi");
        }

        Booking booking = bookingRepository.findById(bookingId)
                .orElseThrow(() -> new ResourceNotFoundException("Không tìm thấy đơn đặt sân id = " + bookingId));

        // Đơn tu_choi đã nhả khung giờ (truy vấn trùng lịch bỏ qua tu_choi), có thể người khác đã đặt vào
        // → không cho duyệt lại, tránh 2 đơn cùng giữ 1 khung giờ.
        if (booking.getStatus() == BookingStatus.tu_choi) {
            throw new BadRequestException("Đơn đã bị từ chối, không thể đổi trạng thái");
        }

        booking.setStatus(status);
        return BookingResponse.from(bookingRepository.save(booking));
    }
}
