package com.pitchos.pitch.service;

import com.pitchos.pitch.dto.CreatePitchRequest;
import com.pitchos.pitch.dto.PitchResponse;
import com.pitchos.pitch.dto.UpdatePitchStatusRequest;
import com.pitchos.pitch.entity.Pitch;
import com.pitchos.pitch.entity.PitchStatus;
import com.pitchos.pitch.entity.PitchType;
import com.pitchos.pitch.exception.ResourceNotFoundException;
import com.pitchos.pitch.repository.PitchRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class PitchService {

    private static final Logger log = LoggerFactory.getLogger(PitchService.class);

    private final PitchRepository pitchRepository;

    public PitchService(PitchRepository pitchRepository) {
        this.pitchRepository = pitchRepository;
    }

    /**
     * Lấy danh sách sân bóng (hỗ trợ lọc theo loại sân và trạng thái)
     */
    @Transactional(readOnly = true)
    public List<PitchResponse> getAllPitches(PitchType pitchType, PitchStatus status) {
        log.info("Lấy danh sách sân bóng - filter pitchType: {}, status: {}", pitchType, status);
        List<Pitch> pitches;

        if (pitchType != null && status != null) {
            pitches = pitchRepository.findByPitchTypeAndStatus(pitchType, status);
        } else if (pitchType != null) {
            pitches = pitchRepository.findByPitchType(pitchType);
        } else if (status != null) {
            pitches = pitchRepository.findByStatus(status);
        } else {
            pitches = pitchRepository.findAll();
        }

        return pitches.stream()
                .map(PitchResponse::fromEntity)
                .toList();
    }

    /**
     * Tra cứu chi tiết sân bóng theo ID (cho khách hàng và Booking Service gọi FeignClient)
     */
    @Transactional(readOnly = true)
    public PitchResponse getPitchById(Long id) {
        log.info("Tra cứu chi tiết sân bóng ID: {}", id);
        Pitch pitch = pitchRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Không tìm thấy sân bóng với mã ID: " + id));
        return PitchResponse.fromEntity(pitch);
    }

    /**
     * Thêm mới một sân bóng (yêu cầu quyền chusan hoặc admin)
     */
    @Transactional
    public PitchResponse createPitch(CreatePitchRequest request) {
        log.info("Thêm mới sân bóng: {}", request.getName());

        Pitch pitch = Pitch.builder()
                .name(request.getName().trim())
                .pitchType(request.getPitchType())
                .pricePerHour(request.getPricePerHour())
                .address(request.getAddress().trim())
                .thumbnailUrl(request.getThumbnailUrl())
                .googleMapUrl(request.getGoogleMapUrl())
                .status(PitchStatus.hoat_dong) // Mặc định sân mới tạo sẽ ở trạng thái hoạt động
                .build();

        Pitch saved = pitchRepository.save(pitch);
        log.info("Đã tạo thành công sân bóng ID: {}", saved.getId());
        return PitchResponse.fromEntity(saved);
    }

    /**
     * Cập nhật trạng thái sân bóng (hoat_dong hoặc bao_tri)
     */
    @Transactional
    public PitchResponse updatePitchStatus(Long id, UpdatePitchStatusRequest request) {
        log.info("Cập nhật trạng thái sân ID: {} sang {}", id, request.getStatus());
        Pitch pitch = pitchRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Không tìm thấy sân bóng với mã ID: " + id));

        pitch.setStatus(request.getStatus());
        Pitch updated = pitchRepository.save(pitch);
        log.info("Đã cập nhật trạng thái sân ID: {} thành công", updated.getId());
        return PitchResponse.fromEntity(updated);
    }
}
