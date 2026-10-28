package com.pitchos.pitch.security;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.pitchos.pitch.dto.ErrorResponse;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.AuthenticationEntryPoint;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.access.AccessDeniedHandler;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

import java.time.LocalDateTime;

@Configuration
@EnableWebSecurity
@EnableMethodSecurity
public class SecurityConfig {

    private final JwtUtil jwtUtil;
    private final ObjectMapper objectMapper = new ObjectMapper().registerModule(new JavaTimeModule());

    public SecurityConfig(JwtUtil jwtUtil) {
        this.jwtUtil = jwtUtil;
    }

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
                .csrf(csrf -> csrf.disable())
                .headers(headers -> headers.frameOptions(frame -> frame.disable())) // Cho phép H2-console
                .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
                .authorizeHttpRequests(auth -> auth
                        // 1. Cho phép truy cập công khai xem danh sách và chi tiết sân bóng
                        .requestMatchers(HttpMethod.GET, "/api/v1/pitches/**").permitAll()

                        // 2. Cho phép công khai Swagger UI, OpenAPI Docs và H2 Console
                        .requestMatchers(
                                "/swagger-ui/**",
                                "/swagger-ui.html",
                                "/api-docs/**",
                                "/v3/api-docs/**",
                                "/error",
                                "/h2-console/**"
                        ).permitAll()

                        // 3. Phân quyền chặt chẽ các thao tác quản trị sân cho 'chusan' và 'admin'
                        .requestMatchers(HttpMethod.POST, "/api/v1/pitches").hasAnyRole("chusan", "admin")
                        .requestMatchers(HttpMethod.PATCH, "/api/v1/pitches/*/status").hasAnyRole("chusan", "admin")

                        // 4. Các request còn lại yêu cầu xác thực
                        .anyRequest().authenticated()
                )
                // Cấu hình phản hồi mã lỗi bảo mật 401 Unauthorized và 403 Forbidden chuẩn JSON
                .exceptionHandling(ex -> ex
                        .authenticationEntryPoint(authenticationEntryPoint())
                        .accessDeniedHandler(accessDeniedHandler())
                )
                .addFilterBefore(new JwtAuthenticationFilter(jwtUtil), UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }

    /**
     * Xử lý lỗi 401 Unauthorized: Khi client gọi API cần token nhưng không gửi token hoặc token sai/hết hạn
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
                    .message("Chưa xác thực danh tính. Vui lòng gửi kèm Bearer JWT Token hợp lệ vào Header Authorization.")
                    .path(request.getRequestURI())
                    .build();

            response.getWriter().write(objectMapper.writeValueAsString(errorResponse));
        };
    }

    /**
     * Xử lý lỗi 403 Forbidden: Khi token hợp lệ nhưng vai trò người dùng (ví dụ: 'user') không đủ quyền hạn
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
                    .message("Truy cập bị từ chối. Tài khoản của bạn không đủ quyền thực hiện thao tác này (yêu cầu vai trò 'chusan' hoặc 'admin').")
                    .path(request.getRequestURI())
                    .build();

            response.getWriter().write(objectMapper.writeValueAsString(errorResponse));
        };
    }
}
