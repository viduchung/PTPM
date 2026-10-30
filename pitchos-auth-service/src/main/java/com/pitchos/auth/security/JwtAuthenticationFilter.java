package com.pitchos.auth.security;

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
 * Bộ lọc bảo mật trích xuất Bearer JWT từ Header "Authorization" và nạp quyền vào SecurityContextHolder.
 *
 * Giữ nguyên quy ước nạp quyền của Pitch Service (Linh): nạp đồng thời cả dạng chuẩn
 * Spring Security "ROLE_<role>" (dùng cho hasRole / hasAnyRole) và dạng nguyên bản "<role>"
 * (dùng cho hasAuthority), để cấu hình phân quyền viết theo kiểu nào cũng chạy.
 *
 * Khi token sai chữ ký hoặc hết hạn, filter chỉ xóa context chứ không tự trả lỗi —
 * việc phát sinh 401 được giao cho AuthenticationEntryPoint trong SecurityConfig.
 */
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private static final Logger log = LoggerFactory.getLogger(JwtAuthenticationFilter.class);

    private final JwtTokenProvider jwtTokenProvider;

    public JwtAuthenticationFilter(JwtTokenProvider jwtTokenProvider) {
        this.jwtTokenProvider = jwtTokenProvider;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain) throws ServletException, IOException {

        String authHeader = request.getHeader("Authorization");

        if (authHeader != null && authHeader.startsWith("Bearer ")) {
            String token = authHeader.substring(7).trim();
            try {
                Claims claims = jwtTokenProvider.parseToken(token);
                String username = jwtTokenProvider.getUsername(claims);
                String role = jwtTokenProvider.getRole(claims);

                if (role != null) {
                    List<SimpleGrantedAuthority> authorities = new ArrayList<>();
                    authorities.add(new SimpleGrantedAuthority("ROLE_" + role.toLowerCase()));
                    authorities.add(new SimpleGrantedAuthority(role.toLowerCase()));

                    UsernamePasswordAuthenticationToken authentication =
                            new UsernamePasswordAuthenticationToken(username, null, authorities);

                    SecurityContextHolder.getContext().setAuthentication(authentication);
                    log.debug("Xác thực JWT thành công: user={}, role={}", username, role);
                }
            } catch (JwtException | IllegalArgumentException ex) {
                log.warn("Token JWT không hợp lệ hoặc đã hết hạn: {}", ex.getMessage());
                SecurityContextHolder.clearContext();
            }
        }

        filterChain.doFilter(request, response);
    }
}
