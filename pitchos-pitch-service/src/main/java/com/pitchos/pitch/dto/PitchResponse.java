package com.pitchos.pitch.dto;

import com.pitchos.pitch.entity.Pitch;
import com.pitchos.pitch.entity.PitchStatus;
import com.pitchos.pitch.entity.PitchType;
import io.swagger.v3.oas.annotations.media.Schema;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Schema(description = "Thông tin chi tiết sân bóng")
public class PitchResponse {

    @Schema(description = "Mã định danh sân bóng", example = "1")
    private Long id;

    @Schema(description = "Tên sân bóng", example = "Sân bóng Mini Tiểu Ngư")
    private String name;

    @Schema(description = "Loại sân bóng (san_5, san_7, san_10)", example = "san_5")
    private PitchType pitchType;

    @Schema(description = "Đơn giá thuê mỗi giờ (VNĐ)", example = "300000.00")
    private BigDecimal pricePerHour;

    @Schema(description = "Địa chỉ sân bóng", example = "Số 12 Chùa Bộc, Đống Đa, Hà Nội")
    private String address;

    @Schema(description = "URL ảnh đại diện sân", example = "https://images.unsplash.com/photo-1529900240041-22f1df4d0a11")
    private String thumbnailUrl;

    @Schema(description = "Link Google Maps chỉ đường", example = "https://maps.google.com/?q=21.0076,105.8286")
    private String googleMapUrl;

    @Schema(description = "Trạng thái hoạt động (hoat_dong / bao_tri)", example = "hoat_dong")
    private PitchStatus status;

    @Schema(description = "Thời điểm khởi tạo bản ghi")
    private LocalDateTime createdAt;

    public PitchResponse() {
    }

    public PitchResponse(Long id, String name, PitchType pitchType, BigDecimal pricePerHour,
                         String address, String thumbnailUrl, String googleMapUrl,
                         PitchStatus status, LocalDateTime createdAt) {
        this.id = id;
        this.name = name;
        this.pitchType = pitchType;
        this.pricePerHour = pricePerHour;
        this.address = address;
        this.thumbnailUrl = thumbnailUrl;
        this.googleMapUrl = googleMapUrl;
        this.status = status;
        this.createdAt = createdAt;
    }

    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        private Long id;
        private String name;
        private PitchType pitchType;
        private BigDecimal pricePerHour;
        private String address;
        private String thumbnailUrl;
        private String googleMapUrl;
        private PitchStatus status;
        private LocalDateTime createdAt;

        public Builder id(Long id) { this.id = id; return this; }
        public Builder name(String name) { this.name = name; return this; }
        public Builder pitchType(PitchType pitchType) { this.pitchType = pitchType; return this; }
        public Builder pricePerHour(BigDecimal pricePerHour) { this.pricePerHour = pricePerHour; return this; }
        public Builder address(String address) { this.address = address; return this; }
        public Builder thumbnailUrl(String thumbnailUrl) { this.thumbnailUrl = thumbnailUrl; return this; }
        public Builder googleMapUrl(String googleMapUrl) { this.googleMapUrl = googleMapUrl; return this; }
        public Builder status(PitchStatus status) { this.status = status; return this; }
        public Builder createdAt(LocalDateTime createdAt) { this.createdAt = createdAt; return this; }

        public PitchResponse build() {
            return new PitchResponse(id, name, pitchType, pricePerHour, address, thumbnailUrl, googleMapUrl, status, createdAt);
        }
    }

    public static PitchResponse fromEntity(Pitch pitch) {
        if (pitch == null) return null;
        return PitchResponse.builder()
                .id(pitch.getId())
                .name(pitch.getName())
                .pitchType(pitch.getPitchType())
                .pricePerHour(pitch.getPricePerHour())
                .address(pitch.getAddress())
                .thumbnailUrl(pitch.getThumbnailUrl())
                .googleMapUrl(pitch.getGoogleMapUrl())
                .status(pitch.getStatus())
                .createdAt(pitch.getCreatedAt())
                .build();
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public PitchType getPitchType() { return pitchType; }
    public void setPitchType(PitchType pitchType) { this.pitchType = pitchType; }

    public BigDecimal getPricePerHour() { return pricePerHour; }
    public void setPricePerHour(BigDecimal pricePerHour) { this.pricePerHour = pricePerHour; }

    public String getAddress() { return address; }
    public void setAddress(String address) { this.address = address; }

    public String getThumbnailUrl() { return thumbnailUrl; }
    public void setThumbnailUrl(String thumbnailUrl) { this.thumbnailUrl = thumbnailUrl; }

    public String getGoogleMapUrl() { return googleMapUrl; }
    public void setGoogleMapUrl(String googleMapUrl) { this.googleMapUrl = googleMapUrl; }

    public PitchStatus getStatus() { return status; }
    public void setStatus(PitchStatus status) { this.status = status; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}
