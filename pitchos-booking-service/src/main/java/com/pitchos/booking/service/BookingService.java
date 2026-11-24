package com.pitchos.booking.service;

import com.pitchos.booking.client.PitchGateway;
import com.pitchos.booking.dto.BookingRequest;
import com.pitchos.booking.dto.BookingResponse;
import com.pitchos.booking.dto.PitchResponseDTO;
import com.pitchos.booking.entity.Booking;
import com.pitchos.booking.entity.BookingStatus;
import com.pitchos.booking.exception.BadGatewayException;
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
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Slf4j
@Service
@RequiredArgsConstructor
public class BookingService {

    /** Trạng thái sân cho phép đặt, do Provider pitchos-pitch-service công bố. */
    private static final String PITCH_STATUS_ACTIVE = "hoat_dong";

    /** Số phút trong một giờ, dùng khi quy đổi đơn giá/giờ sang tiền của khoảng thời gian đặt. */
    private static final int MINUTES_PER_HOUR = 60;

    private final BookingRepository bookingRepository;
    private final PitchGateway pitchGateway;

    /** Mỗi sân một khóa: các request đặt cùng sân phải lần lượt "kiểm tra trùng lịch → lưu đơn". */
    private final ConcurrentHashMap<Long, Object> pitchLocks = new ConcurrentHashMap<>();

    /**
     * Đặt sân: gọi Provider lấy giá → kiểm tra dữ liệu nhận về → tính tổng tiền
     * → kiểm tra trùng lịch → lưu đơn cho_duyet.
     *
     * Các mã lỗi tích hợp: 404 (sân không tồn tại), 502 (đơn giá Provider không hợp lệ),
     * 400 (sân bảo trì / trùng lịch / sai giờ), 503 (Provider sập hoặc quá thời gian chờ).
     */
    public BookingResponse createBooking(Long userId, BookingRequest request) {
        if (!request.getEndTime().isAfter(request.getStartTime())) {
            throw new BadRequestException("endTime phải sau startTime");
        }

        // 1. Gọi Provider qua OpenFeign + Service ID (Eureka tra cứu, LoadBalancer chọn instance)
        PitchResponseDTO pitch = pitchGateway.getPitchById(request.getPitchId());
        log.info("Pitch Service trả về sân {}: giá {} /giờ, trạng thái {}",
                pitch.getId(), pitch.getPricePerHour(), pitch.getStatus());

        // 2. KT2 - Kiểm tra tính hợp lệ của dữ liệu nhận về từ Provider trước khi dùng
        validateProviderData(pitch);

        // 3. totalPrice = số giờ * pricePerHour
        BigDecimal totalPrice = calculateTotalPrice(pitch.getPricePerHour(), request);

        // 4-5. Kiểm tra trùng lịch và lưu đơn phải liền một khối cho từng sân: nếu 2 request gửi đồng thời
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

    /**
     * KT2 (IT03) - Không tin tưởng mù quáng dữ liệu của Provider:
     *  - Đơn giá null hoặc <= 0: dữ liệu dịch vụ phía sau bị sai → 502 Bad Gateway.
     *  - Sân không ở trạng thái hoat_dong: lỗi nghiệp vụ của yêu cầu → 400 Bad Request.
     */
    private void validateProviderData(PitchResponseDTO pitch) {
        if (pitch.getPricePerHour() == null
                || pitch.getPricePerHour().compareTo(BigDecimal.ZERO) <= 0) {
            throw new BadGatewayException("Dữ liệu đơn giá từ Pitch Service không hợp lệ");
        }
        if (!PITCH_STATUS_ACTIVE.equalsIgnoreCase(pitch.getStatus())) {
            throw new BadRequestException("Sân bóng hiện không hoạt động hoặc đang bảo trì");
        }
    }

    private BigDecimal calculateTotalPrice(BigDecimal pricePerHour, BookingRequest request) {
        long minutes = Duration.between(request.getStartTime(), request.getEndTime()).toMinutes();
        return pricePerHour
                .multiply(BigDecimal.valueOf(minutes))
                .divide(BigDecimal.valueOf(MINUTES_PER_HOUR), 2, RoundingMode.HALF_UP);
    }

    /**
     * KT2 (TC03) - Trả về thông tin instance Provider mà LoadBalancer vừa phân phối,
     * dùng để gửi 20 request liên tiếp và lập bảng phân phối tải giữa 2 instance Pitch.
     */
    public Map<String, Object> getServingPitchInstance() {
        Map<String, Object> instanceInfo = pitchGateway.getInstanceInfo();
        log.info("LoadBalancer phân phối request sang instance Pitch: {}", instanceInfo);
        return instanceInfo;
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
