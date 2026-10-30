package com.pitchos.auth.security;

import com.pitchos.auth.entity.User;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.security.Key;
import java.util.Date;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Trung tâm cấp phát và xác thực JSON Web Token của hệ thống PitchOS.
 *
 * HỢP ĐỒNG TOKEN DÙNG CHUNG TOÀN HỆ THỐNG (bắt buộc giữ nguyên):
 *   - Thuật toán ký: HMAC-SHA256 (HS256) với khóa jwt.secret dùng chung trong file .env tổng.
 *   - sub      : username (ví dụ "chusan")
 *   - userId   : mã ID số của người dùng — Booking Service dùng trường này làm principal,
 *                nếu thiếu sẽ ném NumberFormatException nên TUYỆT ĐỐI không được bỏ.
 *   - role     : chuỗi vai trò viết thường, KHÔNG có tiền tố ROLE_ ("admin" | "chusan" | "user").
 *                Pitch Service và Booking Service tự ghép "ROLE_" + role rồi so với
 *                hasRole("user") / hasAnyRole("chusan","admin"), nên nếu cấp "ROLE_USER"
 *                thì authority sẽ thành ROLE_ROLE_USER và mọi API của 2 dịch vụ kia trả 403.
 *   - fullName : họ tên hiển thị (thông tin bổ sung, 2 dịch vụ kia bỏ qua).
 *   - iat, exp : thời điểm phát hành và hết hạn.
 *
 * Lưu ý kỹ thuật: khóa được nạp bằng Decoders.BASE64.decode(secret) — giống hệt JwtUtil
 * của Pitch Service và Booking Service. Phải dùng đúng cách giải mã này, nếu không
 * chữ ký hai bên sẽ lệch và token bị từ chối.
 */
@Component
public class JwtTokenProvider {

    private static final Logger log = LoggerFactory.getLogger(JwtTokenProvider.class);

    private final Key key;
    private final long expirationMs;

    public JwtTokenProvider(
            @Value("${jwt.secret:404E635266556A586E3272357538782F413F4428472B4B6250645367566B5970}") String secret,
            @Value("${jwt.expiration-ms:86400000}") long expirationMs) {
        this.key = Keys.hmacShaKeyFor(Decoders.BASE64.decode(secret));
        this.expirationMs = expirationMs;
    }

    /**
     * Sinh Access Token cho người dùng vừa đăng nhập thành công.
     */
    public String generateToken(User user) {
        Date now = new Date();
        Date expiryDate = new Date(now.getTime() + expirationMs);

        // Dùng LinkedHashMap để thứ tự claim trong payload luôn ổn định khi soi trên jwt.io
        Map<String, Object> claims = new LinkedHashMap<>();
        claims.put("userId", user.getId());
        claims.put("role", user.getRole().name().toLowerCase());
        claims.put("fullName", user.getFullName());

        String token = Jwts.builder()
                .setSubject(user.getUsername())
                .addClaims(claims)
                .setIssuedAt(now)
                .setExpiration(expiryDate)
                .signWith(key, SignatureAlgorithm.HS256)
                .compact();

        log.info("Đã cấp phát JWT cho user '{}' (role: {}), hết hạn lúc {}",
                user.getUsername(), user.getRole(), expiryDate);
        return token;
    }

    /**
     * Giải mã token và trả về danh sách Claims.
     * Ném JwtException nếu chữ ký sai hoặc token đã hết hạn.
     */
    public Claims parseToken(String token) {
        return Jwts.parserBuilder()
                .setSigningKey(key)
                .build()
                .parseClaimsJws(token)
                .getBody();
    }

    public String getUsername(Claims claims) {
        return claims.getSubject();
    }

    public Long getUserId(Claims claims) {
        Object userId = claims.get("userId");
        if (userId == null) {
            return null;
        }
        return Long.valueOf(String.valueOf(userId));
    }

    /** Vai trò viết thường: admin | chusan | user */
    public String getRole(Claims claims) {
        return claims.get("role", String.class);
    }

    /** Thời gian sống của token tính theo giây, phục vụ trường expiresIn khi đăng nhập. */
    public long getExpiresInSeconds() {
        return expirationMs / 1000;
    }
}
