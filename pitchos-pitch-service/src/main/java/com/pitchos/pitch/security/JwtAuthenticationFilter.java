package com.pitchos.pitch.security;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.JwtException;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * Bộ lọc bảo mật trích xuất Bearer JWT từ Header Authorization.
 * Nạp quyền hạn người dùng (ROLE_<role>) vào SecurityContextHolder.
 */
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private static final Logger log = LoggerFactory.getLogger(JwtAuthenticationFilter.class);

    private final JwtUtil jwtUtil;

    public JwtAuthenticationFilter(JwtUtil jwtUtil) {
        this.jwtUtil = jwtUtil;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain) throws ServletException, IOException {

        String authHeader = request.getHeader("Authorization");

        if (authHeader != null && authHeader.startsWith("Bearer ")) {
            String token = authHeader.substring(7).trim();
            try {
                Claims claims = jwtUtil.parseToken(token);
                String role = jwtUtil.getRole(claims);
                String subject = claims.getSubject();
                Long userId = jwtUtil.getUserId(claims);

                if (role != null) {
                    List<SimpleGrantedAuthority> authorities = new ArrayList<>();
                    // Nạp cả dạng ROLE_<role> chuẩn Spring Security và dạng nguyên bản <role>
                    authorities.add(new SimpleGrantedAuthority("ROLE_" + role.toLowerCase()));
                    authorities.add(new SimpleGrantedAuthority(role.toLowerCase()));

                    UsernamePasswordAuthenticationToken authentication =
                            new UsernamePasswordAuthenticationToken(
                                    subject != null ? subject : userId,
                                    null,
                                    authorities
                            );

                    SecurityContextHolder.getContext().setAuthentication(authentication);
                    log.debug("Xác thực JWT thành công: user={}, role={}", subject, role);
                }
            } catch (JwtException | IllegalArgumentException ex) {
                log.warn("Token JWT không hợp lệ hoặc đã hết hạn: {}", ex.getMessage());
                SecurityContextHolder.clearContext();
            }
        }

        filterChain.doFilter(request, response);
    }
}
