package com.pitchos.booking.support;

import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;

import java.security.Key;
import java.util.Date;

/**
 * Sinh JWT giống hệt token do Auth Service (Hoàng) cấp: ký HS256 bằng jwt.secret dùng chung,
 * có claim "userId" và "role" (user | chusan | admin).
 */
public final class TestTokens {

    private static final String SECRET =
            "404E635266556A586E3272357538782F413F4428472B4B6250645367566B5970";

    private static final long ONE_HOUR_MS = 3_600_000L;

    private TestTokens() {
    }

    public static String bearer(long userId, String role) {
        Key key = Keys.hmacShaKeyFor(Decoders.BASE64.decode(SECRET));
        String token = Jwts.builder()
                .setSubject(String.valueOf(userId))
                .claim("userId", userId)
                .claim("role", role)
                .setIssuedAt(new Date())
                .setExpiration(new Date(System.currentTimeMillis() + ONE_HOUR_MS))
                .signWith(key, SignatureAlgorithm.HS256)
                .compact();
        return "Bearer " + token;
    }
}
