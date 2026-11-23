package com.pitchos.pitch.entity;

import jakarta.persistence.*;
import org.hibernate.annotations.CreationTimestamp;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "pitches")
public class Pitch {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 150)
    private String name;

    @Enumerated(EnumType.STRING)
    @Column(name = "pitch_type", nullable = false)
    private PitchType pitchType = PitchType.san_5;

    @Column(name = "price_per_hour", nullable = false, precision = 12, scale = 2)
    private BigDecimal pricePerHour;

    @Column(nullable = false, length = 255)
    private String address;

    @Column(name = "thumbnail_url", length = 500)
    private String thumbnailUrl;

    @Column(name = "google_map_url", columnDefinition = "TEXT")
    private String googleMapUrl;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private PitchStatus status = PitchStatus.hoat_dong;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    public Pitch() {
    }

    public Pitch(Long id, String name, PitchType pitchType, BigDecimal pricePerHour, String address,
                 String thumbnailUrl, String googleMapUrl, PitchStatus status, LocalDateTime createdAt) {
        this.id = id;
        this.name = name;
        this.pitchType = pitchType != null ? pitchType : PitchType.san_5;
        this.pricePerHour = pricePerHour;
        this.address = address;
        this.thumbnailUrl = thumbnailUrl;
        this.googleMapUrl = googleMapUrl;
        this.status = status != null ? status : PitchStatus.hoat_dong;
        this.createdAt = createdAt;
    }

    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        private Long id;
        private String name;
        private PitchType pitchType = PitchType.san_5;
        private BigDecimal pricePerHour;
        private String address;
        private String thumbnailUrl;
        private String googleMapUrl;
        private PitchStatus status = PitchStatus.hoat_dong;
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

        public Pitch build() {
            return new Pitch(id, name, pitchType, pricePerHour, address, thumbnailUrl, googleMapUrl, status, createdAt);
        }
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
