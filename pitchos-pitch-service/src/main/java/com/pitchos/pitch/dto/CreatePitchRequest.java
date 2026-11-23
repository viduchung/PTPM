package com.pitchos.pitch.dto;

import com.pitchos.pitch.entity.PitchType;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.Size;

import java.math.BigDecimal;

@Schema(description = "Thông tin yêu cầu tạo sân bóng mới")
public class CreatePitchRequest {

    @NotBlank(message = "Tên sân bóng không được để trống")
    @Size(max = 150, message = "Tên sân không được vượt quá 150 ký tự")
    @Schema(description = "Tên sân bóng", example = "Sân bóng Mini Tiểu Ngư")
    private String name;

    @NotNull(message = "Loại sân không được để trống (san_5, san_7, san_10)")
    @Schema(description = "Loại sân bóng", example = "san_5")
    private PitchType pitchType;

    @NotNull(message = "Đơn giá thuê mỗi giờ không được để trống")
    @Positive(message = "Đơn giá thuê mỗi giờ phải lớn hơn 0")
    @Schema(description = "Đơn giá thuê mỗi giờ (VNĐ)", example = "300000.00")
    private BigDecimal pricePerHour;

    @NotBlank(message = "Địa chỉ sân không được để trống")
    @Size(max = 255, message = "Địa chỉ sân không được vượt quá 255 ký tự")
    @Schema(description = "Địa chỉ sân bóng", example = "Số 12 Chùa Bộc, Đống Đa, Hà Nội")
    private String address;

    @Schema(description = "URL ảnh đại diện sân", example = "https://images.unsplash.com/photo-1529900240041-22f1df4d0a11")
    private String thumbnailUrl;

    @Schema(description = "Link Google Maps chỉ đường", example = "https://maps.google.com/?q=21.0076,105.8286")
    private String googleMapUrl;

    public CreatePitchRequest() {
    }

    public CreatePitchRequest(String name, PitchType pitchType, BigDecimal pricePerHour,
                              String address, String thumbnailUrl, String googleMapUrl) {
        this.name = name;
        this.pitchType = pitchType;
        this.pricePerHour = pricePerHour;
        this.address = address;
        this.thumbnailUrl = thumbnailUrl;
        this.googleMapUrl = googleMapUrl;
    }

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
}
