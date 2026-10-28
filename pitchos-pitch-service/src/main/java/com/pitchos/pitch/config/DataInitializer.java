package com.pitchos.pitch.config;

import com.pitchos.pitch.entity.Pitch;
import com.pitchos.pitch.entity.PitchStatus;
import com.pitchos.pitch.entity.PitchType;
import com.pitchos.pitch.repository.PitchRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.util.List;

@Component
public class DataInitializer implements CommandLineRunner {

    private static final Logger log = LoggerFactory.getLogger(DataInitializer.class);

    private final PitchRepository pitchRepository;

    public DataInitializer(PitchRepository pitchRepository) {
        this.pitchRepository = pitchRepository;
    }

    @Override
    public void run(String... args) {
        if (pitchRepository.count() == 0) {
            log.info("CSDL chưa có dữ liệu sân bóng. Đang khởi tạo 4 sân mẫu từ pitch-service.sql...");

            List<Pitch> initialPitches = List.of(
                    Pitch.builder()
                            .name("Sân bóng Mini Tiểu Ngư")
                            .pitchType(PitchType.san_5)
                            .pricePerHour(new BigDecimal("300000.00"))
                            .address("Số 12 Chùa Bộc, Đống Đa, Hà Nội")
                            .thumbnailUrl("https://images.unsplash.com/photo-1529900240041-22f1df4d0a11")
                            .googleMapUrl("https://maps.google.com/?q=21.0076,105.8286")
                            .status(PitchStatus.hoat_dong)
                            .build(),
                    Pitch.builder()
                            .name("Sân bóng K34 Bạch Đằng")
                            .pitchType(PitchType.san_7)
                            .pricePerHour(new BigDecimal("500000.00"))
                            .address("K34 Bạch Đằng, Phường 2, Tân Bình, TP.HCM")
                            .thumbnailUrl("https://images.unsplash.com/photo-1574629810360-7efbbe195018")
                            .googleMapUrl("https://maps.google.com/?q=10.8123,106.6654")
                            .status(PitchStatus.hoat_dong)
                            .build(),
                    Pitch.builder()
                            .name("Sân Chuyên Việt - Sân 1")
                            .pitchType(PitchType.san_5)
                            .pricePerHour(new BigDecimal("250000.00"))
                            .address("Số 98 Tiểu La, Hòa Cường Bắc, Hải Châu, Đà Nẵng")
                            .thumbnailUrl("https://images.unsplash.com/photo-1551958219-acbc608c6377")
                            .googleMapUrl("https://maps.google.com/?q=16.0512,108.2145")
                            .status(PitchStatus.bao_tri)
                            .build(),
                    Pitch.builder()
                            .name("Sân cỏ nhân tạo Mỹ Đình Sông Đà")
                            .pitchType(PitchType.san_10)
                            .pricePerHour(new BigDecimal("800000.00"))
                            .address("Khu liên hợp Thể thao Mỹ Đình, Nam Từ Liêm, Hà Nội")
                            .thumbnailUrl("https://images.unsplash.com/photo-1508098682722-e99c43a406b2")
                            .googleMapUrl("https://maps.google.com/?q=21.0205,105.7634")
                            .status(PitchStatus.hoat_dong)
                            .build()
            );

            pitchRepository.saveAll(initialPitches);
            log.info("Khởi tạo thành công {} sân bóng mẫu sẵn sàng phục vụ kiểm thử và demo!", initialPitches.size());
        } else {
            log.info("CSDL đã có sẵn {} bản ghi sân bóng.", pitchRepository.count());
        }
    }
}
