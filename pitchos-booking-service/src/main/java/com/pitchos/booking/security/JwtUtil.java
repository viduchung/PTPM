package com.pitchos.booking.security;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.security.Key;

/**
 * Giải mã JWT do Auth Service (Hoàng) cấp, dùng chung jwt.secret.
 * Token cần có claim "role" (admin | chusan | user) và "userId" (nếu thiếu thì "sub" phải là id số).
 */
@Component
public class JwtUtil {

    private final Key key;

    public JwtUtil(@Value("${jwt.secret}") String secret) {
        this.key = Keys.hmacShaKeyFor(Decoders.BASE64.decode(secret));
    }

    /** Ném JwtException nếu token sai chữ ký hoặc đã hết hạn. */
    public Claims parseToken(String token) {
        return Jwts.parserBuilder()
                .setSigningKey(key)
                .build()
                .parseClaimsJws(token)
                .getBody();
    }

    public Long getUserId(Claims claims) {
        Object userId = claims.get("userId");
        return Long.valueOf(String.valueOf(userId != null ? userId : claims.getSubject()));
    }

    public String getRole(Claims claims) {
        return claims.get("role", String.class);
    }
}
