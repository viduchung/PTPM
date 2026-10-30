package com.pitchos.auth.security;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.pitchos.auth.dto.ErrorResponse;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.AuthenticationEntryPoint;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.access.AccessDeniedHandler;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

import java.time.LocalDateTime;

/**
 * Cấu hình bảo mật Auth & User Service (Port 8081).
 *
 * MA TRẬN PHÂN QUYỀN:
 *   POST /api/v1/auth/register   → Công khai (mọi tài khoản mới mặc định role 'user')
 *   POST /api/v1/auth/login      → Công khai
 *   GET  /api/v1/users/me        → Mọi vai trò đã đăng nhập
 *   GET  /api/v1/users/{id}      → 'user' chỉ xem được chính mình (kiểm tra quyền sở hữu),
 *                                  'chusan' và 'admin' xem được mọi tài khoản
 *   GET  /api/v1/users           → Chỉ 'admin'
 *
 * Không gửi / sai token → 401 Unauthorized (AuthenticationEntryPoint)
 * Token hợp lệ nhưng sai vai trò → 403 Forbidden (AccessDeniedHandler)
 *
 * Khuôn JSON của 2 lỗi trên giữ giống Pitch Service (Linh) để client xử lý thống nhất.
 */
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
public class SecurityConfig {

    private final JwtTokenProvider jwtTokenProvider;
    private final ObjectMapper objectMapper = new ObjectMapper().registerModule(new JavaTimeModule());

    public SecurityConfig(JwtTokenProvider jwtTokenProvider) {
        this.jwtTokenProvider = jwtTokenProvider;
    }

    /**
     * Bean mã hóa mật khẩu một chiều bằng BCrypt (tự sinh salt riêng cho từng mật khẩu).
     */
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
                .csrf(csrf -> csrf.disable())
                .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
                .authorizeHttpRequests(auth -> auth
                        // 1. Hai API xác thực phải công khai, nếu không sẽ không ai đăng nhập được
                        .requestMatchers(HttpMethod.POST, "/api/v1/auth/register", "/api/v1/auth/login").permitAll()

                        // 2. Công khai Swagger UI, OpenAPI Docs và trang lỗi mặc định
                        .requestMatchers(
                                "/swagger-ui/**",
                                "/swagger-ui.html",
                                "/api-docs/**",
                                "/v3/api-docs/**",
                                "/error"
                        ).permitAll()

                        // 3. Danh sách toàn bộ người dùng: chỉ Quản trị viên
                        .requestMatchers(HttpMethod.GET, "/api/v1/users").hasRole("admin")

                        // 4. Các request còn lại yêu cầu đăng nhập
                        .anyRequest().authenticated()
                )
                // Cấu hình phản hồi mã lỗi bảo mật 401 Unauthorized và 403 Forbidden chuẩn JSON
                .exceptionHandling(ex -> ex
                        .authenticationEntryPoint(authenticationEntryPoint())
                        .accessDeniedHandler(accessDeniedHandler())
                )
                .addFilterBefore(new JwtAuthenticationFilter(jwtTokenProvider), UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }

    /**
     * Xử lý lỗi 401 Unauthorized: client gọi API cần token nhưng không gửi token,
     * hoặc token sai chữ ký / đã hết hạn. Hệ thống KHÔNG BIẾT bạn là ai.
     */
    @Bean
    public AuthenticationEntryPoint authenticationEntryPoint() {
        return (request, response, authException) -> {
            response.setStatus(HttpStatus.UNAUTHORIZED.value());
            response.setContentType(MediaType.APPLICATION_JSON_VALUE);
            response.setCharacterEncoding("UTF-8");

            ErrorResponse errorResponse = ErrorResponse.builder()
                    .timestamp(LocalDateTime.now())
                    .status(HttpStatus.UNAUTHORIZED.value())
                    .error("Unauthorized")
                    .message("Chưa xác thực danh tính. Vui lòng đăng nhập và gửi kèm Bearer JWT Token hợp lệ vào Header Authorization.")
                    .path(request.getRequestURI())
                    .build();

            response.getWriter().write(objectMapper.writeValueAsString(errorResponse));
        };
    }

    /**
     * Xử lý lỗi 403 Forbidden: token hợp lệ (hệ thống BIẾT bạn là ai) nhưng vai trò
     * không đủ quyền, hoặc bạn không sở hữu tài nguyên đang truy cập.
     */
    @Bean
    public AccessDeniedHandler accessDeniedHandler() {
        return (request, response, accessDeniedException) -> {
            response.setStatus(HttpStatus.FORBIDDEN.value());
            response.setContentType(MediaType.APPLICATION_JSON_VALUE);
            response.setCharacterEncoding("UTF-8");

            ErrorResponse errorResponse = ErrorResponse.builder()
                    .timestamp(LocalDateTime.now())
                    .status(HttpStatus.FORBIDDEN.value())
                    .error("Forbidden")
                    .message("Truy cập bị từ chối. Tài khoản của bạn không đủ quyền thực hiện thao tác này.")
                    .path(request.getRequestURI())
                    .build();

            response.getWriter().write(objectMapper.writeValueAsString(errorResponse));
        };
    }
}
