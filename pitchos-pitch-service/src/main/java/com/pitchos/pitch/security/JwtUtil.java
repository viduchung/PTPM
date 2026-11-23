package com.pitchos.pitch.security;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.security.Key;
import java.util.Date;
import java.util.Map;

/**
 * Tiện ích giải mã và xác thực JSON Web Token (JWT) dùng chung trong hệ thống PitchOS.
 * Đồng bộ chuỗi khóa bí mật jwt.secret chuẩn HMAC-SHA256 từ file .env tổng.
 */
@Component
public class JwtUtil {

    private final Key key;

    public JwtUtil(@Value("${jwt.secret:404E635266556A586E3272357538782F413F4428472B4B6250645367566B5970}") String secret) {
        this.key = Keys.hmacShaKeyFor(Decoders.BASE64.decode(secret));
    }

    /**
     * Giải mã Token và trích xuất danh sách Claims.
     * Ném JwtException nếu chữ ký không hợp lệ hoặc token đã hết hạn.
     */
    public Claims parseToken(String token) {
        return Jwts.parserBuilder()
                .setSigningKey(key)
                .build()
                .parseClaimsJws(token)
                .getBody();
    }

    /**
     * Lấy ID người dùng từ Claims
     */
    public Long getUserId(Claims claims) {
        Object userId = claims.get("userId");
        if (userId != null) {
            return Long.valueOf(String.valueOf(userId));
        }
        try {
            return Long.valueOf(claims.getSubject());
        } catch (NumberFormatException e) {
            return null;
        }
    }

    /**
     * Lấy vai trò (Role: admin | chusan | user) từ Claims
     */
    public String getRole(Claims claims) {
        return claims.get("role", String.class);
    }

    /**
     * Lấy Subject (username) từ Claims
     */
    public String getSubject(Claims claims) {
        return claims.getSubject();
    }

    /**
     * Hàm tiện ích tạo token thử nghiệm (phục vụ test nội bộ hoặc diễn tập kịch bản demo)
     */
    public String generateTestToken(String username, Long userId, String role, long expirationMillis) {
        return Jwts.builder()
                .setSubject(username)
                .addClaims(Map.of("userId", userId, "role", role))
                .setIssuedAt(new Date())
                .setExpiration(new Date(System.currentTimeMillis() + expirationMillis))
                .signWith(key, SignatureAlgorithm.HS256)
                .compact();
    }
}
